# Type Definitions

Complete TypeScript interfaces for @railpath/finance-toolkit.

## Portfolio Performance Types

### TimeWeightedReturnOptions / TimeWeightedReturnResult

```typescript
interface TimeWeightedReturnOptions {
  portfolioValues: number[];
  cashFlows: number[];
  annualizationFactor?: number;
}

interface TimeWeightedReturnResult {
  twr: number;
  annualizedTWR: number;
  periodReturns: number[];
}
```

### MoneyWeightedReturnOptions / MoneyWeightedReturnResult

```typescript
interface MoneyWeightedReturnOptions {
  cashFlows: number[];
  dates: Date[];
  finalValue: number;
  initialValue?: number;
}

interface MoneyWeightedReturnResult {
  mwr: number;
  annualizedMWR: number;
  npv: number;
  iterations: number;
}
```

### PortfolioMetricsOptions / PortfolioMetricsResult

```typescript
interface PortfolioMetricsOptions {
  portfolioValues: number[];
  riskFreeRate: number;
  annualizationFactor?: number;
}

interface PortfolioMetricsResult {
  cagr: number;
  sharpeRatio: number;
  sortinoRatio: number;
  maxDrawdown: number;
  volatility: number;
  var95: number;
  expectedShortfall: number;
}
```

### PerformanceAttributionOptions / PerformanceAttributionResult

```typescript
interface PerformanceAttributionOptions {
  returns: number[];
  factorReturns: number[][];
  dates?: Date[];
}

interface PerformanceAttributionResult {
  factorContributions: number[];
  activeReturn: number;
  explained: number;
}
```

## Risk Metrics Types

### VaROptions

```typescript
interface VaROptions {
  returns: number[];
  confidenceLevel: number;        // 0.95 or 0.99
  method: 'historical' | 'parametric' | 'monteCarlo';
  timeHorizon?: number;
}
```

### SharpeRatioOptions / SharpeRatioResult

```typescript
interface SharpeRatioOptions {
  returns: number[];
  riskFreeRate: number;
  annualizationFactor?: number;
}

interface SharpeRatioResult {
  sharpeRatio: number;
  annualizedReturn: number;
  annualizedVolatility: number;
  excessReturn: number;
}
```

### SortinoRatioOptions / SortinoRatioResult

```typescript
interface SortinoRatioOptions {
  returns: number[];
  riskFreeRate: number;
  annualizationFactor?: number;
  threshold?: number;
}

interface SortinoRatioResult {
  sortinoRatio: number;
  downregulation: number;
  excessReturn: number;
}
```

### MaxDrawdownOptions / MaxDrawdownResult

```typescript
interface MaxDrawdownOptions {
  portfolioValues: number[];
}

interface MaxDrawdownResult {
  maxDrawdown: number;
  peakValue: number;
  troughValue: number;
  duration: number;
}
```

### AlphaOptions / BetaOptions

```typescript
interface AlphaOptions {
  returns: number[];
  benchmarkReturns: number[];
  riskFreeRate: number;
}

interface BetaOptions {
  returns: number[];
  benchmarkReturns: number[];
}
```

### ExpectedShortfallOptions

```typescript
interface ExpectedShortfallOptions {
  returns: number[];
  confidenceLevel: number;
}
```

### InformationRatioOptions / InformationRatioResult

```typescript
interface InformationRatioOptions {
  returns: number[];
  benchmarkReturns: number[];
  annualizationFactor?: number;
}

interface InformationRatioResult {
  informationRatio: number;
  activeReturn: number;
  trackingError: number;
}
```

### CalmarRatioOptions

```typescript
interface CalmarRatioOptions {
  portfolioValues: number[];
  annualizationFactor?: number;
}
```

## Technical Indicators Types

### SMAOptions / SMAResult

```typescript
interface SMAOptions {
  prices: number[];
  period: number;
}

interface SMAResult {
  sma: number[];
  count: number;
  indices: number[];
}
```

### EMAOptions / EMAResult

```typescript
interface EMAOptions {
  prices: number[];
  period: number;
}

interface EMAResult {
  ema: number[];
  smoothingFactor: number;
}
```

### MACDOptions / MACDResult

