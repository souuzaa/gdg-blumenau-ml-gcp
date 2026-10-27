"""Caminho 1 da talk: treinar e avaliar um classificador de pinguins com scikit-learn.

Roda igual no seu computador e no Colab.

    python 01-local-e-colab/penguins_sklearn.py
    python 01-local-e-colab/penguins_sklearn.py --salvar modelo.joblib
"""

import argparse
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
ALVO = "species"

CSV_LOCAL = Path(__file__).resolve().parents[1] / "data" / "penguins.csv"
CSV_URL = "https://raw.githubusercontent.com/souuzaa/gdg-blumenau-ml-gcp/main/data/penguins.csv"


def carregar_dados() -> pd.DataFrame:
    """Lê o CSV do repositório. Se não achar, baixa do GitHub."""
    origem = CSV_LOCAL if CSV_LOCAL.exists() else CSV_URL
    df = pd.read_csv(origem)
    print(f"Dados: {origem}")
    # Igual ao slide: remove qualquer linha com valor vazio (sobram 333 pinguins).
    return df.dropna()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--salvar", help="caminho para salvar o modelo treinado (.joblib)")
    args = parser.parse_args()

    df = carregar_dados()
    X, y = df[FEATURES], df[ALVO]
    print(f"{len(df)} pinguins, espécies: {sorted(y.unique())}\n")

    # 20% fica guardado. O modelo nunca vê esses pinguins durante o treino.
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    # StandardScaler coloca as medidas na mesma escala (milímetro e grama são grandezas bem diferentes).
    modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    modelo.fit(X_tr, y_tr)

    acertos = int((modelo.predict(X_te) == y_te).sum())
    print(f"Teste: acertou {acertos} de {len(y_te)} ({modelo.score(X_te, y_te):.1%})\n")
    print(classification_report(y_te, modelo.predict(X_te)))
    print("Matriz de confusão (linhas = real, colunas = previsto):")
    print(pd.DataFrame(confusion_matrix(y_te, modelo.predict(X_te), labels=modelo.classes_),
                       index=modelo.classes_, columns=modelo.classes_), "\n")

    # 100% num único sorteio deveria te deixar desconfiado.
    # Validação cruzada repete o teste em 5 divisões diferentes dos dados.
    cv = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), X, y, cv=5)
    print(f"Validação cruzada (5 divisões): média {cv.mean():.1%}, pior divisão {cv.min():.1%}\n")

    # Um pinguim novo, que não está no dataset.
    novo = pd.DataFrame([[45.0, 15.5, 215.0, 5000.0]], columns=FEATURES)
    probs = {c: round(float(p), 3) for c, p in zip(modelo.classes_, modelo.predict_proba(novo)[0])}
    print(f"Pinguim novo {novo.iloc[0].to_dict()}")
    print(f"  -> previsão: {modelo.predict(novo)[0]} | probabilidades: {probs}")

    if args.salvar:
        import joblib

        joblib.dump(modelo, args.salvar)
        print(f"\nModelo salvo em {args.salvar}")


if __name__ == "__main__":
    main()
