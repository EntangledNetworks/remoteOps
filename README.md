This repository contains a tutorial and mini-library that demonstrates how certain resource states can be used to facilitate multi-qubit operations between qubits.
Specifically, here we will consider the use of the so-called Einstein-Podolsky-Rosen (EPR) state: $\left|\Phi_{+}\right>=\frac{\left|00\right>+\left|11\right>}{\sqrt{2}}$ to facilitate two-qubit gates.
Importantly, any two parties in possession of one-half of the EPR state can use it to facilitate two-qubit operations <i>between</i> qubits in their possession, with only classical communication and <i>without</i> those qubits being in close proximity with each other.

To install, clone this repository and run:
```
pip install [src]
```
Here `src` is the directory into which you've cloned this repository. Also ensure that you have QISkit, Jupyter and (optionally) NumPy installed.

To see the tutorial, open Tutorial notebook in `examples/`.