```typescript
interface MACDOptions {
  prices: number[];
  fastPeriod?: number;
  slowPeriod?: number;
  signalPeriod?: number;
}

interface MACDResult {
  macdLine: number[];
  signalLine: number[];
  histogram: number[];
}
```

### RSIOptions / RSIResult

```typescript
interface RSIOptions {
  prices: number[];
  period?: number;
}

interface RSIResult {
  rsi: number[];
  gains: number[];
  losses: number[];
}
```

### StochasticOptions / StochasticResult

```typescript
interface StochasticOptions {
  high: number[];
  low: number[];
  close: number[];
  kPeriod?: number;
  dPeriod?: number;
}

interface StochasticResult {
  percentK: number[];
  percentD: number[];
  highestHigh: number[];
  lowestLow: number[];
}
```

### WilliamsROptions

```typescript
interface WilliamsROptions {
  high: number[];
  low: number[];
  close: number[];
  period?: number;
}
```

### BollingerBandsOptions / BollingerBandsResult

```typescript
interface BollingerBandsOptions {
  prices: number[];
  period?: number;
  stdDevMultiplier?: number;
}

interface BollingerBandsResult {
  upper: number[];
  middle: number[];
  lower: number[];
  percentB: number[];
  bandwidth: number[];
}
```

### ATROptions / ATRResult

```typescript
interface ATROptions {
  high: number[];
  low: number[];
  close: number[];
  period?: number;
}

interface ATRResult {
  atr: number[];
  trueRange: number[];
}
```

## Volatility Types

### EWMAVolatilityOptions

```typescript
interface EWMAVolatilityOptions {
  returns: number[];
  lambda?: number;
}
```

### ParkinsonVolatilityOptions

```typescript
interface ParkinsonVolatilityOptions {
  high: number[];
  low: number[];
  period?: number;
}
```

### GarmanKlassVolatilityOptions

```typescript
interface GarmanKlassVolatilityOptions {
  open: number[];
  high: number[];
  low: number[];
  close: number[];
  period?: number;
}
```

## Portfolio Analysis Types

### CorrelationMatrixOptions

```typescript
interface CorrelationMatrixOptions {
  assetReturns: number[][];
}
```

### CovarianceMatrixOptions

```typescript
interface CovarianceMatrixOptions {
  assetReturns: number[][];
}
```

### PortfolioVolatilityOptions

```typescript
interface PortfolioVolatilityOptions {
  weights: number[];
  covarianceMatrix: number[][];
}
```

### PortfolioOptimizationOptions / PortfolioOptimizationResult

```typescript
interface PortfolioOptimizationConstraints {
  minWeight?: number;
  maxWeight?: number;
  targetReturn?: number;
}

interface PortfolioOptimizationOptions {
  expectedReturns: number[];
  covarianceMatrix: number[][];
  constraints?: PortfolioOptimizationConstraints;
}

interface PortfolioOptimizationResult {
  optimalWeights: number[];
  expectedReturn: number;
  expectedVolatility: number;
  sharpeRatio: number;
}
```

### PortfolioRebalancingOptions / PortfolioRebalancingResult

```typescript
interface PortfolioRebalancingOptions {
  currentWeights: number[];
  targetWeights: number[];
  portfolioValue: number;
}

interface PortfolioRebalancingResult {
  newWeights: number[];
  tradeAmounts: number[];
  totalTradingValue: number;
}
```

### EqualWeightPortfolioOptions

```typescript
interface EqualWeightPortfolioOptions {
  assetCount: number;
}

interface EqualWeightPortfolioResult {
  weights: number[];
}
```

## Machine Learning Types

### DetectRegimeOptions / DetectRegimeResult

```typescript
interface DetectRegimeOptions {
  numStates?: number;
  features?: string[];
  featureWindow?: number;
  stateLabels?: string[];
}

interface DetectRegimeResult {
  currentRegime: string;
  confidence: number;
  regimes: string[];
  probabilities: number[][];
  model: HMMModel;
}
```

### TrainHMMOptions

```typescript
interface TrainHMMOptions {
  featureMatrix: number[][];
  numStates: number;
  maxIterations?: number;
  convergenceThreshold?: number;
}
```

### ExtractFeaturesOptions / ExtractFeaturesResult

```typescript
interface ExtractFeaturesOptions {
  prices: number[];
  features: string[];
  window?: number;
}

interface ExtractFeaturesResult {
  features: number[][];
  raw: number[][];
}
```

