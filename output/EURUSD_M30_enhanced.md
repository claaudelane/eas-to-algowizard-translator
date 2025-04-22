# Strategy Breakdown - EURUSD M30

## Strategy Parameters
**Direction**: Long
**Stop Loss**: 430 pips
**Take Profit**: 397 pips
**Position Size**: 0.1
**Magic Number**: 1269817955
**Opposite Entry Signal**: Yes

## Backtest Statistics
**Profit Factor**: 1.3670115046942584
**Net Profit**: 18525.933812220563
**Max Drawdown**: 13.75634453511506%
**Win/Loss Ratio**: 0.5542857142857143
**Total Trades**: 700

## Strategy Flow Diagram
```
+---------------------------------------+
| Strategy: EURUSD M30 |
+---------------------------------------+

+---------------------------------------+
| ENTRY CONDITIONS                      |
+---------------------------------------+
| 1. Directional Indicators (Period=40) |
| 2. Bears Power (Period=7) |
+---------------------------------------+
                    |
                    V
+---------------------------------------+
| OPEN LONG POSITION             |
| SL: 430 pips, TP: 397 pips |
+---------------------------------------+
                    |
                    V
+---------------------------------------+
| EXIT CONDITIONS                       |
+---------------------------------------+
| 1. Pin Bar (Strength=10) |
| 2. Pin Bar (Strength=6) |
+---------------------------------------+
                    |
                    V
+---------------------------------------+
| CLOSE POSITION                        |
+---------------------------------------+
```

## Entry Conditions:
```
Condition 1:
  Indicator: Directional Indicators
  AlgoWizard: ADX
  Logic: ADX is stronger than N/A with period 40
  Parameters:
    * Period: 40

Condition 2:
  Indicator: Bears Power
  AlgoWizard: Bears Power
  Logic: Bears Power indicator shows downward momentum with period 7
  Parameters:
    * Period: 7

```

## Exit Conditions:
```
Condition 1:
  Indicator: Pin Bar
  AlgoWizard: Pin Bar Pattern
  Logic: Pin Bar pattern identified with strength 10 and length N/A
  Parameters:
    * Strength: 10

Condition 2:
  Indicator: Pin Bar
  AlgoWizard: Pin Bar Pattern
  Logic: Pin Bar pattern identified with strength 6 and length N/A
  Parameters:
    * Strength: 6

```

## AlgoWizard Implementation Notes
1. Create a new strategy in AlgoWizard for EURUSD M30 timeframe
2. Set up entry conditions:
   - Add ADX indicator with parameters as described
   - Add Bears Power indicator with parameters as described
3. Set up exit conditions:
   - Add Pin Bar Pattern indicator with parameters as described
   - Add Pin Bar Pattern indicator with parameters as described
4. Configure stop loss at 430 pips
5. Configure take profit at 397 pips
6. Set position size to 0.1 lots