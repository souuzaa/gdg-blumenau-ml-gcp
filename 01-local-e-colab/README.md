# 01 · Python, no seu computador ou no Colab

O caminho 1 da talk: treinar um classificador de pinguins com scikit-learn, avaliar em dados que o modelo nunca viu e prever um pinguim novo.

## Colab (nada para instalar)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/01-local-e-colab/penguins_sklearn.ipynb)

Clique, faça login com sua conta Google e rode as células em ordem (Shift+Enter).

## Local

```bash
pip install -r 01-local-e-colab/requirements.txt
python 01-local-e-colab/penguins_sklearn.py
python 01-local-e-colab/penguins_sklearn.py --salvar modelo.joblib   # guarda o modelo treinado
```

Saída esperada (resumida):

```
333 pinguins, espécies: ['Adelie', 'Chinstrap', 'Gentoo']
Teste: acertou 67 de 67 (100.0%)
Validação cruzada (5 divisões): média 99.1%, pior divisão 97.0%
```

## Por que 100% é suspeito

Num problema real, acerto perfeito quase sempre é vazamento de dado (o modelo viu a resposta durante o treino) ou bug na avaliação. Aqui não é nenhum dos dois: as três espécies são muito diferentes entre si e o problema é fácil de verdade. A validação cruzada, que repete o teste em cinco divisões diferentes, mostra o número mais honesto.

## Experimentos para fazer

1. Treine com só duas medidas (`bill_length_mm` e `flipper_length_mm`). Quanto a acurácia cai?
2. Troque `LogisticRegression` por `RandomForestClassifier` ou `KNeighborsClassifier`.
3. Tire o `StandardScaler` e o `max_iter=1000` e rode de novo. De onde vem o aviso de convergência?