### HMMModel

```typescript
interface HMMModel {
  transitionMatrix: number[][];      // State transition probabilities
  emissionMeans: number[][];         // Mean for each state's emission
  emissionCovariances: number[][][]; // Covariance for each state
  initialProbabilities: number[];    // Initial state probabilities
  
  forward(observations: number[][]): number[][];
  backward(observations: number[][]): number[][];
  viterbi(observations: number[][]): number[];
  baumWelch(observations: number[][], iterations: number): void;
}
```

## Return Calculation Types

### CalculateReturnsOptions

```typescript
interface CalculateReturnsOptions {
  prices: number[];
  type?: 'simple' | 'log' | 'absolute';
}
```

## Universal Options

### Annualization Factors

```typescript
type AnnualizationFactor = 
  | 252  // Daily returns (trading days per year)
  | 52   // Weekly returns
  | 12   // Monthly returns
  | 1;   // Already annualized
```

## Generic Type Utilities

```typescript
// Extract from options to result
type OptionsToResult<T extends { Options: any; Result: any }> = T['Result'];

// Common numeric matrix type
type Matrix = number[][];

// Common covariance/correlation structure
type CovarianceMatrix = number[][];
type CorrelationMatrix = number[][];

// Portfolio weights (must sum to ~1.0)
type Weights = number[];

// Returns series (can be simple, log, or absolute)
type Returns = number[];

// Price series
type Prices = number[];

// State labels for regime detection
type RegimeLabel = string;
type RegimeLabels = RegimeLabel[];
```

## Import Examples

```typescript
// Import types for type safety
import type {
  SharpeRatioOptions,
  SharpeRatioResult,
  TimeWeightedReturnOptions,
  TimeWeightedReturnResult,
  MACDOptions,
  MACDResult,
  DetectRegimeOptions,
  DetectRegimeResult,
  HMMModel,
  PortfolioOptimizationResult,
  // ... all other types
} from '@railpath/finance-toolkit';

// Use in function definitions
function analyzePortfolio(options: SharpeRatioOptions): SharpeRatioResult {
  // Implementation
}

// Use in variable declarations
const regimeOptions: DetectRegimeOptions = {
  numStates: 3,
  features: ['returns', 'volatility', 'rsi']
};

const result: DetectRegimeResult = detectRegime(prices, regimeOptions);
```

## Validation

All options are validated with Zod before processing:

```typescript
// These will throw ZodError
calculateSharpeRatio({
  returns: [],              // ❌ Empty array invalid
  riskFreeRate: 0.02
});

calculateSharpeRatio({
  returns: [0.01, 0.02],
  riskFreeRate: -0.05       // ❌ Negative rate suspicious
});

// Zod error structure
// {
//   issues: [
//     {
//       path: ['returns'],
//       message: 'Array must contain at least 1 elements',
//       code: 'too_small'
//     }
//   ]
// }
```

## Extending Types

Define custom types for your use case:

```typescript
// Portfolio context
interface Portfolio {
  name: string;
  values: number[];
  returns: number[];
  benchmarkReturns: number[];
}

// Risk context
interface RiskMetrics {
  var95: number;
  var99: number;
  sharpe: number;
  sortino: number;
  maxDD: number;
}

// Analysis result
interface PortfolioAnalysis {
  portfolio: Portfolio;
  metrics: RiskMetrics;
  timestamp: Date;
}

// Type-safe wrapper
function analyzePortfolio(portfolio: Portfolio): PortfolioAnalysis {
  const metrics: RiskMetrics = {
    var95: calculateVaR({ returns: portfolio.returns, confidenceLevel: 0.95 }),
    var99: calculateVaR({ returns: portfolio.returns, confidenceLevel: 0.99 }),
    sharpe: calculateSharpeRatio({ returns: portfolio.returns, riskFreeRate: 0.04 }).sharpeRatio,
    sortino: calculateSortinoRatio({ returns: portfolio.returns, riskFreeRate: 0.04 }).sortinoRatio,
    maxDD: calculateMaxDrawdown({ portfolioValues: portfolio.values }).maxDrawdown
  };

  return { portfolio, metrics, timestamp: new Date() };
}
```
