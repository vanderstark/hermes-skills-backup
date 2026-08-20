# Backtesting & Validation Framework

Production-ready backtesting harness with statistical validation.

## Complete Backtest Harness

Full backtesting implementation with realistic assumptions.

```typescript
import {
  calculateReturns,
  calculateMaxDrawdown,
  calculateSharpeRatio,
  calculateSortinoRatio,
  calculateVolatility
} from '@railpath/finance-toolkit';

interface Trade {
  entry_time: Date;
  entry_price: number;
  exit_time: Date;
  exit_price: number;
  quantity: number;
  side: 'long' | 'short';
  pnl: number;
  pnl_percent: number;
  cost: number;
}

interface BacktestStats {
  totalTrades: number;
  winningTrades: number;
  losingTrades: number;
  winRate: number;
  avgWin: number;
  avgLoss: number;
  profitFactor: number;
  totalPnL: number;
  grossProfit: number;
  grossLoss: number;
  maxConsecutiveWins: number;
  maxConsecutiveLosses: number;
  returnPercent: number;
  sharpeRatio: number;
  sortinoRatio: number;
  maxDrawdown: number;
  calmarRatio: number;
}

class BacktestEngine {
  private trades: Trade[] = [];
  private portfolioValues: number[] = [];
  private baseCapital: number;
  private slippage: number;        // Bid-ask impact
  private commissionPercentage: number;

  constructor(
    baseCapital: number = 100000,
    slippage: number = 0.001,      // 10 basis points
    commissionPercentage: number = 0.001  // 10 basis points
  ) {
    this.baseCapital = baseCapital;
    this.slippage = slippage;
    this.commissionPercentage = commissionPercentage;
    this.portfolioValues = [baseCapital];
  }

  executeTrade(
    entryTime: Date,
    entryPrice: number,
    exitTime: Date,
    exitPrice: number,
    quantity: number,
    side: 'long' | 'short'
  ): Trade {
    // Apply slippage
    const actualEntryPrice = side === 'long'
      ? entryPrice * (1 + this.slippage)
      : entryPrice * (1 - this.slippage);

    const actualExitPrice = side === 'long'
      ? exitPrice * (1 - this.slippage)
      : exitPrice * (1 + this.slippage);

    // Calculate costs
    const entryCost = actualEntryPrice * quantity;
    const exitRevenue = actualExitPrice * quantity;
    const entryCommission = entryCost * this.commissionPercentage;
    const exitCommission = exitRevenue * this.commissionPercentage;

    // Calculate PnL
    let pnl: number;
    if (side === 'long') {
      pnl = exitRevenue - entryCost - entryCommission - exitCommission;
    } else {
      pnl = entryCost - exitRevenue - entryCommission - exitCommission;
    }

    const pnlPercent = pnl / entryCost;

    const trade: Trade = {
      entry_time: entryTime,
      entry_price: actualEntryPrice,
      exit_time: exitTime,
      exit_price: actualExitPrice,
      quantity,
      side,
      pnl,
      pnl_percent: pnlPercent,
      cost: entryCost
    };

    this.trades.push(trade);

    // Update portfolio value
    const lastValue = this.portfolioValues[this.portfolioValues.length - 1];
    this.portfolioValues.push(lastValue + pnl);

    return trade;
  }

  getStats(): BacktestStats {
    if (this.trades.length === 0) {
      return {
        totalTrades: 0,
        winningTrades: 0,
        losingTrades: 0,
        winRate: 0,
        avgWin: 0,
        avgLoss: 0,
        profitFactor: 0,
        totalPnL: 0,
        grossProfit: 0,
        grossLoss: 0,
        maxConsecutiveWins: 0,
        maxConsecutiveLosses: 0,
        returnPercent: 0,
        sharpeRatio: 0,
        sortinoRatio: 0,
        maxDrawdown: 0,
        calmarRatio: 0
      };
    }

    // Basic trade stats
    const winningTrades = this.trades.filter(t => t.pnl > 0);
    const losingTrades = this.trades.filter(t => t.pnl < 0);

    const winRate = winningTrades.length / this.trades.length;
    const avgWin = winningTrades.length > 0
      ? winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length
      : 0;
    const avgLoss = losingTrades.length > 0
      ? losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length
      : 0;

    const grossProfit = winningTrades.reduce((sum, t) => sum + t.pnl, 0);
    const grossLoss = Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0));
    const profitFactor = grossLoss > 0 ? grossProfit / grossLoss : grossProfit > 0 ? Infinity : 0;

    // Consecutive wins/losses
    let maxConsecutiveWins = 0;
    let maxConsecutiveLosses = 0;
    let currentWins = 0;
    let currentLosses = 0;

    for (const trade of this.trades) {
      if (trade.pnl > 0) {
        currentWins++;
        currentLosses = 0;
        maxConsecutiveWins = Math.max(maxConsecutiveWins, currentWins);
      } else if (trade.pnl < 0) {
        currentLosses++;
        currentWins = 0;
        maxConsecutiveLosses = Math.max(maxConsecutiveLosses, currentLosses);
      }
    }

    // Return metrics
    const totalPnL = this.trades.reduce((sum, t) => sum + t.pnl, 0);
    const returnPercent = (totalPnL / this.baseCapital) * 100;

    // Risk-adjusted metrics
    const returns = calculateReturns({
      prices: this.portfolioValues,
      type: 'simple'
    });

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

    const maxDD = calculateMaxDrawdown({
      portfolioValues: this.portfolioValues
    });

    const calmarRatio = returnPercent / (Math.abs(maxDD.maxDrawdown) * 100 + 0.01);

    return {
      totalTrades: this.trades.length,
      winningTrades: winningTrades.length,
      losingTrades: losingTrades.length,
      winRate,
      avgWin,
      avgLoss,
      profitFactor,
      totalPnL,
      grossProfit,
      grossLoss,
      maxConsecutiveWins,
      maxConsecutiveLosses,
      returnPercent,
      sharpeRatio: sharpe.sharpeRatio,
      sortinoRatio: sortino.sortinoRatio,
      maxDrawdown: maxDD.maxDrawdown,
      calmarRatio
    };
  }

  printReport(): void {
    const stats = this.getStats();

    console.log(`
