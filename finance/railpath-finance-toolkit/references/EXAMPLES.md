# Practical Examples

Real-world workflows using @railpath/finance-toolkit.

## Portfolio Performance Dashboard

Calculate comprehensive metrics for client reporting.

```typescript
import { 
  calculatePortfolioMetrics,
  calculatePortfolioRebalancing,
  calculateCorrelationMatrix,
  calculateInformationRatio
} from '@railpath/finance-toolkit';

// Portfolio values over time (daily)
const portfolioValues = [100000, 101500, 103200, 102100, 104500];
const benchmarkReturns = [0.015, 0.018, -0.005, 0.025];
const portfolioReturns = [0.015, 0.017, -0.011, 0.023];
const riskFreeRate = 0.045;

// Comprehensive metrics
const metrics = calculatePortfolioMetrics({
  portfolioValues,
  riskFreeRate
});

console.log(`
Portfolio Dashboard
═══════════════════════════════════════
CAGR:           ${(metrics.cagr * 100).toFixed(2)}%
Sharpe Ratio:   ${metrics.sharpeRatio.toFixed(2)}
Sortino Ratio:  ${metrics.sortinoRatio.toFixed(2)}
Max Drawdown:   ${(metrics.maxDrawdown * 100).toFixed(2)}%
Annual Vol:     ${(metrics.volatility * 100).toFixed(2)}%
Value at Risk:  ${(metrics.var95 * 100).toFixed(2)}%
═══════════════════════════════════════
`);

// Active return vs benchmark
const activeMetrics = calculateInformationRatio({
  returns: portfolioReturns,
  benchmarkReturns,
  annualizationFactor: 252
});

console.log(`
Active Management
─────────────────────────────────────
Information Ratio:  ${activeMetrics.informationRatio.toFixed(2)}
Active Return:      ${(activeMetrics.activeReturn * 100).toFixed(2)}%
Tracking Error:     ${(activeMetrics.trackingError * 100).toFixed(2)}%
`);
```

## Risk-Adjusted Return Analysis

Compare strategies using multiple risk metrics.

```typescript
import { 
  calculateVaR,
  calculateSharpeRatio,
  calculateSortinoRatio,
  calculateMaxDrawdown,
  calculateCalmarRatio
} from '@railpath/finance-toolkit';

const strategy1Returns = [0.02, 0.01, -0.005, 0.015, 0.03, -0.01, 0.025];
const strategy2Returns = [0.015, 0.012, -0.008, 0.008, 0.02, -0.002, 0.018];

function analyzeStrategy(name, returns) {
  const sharpe = calculateSharpeRatio({
    returns,
    riskFreeRate: 0.04,
    annualizationFactor: 252
  });

  const sortino = calculateSortinoRatio({
    returns,
    riskFreeRate: 0.04,
    annualizationFactor: 252
  });

  const var95 = calculateVaR({
    returns,
    confidenceLevel: 0.95,
    method: 'historical'
  });

  const portfolioValues = [100000];
  let value = 100000;
  for (const r of returns) {
    value *= (1 + r);
    portfolioValues.push(value);
  }

  const maxDD = calculateMaxDrawdown({ portfolioValues });
  const calmar = calculateCalmarRatio({
    portfolioValues,
    annualizationFactor: 252
  });

  console.log(`
${name}
────────────────────────────────
Sharpe:          ${sharpe.sharpeRatio.toFixed(2)}
Sortino:         ${sortino.sortinoRatio.toFixed(2)}
VaR (95%):       ${(var95 * 100).toFixed(2)}%
Max Drawdown:    ${(maxDD.maxDrawdown * 100).toFixed(2)}%
Calmar Ratio:    ${calmar.toFixed(2)}
  `);
}

analyzeStrategy('Mean Reversion', strategy1Returns);
analyzeStrategy('Momentum', strategy2Returns);
```

## Technical Analysis with Trading Signals

Build systematic trading signals from multiple indicators.

