"""Degrau 1 da talk: usar um modelo pronto (Gemini) via API, sem treinar nada.

E comparar com o modelo que treinamos em 10 linhas no caminho 1.
Os dois olham os mesmos pinguins de teste. Quem acerta mais?

Modo Gemini API (chave gratuita do Google AI Studio):
    export GEMINI_API_KEY=...
    python 03-gemini-api/gemini_penguins.py

Modo Google Cloud (Agent Platform, cobra no seu projeto):
    gcloud auth application-default login
    python 03-gemini-api/gemini_penguins.py --google-cloud --project SEU_PROJECT_ID

Outros:
    --exemplos 3       mostra 3 pinguins de cada espécie no prompt (few-shot)
    --n 20             quantos pinguins de teste mandar
    --listar-modelos   lista os modelos disponíveis para a sua chave
"""

import argparse
import json
import os
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
ESPECIES = ["Adelie", "Chinstrap", "Gentoo"]
CSV_LOCAL = Path(__file__).resolve().parents[1] / "data" / "penguins.csv"
CSV_URL = "https://raw.githubusercontent.com/souuzaa/gdg-blumenau-ml-gcp/main/data/penguins.csv"
# Alias que aponta para o Flash mais recente. Se não existir para você, rode --listar-modelos
# e passe outro com --modelo (ou GEMINI_MODEL).
MODELO_PADRAO = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")


def cliente(args):
    from google import genai

    if args.google_cloud:
        return genai.Client(vertexai=True, project=args.project, location=args.location)
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        raise SystemExit("Defina GEMINI_API_KEY. Gere uma chave grátis em https://aistudio.google.com/apikey")
    return genai.Client()


def descrever(linha) -> str:
    return (f"bico {linha.bill_length_mm} mm de comprimento e {linha.bill_depth_mm} mm de altura, "
            f"nadadeira {linha.flipper_length_mm} mm, massa {linha.body_mass_g} g")


def montar_prompt(teste: pd.DataFrame, exemplos: pd.DataFrame) -> str:
    partes = [
        "Você é biólogo e conhece os pinguins do arquipélago Palmer, na Antártida.",
        "Classifique cada pinguim abaixo como Adelie, Chinstrap ou Gentoo, só pelas medidas.",
        f"Devolva uma lista JSON com exatamente {len(teste)} espécies, na mesma ordem.",
    ]
    if len(exemplos):
        partes.append("\nExemplos com a resposta certa:")
        partes += [f"- {descrever(l)}: {l.species}" for l in exemplos.itertuples()]
    partes.append("\nPinguins para classificar:")
    partes += [f"{i + 1}. {descrever(l)}" for i, l in enumerate(teste.itertuples())]
    return "\n".join(partes)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelo", default=MODELO_PADRAO)
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--exemplos", type=int, default=0, help="exemplos por espécie no prompt")
    p.add_argument("--google-cloud", action="store_true", help="usa o Agent Platform em vez da Gemini API")
    p.add_argument("--project", default=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    p.add_argument("--location", default="global")
    p.add_argument("--listar-modelos", action="store_true")
    args = p.parse_args()

    from google.genai import types

    client = cliente(args)
    if args.listar_modelos:
        for m in client.models.list():
            print(m.name)
        return

    df = pd.read_csv(CSV_LOCAL if CSV_LOCAL.exists() else CSV_URL).dropna()
    treino, teste = train_test_split(df, test_size=0.2, random_state=42)  # mesmo split do caminho 1
    teste = teste.head(args.n)
    exemplos = (treino.groupby("species").head(args.exemplos) if args.exemplos else treino.head(0))

    # Degrau 1: ninguém treinou nada. Só um prompt.
    resposta = client.models.generate_content(
        model=args.modelo,
        contents=montar_prompt(teste, exemplos),
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema={"type": "ARRAY", "items": {"type": "STRING", "enum": ESPECIES}},
        ),
    )
    previsto_llm = json.loads(resposta.text)
    if len(previsto_llm) != len(teste):
        print(f"Atenção: o modelo devolveu {len(previsto_llm)} respostas para {len(teste)} pinguins.")
    previsto_llm = (previsto_llm + ["?"] * len(teste))[: len(teste)]

    # O modelo treinado no caminho 1, para comparar.
    classico = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    classico.fit(treino[FEATURES], treino["species"])
    previsto_classico = classico.predict(teste[FEATURES])

    real = teste["species"].tolist()
    acerto_llm = sum(a == b for a, b in zip(real, previsto_llm))
    acerto_cls = sum(a == b for a, b in zip(real, previsto_classico))

    print(f"Modelo: {args.modelo} | exemplos no prompt: {len(exemplos)} | pinguins: {len(teste)}\n")
    print(pd.DataFrame({"real": real, "gemini": previsto_llm, "regressao_logistica": previsto_classico})
          .to_string(index=False))
    print(f"\nGemini (sem treino):            {acerto_llm}/{len(teste)}")
    print(f"Regressão logística (treinada): {acerto_cls}/{len(teste)}")
    print("\nDado tabular com rótulo? Um modelo pequeno e treinado costuma ganhar, e custa quase nada.")
    print("Texto, imagem, áudio sem rótulo? Aí o degrau 1 brilha.")


if __name__ == "__main__":
    main()
