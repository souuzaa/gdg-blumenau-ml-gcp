#!/usr/bin/env bash
# Prepara o projeto do Google Cloud para os exemplos da talk.
# Uso:
#   export PROJECT_ID=seu-project-id
#   bash 00-setup/setup_gcp.sh bigquery   # só BigQuery (funciona no sandbox)
#   bash 00-setup/setup_gcp.sh all        # BigQuery + bucket + Agent Platform
set -euo pipefail

MODE="${1:-bigquery}"
: "${PROJECT_ID:?Defina PROJECT_ID antes. Ex: export PROJECT_ID=meu-projeto}"
REGION="${REGION:-us-central1}"
BUCKET="${BUCKET:-${PROJECT_ID}-gdg-ml}"
BQ_DATASET="${BQ_DATASET:-gdg_blumenau}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo ">> Projeto: ${PROJECT_ID} | modo: ${MODE}"
gcloud config set project "${PROJECT_ID}" >/dev/null

echo ">> Ligando a API do BigQuery"
gcloud services enable bigquery.googleapis.com

echo ">> Criando o dataset ${BQ_DATASET} em US (se ainda não existir)"
if bq --project_id="${PROJECT_ID}" show --dataset "${PROJECT_ID}:${BQ_DATASET}" >/dev/null 2>&1; then
  echo "   já existe, seguindo"
else
  bq --project_id="${PROJECT_ID}" mk --dataset --location=US "${PROJECT_ID}:${BQ_DATASET}"
fi

if [[ "${MODE}" == "all" ]]; then
  echo ">> Ligando APIs do Agent Platform (ex-Vertex AI) e do Cloud Storage"
  gcloud services enable aiplatform.googleapis.com storage.googleapis.com

  echo ">> Criando o bucket gs://${BUCKET} em ${REGION} (se ainda não existir)"
  if gcloud storage buckets describe "gs://${BUCKET}" >/dev/null 2>&1; then
    echo "   já existe, seguindo"
  else
    gcloud storage buckets create "gs://${BUCKET}" --location="${REGION}" --uniform-bucket-level-access
  fi

  echo ">> Subindo o CSV dos pinguins para o bucket"
  gcloud storage cp "${ROOT}/data/penguins.csv" "gs://${BUCKET}/data/penguins.csv"
fi

echo
echo "Pronto. Próximos passos:"
echo "  BigQuery ML:        python 02-bigquery-ml/run_bqml.py --project ${PROJECT_ID}"
if [[ "${MODE}" == "all" ]]; then
  echo "  Treino customizado: python 04-treino-customizado/submit_training.py --project ${PROJECT_ID} --bucket ${BUCKET}"
fi
echo "Lembrete: configure um alerta de orçamento antes de rodar o treino customizado."
