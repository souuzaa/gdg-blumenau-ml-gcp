"""Bônus da talk: os mesmos circuitos em Cirq, a biblioteca do Google Quantum AI.

Aqui a gente mede de verdade (com amostragem), como num hardware: rodamos o circuito
1.000 vezes e contamos os resultados.

    pip install -r 05-bonus-quantico/requirements.txt
    python 05-bonus-quantico/qubits_cirq.py
"""

import cirq

REPETICOES = 1000
simulador = cirq.Simulator(seed=42)


def medir(nome: str, circuito: cirq.Circuit, n_bits: int) -> None:
    resultado = simulador.run(circuito, repetitions=REPETICOES)
    contagem = resultado.histogram(key="m")
    texto = "  ".join(
        f"|{format(valor, f'0{n_bits}b')}>: {contagem.get(valor, 0):4d}" for valor in range(2**n_bits)
    )
    print(f"{nome:<14} {texto}   ({REPETICOES} medições)")


if __name__ == "__main__":
    q0, q1 = cirq.LineQubit.range(2)

    superposicao = cirq.Circuit(cirq.H(q0), cirq.measure(q0, key="m"))
    interferencia = cirq.Circuit(cirq.H(q0), cirq.H(q0), cirq.measure(q0, key="m"))
    bell = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key="m"))

    medir("Hadamard", superposicao, 1)
    medir("Hadamard x2", interferencia, 1)
    medir("Bell", bell, 2)

    print("\nRepare: com amostragem, 50/50 quase nunca sai exatamente 500/500. É o ruído estatístico de medir.")
    print("Num hardware real ainda entra o ruído físico dos qubits.\n")

    print("Circuito de Bell:")
    print(bell)

    estado = cirq.Simulator().simulate(cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))).final_state_vector
    print(f"\nVetor de estado sem medir: {estado.round(3)}  (amplitudes de |00>, |01>, |10>, |11>)")
