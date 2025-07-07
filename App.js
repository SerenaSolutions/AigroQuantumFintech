import React, { useState } from 'react';
import './App.css';

function App() {
  const [authMessage, setAuthMessage] = useState('');
  const [bankingMessage, setBankingMessage] = useState('');
  const [investmentMessage, setInvestmentMessage] = useState('');

  // Auth Service State
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [authToken, setAuthToken] = useState('');

  // Core Banking Service State
  const [accountId, setAccountId] = useState('');
  const [accountBalance, setAccountBalance] = useState('');
  const [fromAccount, setFromAccount] = useState('');
  const [toAccount, setToAccount] = useState('');
  const [transferAmount, setTransferAmount] = useState('');

  // Investment Service State
  const [assets, setAssets] = useState('A,B,C');
  const [expectedReturns, setExpectedReturns] = useState('0.1,0.2,0.15');
  const [covariances, setCovariances] = useState('[[0.01, 0.005, 0.002], [0.005, 0.04, 0.01], [0.002, 0.01, 0.02]]');
  const [budget, setBudget] = useState('2');
  const [riskFactor, setRiskFactor] = useState('0.5');
  const [portfolioValue, setPortfolioValue] = useState('1000000');
  const [riskExpectedReturn, setRiskExpectedReturn] = useState('0.05');
  const [riskVolatility, setRiskVolatility] = useState('0.2');
  const [timeHorizonDays, setTimeHorizonDays] = useState('252');
  const [dataToSign, setDataToSign] = useState('test data');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/auth/register?password=' + password, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, full_name: fullName }),
      });
      const data = await response.json();
      setAuthMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setAuthMessage('Error: ' + error.message);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `username=${loginUsername}&password=${loginPassword}`,
      });
      const data = await response.json();
      if (response.ok) {
        setAuthToken(data.access_token);
        setAuthMessage('Login successful! Token: ' + data.access_token);
      } else {
        setAuthMessage('Login failed: ' + (data.detail || 'Unknown error'));
      }
    } catch (error) {
      setAuthMessage('Error: ' + error.message);
    }
  };

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/banking/accounts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ account_id: accountId, balance: parseFloat(accountBalance) }),
      });
      const data = await response.json();
      setBankingMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setBankingMessage('Error: ' + error.message);
    }
  };

  const handleGetAccount = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`/banking/accounts/${accountId}`);
      const data = await response.json();
      setBankingMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setBankingMessage('Error: ' + error.message);
    }
  };

  const handleTransfer = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/banking/transfers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from_account: fromAccount, to_account: toAccount, amount: parseFloat(transferAmount) }),
      });
      const data = await response.json();
      setBankingMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setBankingMessage('Error: ' + error.message);
    }
  };

  const handleOptimizePortfolio = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/investment/v1/optimizePortfolio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assets: assets.split(','),
          expected_returns: expectedReturns.split(',').map(Number),
          covariances: JSON.parse(covariances),
          budget: Number(budget),
          risk_factor: Number(riskFactor),
        }),
      });
      const data = await response.json();
      setInvestmentMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setInvestmentMessage('Error: ' + error.message);
    }
  };

  const handleRunRiskSimulation = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/investment/v1/runRiskSimulation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          portfolio_value: Number(portfolioValue),
          expected_return: Number(riskExpectedReturn),
          volatility: Number(riskVolatility),
          time_horizon_days: Number(timeHorizonDays),
        }),
      });
      const data = await response.json();
      setInvestmentMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setInvestmentMessage('Error: ' + error.message);
    }
  };

  const handleGetQuantumResistantSignature = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/investment/v1/getQuantumResistantSignature', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data_to_sign: dataToSign }),
      });
      const data = await response.json();
      setInvestmentMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setInvestmentMessage('Error: ' + error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>QuantumCore Fintech</h1>

        <div className="section">
          <h2>Auth Service</h2>
          <h3>Register</h3>
          <form onSubmit={handleRegister}>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input type="text" placeholder="Full Name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button type="submit">Register</button>
          </form>

          <h3>Login</h3>
          <form onSubmit={handleLogin}>
            <input type="text" placeholder="Username" value={loginUsername} onChange={(e) => setLoginUsername(e.target.value)} />
            <input type="password" placeholder="Password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} />
            <button type="submit">Login</button>
          </form>
          <pre>{authMessage}</pre>
          {authToken && <p>Current Token: {authToken}</p>}
        </div>

        <div className="section">
          <h2>Core Banking Service</h2>
          <h3>Create Account</h3>
          <form onSubmit={handleCreateAccount}>
            <input type="text" placeholder="Account ID" value={accountId} onChange={(e) => setAccountId(e.target.value)} />
            <input type="number" placeholder="Initial Balance" value={accountBalance} onChange={(e) => setAccountBalance(e.target.value)} />
            <button type="submit">Create Account</button>
          </form>

          <h3>Get Account Details</h3>
          <form onSubmit={handleGetAccount}>
            <input type="text" placeholder="Account ID" value={accountId} onChange={(e) => setAccountId(e.target.value)} />
            <button type="submit">Get Account</button>
          </form>

          <h3>Transfer Funds</h3>
          <form onSubmit={handleTransfer}>
            <input type="text" placeholder="From Account ID" value={fromAccount} onChange={(e) => setFromAccount(e.target.value)} />
            <input type="text" placeholder="To Account ID" value={toAccount} onChange={(e) => setToAccount(e.target.value)} />
            <input type="number" placeholder="Amount" value={transferAmount} onChange={(e) => setTransferAmount(e.target.value)} />
            <button type="submit">Transfer</button>
          </form>
          <pre>{bankingMessage}</pre>
        </div>

        <div className="section">
          <h2>Investment Service</h2>
          <h3>Optimize Portfolio</h3>
          <form onSubmit={handleOptimizePortfolio}>
            <label>Assets (comma-separated):</label>
            <input type="text" value={assets} onChange={(e) => setAssets(e.target.value)} />
            <label>Expected Returns (comma-separated):</label>
            <input type="text" value={expectedReturns} onChange={(e) => setExpectedReturns(e.target.value)} />
            <label>Covariances (JSON array of arrays):</label>
            <textarea value={covariances} onChange={(e) => setCovariances(e.target.value)}></textarea>
            <label>Budget:</label>
            <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} />
            <label>Risk Factor:</label>
            <input type="number" value={riskFactor} onChange={(e) => setRiskFactor(e.target.value)} />
            <button type="submit">Optimize Portfolio</button>
          </form>

          <h3>Run Risk Simulation</h3>
          <form onSubmit={handleRunRiskSimulation}>
            <label>Portfolio Value:</label>
            <input type="number" value={portfolioValue} onChange={(e) => setPortfolioValue(e.target.value)} />
            <label>Expected Return (annual):</label>
            <input type="number" value={riskExpectedReturn} onChange={(e) => setRiskExpectedReturn(e.target.value)} />
            <label>Volatility (annual):</label>
            <input type="number" value={riskVolatility} onChange={(e) => setRiskVolatility(e.target.value)} />
            <label>Time Horizon (days):</label>
            <input type="number" value={timeHorizonDays} onChange={(e) => setTimeHorizonDays(e.target.value)} />
            <button type="submit">Run Simulation</button>
          </form>

          <h3>Quantum-Resistant Signature</h3>
          <form onSubmit={handleGetQuantumResistantSignature}>
            <label>Data to Sign:</label>
            <input type="text" value={dataToSign} onChange={(e) => setDataToSign(e.target.value)} />
            <button type="submit">Get Signature</button>
          </form>
          <pre>{investmentMessage}</pre>
        </div>
      </header>
    </div>
  );
}

export default App;