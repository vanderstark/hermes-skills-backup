# Machine Learning Refinements

Advanced HMM optimization and regime-aware trading strategies.

## HMM Parameter Tuning

Optimize Hidden Markov Model for regime detection.

```typescript
import { 
  detectRegime, 
  trainHMM, 
  extractFeatures 
} from '@railpath/finance-toolkit';

interface HMMOptimizationResult {
  optimalStates: number;
  optimalFeatures: string[];
  modelAccuracy: number;
  regimeStability: number;  // How stable each regime is
  recommendation: string;
}

function optimizeHMMParameters(
  prices: number[],
  stateRange: number[] = [2, 3, 4, 5],
  featureSet: string[][] = [
    ['returns', 'volatility'],
    ['returns', 'volatility', 'rsi'],
    ['returns', 'volatility', 'rsi', 'macd'],
    ['returns', 'volatility', 'rsi', 'macd', 'ema']
  ]
): HMMOptimizationResult {
  let bestAccuracy = 0;
  let bestStates = 3;
  let bestFeatures: string[] = ['returns', 'volatility', 'rsi'];
  let bestStability = 0;

  // Test different state numbers
  for (const numStates of stateRange) {
    // Test different feature combinations
    for (const features of featureSet) {
      // Extract features
      const { features: featureMatrix } = extractFeatures({
        prices,
        features,
        window: 20
      });

      // Train HMM
      const model = trainHMM({
        featureMatrix,
        numStates,
        maxIterations: 100,
        convergenceThreshold: 0.001
      });

      // Evaluate model quality
      const viterbiSequence = model.viterbi(featureMatrix);

      // Regime stability: how long each regime persists (lower = better stability)
      let regimeChangeCount = 0;
      for (let i = 1; i < viterbiSequence.length; i++) {
        if (viterbiSequence[i] !== viterbiSequence[i - 1]) {
          regimeChangeCount++;
        }
      }

      // Stability score: 1 = very stable, 0 = constantly switching
      const stability = 1 - (regimeChangeCount / viterbiSequence.length);

      // Rough accuracy proxy: models with 3-4 distinct regimes 
      // and moderate switching are typically best
      const stateUsage = new Set(viterbiSequence).size;
      const usageScore = stateUsage === numStates ? 0.9 : 0.5; // All states used = good
      const accuracy = stability * 0.6 + usageScore * 0.4;

      if (accuracy > bestAccuracy) {
        bestAccuracy = accuracy;
        bestStates = numStates;
        bestFeatures = [...features];
        bestStability = stability;
      }

      console.log(
        `States: ${numStates}, Features: ${features.length}, Stability: ${(stability * 100).toFixed(1)}%, Accuracy: ${(accuracy * 100).toFixed(1)}%`
      );
    }
  }

  const recommendation =
    bestStates === 3
      ? 'Standard 3-state (bearish/neutral/bullish) - good balance'
      : bestStates === 4
      ? '4-state model (strong/weak bear/bull) - more nuanced'
      : bestStates === 5
      ? '5-state model (extreme/strong/neutral/weak/extreme) - high complexity'
      : 'Custom state count';

  return {
    optimalStates: bestStates,
    optimalFeatures: bestFeatures,
    modelAccuracy: bestAccuracy,
    regimeStability: bestStability,
    recommendation
  };
}

// Usage
const prices = [100, 101, 102, 101, 100, 99, 98, 97, 98, 99, 100, 102, 105, 107, 106];
const optimization = optimizeHMMParameters(prices);

console.log(`
HMM Optimization Results
─────────────────────────────────────
Optimal States:     ${optimization.optimalStates}
Optimal Features:   ${optimization.optimalFeatures.join(', ')}
Model Accuracy:     ${(optimization.modelAccuracy * 100).toFixed(1)}%
Regime Stability:   ${(optimization.regimeStability * 100).toFixed(1)}%

Recommendation: ${optimization.recommendation}
`);
```

## Regime-Aware Portfolio Construction

Build portfolios adapted to current market regime.

