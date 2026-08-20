---
name: railpath-finance-toolkit
description: TypeScript library for portfolio management, risk analytics, and quantitative trading. Provides production-ready functions for performance metrics (TWR/MWR, Sharpe, Sortino, VaR), technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands), volatility calculations, and Hidden Markov Model regime detection. Use when building trading systems, portfolio analytics, risk dashboards, or technical analysis applications requiring validated financial calculations.
---

# RailPath Finance Toolkit Skill

Complete TypeScript library for quantitative finance, portfolio analysis, and systematic trading infrastructure.

## Installation

```bash
npm install @railpath/finance-toolkit
```

Compatible with modern ESM, CommonJS, Jest, TypeScript, and all major bundlers.

## Core Capabilities

### Portfolio Performance
- **Time-Weighted Return (TWR)** - Performance independent of cash flows
- **Money-Weighted Return (MWR)** - IRR-based performance with cash flow consideration
- **Portfolio Metrics** - CAGR, Sharpe, Sortino, VaR, Expected Shortfall, volatility

### Risk Analysis
- **Value at Risk (VaR)** - Historical, Parametric, Monte Carlo methods
- **Expected Shortfall (CVaR)** - Tail risk measurement
- **Maximum Drawdown** - Peak-to-trough analysis
- **Sharpe & Sortino Ratios** - Risk-adjusted returns
- **Alpha & Beta** - CAPM-based metrics

### Technical Indicators
- **Trend**: SMA, EMA, MACD
- **Momentum**: RSI, Stochastic, Williams %R
- **Volatility**: Bollinger Bands, ATR, EWMA Volatility

### Machine Learning
- **Hidden Markov Model (HMM)** - Market regime detection (bullish/bearish/neutral/custom states)
- **Feature Extraction** - Automatic engineering from price data
- **Advanced Algorithms** - Forward, Backward, Viterbi, Baum-Welch

### Portfolio Analysis
- Correlation & Covariance matrices
- Portfolio optimization (mean-variance)
- Rebalancing strategies
- Equal weight allocation

## Common Workflows

### Portfolio Performance Analysis
Import performance functions and calculate returns, then compare against benchmarks:

```typescript
import { 
  calculateTimeWeightedReturn, 
  calculateMoneyWeightedReturn,
  calculatePortfolioMetrics
} from '@railpath/finance-toolkit';

// TWR for buy-and-hold comparison
const twr = calculateTimeWeightedReturn({
  portfolioValues: [1000, 1100, 1200, 1150],
  cashFlows: [0, 100, 0, -50],
  annualizationFactor: 252
});

// MWR when large deposits/withdrawals affect performance
const mwr = calculateMoneyWeightedReturn({
  cashFlows: [1000, 100, -50],
  dates: [new Date('2023-01-01'), new Date('2023-06-01'), new Date('2023-12-01')],
  finalValue: 1150
});
```

### Risk Assessment
Combine multiple risk metrics for comprehensive portfolio analysis:

```typescript
import { 
  calculateVaR, 
  calculateSharpeRatio, 
  calculateMaxDrawdown,
  calculateSortinoRatio 
} from '@railpath/finance-toolkit';

const returns = [0.01, 0.02, -0.01, 0.03, -0.02];

// Downside capture: Sortino better than Sharpe for asymmetric risk
const sortino = calculateSortinoRatio({
  returns,
  riskFreeRate: 0.02,
  annualizationFactor: 252
});

// Tail risk at confidence intervals
const var95 = calculateVaR({
  returns,
  confidenceLevel: 0.95,
  method: 'historical'
});

// Maximum loss from peak
const maxDD = calculateMaxDrawdown({
  portfolioValues: [1000, 1100, 1050, 1200, 1150]
});
```

### Technical Analysis
Build systematic trading signals from price data:

```typescript
import { 
  calculateRSI,
  calculateMACD,
  calculateBollingerBands,
  calculateATR
} from '@railpath/finance-toolkit';

const prices = [100, 102, 101, 103, 105, 104, 106];

// Momentum confirmation
const rsi = calculateRSI({ prices, period: 14 });
const macd = calculateMACD({ prices, fastPeriod: 12, slowPeriod: 26, signalPeriod: 9 });

// Volatility-based position sizing
const atr = calculateATR({ high, low, close, period: 14 });
const bands = calculateBollingerBands({ prices, period: 20, stdDevMultiplier: 2 });
```

