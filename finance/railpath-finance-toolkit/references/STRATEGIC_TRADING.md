# Strategic Trading Approaches

Advanced systematic trading strategies using @railpath/finance-toolkit.

## Mean Reversion System

Exploit overbought/oversold conditions with volatility confirmation.

```typescript
import {
  calculateRSI,
  calculateBollingerBands,
  calculateATR,
  calculateVaR,
  calculateVolatility
} from '@railpath/finance-toolkit';

interface MeanReversionSignal {
  action: 'BUY' | 'SELL' | 'HOLD';
  strength: number;           // 0-1 confidence
  entry: number;
  stopLoss: number;
  takeProfit: number;
  positionSize: number;
  reasoning: string[];
}

function generateMeanReversionSignal(
  prices: number[],
  high: number[],
  low: number[],
  riskPerTrade: number = 1000
): MeanReversionSignal {
  const index = prices.length - 1;
  if (index < 30) return { action: 'HOLD', strength: 0, entry: 0, stopLoss: 0, takeProfit: 0, positionSize: 0, reasoning: ['Insufficient data'] };

  // RSI extreme levels
  const rsi = calculateRSI({ prices, period: 14 });
  const rsiValue = rsi.rsi[index];

  // Volatility bands
  const bands = calculateBollingerBands({ prices, period: 20, stdDevMultiplier: 2 });
  const bandPosition = bands.percentB[index];

  // Volatility confirmation
  const atr = calculateATR({ high, low, close: prices, period: 14 });
  const atrValue = atr.atr[index];
  const volatility = calculateVolatility(
    prices.slice(-20).map((p, i) => i === 0 ? 0 : (prices[prices.length - 20 + i] - prices[prices.length - 21 + i]) / prices[prices.length - 21 + i])
  );

  // VaR for risk sizing
  const returns = prices.slice(-50).map((p, i) => i === 0 ? 0 : (prices[prices.length - 50 + i] - prices[prices.length - 51 + i]) / prices[prices.length - 51 + i]);
  const var95 = calculateVaR({
    returns: returns.filter(r => r !== 0),
    confidenceLevel: 0.95,
    method: 'historical'
  });

  const currentPrice = prices[index];
  const reasoning: string[] = [];
  let buySignal = false;
  let sellSignal = false;
  let confidence = 0;

  // BUY: RSI oversold + lower band touch + high vol
  if (rsiValue < 30 && bandPosition < 0.2 && volatility > 0.015) {
    buySignal = true;
    confidence += 0.35;
    reasoning.push(`RSI oversold: ${rsiValue.toFixed(0)}`);
    reasoning.push(`Band position: ${(bandPosition * 100).toFixed(0)}%`);
    reasoning.push(`Volatility elevated: ${(volatility * 100).toFixed(2)}%`);
  }

  // SELL: RSI overbought + upper band touch + high vol
  if (rsiValue > 70 && bandPosition > 0.8 && volatility > 0.015) {
    sellSignal = true;
    confidence += 0.35;
    reasoning.push(`RSI overbought: ${rsiValue.toFixed(0)}`);
    reasoning.push(`Band position: ${(bandPosition * 100).toFixed(0)}%`);
    reasoning.push(`Volatility elevated: ${(volatility * 100).toFixed(2)}%`);
  }

  // Strengthen signal if price touches band AND RSI extreme
  if (bandPosition < 0.1 && rsiValue < 25) confidence += 0.3;
  if (bandPosition > 0.9 && rsiValue > 75) confidence += 0.3;

  // Weaken signal if volatility very low (low conviction trades)
  if (volatility < 0.008) confidence *= 0.6;

  if (buySignal) {
    const stopLoss = currentPrice - (2 * atrValue);
    const riskAmount = currentPrice - stopLoss;
    const positionSize = Math.floor(riskPerTrade / riskAmount);
    const takeProfit = currentPrice + (riskAmount * 2);

    return {
      action: 'BUY',
      strength: Math.min(confidence, 0.95),
      entry: currentPrice,
      stopLoss,
      takeProfit,
      positionSize,
      reasoning
    };
  }

  if (sellSignal) {
    const stopLoss = currentPrice + (2 * atrValue);
    const riskAmount = stopLoss - currentPrice;
    const positionSize = Math.floor(riskPerTrade / riskAmount);
    const takeProfit = currentPrice - (riskAmount * 2);

    return {
      action: 'SELL',
      strength: Math.min(confidence, 0.95),
      entry: currentPrice,
      stopLoss,
      takeProfit,
      positionSize,
      reasoning
    };
  }

  return {
    action: 'HOLD',
    strength: 0,
    entry: currentPrice,
    stopLoss: 0,
    takeProfit: 0,
    positionSize: 0,
    reasoning: ['No confluence signal']
  };
}

// Usage
const prices = [100, 101, 99, 98, 97, 96, 95, 94.5, 94, 93.5, 94, 95];
const high = prices.map(p => p * 1.02);
const low = prices.map(p => p * 0.98);

const signal = generateMeanReversionSignal(prices, high, low);
console.log(`
Mean Reversion Signal
─────────────────────────────────
Action:         ${signal.action}
Confidence:     ${(signal.strength * 100).toFixed(0)}%
Entry:          ${signal.entry.toFixed(2)}
Stop Loss:      ${signal.stopLoss.toFixed(2)}
Take Profit:    ${signal.takeProfit.toFixed(2)}
Position Size:  ${signal.positionSize} units
Risk/Reward:    1:2.0

