# 00 · Setup do Google Cloud

Só precisa disso para as pastas `02`, `03` (modo Google Cloud) e `04`. Para `01` e `05`, pule direto.

## 1. Conta e projeto

Você tem dois jeitos de começar:

| Opção | Pede cartão? | Serve para |
|---|---|---|
| **BigQuery sandbox** | Não | Pasta `02` inteira |
| **Trial do Google Cloud** (crédito para conta nova) | Sim, mas não cobra sem você fazer upgrade | Tudo, inclusive a pasta `04` |

1. Entre em [console.cloud.google.com](https://console.cloud.google.com) com uma conta Google.
2. Crie um projeto novo (por exemplo `gdg-ml-seunome`). Anote o **Project ID**, não o nome.
3. Para usar só o sandbox, abra o [BigQuery](https://console.cloud.google.com/bigquery) e aceite os termos. Pronto, não precisa de mais nada.

Limites do sandbox: 10 GiB de armazenamento, 1 TiB de consulta por mês, tabelas e modelos expiram em 60 dias.

## 2. Alerta de orçamento (faça antes de qualquer coisa paga)

1. Console → **Faturamento** → **Orçamentos e alertas** → **Criar orçamento**.
2. Valor: algo pequeno, como US$ 5 ou R$ 25.
3. Alertas em 50%, 90% e 100%.

Alerta avisa, não bloqueia. Ele te dá tempo de desligar o que esqueceu ligado.

## 3. Ferramentas no seu computador

Instale o [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (traz `gcloud`, `bq` e `gcloud storage`) e autentique:

```bash
gcloud auth login
gcloud auth application-default login   # credencial que as bibliotecas Python usam
gcloud config set project SEU_PROJECT_ID
```

No Colab você não precisa do CLI. Os notebooks autenticam com `google.colab.auth`.

## 4. Script de setup

O script liga as APIs, cria o dataset do BigQuery e, se você pedir, o bucket para o treino customizado.

```bash
export PROJECT_ID=seu-project-id
bash 00-setup/setup_gcp.sh bigquery     # só o necessário para a pasta 02
bash 00-setup/setup_gcp.sh all          # BigQuery + bucket + APIs da pasta 04
```

Variáveis opcionais: `REGION` (padrão `us-central1`), `BUCKET` (padrão `$PROJECT_ID-gdg-ml`), `BQ_DATASET` (padrão `gdg_blumenau`).

O dataset do BigQuery é criado na localização **US** de propósito: a tabela pública dos pinguins fica em US, e o BigQuery não cruza localizações numa mesma consulta.