═══════════════════════════════════════════════════
BACKTEST REPORT
═══════════════════════════════════════════════════

TRADE SUMMARY
─────────────────────────────────────────────────
Total Trades:         ${stats.totalTrades}
Winning Trades:       ${stats.winningTrades}
Losing Trades:        ${stats.losingTrades}
Win Rate:             ${(stats.winRate * 100).toFixed(1)}%

PROFITABILITY
─────────────────────────────────────────────────
Gross Profit:         $${stats.grossProfit.toFixed(0)}
Gross Loss:           $${stats.grossLoss.toFixed(0)}
Profit Factor:        ${stats.profitFactor.toFixed(2)} ${stats.profitFactor > 1.5 ? '✓' : stats.profitFactor > 1 ? '~' : '✗'}
Total PnL:            $${stats.totalPnL.toFixed(0)}
Return:               ${stats.returnPercent.toFixed(2)}%

AVERAGE TRADE METRICS
─────────────────────────────────────────────────
Average Win:          $${stats.avgWin.toFixed(0)}
Average Loss:         $${stats.avgLoss.toFixed(0)}
Win/Loss Ratio:       ${Math.abs(stats.avgWin / (stats.avgLoss + 0.01)).toFixed(2)}
Max Consecutive Wins: ${stats.maxConsecutiveWins}
Max Consecutive Loss: ${stats.maxConsecutiveLosses}

