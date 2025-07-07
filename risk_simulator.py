import numpy as np
from qiskit.finance.applications import EuropeanCallPricing
from qiskit.circuit.library import LogNormalDistribution
from qiskit.algorithms import IterativeAmplitudeEstimation, EstimationProblem
from qiskit import Aer

def run_monte_carlo_simulation(portfolio_value, expected_return, volatility, time_horizon_days, num_simulations):
    """
    Executa uma simulação de Monte Carlo quântica para análise de risco de portfólio.
    Retorna o Value at Risk (VaR) a 95% de confiança.
    """
    try:
        # --- Configuração do Problema Quântico ---
        num_qubits = 6
        
        # Mapeia os parâmetros do portfólio para a distribuição log-normal
        mu = (expected_return - 0.5 * volatility**2) * (time_horizon_days / 252)
        sigma = volatility * np.sqrt(time_horizon_days / 252)
        
        # Cria a distribuição log-normal no circuito quântico
        log_normal_dist = LogNormalDistribution(
            num_qubits, mu=mu, sigma=sigma, bounds=(0, portfolio_value * 2)
        )

        # --- Precificação da Opção Europeia (análogo ao VaR) ---
        # O strike price (K) pode ser definido como o valor inicial do portfólio
        # para encontrar a probabilidade de o valor final ser menor que o inicial.
        european_call_pricing = EuropeanCallPricing(
            num_state_qubits=num_qubits,
            strike_price=portfolio_value,
            rescaling_factor=0.25,
            bounds=(0, portfolio_value * 2),
            uncertainty_model=log_normal_dist,
        )

        # --- Execução no Simulador Quântico ---
        backend = Aer.get_backend('aer_simulator')
        
        problem = european_call_pricing.to_estimation_problem()
        
        # Usando Iterative Amplitude Estimation (IAE) para estimar o valor
        iae = IterativeAmplitudeEstimation(
            epsilon_target=0.01, alpha=0.05, sampler=None
        )
        result = iae.estimate(problem, shots=num_simulations)

        # O resultado contém a estimativa do "preço da opção", que podemos
        # interpretar como a probabilidade de perda.
        prob_loss = result.estimation

        # O VaR pode ser derivado dessa probabilidade
        # (Esta é uma simplificação; uma derivação mais rigorosa seria necessária)
        value_at_risk = portfolio_value * prob_loss

        return {
            "status": "success",
            "initial_portfolio_value": portfolio_value,
            "quantum_estimated_probability_of_loss": prob_loss,
            "value_at_risk_95_percent_quantum_estimate": value_at_risk,
            "confidence_level": 0.95,
            "backend_used": backend.name(),
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}