"""Bônus da talk: superposição, interferência, emaranhamento e um circuito treinável, em PennyLane.

Tudo simulado no seu computador ou no Colab. O código é o mesmo que rodaria num hardware quântico,
trocando só o "device".

    pip install -r 05-bonus-quantico/requirements.txt
    python 05-bonus-quantico/qubits_pennylane.py
"""

import pennylane as qml
from pennylane import numpy as np

# 1 qubit simulado
dev1 = qml.device("default.qubit", wires=1)


@qml.qnode(dev1)
def superposicao():
    qml.Hadamard(wires=0)  # tira o qubit do 0 e coloca em 50/50
    return qml.probs(wires=0)


@qml.qnode(dev1)
def interferencia():
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=0)  # as amplitudes de |1> se cancelam, as de |0> se somam
    return qml.probs(wires=0)


# 2 qubits simulados
dev2 = qml.device("default.qubit", wires=2)


@qml.qnode(dev2)
def bell():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])  # o segundo qubit passa a "copiar" o primeiro
    return qml.probs(wires=[0, 1])


@qml.qnode(dev2)
def circuito_variacional(params):
    """Os ângulos são pesos treináveis, como numa rede neural."""
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    qml.RZ(params[2], wires=0)
    qml.RY(params[3], wires=1)
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))


def treinar_circuito(passos: int = 60):
    """Gradiente descendente para levar o valor esperado ao mínimo teórico (-1)."""
    params = np.array([0.1, 0.2, 0.3, 0.4], requires_grad=True)
    opt = qml.GradientDescentOptimizer(stepsize=0.35)
    for passo in range(passos):
        params, custo = opt.step_and_cost(circuito_variacional, params)
        if passo % 10 == 0:
            print(f"  passo {passo:2d}: custo {float(custo):+.4f}")
    print(f"  final:    custo {float(circuito_variacional(params)):+.4f} (mínimo teórico -1)")


def mostrar(nome, probs, rotulos):
    texto = "  ".join(f"|{r}>: {float(p):.0%}" for r, p in zip(rotulos, probs))
    print(f"{nome:<14} {texto}")


if __name__ == "__main__":
    mostrar("Sem porta", [1.0, 0.0], ["0", "1"])
    mostrar("Hadamard", superposicao(), ["0", "1"])
    mostrar("Hadamard x2", interferencia(), ["0", "1"])
    mostrar("Bell", bell(), ["00", "01", "10", "11"])
    print("\nSó dá 00 ou 11. Mediu um qubit, sabe o outro.\n")
    print("Circuito variacional (forward, custo, gradiente, atualiza, repete):")
    treinar_circuito()
    print("\nDesenho do circuito de Bell:")
    print(qml.draw(bell)())