RISK-ADJUSTED METRICS
─────────────────────────────────────────────────
Sharpe Ratio:         ${stats.sharpeRatio.toFixed(2)} ${stats.sharpeRatio > 1 ? '✓' : '✗'}
Sortino Ratio:        ${stats.sortinoRatio.toFixed(2)} ${stats.sortinoRatio > 1.5 ? '✓' : '✗'}
Max Drawdown:         ${(stats.maxDrawdown * 100).toFixed(2)}%
Calmar Ratio:         ${stats.calmarRatio.toFixed(2)}

═══════════════════════════════════════════════════
    `);
  }
}

// Usage
const engine = new BacktestEngine(100000, 0.001, 0.001);

// Simulate some trades
engine.executeTrade(
  new Date('2024-01-01'),
  100,
  new Date('2024-01-02'),
  102,
  100,
  'long'
);

engine.executeTrade(
  new Date('2024-01-03'),
  102,
  new Date('2024-01-04'),
  101,
  100,
  'long'
);

engine.printReport();
```

## Walk-Forward Analysis

Out-of-sample validation with rolling windows.

```typescript
interface WalkForwardResult {
  inSampleReturn: number;
  outOfSampleReturn: number;
  returnDecay: number;           // How much performance degrades
  isRobust: boolean;             // < 20% decay is acceptable
  recommendation: string;
}

function walkForwardAnalysis(
  prices: number[],
  trainWindow: number = 120,    // 120 days training
  testWindow: number = 20,      // 20 days testing
  stepSize: number = 20         // Roll forward 20 days
): WalkForwardResult[] {
  const results: WalkForwardResult[] = [];

  for (let i = 0; i + trainWindow + testWindow <= prices.length; i += stepSize) {
    const trainStart = i;
    const trainEnd = i + trainWindow;
    const testStart = trainEnd;
    const testEnd = testStart + testWindow;

    const trainPrices = prices.slice(trainStart, trainEnd);
    const testPrices = prices.slice(testStart, testEnd);

    // Train on in-sample data
    // (Simplified: just calculate returns)
    const trainReturns = calculateReturns({ prices: trainPrices });
    const inSampleReturn = trainReturns.reduce((a, b) => a + b, 0);

    // Test on out-of-sample data
    const testReturns = calculateReturns({ prices: testPrices });
    const outOfSampleReturn = testReturns.reduce((a, b) => a + b, 0);

    // Calculate decay
    const returnDecay = Math.abs(
      (outOfSampleReturn - inSampleReturn) / (Math.abs(inSampleReturn) + 0.0001)
    );

    results.push({
      inSampleReturn,
      outOfSampleReturn,
      returnDecay,
      isRobust: returnDecay < 0.2,
      recommendation:
        returnDecay < 0.1
          ? '✓ Excellent robustness'
          : returnDecay < 0.2
          ? '~ Acceptable robustness'
          : '✗ High decay - likely overfitted'
    });
  }

  return results;
}

// Usage
const prices = Array.from({ length: 300 }, (_, i) => 100 * Math.exp((Math.random() - 0.5) * 0.02 * i / 100));
const wfResults = walkForwardAnalysis(prices, 120, 20, 20);

console.log(`
Walk-Forward Analysis Results
─────────────────────────────────────────
`);
wfResults.forEach((result, i) => {
  console.log(`
Period ${i + 1}:
  In-Sample Return:       ${(result.inSampleReturn * 100).toFixed(2)}%
  Out-of-Sample Return:   ${(result.outOfSampleReturn * 100).toFixed(2)}%
  Return Decay:           ${(result.returnDecay * 100).toFixed(1)}%
  ${result.recommendation}
  `);
});

const avgDecay = wfResults.reduce((sum, r) => sum + r.returnDecay, 0) / wfResults.length;
console.log(`
Average Decay: ${(avgDecay * 100).toFixed(1)}%
Overall: ${avgDecay < 0.15 ? '✓ Strategy is robust' : '✗ Strategy may be overfitted'}
`);
```

## Optimization Overfitting Detection

