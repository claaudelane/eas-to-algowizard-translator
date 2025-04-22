# Strategy Breakdown - EURUSD M5

## Strategy Parameters
**Direction**: Long
**Stop Loss**: 20 pips
**Take Profit**: 40 pips
**Position Size**: 0.1

## Backtest Settings
**Period**: 2020-01-01 to 2023-01-01
**Initial Deposit**: 10000
**Spread**: 2 points

## Optimization Parameters
**Criterion**: Profit Factor
**Parameters**:
- RSI Period: 7 to 21, step 1
- MA Period: 20 to 100, step 5

## Strategy Flow Diagram
```
+---------------------------------------+
| Strategy: EURUSD M5 |
+---------------------------------------+

+---------------------------------------+
| ENTRY CONDITIONS                      |
+---------------------------------------+
| 1. RSI - RSI crosses below the level li |
| 2. MA - Price crosses above MA         |
| 3. Bollinger Bands - Price crosses below the lower  |
+---------------------------------------+
                    |
                    V
+---------------------------------------+
| OPEN LONG POSITION             |
| SL: 20 pips, TP: 40 pips     |
+---------------------------------------+
                    |
                    V
+---------------------------------------+
| EXIT CONDITIONS                       |
+---------------------------------------+
| 1. Trailing Stop - Trailing Stop triggers         |
| 2. RSI - RSI crosses above the level li |
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
  EAS: RSI - RSI crosses below the level line
  AlgoWizard: RSI - RSI crosses below the level line
  Parameters:
    * Period: 14
    * Level: 30
    * Price: Close

Condition 2:
  EAS: MA - Price crosses above MA
  AlgoWizard: Moving Average - Price crosses above MA
  Parameters:
    * Period: 50
    * Method: SMA
    * Price: Close
    * Shift: 0

Condition 3:
  EAS: Bollinger Bands - Price crosses below the lower band
  AlgoWizard: Bollinger Bands - Price crosses below the lower band
  Parameters:
    * Period: 20
    * Deviations: 2
    * Price: Close

```

## Exit Conditions:
**Logical Relationship**: All conditions must be true (AND relationship)
```
Condition 1:
  EAS: Trailing Stop - Trailing Stop triggers
  AlgoWizard: Trailing Stop - Trailing Stop triggers
  Parameters:
    * Distance: 20
    * Step: 5

Condition 2:
  EAS: RSI - RSI crosses above the level line
  AlgoWizard: RSI - RSI crosses above the level line
  Parameters:
    * Period: 14
    * Level: 70
    * Price: Close

```

## AlgoWizard Implementation Notes
1. Create a new strategy in AlgoWizard
2. Set up the following blocks:
   - Entry block with conditions as described above
   - Exit block with conditions as described above
   - Set stop loss and take profit values
3. Configure position sizing
4. Verify all indicator parameters match the EAS configuration
5. Set up optimization parameters:
   - RSI Period: range 7 to 21
   - MA Period: range 20 to 100