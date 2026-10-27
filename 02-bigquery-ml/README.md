# 02 · BigQuery ML (degrau 2)

O mesmo classificador de pinguins, só que em SQL. O dado já está numa tabela pública do BigQuery, então o modelo nasce, é avaliado e faz previsão sem sair do banco. Sem servidor, sem exportar CSV, sem Python obrigatório.

Funciona no **BigQuery sandbox**, sem cartão de crédito. Se o sandbox recusar o `CREATE MODEL` no seu projeto, ative o faturamento: o free tier mensal cobre com folga um modelo deste tamanho.

## As consultas

| Arquivo | O que faz |
|---|---|
| `sql/00_base_com_split.sql` | Cria uma view com 80% das linhas marcadas como treino e 20% como teste |
| `sql/01_criar_modelo.sql` | `CREATE MODEL`: regressão logística com as 4 medidas |
| `sql/02_avaliar.sql` | `ML.EVALUATE` no conjunto de teste: precisão, recall, acurácia, log loss |
| `sql/03_matriz_confusao.sql` | `ML.CONFUSION_MATRIX`: quem o modelo confunde com quem |
| `sql/04_prever.sql` | `ML.PREDICT` no teste, das previsões menos confiantes para as mais |
| `sql/05_pinguim_novo.sql` | Previsão para um pinguim inventado |
| `sql/99_limpar.sql` | Apaga modelo e view |

Na tabela pública, as medidas do bico se chamam `culmen_*` em vez de `bill_*`. É o mesmo dado.

## Quatro jeitos de rodar

Antes, crie o dataset `gdg_blumenau` na localização **US** (a tabela pública fica em US e o BigQuery não mistura localizações). O script [`00-setup/setup_gcp.sh bigquery`](../00-setup/) faz isso, e os runners abaixo também.

### 1. Console (o mais simples)

Abra o [BigQuery Studio](https://console.cloud.google.com/bigquery), crie o dataset `gdg_blumenau` (localização US) e cole os arquivos de `sql/` em ordem, um por vez.

### 2. Python

```bash
pip install -r 02-bigquery-ml/requirements.txt
gcloud auth application-default login
python 02-bigquery-ml/run_bqml.py --project SEU_PROJECT_ID
python 02-bigquery-ml/run_bqml.py --project SEU_PROJECT_ID --limpar
```

### 3. CLI `bq`

```bash
export PROJECT_ID=seu-project-id
bash 02-bigquery-ml/run_bqml.sh
bash 02-bigquery-ml/run_bqml.sh limpar
```

### 4. Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/02-bigquery-ml/bqml_penguins.ipynb)

## Para ir além

- Troque `LOGISTIC_REG` por `BOOSTED_TREE_CLASSIFIER` ou `RANDOM_FOREST_CLASSIFIER` e compare o `ML.EVALUATE`.
- Inclua `island` e `sex` como features. O BigQuery ML faz o one-hot encoding sozinho.
- Teste `ML.EXPLAIN_PREDICT` para ver quais medidas mais pesaram em cada previsão.

Custo: o BigQuery cobra pelo volume de dado processado. A tabela dos pinguins tem poucos KB, então tudo aqui fica muito abaixo do free tier mensal.
