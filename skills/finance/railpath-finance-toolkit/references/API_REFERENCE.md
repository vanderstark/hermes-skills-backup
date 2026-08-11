# API Reference

Complete function documentation for @railpath/finance-toolkit.

## Portfolio Performance

### calculateTimeWeightedReturn
Performance calculation independent of cash flows.

```typescript
function calculateTimeWeightedReturn(options: {
  portfolioValues: number[];      // Portfolio values at each period
  cashFlows: number[];            // Cash flows at each period (0 for no flow)
  annualizationFactor?: number;   // 252 (daily), 52 (weekly), 12 (monthly), 1 (annual)
}): {
  twr: number;                    // Total return for period
  annualizedTWR: number;          // Annualized return
  periodReturns: number[];        // Returns per period
}
```

**Use when**: Buy-and-hold comparison, benchmarking against indices, or evaluating performance independent of investor deposits/withdrawals.

### calculateMoneyWeightedReturn
IRR-based performance accounting for cash flow timing and size.

```typescript
function calculateMoneyWeightedReturn(options: {
  cashFlows: number[];            // All cash flows including initial investment
  dates: Date[];                  // Dates corresponding to cash flows
  finalValue: number;             // Portfolio value at end
  initialValue?: number;          // Starting value (default: 0)
}): {
  mwr: number;                    // IRR/MWR for the period
  annualizedMWR: number;          // Annualized return
  npv: number;                    // Net present value at discount rate
  iterations: number;             // Iterations to convergence
}
```

**Use when**: Evaluating performance with significant deposits/withdrawals, calculating client returns, comparing investor effectiveness.

### calculatePortfolioMetrics
Comprehensive one-shot portfolio analysis.

```typescript
function calculatePortfolioMetrics(options: {
  portfolioValues: number[];      // Portfolio value at each period
  riskFreeRate: number;           // Annual risk-free rate (e.g., 0.02)
  annualizationFactor?: number;   // Default: 252 (daily returns)
}): {
  cagr: number;                   // Compound Annual Growth Rate
  sharpeRatio: number;            // Return per unit risk
  sortinoRatio: number;           // Return per unit downside risk
  maxDrawdown: number;            // Max peak-to-trough loss
  volatility: number;             // Annual volatility
  var95: number;                  // Value at Risk at 95% confidence
  expectedShortfall: number;      // Average loss beyond VaR
}
```

**Use when**: Quick dashboard overview, initial portfolio assessment, comparing strategies side-by-side.

### calculatePerformanceAttribution
Factor-based performance analysis.

```typescript
function calculatePerformanceAttribution(options: {
  returns: number[];              // Portfolio returns
  factorReturns: number[][];      // Returns for each factor
  dates?: Date[];                 // Optional dates for time-series
}): {
  factorContributions: number[];  // Contribution from each factor
  activeReturn: number;           // Return above factors
  explained: number;              // % return explained by factors
}
```

## Risk Metrics

### calculateVaR (Flexible)
Value at Risk across multiple methods.

```typescript
function calculateVaR(options: {
  returns: number[];              // Historical returns
  confidenceLevel: number;        // 0.95 (95%) or 0.99 (99%)
  method: 'historical' | 'parametric' | 'monteCarlo';
  timeHorizon?: number;           // Days ahead (default: 1)
}): number
```

### calculateVaR95 / calculateVaR99
Convenience functions for common confidence levels.

```typescript
calculateVaR95({ returns, method: 'historical' }): number
calculateVaR99({ returns, method: 'parametric' }): number
```

**Methods**:
- **historical**: Uses empirical percentile (no distribution assumptions)
- **parametric**: Assumes normal distribution (faster, less data needed)
- **monteCarlo**: Simulation-based (handles complex risk, computationally intensive)

### calculateSharpeRatio
Risk-adjusted return metric.