### Market Regime Detection
Use machine learning to identify and adapt to market conditions:

```typescript
import { detectRegime } from '@railpath/finance-toolkit';

// Default 3-state regime (bearish, neutral, bullish)
const regime = detectRegime(prices);
console.log(regime.currentRegime); // 'bullish'
console.log(regime.confidence); // 0.85

// Custom regimes with additional features
const advanced = detectRegime(prices, {
  numStates: 4,
  features: ['returns', 'volatility', 'rsi', 'macd'],
  featureWindow: 20,
  stateLabels: ['strong_bear', 'weak_bear', 'weak_bull', 'strong_bull']
});
```

## Type Safety

All functions are fully typed with Zod validation. Import types for IDE autocomplete:

```typescript
import type { 
  SharpeRatioOptions,
  SharpeRatioResult,
  MACDOptions,
  MACDResult,
  DetectRegimeOptions
} from '@railpath/finance-toolkit';

const options: SharpeRatioOptions = {
  returns: [0.01, 0.02, -0.01],
  riskFreeRate: 0.02,
  annualizationFactor: 252
};

const result: SharpeRatioResult = calculateSharpeRatio(options);
```

## API Organization

All functions follow consistent patterns:

- **Portfolio Performance**: `calculateTimeWeightedReturn`, `calculateMoneyWeightedReturn`, `calculatePortfolioMetrics`
- **Risk Metrics**: `calculateVaR*`, `calculateSharpe*`, `calculateSortino*`, `calculateMaxDrawdown`
- **Technical Indicators**: `calculate[IndicatorName]` (SMA, EMA, MACD, RSI, Stochastic, Williams%R, BollingerBands, ATR)
- **Volatility**: `calculateVolatility`, `calculateEWMAVolatility`, `calculateParkinsonVolatility`, `calculateGarmanKlassVolatility`
- **Portfolio Analysis**: `calculateCorrelationMatrix`, `calculateCovarianceMatrix`, `calculatePortfolioVolatility`
- **ML Regime Detection**: `detectRegime`, `trainHMM`, `extractFeatures`, plus low-level HMM algorithms

## Reference Materials

For detailed information, consult:

**Core References**
- **[API_REFERENCE.md](references/API_REFERENCE.md)** - Complete function signatures, parameters, return types
- **[EXAMPLES.md](references/EXAMPLES.md)** - Practical workflow examples: portfolio analysis, risk dashboards, technical analysis, regime-based trading
- **[TYPE_DEFINITIONS.md](references/TYPE_DEFINITIONS.md)** - TypeScript interfaces for all functions

**Advanced Trading Domains**
- **[STRATEGIC_TRADING.md](references/STRATEGIC_TRADING.md)** - Mean reversion systems, momentum trading, multi-timeframe confluence, order flow analysis
- **[ML_REFINEMENTS.md](references/ML_REFINEMENTS.md)** - HMM optimization, regime-aware portfolios, adaptive trading rules, feature engineering, ensemble models
- **[BACKTESTING_VALIDATION.md](references/BACKTESTING_VALIDATION.md)** - Complete backtest harness, walk-forward analysis, overfitting detection, Monte Carlo simulation

## Quality Guarantees

- **1200+ tests** across 59 test files ensuring accuracy
- **Battle-tested** against Python equivalents (numpy, scipy, pandas)
- **Performance benchmarks** for datasets of various sizes
- **Zero runtime dependencies** - CommonJS build for maximum compatibility
- **Full TypeScript support** with Zod validation

## Common Use Cases

**Portfolio Managers**: Performance attribution, benchmarking, cash flow analysis, risk optimization

**Risk Managers**: VaR/ES monitoring, stress testing, concentration analysis, drawdown tracking

**Quantitative Analysts**: Factor models, volatility forecasting, correlation analysis, regime detection

**Technical Traders**: Trend signals (SMA/EMA/MACD), momentum indicators (RSI/Stochastic), volatility-based positioning

**Systematic Traders**: Mean reversion & momentum systems, multi-timeframe confluence, order flow analysis, regime-aware position sizing

**Machine Learning Engineers**: HMM regime optimization, feature engineering, ensemble model combining, adaptive trading rules

**Quant Researchers**: Walk-forward backtesting, overfitting detection, Monte Carlo validation, strategy robustness analysis

**Financial Advisors**: Client performance reporting, risk assessment, asset allocation optimization