```typescript
import {
  detectRegime,
  calculatePortfolioOptimization,
  calculateCovarianceMatrix
} from '@railpath/finance-toolkit';

interface RegimeAwareAllocation {
  regime: string;
  weights: number[];
  expectedReturn: number;
  volatility: number;
  sharpeRatio: number;
  reasoning: string;
}

// Define regime-specific allocations
const regimeAllocations = {
  bullish: {
    // Growth-oriented in bull markets
    expectedReturns: [0.12, 0.10, 0.06, 0.04],  // TECH, GROWTH, BONDS, CASH
    maxDrawdown: 0.20,
    reasoning: 'Growth assets favored - risk-on'
  },
  neutral: {
    // Balanced in neutral markets
    expectedReturns: [0.08, 0.08, 0.06, 0.04],  // More balanced
    maxDrawdown: 0.12,
    reasoning: 'Balanced allocation - reduce concentration'
  },
  bearish: {
    // Defensive in bear markets
    expectedReturns: [0.04, 0.04, 0.06, 0.04],  // Defensive bias
    maxDrawdown: 0.08,
    reasoning: 'Defensive positioning - reduce volatility'
  }
};

function constructRegimeAwarePortfolio(
  prices: number[],
  assetReturnsHistory: number[][],
  regimeLookback: number = 20
): RegimeAwareAllocation {
  // Detect current regime
  const regime = detectRegime(prices, {
    numStates: 3,
    features: ['returns', 'volatility', 'rsi'],
    featureWindow: regimeLookback,
    stateLabels: ['bearish', 'neutral', 'bullish']
  });

  const currentRegime = regime.currentRegime as keyof typeof regimeAllocations;
  const regimeSpec = regimeAllocations[currentRegime];

  // Calculate covariance
  const cov = calculateCovarianceMatrix({ assetReturns: assetReturnsHistory });

  // Optimize for regime
  const optimization = calculatePortfolioOptimization({
    expectedReturns: regimeSpec.expectedReturns,
    covarianceMatrix: cov,
    constraints: {
      minWeight: 0.05,  // Minimum 5% per position
      maxWeight: 0.50   // Maximum 50%
    }
  });

  return {
    regime: currentRegime,
    weights: optimization.optimalWeights,
    expectedReturn: optimization.expectedReturn,
    volatility: optimization.expectedVolatility,
    sharpeRatio: optimization.sharpeRatio,
    reasoning: regimeSpec.reasoning
  };
}

// Usage
const prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110];
const assetReturns = [
  [0.01, 0.02, 0.015, 0.018],   // Tech
  [0.008, 0.012, 0.010, 0.011],   // Growth
  [0.003, 0.002, 0.004, 0.003],   // Bonds
  [0.001, 0.001, 0.001, 0.001]    // Cash
];

const allocation = constructRegimeAwarePortfolio(prices, assetReturns);

console.log(`
Regime-Aware Portfolio (${allocation.regime.toUpperCase()})
──────────────────────────────────────────
Expected Return:    ${(allocation.expectedReturn * 100).toFixed(2)}%
Volatility:         ${(allocation.volatility * 100).toFixed(2)}%
Sharpe Ratio:       ${allocation.sharpeRatio.toFixed(2)}

Allocation:
  Tech (40-50%):     ${(allocation.weights[0] * 100).toFixed(0)}%
  Growth (20-30%):   ${(allocation.weights[1] * 100).toFixed(0)}%
  Bonds (10-30%):    ${(allocation.weights[2] * 100).toFixed(0)}%
  Cash (5-10%):      ${(allocation.weights[3] * 100).toFixed(0)}%

Regime Rationale: ${allocation.reasoning}
`);
```

## Adaptive Trading Rules Based on Regime

Dynamically adjust trading parameters based on regime.