```typescript
function calculateSharpeRatio(options: {
  returns: number[];              // Period returns
  riskFreeRate: number;           // Annual rate (e.g., 0.02)
  annualizationFactor?: number;   // 252 (daily), 52 (weekly), 12 (monthly)
}): {
  sharpeRatio: number;            // Return per unit risk
  annualizedReturn: number;
  annualizedVolatility: number;
  excessReturn: number;
}
```

**Interpretation**: Higher is better. 1.0+ is good, 2.0+ is excellent.

### calculateSortinoRatio
Downside-adjusted Sharpe (ignores upside volatility).

```typescript
function calculateSortinoRatio(options: {
  returns: number[];
  riskFreeRate: number;
  annualizationFactor?: number;
  threshold?: number;             // Downside threshold (default: risk-free rate)
}): {
  sortinoRatio: number;
  downregulation: number;         // Volatility below threshold
  excessReturn: number;
}
```

**Use when**: Asymmetric returns (more downside than upside volatility), trend-following strategies.

### calculateMaxDrawdown
Largest peak-to-trough loss.

```typescript
function calculateMaxDrawdown(options: {
  portfolioValues: number[];      // Daily/periodic portfolio values
}): {
  maxDrawdown: number;            // As decimal (e.g., -0.35 = -35%)
  peakValue: number;              // Peak before drawdown
  troughValue: number;            // Lowest point
  duration: number;               // Days/periods from peak to trough
}
```

### calculateStandardDeviation
Classical volatility measure.

```typescript
function calculateStandardDeviation(returns: number[]): number
```

### calculateSkewness / calculateKurtosis
Distribution shape analysis.

```typescript
calculateSkewness(returns: number[]): number   // Asymmetry (-1 to 1)
calculateKurtosis(returns: number[]): number   // Tail thickness (excess kurtosis)
```

### calculateAlpha / calculateBeta
CAPM metrics.

```typescript
function calculateAlpha(options: {
  returns: number[];
  benchmarkReturns: number[];
  riskFreeRate: number;
}): number                                      // Alpha (excess return)

function calculateBeta(options: {
  returns: number[];
  benchmarkReturns: number[];
}): number                                      // Beta (systematic risk)
```

### calculateExpectedShortfall
Average loss beyond VaR (tail risk).

```typescript
function calculateHistoricalExpectedShortfall(options: {
  returns: number[];
  confidenceLevel: number;        // 0.95 or 0.99
}): number

function calculateParametricExpectedShortfall(options: {
  returns: number[];
  confidenceLevel: number;
}): number                                      // Assumes normal distribution
```

### calculateInformationRatio
Active return vs. tracking error.

```typescript
function calculateInformationRatio(options: {
  returns: number[];              // Portfolio returns
  benchmarkReturns: number[];     // Benchmark returns
  annualizationFactor?: number;
}): {
  informationRatio: number;
  activeReturn: number;
  trackingError: number;
}
```

### calculateCalmarRatio
Return vs. maximum drawdown.

```typescript
function calculateCalmarRatio(options: {
  portfolioValues: number[];
  annualizationFactor?: number;
}): number
```

## Technical Indicators

### calculateSMA
Simple Moving Average.

```typescript
function calculateSMA(options: {
  prices: number[];
  period: number;                 // e.g., 20 for 20-period SMA
}): {
  sma: number[];                  // SMA values
  count: number;                  // Number of valid SMA values
  indices: number[];              // Starting indices in original prices
}
```

### calculateEMA
Exponential Moving Average (more weight to recent prices).

```typescript
function calculateEMA(options: {
  prices: number[];
  period: number;                 // e.g., 12 for 12-period EMA
}): {
  ema: number[];
  smoothingFactor: number;        // 2 / (period + 1)
}
```

### calculateMACD
Moving Average Convergence Divergence.

```typescript
function calculateMACD(options: {
  prices: number[];
  fastPeriod?: number;            // Default: 12
  slowPeriod?: number;            // Default: 26
  signalPeriod?: number;          // Default: 9
}): {
  macdLine: number[];             // Fast EMA - Slow EMA
  signalLine: number[];           // EMA of MACD line
  histogram: number[];            // MACD - Signal
}
```

