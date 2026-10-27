#!/usr/bin/env bash
# Mesmo fluxo do run_bqml.py, usando só a CLI do BigQuery (bq).
# Uso:
#   export PROJECT_ID=seu-project-id
#   bash 02-bigquery-ml/run_bqml.sh          # roda tudo
#   bash 02-bigquery-ml/run_bqml.sh limpar   # apaga modelo e view
set -euo pipefail

: "${PROJECT_ID:?Defina PROJECT_ID antes. Ex: export PROJECT_ID=meu-projeto}"
BQ_DATASET="${BQ_DATASET:-gdg_blumenau}"
SQL_DIR="$(cd "$(dirname "$0")" && pwd)/sql"

if ! bq --project_id="${PROJECT_ID}" show --dataset "${PROJECT_ID}:${BQ_DATASET}" >/dev/null 2>&1; then
  bq --project_id="${PROJECT_ID}" mk --dataset --location=US "${PROJECT_ID}:${BQ_DATASET}"
fi

if [[ "${1:-}" == "limpar" ]]; then
  ARQUIVOS=(99_limpar.sql)
else
  ARQUIVOS=(00_base_com_split.sql 01_criar_modelo.sql 02_avaliar.sql 03_matriz_confusao.sql 04_prever.sql 05_pinguim_novo.sql)
fi

for arq in "${ARQUIVOS[@]}"; do
  echo
  echo "===== ${arq} ====="
  sql="$(sed "s/\`gdg_blumenau\./\`${PROJECT_ID}.${BQ_DATASET}./g" "${SQL_DIR}/${arq}")"
  bq --project_id="${PROJECT_ID}" query --use_legacy_sql=false --format=pretty "${sql}"
done