Identify parameter combinations that only work in-sample.

```typescript
interface OptimizationMetrics {
  parameterSet: Record<string, number>;
  inSampleSharpe: number;
  outOfSampleSharpe: number;
  degradation: number;           // Sharpe degradation %
  isOverfitted: boolean;
}

function detectOverfitting(
  optimizationResults: OptimizationMetrics[]
): {
  robustParameters: OptimizationMetrics[];
  overfittedParameters: OptimizationMetrics[];
  degradationDistribution: { mean: number; stdDev: number };
} {
  // Calculate degradation statistics
  const degradations = optimizationResults.map(r => r.degradation);
  const mean = degradations.reduce((a, b) => a + b) / degradations.length;
  const variance = degradations.reduce((sum, d) => sum + Math.pow(d - mean, 2), 0) / degradations.length;
  const stdDev = Math.sqrt(variance);

  // Flag as overfit if 2+ standard deviations above mean
  const threshold = mean + 2 * stdDev;

  const robustParameters = optimizationResults.filter(r => r.degradation <= threshold);
  const overfittedParameters = optimizationResults.filter(r => r.degradation > threshold);

  return {
    robustParameters,
    overfittedParameters,
    degradationDistribution: { mean, stdDev }
  };
}

// Usage
const optimResults: OptimizationMetrics[] = [
  {
    parameterSet: { rsiPeriod: 14, rsiThreshold: 30 },
    inSampleSharpe: 1.8,
    outOfSampleSharpe: 1.5,
    degradation: 0.17,
    isOverfitted: false
  },
  {
    parameterSet: { rsiPeriod: 8, rsiThreshold: 25 },
    inSampleSharpe: 2.1,
    outOfSampleSharpe: 0.8,
    degradation: 0.62,
    isOverfitted: true
  },
  {
    parameterSet: { rsiPeriod: 14, rsiThreshold: 32 },
    inSampleSharpe: 1.9,
    outOfSampleSharpe: 1.6,
    degradation: 0.16,
    isOverfitted: false
  }
];

const detection = detectOverfitting(optimResults);

console.log(`
Overfitting Detection
─────────────────────────────────────────
Degradation Distribution:
  Mean:      ${(detection.degradationDistribution.mean * 100).toFixed(1)}%
  Std Dev:   ${(detection.degradationDistribution.stdDev * 100).toFixed(1)}%
  Threshold: ${(detection.degradationDistribution.mean + 2 * detection.degradationDistribution.stdDev) * 100).toFixed(1)}%

Robust Parameters: ${detection.robustParameters.length}
${detection.robustParameters.map((r, i) => `
  ${i + 1}. RSI ${r.parameterSet.rsiPeriod}/${r.parameterSet.rsiThreshold}
     In-Sample: ${r.inSampleSharpe.toFixed(2)} → Out-of-Sample: ${r.outOfSampleSharpe.toFixed(2)} (${(r.degradation * 100).toFixed(1)}% decay)`).join('\n')}

Overfitted Parameters: ${detection.overfittedParameters.length} ✗
${detection.overfittedParameters.map((r, i) => `
  ${i + 1}. RSI ${r.parameterSet.rsiPeriod}/${r.parameterSet.rsiThreshold}
     In-Sample: ${r.inSampleSharpe.toFixed(2)} → Out-of-Sample: ${r.outOfSampleSharpe.toFixed(2)} (${(r.degradation * 100).toFixed(1)}% decay)`).join('\n')}
`);
```

## Monte Carlo Simulation for Risk Analysis

Test strategy robustness through path simulation.