**Signal**: Bullish when MACD crosses above signal line.

### calculateRSI
Relative Strength Index (0-100 momentum).

```typescript
function calculateRSI(options: {
  prices: number[];
  period?: number;                // Default: 14
}): {
  rsi: number[];                  // RSI values (0-100)
  gains: number[];                // Average gains per period
  losses: number[];               // Average losses per period
}
```

**Levels**: >70 overbought, <30 oversold, 50 neutral.

### calculateStochastic
Stochastic Oscillator.

```typescript
function calculateStochastic(options: {
  high: number[];
  low: number[];
  close: number[];
  kPeriod?: number;               // Default: 14
  dPeriod?: number;               // Default: 3
}): {
  percentK: number[];             // %K line
  percentD: number[];             // %D line (SMA of %K)
  highestHigh: number[];
  lowestLow: number[];
}
```

### calculateWilliamsR
Williams %R (-100 to 0).

```typescript
function calculateWilliamsR(options: {
  high: number[];
  low: number[];
  close: number[];
  period?: number;                // Default: 14
}): number[]
```

### calculateBollingerBands
Volatility-based bands.

```typescript
function calculateBollingerBands(options: {
  prices: number[];
  period?: number;                // Default: 20
  stdDevMultiplier?: number;      // Default: 2
}): {
  upper: number[];
  middle: number[];               // SMA
  lower: number[];
  percentB: number[];             // Position between bands (0-1)
  bandwidth: number[];            // (Upper - Lower) / Middle
}
```

### calculateATR
Average True Range (volatility).

```typescript
function calculateATR(options: {
  high: number[];
  low: number[];
  close: number[];
  period?: number;                // Default: 14
}): {
  atr: number[];
  trueRange: number[];
}
```

**Use for**: Position sizing, stop-loss placement, volatility-adjusted entry/exit.

## Volatility Calculations

### calculateVolatility
Standard deviation of returns.

```typescript
function calculateVolatility(returns: number[]): number
```

### calculateEWMAVolatility
Exponentially Weighted Moving Average volatility.

```typescript
function calculateEWMAVolatility(options: {
  returns: number[];
  lambda?: number;                // Decay factor (default: 0.94)
}): number[]
```

**Use when**: Recent volatility matters more (e.g., post-event).

### calculateParkinsonVolatility
High-Low range based (no closing price needed).

```typescript
function calculateParkinsonVolatility(options: {
  high: number[];
  low: number[];
  period?: number;
}): number[]
```

### calculateGarmanKlassVolatility
OHLC-based (most information from open/high/low/close).

```typescript
function calculateGarmanKlassVolatility(options: {
  open: number[];
  high: number[];
  low: number[];
  close: number[];
  period?: number;
}): number[]
```

## Portfolio Analysis

### calculateCorrelationMatrix
Asset correlation structure.

```typescript
function calculateCorrelationMatrix(options: {
  assetReturns: number[][];       // Each row = asset, each column = return
}): number[][]                    // Correlation matrix (n x n)
```

### calculateCovarianceMatrix
Asset covariance structure.

```typescript
function calculateCovarianceMatrix(options: {
  assetReturns: number[][];
}): number[][]                    // Covariance matrix (n x n)
```

### calculatePortfolioVolatility
Combined portfolio risk from weights and correlations.

```typescript
function calculatePortfolioVolatility(options: {
  weights: number[];              // Asset weights (sum = 1)
  covarianceMatrix: number[][];   // Asset covariance
}): number
```

### calculatePortfolioOptimization
Mean-variance optimization.