Reasoning:
${signal.reasoning.map(r => `  • ${r}`).join('\n')}
`);
```

## Momentum Trading System

Trend-following with multi-timeframe confirmation.

```typescript
import {
  calculateEMA,
  calculateMACD,
  calculateRSI,
  calculateATR,
  calculateVolatility
} from '@railpath/finance-toolkit';

interface MomentumSignal {
  action: 'BUY' | 'SELL' | 'HOLD';
  momentum: number;           // -1 to +1 strength
  shortTermTrend: 'up' | 'down' | 'neutral';
  mediumTermTrend: 'up' | 'down' | 'neutral';
  longTermTrend: 'up' | 'down' | 'neutral';
  confluence: number;         // Number of aligned signals
  entry: number;
  stopLoss: number;
  takeProfit: number;
}

function generateMomentumSignal(
  prices: number[],
  high: number[],
  low: number[],
  timeframes: { shortPeriod: number; mediumPeriod: number; longPeriod: number } = {
    shortPeriod: 12,
    mediumPeriod: 26,
    longPeriod: 50
  }
): MomentumSignal {
  const index = prices.length - 1;
  if (index < 60) return {
    action: 'HOLD',
    momentum: 0,
    shortTermTrend: 'neutral',
    mediumTermTrend: 'neutral',
    longTermTrend: 'neutral',
    confluence: 0,
    entry: prices[index],
    stopLoss: 0,
    takeProfit: 0
  };

  // Multi-timeframe EMAs
  const emaShort = calculateEMA({ prices, period: timeframes.shortPeriod });
  const emaMedium = calculateEMA({ prices, period: timeframes.mediumPeriod });
  const emaLong = calculateEMA({ prices, period: timeframes.longPeriod });

  // Momentum confirmation
  const macd = calculateMACD({ prices, fastPeriod: 12, slowPeriod: 26, signalPeriod: 9 });
  const rsi = calculateRSI({ prices, period: 14 });
  const atr = calculateATR({ high, low, close: prices, period: 14 });

  const shortEma = emaShort.ema[index];
  const mediumEma = emaMedium.ema[index];
  const longEma = emaLong.ema[index];
  const currentPrice = prices[index];
  const macdLine = macd.macdLine[index];
  const signalLine = macd.signalLine[index];
  const rsiValue = rsi.rsi[index];
  const atrValue = atr.atr[index];

  // Determine trends
  const shortTermTrend = shortEma > mediumEma ? 'up' : shortEma < mediumEma ? 'down' : 'neutral';
  const mediumTermTrend = mediumEma > longEma ? 'up' : mediumEma < longEma ? 'down' : 'neutral';
  const longTermTrend = currentPrice > longEma ? 'up' : currentPrice < longEma ? 'down' : 'neutral';

  // Momentum signals
  let confluenceCount = 0;
  let buyMomentum = 0;
  let sellMomentum = 0;

  // EMA alignment bullish
  if (shortEma > mediumEma && mediumEma > longEma) {
    confluenceCount++;
    buyMomentum += 0.3;
  }
  // EMA alignment bearish
  if (shortEma < mediumEma && mediumEma < longEma) {
    confluenceCount++;
    sellMomentum += 0.3;
  }

  // MACD bullish
  if (macdLine > signalLine && macdLine > 0) {
    confluenceCount++;
    buyMomentum += 0.25;
  }
  // MACD bearish
  if (macdLine < signalLine && macdLine < 0) {
    confluenceCount++;
    sellMomentum += 0.25;
  }

  // RSI bullish (not overbought)
  if (rsiValue > 50 && rsiValue < 70) {
    confluenceCount++;
    buyMomentum += 0.2;
  }
  // RSI bearish (not oversold)
  if (rsiValue < 50 && rsiValue > 30) {
    confluenceCount++;
    sellMomentum += 0.2;
  }

  // Price above EMA = bullish
  if (currentPrice > longEma) {
    buyMomentum += 0.15;
  }
  // Price below EMA = bearish
  if (currentPrice < longEma) {
    sellMomentum += 0.15;
  }

  const netMomentum = buyMomentum - sellMomentum;

  // Generate signal
  let action: 'BUY' | 'SELL' | 'HOLD' = 'HOLD';
  let stopLoss = 0;
  let takeProfit = 0;

  if (netMomentum > 0.5 && confluenceCount >= 2) {
    action = 'BUY';
    stopLoss = currentPrice - (2 * atrValue);
    takeProfit = currentPrice + (3 * atrValue);
  } else if (netMomentum < -0.5 && confluenceCount >= 2) {
    action = 'SELL';
    stopLoss = currentPrice + (2 * atrValue);
    takeProfit = currentPrice - (3 * atrValue);
  }

  return {
    action,
    momentum: Math.max(-1, Math.min(1, netMomentum)),
    shortTermTrend,
    mediumTermTrend,
    longTermTrend,
    confluence: confluenceCount,
    entry: currentPrice,
    stopLoss,
    takeProfit
  };
}

// Usage
const prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110];
const high = prices.map(p => p * 1.01);
const low = prices.map(p => p * 0.99);

const signal = generateMomentumSignal(prices, high, low);
console.log(`
Momentum Trading Signal
─────────────────────────────────
Action:         ${signal.action}
Net Momentum:   ${signal.momentum.toFixed(2)}
Confluence:     ${signal.confluence}/4 signals aligned

