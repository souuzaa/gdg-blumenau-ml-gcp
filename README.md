# Do notebook à nuvem: ML no Google Cloud

Código da talk **"Do notebook à nuvem: machine learning no Google Cloud para quem está começando (e um bônus quântico)"**, apresentada no GDG Blumenau em 21/11/2026.

A ideia é simples: o mesmo problema resolvido em vários degraus, do seu computador até um modelo servido no Google Cloud. Você escolhe até onde quer ir.

O problema é o mesmo em todos os exemplos: **descobrir a espécie de um pinguim** (Adelie, Chinstrap ou Gentoo) só pelas medidas do corpo. É um dataset pequeno, público e didático, perfeito pra focar no caminho e não no dado.

## O que tem aqui

| Pasta | O que você aprende | Onde roda | Custo |
|---|---|---|---|
| [`00-setup`](00-setup/) | Criar projeto, ligar o alerta de orçamento, autenticar | Seu terminal | R$ 0 |
| [`01-local-e-colab`](01-local-e-colab/) | Treinar e avaliar um modelo com scikit-learn | Local ou Colab | R$ 0 |
| [`02-bigquery-ml`](02-bigquery-ml/) | O mesmo modelo em SQL, sem sair do banco | BigQuery (console, `bq`, Python ou Colab) | R$ 0 no sandbox |
| [`03-gemini-api`](03-gemini-api/) | Degrau 1: usar um modelo pronto via API e comparar com o seu | Local ou Colab | Free tier da Gemini API |
| [`04-treino-customizado`](04-treino-customizado/) | Degrau 4: treino gerenciado, registro e endpoint | Gemini Enterprise Agent Platform (ex-Vertex AI) | Centavos, **se você limpar no final** |
| [`05-bonus-quantico`](05-bonus-quantico/) | Superposição e emaranhamento em PennyLane e Cirq | Local ou Colab | R$ 0 |

Abrir direto no Colab:

| Notebook | |
|---|---|
| Pinguins com scikit-learn | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/01-local-e-colab/penguins_sklearn.ipynb) |
| Pinguins com BigQuery ML | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/02-bigquery-ml/bqml_penguins.ipynb) |
| Gemini contra o modelo treinado | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/03-gemini-api/gemini_penguins.ipynb) |
| Bônus quântico | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/05-bonus-quantico/qubits.ipynb) |

## Começando em 2 minutos (local)

Precisa de Python 3.10 ou mais novo.

```bash
git clone https://github.com/souuzaa/gdg-blumenau-ml-gcp.git
cd gdg-blumenau-ml-gcp
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r 01-local-e-colab/requirements.txt
python 01-local-e-colab/penguins_sklearn.py
```

Cada pasta tem o seu `requirements.txt` e o seu README. Instale só o que for usar.

## A escada da talk

```
Degrau 4  Treino customizado   seu código, training job, registry, endpoint     -> 04-treino-customizado
Degrau 3  AutoML               você traz dado rotulado, o Google escolhe o modelo (não incluído: custa mais)
Degrau 2  BigQuery ML          CREATE MODEL em SQL, onde o dado já está          -> 02-bigquery-ml
Degrau 1  API pronta           manda o dado, recebe a resposta                   -> 03-gemini-api
```

Regra prática: comece pelo menor degrau que resolve o problema. Suba só quando ele não der mais conta.

## Antes de usar qualquer coisa paga

1. **Crie um alerta de orçamento** (passo a passo em [`00-setup`](00-setup/)). Leva dois minutos.
2. **Endpoint ligado cobra por hora**, mesmo sem ninguém chamar. O exemplo `04` tem um script de limpeza. Rode.
3. Prefira o **BigQuery sandbox** para aprender: não pede cartão de crédito.

## Aviso de navegação: Vertex AI mudou de nome

Em abril de 2026 o Vertex AI passou a fazer parte da **Gemini Enterprise Agent Platform**. Treino customizado, AutoML, Model Registry e Endpoints continuam lá, no menu *Models*. A API ainda é `aiplatform.googleapis.com` e o SDK Python ainda é `google-cloud-aiplatform`. Tutorial antigo falando "Vertex AI" continua valendo, só procure em outro menu.

## Para continuar estudando

- *Mãos à obra: aprendizado de máquina com Scikit-Learn, Keras & TensorFlow*, Aurélien Géron (Alta Books)
- *Engenharia de IA: construindo aplicações com modelos de fundação*, Chip Huyen (Novatec)
- *The Infinity Machine*, Sebastian Mallaby (Penguin Press)
- *Quantum Computing for the Quantum Curious*, Hughes et al. (Springer, acesso aberto)
- [Google Cloud Skills Boost](https://www.cloudskillsboost.google/)

Artigos que inspiraram a talk:

- [Fine-tuning an LLM for Financial Analysis: Three Attempts, Real Lessons](https://medium.com/@rafa.souza.pinto/fine-tuning-an-llm-for-financial-analysis-three-attempts-real-lessons-c9eec7c3e605) · código: [souuzaa/custom-model](https://github.com/souuzaa/custom-model)
- [The full local AI stack for financial anomaly detection](https://medium.com/@rafa.souza.pinto/the-full-local-ai-stack-for-financial-anomaly-detection-architecture-tradeoffs-and-what-9b96fce20672)
- [Classical vs Quantum Computing: A Hands-On Experiment with Real Market Data](https://medium.com/@rafa.souza.pinto/classical-vs-quantum-computing-a-hands-on-experiment-with-real-market-data-485130d86c80) · código: [souuzaa/quantum-backtest-sample](https://github.com/souuzaa/quantum-backtest-sample)

## Dados

`data/penguins.csv` é o dataset [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) (Gorman, Williams & Fraser, 2014), distribuído sob CC0. No BigQuery, a mesma base está em `bigquery-public-data.ml_datasets.penguins`, com as colunas `bill_*` chamadas de `culmen_*`.

## Autor

Rafael Souza · [LinkedIn](https://www.linkedin.com/in/rafael-souza-pinto/) · [Medium](https://medium.com/@rafa.souza.pinto) · [GitHub](https://github.com/souuzaa)

Achou um bug? Abra uma issue. Encontrar bug no próprio código é metade da talk.