```typescript
import {
  calculateRSI,
  calculateMACD,
  calculateBollingerBands,
  calculateATR,
  calculateEMA
} from '@railpath/finance-toolkit';

const prices = [100, 101, 99, 102, 104, 103, 105, 107, 106, 108, 110, 109];
const high = [101, 102, 100, 103, 105, 104, 106, 108, 107, 109, 111, 110];
const low = [99, 100, 98, 101, 103, 102, 104, 106, 105, 107, 109, 108];

// Momentum analysis
const rsi = calculateRSI({ prices, period: 14 });
const macd = calculateMACD({ prices, fastPeriod: 12, slowPeriod: 26, signalPeriod: 9 });

// Volatility-based entry/exit
const atr = calculateATR({ high, low, close: prices, period: 14 });
const bands = calculateBollingerBands({ prices, period: 20, stdDevMultiplier: 2 });

// Trend confirmation
const ema = calculateEMA({ prices, period: 12 });

function generateSignal(index) {
  if (index < 2) return 'HOLD'; // Not enough data

  const rsiValue = rsi.rsi[index];
  const macdHistogram = macd.histogram[index];
  const bandPosition = bands.percentB[index];
  const emaSlope = ema.ema[index] > ema.ema[index - 1] ? 'up' : 'down';

  // Multi-indicator confirmation
  if (
    rsiValue < 30 &&
    macdHistogram < 0 &&
    bandPosition < 0.2 &&
    emaSlope === 'up'
  ) {
    return 'STRONG_BUY';
  }

  if (rsiValue < 40 && macdHistogram < 0) {
    return 'BUY';
  }

  if (rsiValue > 70 && macdHistogram > 0) {
    return 'SELL';
  }

  if (rsiValue > 60 && bandPosition > 0.8) {
    return 'PROFIT_TAKING';
  }

  return 'HOLD';
}

// Position sizing based on volatility
function calculatePositionSize(riskAmount, index) {
  const atrValue = atr.atr[index];
  const stopLoss = 2 * atrValue;
  const shares = Math.floor(riskAmount / stopLoss);
  return { shares, stopLoss, stopPrice: prices[index] - stopLoss };
}

for (let i = 2; i < prices.length; i++) {
  const signal = generateSignal(i);
  if (signal !== 'HOLD') {
    const position = calculatePositionSize(1000, i);
    console.log(`
Index ${i}: Signal ${signal} at ${prices[i]}
  Position: ${position.shares} shares
  Stop Loss: ${position.stopPrice.toFixed(2)}
    `);
  }
}
```

## Portfolio Optimization & Rebalancing

Construct optimal portfolio and rebalance.

```typescript
import {
  calculatePortfolioOptimization,
  calculatePortfolioRebalancing,
  calculateCorrelationMatrix,
  calculateCovarianceMatrix
} from '@railpath/finance-toolkit';

// Asset expected returns and historical returns
const expectedReturns = [0.08, 0.10, 0.06];
const assetReturns = [
  [0.01, 0.02, -0.01, 0.015, 0.02],   // Asset 1
  [0.012, 0.025, -0.005, 0.018, 0.022],   // Asset 2
  [0.008, 0.015, -0.015, 0.010, 0.012]    // Asset 3
];

// Calculate covariance
const cov = calculateCovarianceMatrix({ assetReturns });

// Optimize for Sharpe ratio
const optimal = calculatePortfolioOptimization({
  expectedReturns,
  covarianceMatrix: cov,
  constraints: {
    minWeight: 0.1,      // Min 10% per asset
    maxWeight: 0.5       // Max 50% per asset
  }
});

console.log(`
Optimal Portfolio
─────────────────────────────────
Weights:        ${optimal.optimalWeights.map(w => (w * 100).toFixed(1)).join('%, ')}%
Expected Return: ${(optimal.expectedReturn * 100).toFixed(2)}%
Volatility:     ${(optimal.expectedVolatility * 100).toFixed(2)}%
Sharpe Ratio:   ${optimal.sharpeRatio.toFixed(2)}
`);

// Rebalance current portfolio to target
const currentValue = 100000;
const currentWeights = [0.35, 0.50, 0.15];  // Current allocation
const targetWeights = optimal.optimalWeights;

const rebalance = calculatePortfolioRebalancing({
  currentWeights,
  targetWeights,
  portfolioValue: currentValue
});

console.log(`
Rebalancing Trades
─────────────────────────────────
Asset 1: ${rebalance.tradeAmounts[0] > 0 ? 'BUY' : 'SELL'} $${Math.abs(rebalance.tradeAmounts[0]).toFixed(0)}
Asset 2: ${rebalance.tradeAmounts[1] > 0 ? 'BUY' : 'SELL'} $${Math.abs(rebalance.tradeAmounts[1]).toFixed(0)}
Asset 3: ${rebalance.tradeAmounts[2] > 0 ? 'BUY' : 'SELL'} $${Math.abs(rebalance.tradeAmounts[2]).toFixed(0)}
Total Trading: $${rebalance.totalTradingValue.toFixed(0)}
`);
```