```typescript
function calculatePortfolioOptimization(options: {
  expectedReturns: number[];      // Expected return per asset
  covarianceMatrix: number[][];   // Asset covariance
  constraints?: {
    minWeight?: number;           // Minimum per asset (default: 0)
    maxWeight?: number;           // Maximum per asset (default: 1)
    targetReturn?: number;        // Minimize variance for target return
  };
}): {
  optimalWeights: number[];
  expectedReturn: number;
  expectedVolatility: number;
  sharpeRatio: number;
}
```

### calculatePortfolioRebalancing
Rebalancing trade calculations.

```typescript
function calculatePortfolioRebalancing(options: {
  currentWeights: number[];
  targetWeights: number[];
  portfolioValue: number;
}): {
  newWeights: number[];
  tradeAmounts: number[];         // Positive = buy, negative = sell
  totalTradingValue: number;
}
```

### calculateEqualWeightPortfolio
Naive diversification.

```typescript
function calculateEqualWeightPortfolio(options: {
  assetCount: number;
}): {
  weights: number[];              // 1/n for each asset
}
```

## Machine Learning - Regime Detection

### detectRegime
Market regime identification via Hidden Markov Model.

```typescript
function detectRegime(
  prices: number[],
  options?: {
    numStates?: number;           // 2-5+ (default: 3)
    features?: string[];          // 'returns', 'volatility', 'rsi', 'macd', 'ema'
    featureWindow?: number;       // Look-back period (default: 20)
    stateLabels?: string[];       // Custom regime names
  }
): {
  currentRegime: string;          // Current regime label
  confidence: number;             // Probability (0-1)
  regimes: string[];              // Regime sequence over time
  probabilities: number[][];      // State probabilities per period
  model: HMMModel;                // Trained model for forward()
}
```

**Default states**: `['bearish', 'neutral', 'bullish']`

**Features**:
- `returns` - Price returns
- `volatility` - Rolling volatility
- `rsi` - RSI indicator
- `macd` - MACD histogram
- `ema` - EMA slope

### trainHMM
Low-level HMM training.

```typescript
function trainHMM(options: {
  featureMatrix: number[][];      // Standardized features
  numStates: number;
  maxIterations?: number;         // Baum-Welch iterations
  convergenceThreshold?: number;
}): HMMModel
```

### extractFeatures
Automatic feature engineering from price data.

```typescript
function extractFeatures(options: {
  prices: number[];
  features: string[];             // Subset of: returns, volatility, rsi, macd, ema
  window?: number;
}): {
  features: number[][];           // Standardized (0-mean, unit variance)
  raw: number[][];                // Original values
}
```

### Advanced HMM Algorithms

```typescript
// Forward algorithm - probability of observations
hmm.forward(observations: number[][]): number[][]

// Backward algorithm - backward pass for smoothing
hmm.backward(observations: number[][]): number[][]

// Viterbi - most likely state sequence
hmm.viterbi(observations: number[][]): number[]

// Baum-Welch - EM training algorithm
hmm.baumWelch(observations: number[][], iterations: number): void
```

## Return Calculations

### calculateReturns
Various return types from prices.

```typescript
function calculateReturns(options: {
  prices: number[];
  type?: 'simple' | 'log' | 'absolute';  // Default: 'simple'
}): number[]
```

- **simple**: (P_t - P_t-1) / P_t-1
- **log**: ln(P_t / P_t-1)
- **absolute**: P_t - P_t-1

## Installation & Type Imports

```typescript
// CommonJS
const { calculateSharpeRatio } = require('@railpath/finance-toolkit');

// ESM
import { calculateSharpeRatio } from '@railpath/finance-toolkit';

// Types
import type { 
  SharpeRatioOptions, 
  SharpeRatioResult,
  MACDOptions,
  MACDResult,
  DetectRegimeOptions,
  HMMModel
} from '@railpath/finance-toolkit';
```

## Error Handling

All functions validate inputs with Zod:

```typescript
try {
  const sharpe = calculateSharpeRatio({
    returns: [],           // Will error: empty array
    riskFreeRate: 0.02
  });
} catch (error) {
  // ZodError with field-level validation messages
  console.error(error.issues);
}
```
