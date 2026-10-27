"""Script de treino que roda dentro do Agent Platform (ex-Vertex AI) ou no seu computador.

No Google Cloud, o Agent Platform define a variável AIP_MODEL_DIR (uma pasta gs://).
O container de inferência de scikit-learn espera encontrar um arquivo model.joblib nela.

Local:
    python trainer/train.py --data ../data/penguins.csv
    (salva em ./model/model.joblib)
"""

import argparse
import json
import os
import tempfile
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
ALVO = "species"


def gcs_para_fuse(caminho: str) -> str:
    """No treino gerenciado, os buckets ficam montados em /gcs/<bucket>/ (Cloud Storage FUSE)."""
    if caminho.startswith("gs://") and Path("/gcs").exists():
        return "/gcs/" + caminho[len("gs://"):]
    return caminho


def ler_csv(caminho: str) -> pd.DataFrame:
    local = gcs_para_fuse(caminho)
    if local.startswith("gs://"):
        # Sem FUSE (por exemplo, rodando no seu computador apontando para o bucket).
        from google.cloud import storage

        bucket, _, blob = local[len("gs://"):].partition("/")
        destino = Path(tempfile.mkdtemp()) / "dados.csv"
        storage.Client().bucket(bucket).blob(blob).download_to_filename(destino)
        local = str(destino)
    return pd.read_csv(local)


def salvar(arquivos: dict, pasta: str) -> None:
    """Salva {nome: caminho_local} na pasta do modelo, seja local, FUSE ou gs://."""
    destino = gcs_para_fuse(pasta)
    if destino.startswith("gs://"):
        from google.cloud import storage

        bucket, _, prefixo = destino[len("gs://"):].partition("/")
        b = storage.Client().bucket(bucket)
        for nome, origem in arquivos.items():
            b.blob(f"{prefixo.rstrip('/')}/{nome}").upload_from_filename(origem)
        return
    Path(destino).mkdir(parents=True, exist_ok=True)
    for nome, origem in arquivos.items():
        Path(destino, nome).write_bytes(Path(origem).read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="CSV local ou gs://bucket/data/penguins.csv")
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()

    df = ler_csv(args.data).dropna()
    # .to_numpy(): o container de inferência recebe listas de números, sem nome de coluna.
    X, y = df[FEATURES].to_numpy(), df[ALVO].to_numpy()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=args.test_size, random_state=42)

    modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    modelo.fit(X_tr, y_tr)
    acuracia = float(modelo.score(X_te, y_te))
    print(f"Treino: {len(y_tr)} pinguins | teste: {len(y_te)} | acurácia no teste: {acuracia:.1%}")

    tmp = Path(tempfile.mkdtemp())
    joblib.dump(modelo, tmp / "model.joblib")
    (tmp / "metrics.json").write_text(json.dumps(
        {"accuracy": acuracia, "n_train": len(y_tr), "n_test": len(y_te), "features": FEATURES}, indent=2))

    pasta_modelo = os.environ.get("AIP_MODEL_DIR", "model")
    salvar({"model.joblib": str(tmp / "model.joblib"), "metrics.json": str(tmp / "metrics.json")}, pasta_modelo)
    print(f"Modelo salvo em {pasta_modelo}")


if __name__ == "__main__":
    main()
