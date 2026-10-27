"""Caminho 2 da talk: o mesmo modelo dos pinguins em SQL, rodando no BigQuery ML.

Executa os arquivos de sql/ em ordem e mostra o resultado de cada um.

    pip install -r 02-bigquery-ml/requirements.txt
    gcloud auth application-default login
    python 02-bigquery-ml/run_bqml.py --project SEU_PROJECT_ID

    python 02-bigquery-ml/run_bqml.py --project P --mostrar-sql   # só imprime o SQL, não roda nada
    python 02-bigquery-ml/run_bqml.py --project P --limpar        # apaga modelo e view
"""

import argparse
import time
from pathlib import Path

PASTA_SQL = Path(__file__).resolve().parent / "sql"
DATASET_PADRAO = "gdg_blumenau"
ETAPAS = [
    "00_base_com_split.sql",
    "01_criar_modelo.sql",
    "02_avaliar.sql",
    "03_matriz_confusao.sql",
    "04_prever.sql",
    "05_pinguim_novo.sql",
]


def carregar_sql(arquivo: str, project: str, dataset: str) -> str:
    sql = (PASTA_SQL / arquivo).read_text(encoding="utf-8")
    # Os .sql usam `gdg_blumenau.` para dar pra colar direto no console.
    # Aqui qualificamos com o projeto para não depender de nenhum padrão.
    return sql.replace(f"`{DATASET_PADRAO}.", f"`{project}.{dataset}.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--project", required=True, help="Project ID do Google Cloud")
    p.add_argument("--dataset", default=DATASET_PADRAO)
    p.add_argument("--mostrar-sql", action="store_true", help="só imprime o SQL")
    p.add_argument("--limpar", action="store_true", help="apaga modelo e view")
    args = p.parse_args()

    etapas = ["99_limpar.sql"] if args.limpar else ETAPAS

    if args.mostrar_sql:
        for arq in etapas:
            print(f"-- ===== {arq} =====\n{carregar_sql(arq, args.project, args.dataset)}\n")
        return

    from google.cloud import bigquery

    client = bigquery.Client(project=args.project)

    # A tabela pública dos pinguins fica em US. O dataset precisa estar na mesma localização.
    ds = bigquery.Dataset(f"{args.project}.{args.dataset}")
    ds.location = "US"
    client.create_dataset(ds, exists_ok=True)

    for arq in etapas:
        sql = carregar_sql(arq, args.project, args.dataset)
        print(f"\n===== {arq} =====")
        inicio = time.time()
        job = client.query(sql)
        resultado = job.result()
        segundos = time.time() - inicio
        if job.statement_type in ("SELECT", None) and resultado.total_rows:
            df = resultado.to_dataframe()
            mostrar(df)
        else:
            print(f"ok ({job.statement_type or 'script'})")
        mb = (job.total_bytes_processed or 0) / 1e6
        print(f"[{segundos:.0f}s, {mb:.2f} MB processados]")


def mostrar(df) -> None:
    import pandas as pd

    with pd.option_context("display.max_columns", 20, "display.width", 160, "display.max_colwidth", 60):
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
