# Strategy Breakdown - EURUSD M30

## Strategy Parameters
**Direction**: Long
**Stop Loss**: 430 pips
**Take Profit**: 397 pips
**Position Size**: 0.1

## Backtest Statistics
**Profit Factor**: 1.3670115046942584
**Total Trades**: 700
**Win/Loss Ratio**: 0.5542857142857143
**Max Drawdown**: 13.75634453511506%

## Strategy Flow Diagram
```
+---------------------------------------+
| Strategy: EURUSD M30 |
+---------------------------------------+

+---------------------------------------+
| ENTRY CONDITIONS                      |
+---------------------------------------+
| 1. Directional Indicators - Directional Indicators conditi |
| 2. Bears Power - Bears Power condition          |
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
| 1. Pin Bar - Pin Bar condition              |
| 2. Pin Bar - Pin Bar condition              |
+---------------------------------------+
                    |
                    V
+---------------------------------------+
| CLOSE POSITION                        |
+---------------------------------------+
```

## Entry Conditions:
**Logical Relationship**: All conditions must be true (AND relationship)
```
Condition 1:
  EAS: Directional Indicators - Directional Indicators condition
  AlgoWizard: ADX - Directional Indicators condition
  Parameters:
    * Parameter 1: 40

Condition 2:
  EAS: Bears Power - Bears Power condition
  AlgoWizard: Bears Power - Bears Power condition
  Parameters:
    * Parameter 1: 7

```

## Exit Conditions:
**Logical Relationship**: All conditions must be true (AND relationship)
```
Condition 1:
  EAS: Pin Bar - Pin Bar condition
  AlgoWizard: Pin Bar - Pin Bar condition
  Parameters:
    * Parameter 1: 10
    * Parameter 2: 40

Condition 2:
  EAS: Pin Bar - Pin Bar condition
  AlgoWizard: Pin Bar - Pin Bar condition
  Parameters:
    * Parameter 1: 6
    * Parameter 2: 32

```

## AlgoWizard Implementation Notes
1. Create a new strategy in AlgoWizard
2. Set up the following blocks:
   - Entry block with conditions as described above
   - Exit block with conditions as described above
   - Set stop loss and take profit values
3. Configure position sizing
4. Verify all indicator parameters match the EAS configuration