```typescript
import { detectRegime } from '@railpath/finance-toolkit';

interface AdaptiveTradeParams {
  regime: string;
  positionSizeMultiplier: number;
  stopLossPercent: number;
  takeProfitPercent: number;
  maxConcurrentTrades: number;
  orderType: 'market' | 'limit';
  timeInForce: 'day' | 'gtc';
  riskPerTrade: number;
  winRateThreshold: number;
}

function getAdaptiveTradeParams(prices: number[], regime?: string): AdaptiveTradeParams {
  // Detect regime if not provided
  const detectedRegime = regime || detectRegime(prices, {
    numStates: 3,
    features: ['returns', 'volatility'],
    stateLabels: ['bearish', 'neutral', 'bullish']
  }).currentRegime;

  // Define adaptive parameters
  const regimeParams: Record<string, AdaptiveTradeParams> = {
    bullish: {
      regime: 'bullish',
      positionSizeMultiplier: 1.2,      // 20% larger positions
      stopLossPercent: 0.03,            // 3% stop loss
      takeProfitPercent: 0.06,          // 6% take profit
      maxConcurrentTrades: 5,
      orderType: 'market',              // More aggressive entries
      timeInForce: 'day',
      riskPerTrade: 2000,
      winRateThreshold: 0.45            // Lower bar in strong trends
    },
    neutral: {
      regime: 'neutral',
      positionSizeMultiplier: 1.0,      // Standard size
      stopLossPercent: 0.025,           // 2.5% stop loss
      takeProfitPercent: 0.05,          // 5% take profit
      maxConcurrentTrades: 3,
      orderType: 'limit',               // Selective entry
      timeInForce: 'gtc',
      riskPerTrade: 1500,
      winRateThreshold: 0.50            // Equal risk/reward
    },
    bearish: {
      regime: 'bearish',
      positionSizeMultiplier: 0.6,      // 40% smaller positions
      stopLossPercent: 0.02,            // 2% tight stop loss
      takeProfitPercent: 0.04,          // 4% take profit
      maxConcurrentTrades: 2,           // Fewer concurrent trades
      orderType: 'limit',               // Conservative entries
      timeInForce: 'gtc',
      riskPerTrade: 1000,               // Lower risk
      winRateThreshold: 0.55            // Higher bar required
    }
  };

  return regimeParams[detectedRegime] || regimeParams['neutral'];
}

// Usage example: Apply adaptive params to trade execution
function executeTradeWithAdaptiveParams(
  entryPrice: number,
  prices: number[],
  desiredRiskAmount: number = 1000
): void {
  const params = getAdaptiveTradeParams(prices);

  const adjustedRisk = desiredRiskAmount * params.positionSizeMultiplier;
  const stopLoss = entryPrice * (1 - params.stopLossPercent);
  const takeProfit = entryPrice * (1 + params.takeProfitPercent);
  const positionSize = Math.floor(adjustedRisk / (entryPrice - stopLoss));

  console.log(`
Trade Execution (${params.regime.toUpperCase()} REGIME)
──────────────────────────────────────────
Entry Price:          ${entryPrice.toFixed(2)}
Position Size:        ${positionSize} units
Stop Loss:            ${stopLoss.toFixed(2)} (-${params.stopLossPercent * 100}%)
Take Profit:          ${takeProfit.toFixed(2)} (+${params.takeProfitPercent * 100}%)
Risk Amount:          $${adjustedRisk.toFixed(0)}

Trade Parameters:
  Max Concurrent:     ${params.maxConcurrentTrades} trades
  Order Type:         ${params.orderType.toUpperCase()}
  Time in Force:      ${params.timeInForce.toUpperCase()}
  Win Rate Required:  ${(params.winRateThreshold * 100).toFixed(0)}%

Risk/Reward Ratio:    1:${(params.takeProfitPercent / params.stopLossPercent).toFixed(1)}
  `);
}

const prices = [100, 101, 102, 103, 104, 105, 106];
executeTradeWithAdaptiveParams(104.5, prices);
```

## Feature Engineering Best Practices

Optimize feature extraction for regime detection.

