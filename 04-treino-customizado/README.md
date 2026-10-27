# 04 · Treino customizado no Agent Platform (degrau 4)

O mesmo modelo dos pinguins, agora do jeito que vai para produção: um **job de treino gerenciado**, o modelo no **Model Registry** e um **endpoint** respondendo previsões por HTTP.

> Em abril de 2026 o Vertex AI virou parte da **Gemini Enterprise Agent Platform**. No console, procure por *Models*. O SDK continua `google-cloud-aiplatform`.

## Quanto custa

- **Job de treino:** uma máquina `n1-standard-4` por poucos minutos. Centavos.
- **Endpoint:** uma `n1-standard-2` ligada **cobra por hora, mesmo sem ninguém chamar**.
- **Model Registry e bucket:** praticamente zero para um arquivo deste tamanho.

Configure o alerta de orçamento ([`00-setup`](../00-setup/)) e rode o `limpar` no final.

## Passo a passo

```bash
export PROJECT_ID=seu-project-id
bash 00-setup/setup_gcp.sh all            # liga APIs, cria bucket e sobe o CSV

cd 04-treino-customizado
pip install -r requirements.txt
gcloud auth application-default login

# 1. Treino gerenciado + registro do modelo (5 a 10 minutos)
python submit_training.py treinar --project $PROJECT_ID --bucket $PROJECT_ID-gdg-ml

# 2. Endpoint + previsão de teste (10 a 20 minutos para subir; cobra por hora a partir daqui)
python submit_training.py publicar --project $PROJECT_ID

# 3. Limpeza. Não pule.
python submit_training.py limpar --project $PROJECT_ID
```

Saída esperada do passo 2:

```
  [45.0, 15.5, 215.0, 5000.0] -> Gentoo
  [39.1, 18.7, 181.0, 3750.0] -> Adelie
  [49.5, 19.0, 200.0, 3800.0] -> Chinstrap
```

## O que acontece por baixo

1. O SDK empacota `trainer/train.py` e manda para um container pronto do Google.
2. O job lê o CSV do bucket (montado em `/gcs/` dentro da máquina) e treina.
3. O script salva `model.joblib` na pasta que o Agent Platform passa em `AIP_MODEL_DIR`.
4. O modelo é registrado com um container de inferência de scikit-learn.
5. No `publicar`, o modelo ganha uma máquina e um endpoint HTTP.

## Testar o script de treino no seu computador

```bash
cd 04-treino-customizado
python trainer/train.py --data ../data/penguins.csv     # salva em ./model/
```

## Deu erro de container?

Os nomes dos containers prontos mudam com o tempo. Confira as listas atuais:
[treino](https://cloud.google.com/vertex-ai/docs/training/pre-built-containers) e
[inferência](https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers),
e passe outros com `--container-treino` e `--container-inferencia`.

Regra de ouro: a versão do scikit-learn usada no treino precisa bater com a do container de inferência. Se o modelo foi salvo numa versão e carregado em outra, a previsão pode falhar.

**Plano B:** treine no seu computador com `scikit-learn==1.5.2` e só registre no Google Cloud:

```bash
python trainer/train.py --data ../data/penguins.csv
python submit_training.py enviar-local --project $PROJECT_ID --bucket $PROJECT_ID-gdg-ml
python submit_training.py publicar --project $PROJECT_ID
```
