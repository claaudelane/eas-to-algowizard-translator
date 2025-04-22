# Strategy Breakdown - EURUSD M30

## Strategy Parameters
**Direction**: Long
**Stop Loss**: 430 pips
**Take Profit**: 397 pips
**Position Size**: 0.1
**Magic Number**: 1269817955

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
| SL: 430 pips, TP: 397 pips     |
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
  Parameters:
    * Period: 40

Condition 2:
  Indicator: Bears Power
  AlgoWizard: Bears Power
  Parameters:
    * Period: 7

```

## Exit Conditions:
```
Condition 1:
  Indicator: Pin Bar
  AlgoWizard: Pin Bar Pattern
  Parameters:
    * Strength: 10

Condition 2:
  Indicator: Pin Bar
  AlgoWizard: Pin Bar Pattern
  Parameters:
    * Strength: 6

```

## AlgoWizard Implementation Notes
1. Create a new strategy in AlgoWizard
2. Set up the following blocks:
   - Entry block with conditions as described above
   - Exit block with conditions as described above
   - Set stop loss and take profit values
3. Configure position sizing
4. Verify all indicator parameters match the EAS configuration