```typescript
import { extractFeatures, detectRegime } from '@railpath/finance-toolkit';

interface FeatureQuality {
  feature: string;
  variance: number;           // Information content
  correlation: number;        // Correlation with regime shifts
  relevance: string;          // Domain interpretation
  recommendedWindow: number;
}

function evaluateFeatureQuality(
  prices: number[],
  features: string[]
): FeatureQuality[] {
  const extractedFeatures = extractFeatures({
    prices,
    features,
    window: 20
  });

  const qualities: FeatureQuality[] = [];

  // Evaluate each feature
  for (let i = 0; i < features.length; i++) {
    const featureData = extractedFeatures.features.map(row => row[i]);

    // Calculate variance (higher = more information)
    const mean = featureData.reduce((a, b) => a + b) / featureData.length;
    const variance = featureData.reduce((sum, x) => sum + Math.pow(x - mean, 2), 0) / featureData.length;

    // Recommend window size based on feature
    let recommendedWindow = 20;
    if (features[i] === 'returns') recommendedWindow = 20;
    if (features[i] === 'volatility') recommendedWindow = 14;
    if (features[i] === 'rsi') recommendedWindow = 14;
    if (features[i] === 'macd') recommendedWindow = 26;
    if (features[i] === 'ema') recommendedWindow = 12;

    qualities.push({
      feature: features[i],
      variance,
      correlation: Math.random() * 0.5 + 0.3, // Placeholder
      relevance: `${features[i]} captures ${
        features[i] === 'returns'
          ? 'price momentum'
          : features[i] === 'volatility'
          ? 'market uncertainty'
          : features[i] === 'rsi'
          ? 'overbought/oversold conditions'
          : 'trend strength'
      }`,
      recommendedWindow
    });
  }

  return qualities.sort((a, b) => b.variance - a.variance);
}

// Usage
const prices = [100, 101, 102, 103, 104, 105, 106];
const featureQualities = evaluateFeatureQuality(prices, ['returns', 'volatility', 'rsi', 'macd']);

console.log(`
Feature Quality Analysis
─────────────────────────────────────────`);
featureQualities.forEach((q, i) => {
  console.log(`
${i + 1}. ${q.feature.toUpperCase()}
   Variance:        ${q.variance.toFixed(4)} (information content)
   Correlation:     ${q.correlation.toFixed(3)} (regime relevance)
   Recommended:     ${q.recommendedWindow}-period window
   Role:            ${q.relevance}
  `);
});

console.log(`
Feature Selection Strategy:
──────────────────────────
✓ Use top 2-3 features for best balance of speed/accuracy
✓ Always include 'returns' and 'volatility' as baseline
✓ Add 'rsi' for momentum signals, 'macd' for trend confirmation
✓ Avoid using all 5 features unless computational budget allows
`);
```

## Multi-Model Ensemble for Regime Detection

Combine multiple HMM configurations for robust regime detection.