## Regime-Based Trading Strategy

Adapt strategy to market conditions.

```typescript
import { detectRegime } from '@railpath/finance-toolkit';
import {
  calculateSMA,
  calculateEMA,
  calculateATR
} from '@railpath/finance-toolkit';

const prices = [100, 101.5, 100.2, 102.1, 104.3, 103.1, 105.2, 107.5, 106.1, 108.5];

// Detect current market regime
const regime = detectRegime(prices, {
  numStates: 3,
  features: ['returns', 'volatility', 'rsi'],
  featureWindow: 20,
  stateLabels: ['bearish', 'neutral', 'bullish']
});

console.log(`Current Regime: ${regime.currentRegime} (${(regime.confidence * 100).toFixed(0)}% confidence)`);

// Adapt strategy to regime
function getStrategyParams(currentRegime) {
  const params = {
    bullish: {
      positionSize: 1.0,      // Full size
      riskLimit: 0.02,        // 2% risk per trade
      takeProfitMultiplier: 3, // 3:1 R:R
      useTrail: true          // Trailing stops
    },
    neutral: {
      positionSize: 0.5,      // Reduce exposure
      riskLimit: 0.015,
      takeProfitMultiplier: 2,
      useTrail: false
    },
    bearish: {
      positionSize: 0.25,     // Minimal exposure
      riskLimit: 0.01,
      takeProfitMultiplier: 1.5,
      useTrail: false
    }
  };
  return params[currentRegime];
}

const params = getStrategyParams(regime.currentRegime);

// Use regime-adjusted parameters
const ema = calculateEMA({ prices, period: 12 });
const atr = calculateATR({
  high: prices.map(p => p * 1.01),
  low: prices.map(p => p * 0.99),
  close: prices,
  period: 14
});

const lastPrice = prices[prices.length - 1];
const lastATR = atr.atr[atr.atr.length - 1];
const riskAmount = 1000;
const positionSize = (riskAmount / lastATR) * params.positionSize;
const stopLoss = lastPrice - (2 * lastATR);
const takeProfit = lastPrice + (lastATR * params.takeProfitMultiplier);

console.log(`
Trade Parameters (${regime.currentRegime.toUpperCase()})
─────────────────────────────────────
Position Size:  ${positionSize.toFixed(0)} units
Entry:          ${lastPrice.toFixed(2)}
Stop Loss:      ${stopLoss.toFixed(2)} (-${((lastPrice - stopLoss) / lastPrice * 100).toFixed(1)}%)
Take Profit:    ${takeProfit.toFixed(2)} (+${((takeProfit - lastPrice) / lastPrice * 100).toFixed(1)}%)
Risk/Reward:    1:${params.takeProfitMultiplier.toFixed(1)}
`);
```

## Risk Monitoring Dashboard

Real-time risk tracking across positions.

