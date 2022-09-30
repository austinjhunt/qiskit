import numpy as np
from qiskit import transpile, QuantumCircuit # QuantumCircuit can be thought as the instructions of the quantum system. It holds all your quantum operations.
from qiskit.providers.aer import QasmSimulator # is the Aer high performance circuit simulator.
from qiskit.visualization import plot_histogram # creates histograms

# Use Aer's qasm_simulator
simulator = QasmSimulator()

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(2, 2) # initializing with 2 qubits in the zero state; with 2 classical bits set to zero; and circuit is the quantum circuit.


# add gates (operations) to manipulate the registers of your circuit.
# Add A Hadamard gate H on qubit 0, which puts it into a superposition state.
circuit.h(0)
 
# Add a controlled-Not operation (CNOT) on control qubit 0 and target qubit 1, putting the qubits in an entangled state.
circuit.cx(0, 1)

# Map the quantum measurement to the classical bits
# If you pass the entire quantum and classical registers to measure, the ith qubit’s measurement result will be stored in the ith classical bit.
circuit.measure([0,1], [0,1])

# compile the circuit down to low-level QASM instructions
# supported by the backend (not needed for simple circuits)
compiled_circuit = transpile(circuit, simulator)

# Execute the circuit on the qasm simulator
# (simulate the circuit; each run of the circuit will yield either the bit string 00 or 11)
# number of runs specified with shots= argument. Default is 1024. 
job = simulator.run(compiled_circuit, shots=1000)

# Grab results from the job
result = job.result()

# Once you have a result object, you can access the counts via the 
# method get_counts(circuit). This gives you the aggregate outcomes of the experiment you ran.
counts = result.get_counts(compiled_circuit)
print("\nTotal count for 00 and 11 are:",counts)

# Draw the circuit
# arguments documented by Github Issue here: https://github.com/Qiskit/qiskit/issues/579
circuit.draw(output='mpl', filename='sample2_circuit.png')

plot_histogram(counts, filename='sample2_histogram.png')