```typescript
interface MonteCarloResult {
  expectedReturn: number;
  returnStdDev: number;
  percentile1: number;   // Worst 1% scenario
  percentile5: number;   // Worst 5% scenario
  percentile95: number;  // Best 5% scenario
  percentile99: number;  // Best 1% scenario
  percentileMedian: number;
  winProbability: number; // Probability of positive return
}

function monteCarloSimulation(
  tradeReturns: number[],
  simulations: number = 10000,
  horizon: number = 252  // 1-year horizon
): MonteCarloResult {
  const simulationResults: number[] = [];

  for (let sim = 0; sim < simulations; sim++) {
    // Random walk of trades
    let simReturn = 1;
    for (let day = 0; day < horizon; day++) {
      // Randomly sample from historical returns
      const randomReturn = tradeReturns[Math.floor(Math.random() * tradeReturns.length)];
      simReturn *= (1 + randomReturn);
    }
    simulationResults.push((simReturn - 1) * 100); // Convert to percentage
  }

  // Sort results
  simulationResults.sort((a, b) => a - b);

  const mean = simulationResults.reduce((a, b) => a + b) / simulationResults.length;
  const variance = simulationResults.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / simulationResults.length;
  const stdDev = Math.sqrt(variance);

  const winProbability = simulationResults.filter(r => r > 0).length / simulationResults.length;

  return {
    expectedReturn: mean,
    returnStdDev: stdDev,
    percentile1: simulationResults[Math.floor(simulations * 0.01)],
    percentile5: simulationResults[Math.floor(simulations * 0.05)],
    percentile95: simulationResults[Math.floor(simulations * 0.95)],
    percentile99: simulationResults[Math.floor(simulations * 0.99)],
    percentileMedian: simulationResults[Math.floor(simulations * 0.5)],
    winProbability
  };
}

// Usage
const tradeReturns = [0.01, 0.02, -0.01, 0.015, 0.03, -0.005, 0.02];
const mcResult = monteCarloSimulation(tradeReturns, 10000, 252);

console.log(`
Monte Carlo Risk Analysis (10,000 simulations, 252-day horizon)
─────────────────────────────────────────────────────────────────
Expected Return:    ${mcResult.expectedReturn.toFixed(2)}%
Return Std Dev:     ${mcResult.returnStdDev.toFixed(2)}%

Confidence Intervals:
  Worst 1% (1st %ile):    ${mcResult.percentile1.toFixed(2)}%
  Worst 5% (5th %ile):    ${mcResult.percentile5.toFixed(2)}%
  Median (50th %ile):     ${mcResult.percentileMedian.toFixed(2)}%
  Best 5% (95th %ile):    ${mcResult.percentile95.toFixed(2)}%
  Best 1% (99th %ile):    ${mcResult.percentile99.toFixed(2)}%

Win Probability:    ${(mcResult.winProbability * 100).toFixed(1)}%

Risk Interpretation:
  1 in 100 worst case: ${mcResult.percentile1.toFixed(2)}% return
  1 in 20 favorable:   ${mcResult.percentile95.toFixed(2)}% return
`);
```

---

## Validation Checklist

Before deploying a trading strategy, verify:

✓ **Backtesting Standards**
- [ ] At least 2+ years of data
- [ ] Win rate > 40% (ideally 45-55%)
- [ ] Profit factor > 1.5 (ideally 2.0+)
- [ ] Sharpe ratio > 1.0 (ideally 1.5+)
- [ ] Max drawdown < 20% (ideally < 15%)

✓ **Walk-Forward Validation**
- [ ] Out-of-sample performance within 20% of in-sample
- [ ] At least 5 walk-forward periods
- [ ] Consistent performance across periods

✓ **Overfitting Detection**
- [ ] Parameter degradation < 2 std deviations
- [ ] No overly complex parameter combinations
- [ ] Tested on fresh data period

✓ **Monte Carlo Analysis**
- [ ] Win probability > 50%
- [ ] 5th percentile loss < max drawdown * 1.5
- [ ] At least 10,000 simulation paths

✓ **Reality Checks**
- [ ] Account for slippage (10-50 basis points)
- [ ] Account for commissions
- [ ] Account for market gaps
- [ ] Test on multiple markets/timeframes