```typescript
import { detectRegime } from '@railpath/finance-toolkit';

interface EnsembleRegimeDetection {
  consensusRegime: string;
  confidence: number;          // % of models agreeing
  minorityView: string;
  regimeStability: number;     // How confident across all models
  recommendation: string;
}

function ensembleRegimeDetection(
  prices: number[],
  verbose: boolean = false
): EnsembleRegimeDetection {
  // Run multiple models with different configurations
  const models = [
    // Conservative: Simple 3-state with minimal features
    detectRegime(prices, {
      numStates: 3,
      features: ['returns', 'volatility'],
      stateLabels: ['bearish', 'neutral', 'bullish']
    }),

    // Standard: 3-state with moderate features
    detectRegime(prices, {
      numStates: 3,
      features: ['returns', 'volatility', 'rsi'],
      stateLabels: ['bearish', 'neutral', 'bullish']
    }),

    // Detailed: 4-state for finer gradation
    detectRegime(prices, {
      numStates: 4,
      features: ['returns', 'volatility', 'rsi', 'macd'],
      stateLabels: ['strong_bearish', 'weak_bearish', 'weak_bullish', 'strong_bullish']
    }),

    // Aggressive: 5-state for maximum nuance
    detectRegime(prices, {
      numStates: 5,
      features: ['returns', 'volatility', 'rsi', 'macd', 'ema'],
      stateLabels: ['crash', 'bearish', 'neutral', 'bullish', 'euphoria']
    })
  ];

  // Map all regimes to base classes for comparison
  const baseRegimes = models.map(m => {
    if (m.currentRegime.includes('bear')) return 'bearish';
    if (m.currentRegime.includes('bull')) return 'bullish';
    return 'neutral';
  });

  // Count agreement
  const bullishVotes = baseRegimes.filter(r => r === 'bullish').length;
  const bearishVotes = baseRegimes.filter(r => r === 'bearish').length;
  const neutralVotes = baseRegimes.filter(r => r === 'neutral').length;

  const voteDistribution = { bullish: bullishVotes, bearish: bearishVotes, neutral: neutralVotes };
  const maxVotes = Math.max(...Object.values(voteDistribution));
  const confidence = maxVotes / models.length;

  let consensusRegime = 'neutral';
  let minorityView = '';

  if (bullishVotes === maxVotes) {
    consensusRegime = 'bullish';
    const minority = voteDistribution.bearish > 0 ? 'Minority bearish' : '';
    minorityView = minority || (voteDistribution.neutral > 0 ? 'Some neutral signals' : '');
  } else if (bearishVotes === maxVotes) {
    consensusRegime = 'bearish';
    const minority = voteDistribution.bullish > 0 ? 'Minority bullish' : '';
    minorityView = minority || (voteDistribution.neutral > 0 ? 'Some neutral signals' : '');
  } else {
    minorityView = `Split: ${bullishVotes} bull, ${bearishVotes} bear`;
  }

  // Calculate stability
  const avgConfidence = models.reduce((sum, m) => sum + m.confidence, 0) / models.length;
  const regimeStability = avgConfidence * confidence;

  let recommendation = '';
  if (confidence === 1.0) {
    recommendation = 'Strong consensus - high conviction signal';
  } else if (confidence >= 0.75) {
    recommendation = 'Good consensus - moderate conviction';
  } else if (confidence >= 0.5) {
    recommendation = 'Split opinion - wait for clarity';
  } else {
    recommendation = 'No consensus - unclear regime, reduce exposure';
  }

  if (verbose) {
    console.log(`
Ensemble Regime Detection
─────────────────────────────────────────
Model 1 (Conservative):  ${models[0].currentRegime} (${(models[0].confidence * 100).toFixed(0)}%)
Model 2 (Standard):      ${models[1].currentRegime} (${(models[1].confidence * 100).toFixed(0)}%)
Model 3 (Detailed):      ${models[2].currentRegime} (${(models[2].confidence * 100).toFixed(0)}%)
Model 4 (Aggressive):    ${models[3].currentRegime} (${(models[3].confidence * 100).toFixed(0)}%)

CONSENSUS: ${consensusRegime.toUpperCase()}
Votes: ${bullishVotes} bullish, ${bearishVotes} bearish, ${neutralVotes} neutral
Confidence: ${(confidence * 100).toFixed(0)}%
Stability: ${(regimeStability * 100).toFixed(0)}%
${minorityView ? `Note: ${minorityView}` : ''}
    `);
  }

  return {
    consensusRegime,
    confidence,
    minorityView,
    regimeStability,
    recommendation
  };
}

// Usage
const prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110];
const ensemble = ensembleRegimeDetection(prices, true);

console.log(`
Trading Action Based on Ensemble:
──────────────────────────────────
${ensemble.recommendation}
${ensemble.confidence >= 0.75 ? '✓ Safe to execute trades' : '⚠ Consider reducing exposure'}
`);
```

---

## Best Practices Summary

### Feature Selection
- Start with `['returns', 'volatility']` - captures core regime dynamics
- Add `'rsi'` if you want to detect overbought/oversold shifts
- Add `'macd'` to catch momentum changes
- Test with `'ema'` only if computational resources permit

### Model Architecture
- **2-3 states**: Fast, stable, good for simple trending
- **3-4 states**: Standard balance of granularity and stability
- **5+ states**: Maximum detail, but risk of overfitting

### Ensemble Strategies
- Use 3-4 models with different configurations
- Weight by confidence scores, not equally
- Switch conservatively when consensus breaks
- Reduce position size in split-opinion scenarios

### Monitoring Metrics
- Track regime transition frequency (should be < 10% of observations)
- Monitor model divergence (high = uncertain environment)
- Log false regime signals and adjust accordingly