Trend Structure:
  Short (12):   ${signal.shortTermTrend.toUpperCase()}
  Medium (26):  ${signal.mediumTermTrend.toUpperCase()}
  Long (50):    ${signal.longTermTrend.toUpperCase()}

Entry:          ${signal.entry.toFixed(2)}
Stop Loss:      ${signal.stopLoss.toFixed(2)}
Take Profit:    ${signal.takeProfit.toFixed(2)}
`);
```

## Multi-Timeframe Confluence System

Trade only when multiple timeframes align.

```typescript
import {
  calculateEMA,
  calculateRSI,
  calculateMACD,
  calculateSMA
} from '@railpath/finance-toolkit';

interface TimeframeAnalysis {
  timeframe: string;
  trend: 'up' | 'down' | 'neutral';
  strength: number;          // 0-1
  signalAlignment: number;   // Count of aligned indicators
}

interface ConfluenceSignal {
  action: 'BUY' | 'SELL' | 'HOLD';
  confluenceScore: number;   // 0-1, higher = stronger
  analysis: TimeframeAnalysis[];
  tradeBias: string;
  recommendation: string;
}

function analyzeTimeframe(
  prices: number[],
  timeframeName: string,
  emaPeriod: number
): TimeframeAnalysis {
  if (prices.length < Math.max(emaPeriod, 14)) {
    return {
      timeframe: timeframeName,
      trend: 'neutral',
      strength: 0,
      signalAlignment: 0
    };
  }

  const ema = calculateEMA({ prices, period: emaPeriod });
  const rsi = calculateRSI({ prices, period: 14 });
  const macd = calculateMACD({ prices });

  const lastPrice = prices[prices.length - 1];
  const lastEma = ema.ema[ema.ema.length - 1];
  const lastRsi = rsi.rsi[rsi.rsi.length - 1];
  const lastMacd = macd.macdLine[macd.macdLine.length - 1];
  const lastSignal = macd.signalLine[macd.signalLine.length - 1];

  let trend: 'up' | 'down' | 'neutral' = 'neutral';
  let signalAlignment = 0;

  // EMA alignment
  if (lastPrice > lastEma) {
    trend = 'up';
    signalAlignment++;
  } else if (lastPrice < lastEma) {
    trend = 'down';
    signalAlignment++;
  }

  // RSI confirmation
  if (trend === 'up' && lastRsi > 50) signalAlignment++;
  if (trend === 'down' && lastRsi < 50) signalAlignment++;

  // MACD confirmation
  if (trend === 'up' && lastMacd > lastSignal) signalAlignment++;
  if (trend === 'down' && lastMacd < lastSignal) signalAlignment++;

  const strength = signalAlignment / 3; // Normalized to 0-1

  return {
    timeframe: timeframeName,
    trend,
    strength,
    signalAlignment
  };
}

function generateConfluenceSignal(
  dailyPrices: number[],
  four_hourPrices: number[],
  hourlyPrices: number[]
): ConfluenceSignal {
  const analysis: TimeframeAnalysis[] = [
    analyzeTimeframe(dailyPrices, '1D', 50),
    analyzeTimeframe(four_hourPrices, '4H', 26),
    analyzeTimeframe(hourlyPrices, '1H', 12)
  ];

  // Count aligned signals
  const bullishCount = analysis.filter(a => a.trend === 'up').length;
  const bearishCount = analysis.filter(a => a.trend === 'down').length;
  const avgStrength = analysis.reduce((sum, a) => sum + a.strength, 0) / analysis.length;

  let action: 'BUY' | 'SELL' | 'HOLD' = 'HOLD';
  let confluenceScore = 0;
  let tradeBias = 'NEUTRAL';
  let recommendation = 'Wait for alignment';

  if (bullishCount === 3) {
    action = 'BUY';
    confluenceScore = avgStrength;
    tradeBias = 'STRONG BULLISH';
    recommendation = 'All timeframes aligned up - high conviction buy';
  } else if (bearishCount === 3) {
    action = 'SELL';
    confluenceScore = avgStrength;
    tradeBias = 'STRONG BEARISH';
    recommendation = 'All timeframes aligned down - high conviction sell';
  } else if (bullishCount === 2) {
    action = 'BUY';
    confluenceScore = avgStrength * 0.8;
    tradeBias = 'BULLISH';
    recommendation = `${analysis.filter(a => a.trend === 'up').map(a => a.timeframe).join(' + ')} aligned up`;
  } else if (bearishCount === 2) {
    action = 'SELL';
    confluenceScore = avgStrength * 0.8;
    tradeBias = 'BEARISH';
    recommendation = `${analysis.filter(a => a.trend === 'down').map(a => a.timeframe).join(' + ')} aligned down`;
  } else if (bullishCount > bearishCount) {
    tradeBias = 'SLIGHT BULLISH';
    recommendation = 'Awaiting 2+ timeframe alignment for buy signal';
  } else if (bearishCount > bullishCount) {
    tradeBias = 'SLIGHT BEARISH';
    recommendation = 'Awaiting 2+ timeframe alignment for sell signal';
  }

  return {
    action,
    confluenceScore,
    analysis,
    tradeBias,
    recommendation
  };
}

// Usage: Downsample daily prices to 4H and 1H for this example
const dailyPrices = [100, 101, 102, 103, 104, 105, 106, 107, 108];
const four_hourPrices = dailyPrices.flatMap(p => [p, p * 1.002, p * 1.003, p * 1.0025]);
const hourlyPrices = four_hourPrices.flatMap(p => [p, p * 1.001, p * 1.002, p * 1.0015]);

const confluence = generateConfluenceSignal(dailyPrices, four_hourPrices, hourlyPrices);

console.log(`
Multi-Timeframe Confluence Analysis
═════════════════════════════════════════

