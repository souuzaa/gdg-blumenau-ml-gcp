# 03 · Gemini API (degrau 1)

O degrau mais baixo da escada: usar um modelo pronto, sem treinar nada. Mandamos as medidas de 20 pinguins para o Gemini e pedimos a espécie. Depois comparamos com a regressão logística do caminho 1, treinada em menos de um segundo.

O objetivo não é provar que um é melhor que o outro. É sentir quando cada degrau faz sentido.

## Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/03-gemini-api/gemini_penguins.ipynb)

Guarde a chave em **Secrets** (ícone de chave na barra lateral do Colab) com o nome `GEMINI_API_KEY`.

## Local

```bash
pip install -r 03-gemini-api/requirements.txt
export GEMINI_API_KEY=sua-chave          # grátis em https://aistudio.google.com/apikey
python 03-gemini-api/gemini_penguins.py
python 03-gemini-api/gemini_penguins.py --exemplos 3    # few-shot: 3 exemplos de cada espécie no prompt
```

Uma chamada só por execução: os 20 pinguins vão no mesmo prompt e a resposta volta como lista JSON, restrita às três espécies. Cabe no free tier da Gemini API.

### Pelo Google Cloud (Agent Platform)

Mesmo código, autenticação do seu projeto, cobrança no seu faturamento:

```bash
gcloud services enable aiplatform.googleapis.com
gcloud auth application-default login
python 03-gemini-api/gemini_penguins.py --google-cloud --project SEU_PROJECT_ID
```

## Modelo

O padrão é o alias `gemini-flash-latest`, que aponta para o Flash mais recente. Os nomes mudam rápido. Se der erro de modelo não encontrado:

```bash
python 03-gemini-api/gemini_penguins.py --listar-modelos
python 03-gemini-api/gemini_penguins.py --modelo NOME_DA_LISTA
```

## Experimentos

1. Rode com `--exemplos 0`, `1` e `5`. Quanto o few-shot ajuda?
2. Troque o prompt para inglês. Muda alguma coisa?
3. Calcule o custo: quantos tokens a chamada usou (`resposta.usage_metadata`) contra o custo de treinar a regressão logística.