```typescript
import {
  calculateVaR,
  calculateExpectedShortfall,
  calculateMaxDrawdown,
  calculateVolatility,
  calculateBeta,
  calculateAlpha
} from '@railpath/finance-toolkit';

const positions = {
  'US_EQUITY': { value: 500000, returns: [0.01, 0.02, -0.005, 0.015] },
  'INTL_EQUITY': { value: 300000, returns: [0.008, 0.015, -0.01, 0.012] },
  'BONDS': { value: 150000, returns: [0.002, 0.003, 0.001, 0.0025] },
  'COMMODITIES': { value: 50000, returns: [0.05, -0.03, 0.04, 0.02] }
};

const benchmarkReturns = [0.012, 0.018, -0.003, 0.014];
const riskFreeRate = 0.04;

function monitorRisk(name, position) {
  const var95 = calculateVaR({
    returns: position.returns,
    confidenceLevel: 0.95,
    method: 'historical'
  });

  const es = calculateExpectedShortfall({
    returns: position.returns,
    confidenceLevel: 0.95
  });

  const vol = calculateVolatility(position.returns);
  const alpha = calculateAlpha({
    returns: position.returns,
    benchmarkReturns,
    riskFreeRate
  });

  const beta = calculateBeta({
    returns: position.returns,
    benchmarkReturns
  });

  const dollarVaR = position.value * var95;
  const dollarES = position.value * es;

  console.log(`
${name}
─────────────────────────────────
Position Size:    $${(position.value / 1000).toFixed(0)}k
Volatility:       ${(vol * 100).toFixed(2)}%
Beta:             ${beta.toFixed(2)}
Alpha:            ${(alpha * 100).toFixed(2)}%
VaR (95%):        ${(var95 * 100).toFixed(2)}% (${dollarVaR.toFixed(0)})
Expected Shortfall: ${(es * 100).toFixed(2)}% (${dollarES.toFixed(0)})
  `);

  return { dollarVaR, dollarES };
}

// Portfolio summary
let totalValue = 0;
let totalVaR = 0;
let totalES = 0;

for (const [name, position] of Object.entries(positions)) {
  const risk = monitorRisk(name, position);
  totalValue += position.value;
  totalVaR += risk.dollarVaR;
  totalES += risk.dollarES;
}

console.log(`
PORTFOLIO SUMMARY
═════════════════════════════════
Total Value:      $${(totalValue / 1000).toFixed(0)}k
Portfolio VaR:    $${totalVaR.toFixed(0)}
Portfolio ES:     $${totalES.toFixed(0)}
VaR as % of AUM:  ${(totalVaR / totalValue * 100).toFixed(2)}%
═════════════════════════════════
`);
```

## Factor Model Analysis

Decompose returns into factor contributions.

```typescript
import {
  calculatePerformanceAttribution,
  calculateCorrelationMatrix
} from '@railpath/finance-toolkit';

const portfolioReturns = [0.015, 0.018, -0.005, 0.020, 0.025];
const factorReturns = [
  [0.010, 0.015, -0.008, 0.018, 0.022],  // Market factor
  [0.003, 0.005, -0.002, 0.006, 0.008],  // Size factor
  [0.002, 0.004, -0.001, 0.005, 0.007]   // Value factor
];

// Analyze factor contributions
const attribution = calculatePerformanceAttribution({
  returns: portfolioReturns,
  factorReturns
});

console.log(`
Factor Attribution Analysis
─────────────────────────────────
Total Return:           ${(portfolioReturns.reduce((a, r) => a + r) * 100).toFixed(2)}%
Market Contribution:    ${(attribution.factorContributions[0] * 100).toFixed(2)}%
Size Contribution:      ${(attribution.factorContributions[1] * 100).toFixed(2)}%
Value Contribution:     ${(attribution.factorContributions[2] * 100).toFixed(2)}%
Active Return:          ${(attribution.activeReturn * 100).toFixed(2)}%
Factor Explanation:     ${(attribution.explained * 100).toFixed(1)}%
`);

// Factor correlation analysis
const assetReturns = [portfolioReturns, ...factorReturns];
const correlation = calculateCorrelationMatrix({ assetReturns });

console.log(`
Correlation with Factors
─────────────────────────────────
Portfolio vs Market:    ${correlation[0][1].toFixed(3)}
Portfolio vs Size:      ${correlation[0][2].toFixed(3)}
Portfolio vs Value:     ${correlation[0][3].toFixed(3)}
`);
```
