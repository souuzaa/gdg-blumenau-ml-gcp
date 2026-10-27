# 05 · Bônus quântico

Um qubit no seu Colab. Simulado, mas o código é o mesmo que rodaria num computador quântico de verdade, trocando só o *device*.

## Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souuzaa/gdg-blumenau-ml-gcp/blob/main/05-bonus-quantico/qubits.ipynb)

## Local

```bash
pip install -r 05-bonus-quantico/requirements.txt
python 05-bonus-quantico/qubits_pennylane.py   # probabilidades exatas + circuito treinável
python 05-bonus-quantico/qubits_cirq.py        # mesmos circuitos, com medição por amostragem
```

## Os quatro conceitos

| Conceito | O que acontece | Saída |
|---|---|---|
| Superposição | Uma porta Hadamard coloca o qubit em 50/50 | `[0.5, 0.5]` |
| Interferência | Duas Hadamard seguidas: as amplitudes de 1 se cancelam e ele volta para 0 | `[1.0, 0.0]` |
| Emaranhamento | Hadamard + CNOT: só saem 00 ou 11, nunca 01 ou 10 | `[0.5, 0, 0, 0.5]` |
| Circuito variacional | Ângulos das portas viram pesos treináveis, com gradiente descendente | custo chega a -1 |

Superposição é o cenário. Interferência é o truque que todo algoritmo quântico útil usa.

## PennyLane ou Cirq?

- **PennyLane** (Xanadu) tem uma API parecida com PyTorch e é ótima para machine learning quântico.
- **Cirq** é a biblioteca do **Google Quantum AI**, a mesma usada nos experimentos com os chips do Google.

Os dois rodam no Colab gratuito.

## Para ir além

- O experimento completo da talk, com 15 anos de soja, milho e câmbio comparando Monte Carlo clássico e Quantum Amplitude Estimation: [souuzaa/quantum-backtest-sample](https://github.com/souuzaa/quantum-backtest-sample) e o [artigo no Medium](https://medium.com/@rafa.souza.pinto/classical-vs-quantum-computing-a-hands-on-experiment-with-real-market-data-485130d86c80).
- *Quantum Computing for the Quantum Curious* (Springer, acesso aberto): explica superposição e emaranhamento com matemática de ensino médio.
- [Tutoriais do Cirq](https://quantumai.google/cirq/start/basics).

Letra miúda honesta: o hardware quântico de hoje ainda tem ruído e poucos qubits. Simular é o jeito certo de aprender agora.
