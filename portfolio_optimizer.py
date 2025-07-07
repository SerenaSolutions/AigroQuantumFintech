import os
from dotenv import load_dotenv
from qiskit_optimization.applications import PortfolioOptimization
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_ibm_provider import IBMProvider
from qiskit.algorithms.minimum_eigensolvers import SamplingVQE
from qiskit.algorithms.optimizers import SPSA
from qiskit.primitives import Sampler
from qiskit.circuit.library import RealAmplitudes
import numpy as np

# Carregar variáveis de ambiente (sua API key)
load_dotenv()

def solve_portfolio_optimization_quantum(assets, expected_returns, covariances, budget, risk_factor):
    """
    Resolve o problema de otimização de portfólio usando um QPU real da IBM Quantum.
    """
    try:
        # --- Conexão com a IBM Quantum ---
        api_key = os.getenv("IBM_QUANTUM_API_KEY")
        if not api_key or api_key == "COLE_SUA_API_KEY_DA_IBM_AQUI":
            raise ValueError("API Key da IBM Quantum não encontrada no arquivo .env ou não foi definida.")
        
        provider = IBMProvider(token=api_key)
        
        # Seleciona o backend menos ocupado que não seja um simulador
        backend = provider.get_backend(name='ibm_brisbane') # Exemplo: usando o QPU de 127 qubits 'ibm_brisbane'

        # --- Definição do Problema (igual a antes) ---
        prob = PortfolioOptimization(
            expected_returns=np.array(expected_returns),
            covariances=np.array(covariances),
            risk_factor=risk_factor,
            budget=budget,
            bounds=[(0, 1)] * len(assets)
        )
        qp = prob.to_quadratic_program()
        
        # --- Configuração do Solver Quântico ---
        sampler = Sampler()
        optimizer = SPSA(maxiter=50)
        ansatz = RealAmplitudes(num_qubits=len(assets), reps=3)
        
        # VQE (Variational Quantum Eigensolver) é o algoritmo que rodará no QPU
        vqe = SamplingVQE(sampler=sampler, ansatz=ansatz, optimizer=optimizer)
        
        # O otimizador que usa o VQE para resolver o problema
        optimizer_algo = MinimumEigenOptimizer(vqe)

        # --- Execução e Resultado ---
        result = optimizer_algo.solve(qp)
        allocation = result.x
        
        return {
            "status": "success",
            "backend_used": backend.name,
            "optimal_allocation": {assets[i]: allocation[i] for i in range(len(assets))}
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}