Action:         ${confluence.action}
Confluence:     ${(confluence.confluenceScore * 100).toFixed(0)}%
Bias:           ${confluence.tradeBias}

Timeframe Analysis:
${confluence.analysis.map(a => `
  ${a.timeframe.padEnd(4)} Trend: ${a.trend.padEnd(7)} Strength: ${(a.strength * 100).toFixed(0)}% (${a.signalAlignment}/3)
`).join('')}

Recommendation: ${confluence.recommendation}
`);
```

## Order Flow Momentum Integration

Combine price action with volume/spread analysis.

```typescript
import {
  calculateATR,
  calculateVolatility,
  calculateRSI
} from '@railpath/finance-toolkit';

interface OrderFlowAnalysis {
  priceAction: 'bullish' | 'bearish' | 'neutral';
  volumeProfile: 'buying' | 'selling' | 'balanced';
  spreadIndicator: 'wide' | 'normal' | 'tight';
  momentumDirection: 'accelerating' | 'decelerating' | 'stable';
  orderFlowScore: number;  // -1 to +1
  recommendation: string;
}

function analyzeOrderFlow(
  closes: number[],
  highs: number[],
  lows: number[],
  volumes: number[],
  bids: number[],
  asks: number[]
): OrderFlowAnalysis {
  const index = closes.length - 1;

  // Price structure
  const rsi = calculateRSI({ prices: closes, period: 14 });
  const atr = calculateATR({ high: highs, low: lows, close: closes, period: 14 });

  // Volume analysis
  const avgVolume = volumes.slice(-20).reduce((a, b) => a + b, 0) / 20;
  const currentVolume = volumes[index];
  const volumeRatio = currentVolume / avgVolume;

  // Spread analysis
  const currentSpread = asks[index] - bids[index];
  const avgSpread = highs.slice(-20).map((h, i) => h - lows[i]).reduce((a, b) => a + b, 0) / 20;
  const spreadRatio = currentSpread / avgSpread;

  // Price action
  const close = closes[index];
  const open = closes[index - 1]; // Simplified
  const high = highs[index];
  const low = lows[index];
  const bodySize = Math.abs(close - open);
  const wicks = (high - Math.max(close, open)) + (Math.min(close, open) - low);
  const bodyRatio = bodySize / (bodySize + wicks);

  let priceAction: 'bullish' | 'bearish' | 'neutral' = 'neutral';
  let orderFlowScore = 0;

  // Bullish price action: close > open, small wicks
  if (close > open && bodyRatio > 0.6) {
    priceAction = 'bullish';
    orderFlowScore += 0.3;
  }
  // Bearish price action: close < open, small wicks
  if (close < open && bodyRatio > 0.6) {
    priceAction = 'bearish';
    orderFlowScore -= 0.3;
  }

  // Volume confirmation
  let volumeProfile: 'buying' | 'selling' | 'balanced' = 'balanced';
  if (volumeRatio > 1.2 && priceAction === 'bullish') {
    volumeProfile = 'buying';
    orderFlowScore += 0.25;
  }
  if (volumeRatio > 1.2 && priceAction === 'bearish') {
    volumeProfile = 'selling';
    orderFlowScore -= 0.25;
  }

  // Spread indicates liquidity
  let spreadIndicator: 'wide' | 'normal' | 'tight' = 'normal';
  if (spreadRatio > 1.3) {
    spreadIndicator = 'wide';
    orderFlowScore *= 0.8; // Lower confidence with wide spread
  }
  if (spreadRatio < 0.7) {
    spreadIndicator = 'tight';
    orderFlowScore *= 1.1; // Increase confidence with tight spread
  }

  // Momentum from RSI
  const rsiValue = rsi.rsi[index];
  let momentumDirection: 'accelerating' | 'decelerating' | 'stable' = 'stable';
  const rsiPrev = rsi.rsi[index - 1] || rsiValue;

  if ((rsiValue > rsiPrev && rsiValue > 50) || (rsiValue < rsiPrev && rsiValue < 50)) {
    momentumDirection = 'accelerating';
    orderFlowScore += 0.1;
  } else if ((rsiValue < rsiPrev && rsiValue > 50) || (rsiValue > rsiPrev && rsiValue < 50)) {
    momentumDirection = 'decelerating';
    orderFlowScore -= 0.1;
  }

  // Normalize score
  orderFlowScore = Math.max(-1, Math.min(1, orderFlowScore));

  let recommendation = 'Neutral bias';
  if (orderFlowScore > 0.5) {
    recommendation = `Strong buying pressure - ${volumeProfile} with ${spreadIndicator} spread`;
  } else if (orderFlowScore > 0.2) {
    recommendation = `Moderate bullish - watch for confirmation`;
  } else if (orderFlowScore < -0.5) {
    recommendation = `Strong selling pressure - ${volumeProfile} with ${spreadIndicator} spread`;
  } else if (orderFlowScore < -0.2) {
    recommendation = `Moderate bearish - watch for confirmation`;
  }

  return {
    priceAction,
    volumeProfile,
    spreadIndicator,
    momentumDirection,
    orderFlowScore,
    recommendation
  };
}

// Usage
const closes = [100, 100.5, 100.2, 100.8, 101];
const highs = closes.map(c => c * 1.01);
const lows = closes.map(c => c * 0.99);
const volumes = [1000000, 1200000, 800000, 1500000, 900000];
const bids = closes.map(c => c - 0.02);
const asks = closes.map(c => c + 0.02);

const orderFlow = analyzeOrderFlow(closes, highs, lows, volumes, bids, asks);

console.log(`
Order Flow Analysis
──────────────────────────────
Order Flow Score: ${orderFlow.orderFlowScore.toFixed(2)}
Price Action:     ${orderFlow.priceAction.toUpperCase()}
Volume Profile:   ${orderFlow.volumeProfile.toUpperCase()}
Spread:           ${orderFlow.spreadIndicator.toUpperCase()}
Momentum:         ${orderFlow.momentumDirection.toUpperCase()}

📊 ${orderFlow.recommendation}
`);
```

---

## Implementation Best Practices

### 1. Signal Filtering
Always require multiple confluences:
- At least 2/3 indicators aligned for entry
- Signals weakened by 20% if volatility very low
- Signals ignored if spread > 2x average

### 2. Risk Management
- Position sizing from VaR, not fixed amounts
- Stop loss always 2x ATR below entry (buy) or above (sell)
- Risk/Reward minimum 1:1.5, target 1:2+

### 3. Regime Sensitivity
- Reduce position size 30-50% in bearish regimes
- Increase position size in bullish regimes with tight confluence
- Avoid mean reversion in strong trending markets

### 4. Monitoring
- Track signal accuracy by strategy and timeframe
- Disable strategy if win rate < 45% over 20 trades
- Adjust parameters monthly based on regime changes
