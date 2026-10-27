"""Degrau 4 da talk: treino customizado, registro e endpoint no Agent Platform (ex-Vertex AI).

Fluxo, um comando por etapa:

    python submit_training.py treinar  --project P --bucket B   # job de treino gerenciado + registro do modelo
    python submit_training.py publicar --project P              # sobe um endpoint e faz uma previsão  ($ por hora!)
    python submit_training.py limpar   --project P              # derruba endpoint e apaga modelos   (RODE!)

Plano B, se o job de treino der problema de container:

    python trainer/train.py --data ../data/penguins.csv          # treina no seu computador
    python submit_training.py enviar-local --project P --bucket B   # sobe ./model para o bucket e registra

Requer: gcloud auth application-default login e APIs ligadas (00-setup/setup_gcp.sh all).
"""

import argparse
import sys
from pathlib import Path

from google.cloud import aiplatform

NOME = "gdg-pinguins"
AQUI = Path(__file__).resolve().parent

# Containers prontos do Google. Se algum falhar, confira os nomes atuais em:
# https://cloud.google.com/vertex-ai/docs/training/pre-built-containers
# https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
# O scikit-learn do treino precisa ter a mesma versão do container de inferência.
CONTAINER_TREINO = "us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-17.py310:latest"
CONTAINER_INFERENCIA = "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-5:latest"
SKLEARN = "scikit-learn==1.5.2"

PINGUINS_TESTE = [
    [45.0, 15.5, 215.0, 5000.0],  # cara de Gentoo
    [39.1, 18.7, 181.0, 3750.0],  # cara de Adelie
    [49.5, 19.0, 200.0, 3800.0],  # cara de Chinstrap
]


def init(args) -> None:
    staging = f"gs://{args.bucket}/staging" if getattr(args, "bucket", None) else None
    aiplatform.init(project=args.project, location=args.region, staging_bucket=staging)


def treinar(args) -> None:
    init(args)
    job = aiplatform.CustomTrainingJob(
        display_name=f"{NOME}-treino",
        script_path=str(AQUI / "trainer" / "train.py"),
        container_uri=args.container_treino,
        requirements=[SKLEARN, "pandas", "joblib", "google-cloud-storage"],
        model_serving_container_image_uri=args.container_inferencia,
    )
    print("Enviando o job. Leva alguns minutos (a máquina precisa subir). Acompanhe no console.")
    modelo = job.run(
        model_display_name=NOME,
        args=[f"--data=gs://{args.bucket}/data/penguins.csv"],
        base_output_dir=f"gs://{args.bucket}/{NOME}",
        replica_count=1,
        machine_type="n1-standard-4",
    )
    print(f"\nModelo registrado: {modelo.resource_name}")
    print("Próximo passo (cobra por hora enquanto estiver no ar):")
    print(f"  python submit_training.py publicar --project {args.project} --region {args.region}")


def enviar_local(args) -> None:
    """Plano B: registra um modelo treinado no seu computador."""
    init(args)
    pasta = AQUI / "model"
    if not (pasta / "model.joblib").exists():
        sys.exit("Não achei model/model.joblib. Rode antes: python trainer/train.py --data ../data/penguins.csv")
    import sklearn

    if sklearn.__version__ != SKLEARN.split("==")[1]:
        print(f"Atenção: seu scikit-learn local é {sklearn.__version__}, o container de inferência usa {SKLEARN}.")
    from google.cloud import storage

    destino = f"{NOME}/local-model"
    b = storage.Client(project=args.project).bucket(args.bucket)
    for arq in ("model.joblib", "metrics.json"):
        if (pasta / arq).exists():
            b.blob(f"{destino}/{arq}").upload_from_filename(str(pasta / arq))
    modelo = aiplatform.Model.upload(
        display_name=NOME,
        artifact_uri=f"gs://{args.bucket}/{destino}",
        serving_container_image_uri=args.container_inferencia,
    )
    print(f"Modelo registrado: {modelo.resource_name}")


def publicar(args) -> None:
    init(args)
    modelos = aiplatform.Model.list(filter=f'display_name="{NOME}"', order_by="create_time desc")
    if not modelos:
        sys.exit("Nenhum modelo registrado. Rode 'treinar' ou 'enviar-local' antes.")
    modelo = modelos[0]
    print(f"Publicando {modelo.resource_name}. Leva de 10 a 20 minutos na primeira vez.")
    print("A partir daqui o endpoint cobra por hora. Não esqueça do 'limpar'.")
    endpoint = modelo.deploy(
        deployed_model_display_name=NOME,
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=1,
    )
    resposta = endpoint.predict(instances=PINGUINS_TESTE)
    for medidas, especie in zip(PINGUINS_TESTE, resposta.predictions):
        print(f"  {medidas} -> {especie}")
    print(f"\nEndpoint no ar: {endpoint.resource_name}")
    print(f"Para derrubar: python submit_training.py limpar --project {args.project} --region {args.region}")


def limpar(args) -> None:
    init(args)
    # Endpoints criados pelo SDK recebem o nome do modelo + "_endpoint".
    for ep in aiplatform.Endpoint.list():
        if ep.display_name.startswith(NOME):
            print(f"Derrubando endpoint {ep.display_name}")
            ep.undeploy_all()
            ep.delete()
    if args.manter_modelos:
        print("Modelos mantidos no registry (não cobram nada parados).")
    else:
        for m in aiplatform.Model.list(filter=f'display_name="{NOME}"'):
            print(f"Apagando modelo {m.resource_name}")
            m.delete()
    print("Limpo. Os arquivos no bucket continuam lá; apague com:")
    print(f"  gcloud storage rm -r gs://SEU_BUCKET/{NOME}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for nome, func, precisa_bucket in [
        ("treinar", treinar, True), ("enviar-local", enviar_local, True),
        ("publicar", publicar, False), ("limpar", limpar, False),
    ]:
        s = sub.add_parser(nome)
        s.add_argument("--project", required=True)
        s.add_argument("--region", default="us-central1")
        s.add_argument("--bucket", required=precisa_bucket, help="sem gs://, ex: meu-projeto-gdg-ml")
        s.add_argument("--container-treino", default=CONTAINER_TREINO)
        s.add_argument("--container-inferencia", default=CONTAINER_INFERENCIA)
        if nome == "limpar":
            s.add_argument("--manter-modelos", action="store_true")
        s.set_defaults(func=func)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
