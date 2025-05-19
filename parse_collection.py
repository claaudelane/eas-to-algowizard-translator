#!/usr/bin/env python3
"""
EAS Collection Parser to AlgoWizard Translator

This script parses Expert Advisor Studio (EAS) Collection JSON strategy files and
transforms them into a structured format compatible with StrategyQuant X AlgoWizard.
"""

import json
import os
import argparse
from pathlib import Path
import sys

# Mapping for indicator names to more descriptive versions
INDICATOR_MAPPING = {
    "Directional Indicators": "ADX",
    "Bears Power": "Bears Power",
    "Bulls Power": "Bulls Power",
    "Pin Bar": "Pin Bar Pattern",
    "Engulfing Pattern": "Engulfing Candlestick",
    "RSI": "RSI",
    "MA": "Moving Average",
    "Bollinger Bands": "Bollinger Bands",
    "MACD": "MACD",
    "Stochastic": "Stochastic"
    # Add more mappings as needed
}

# Logic interpretation for indicators based on parameters
LOGIC_INTERPRETATIONS = {
    "Directional Indicators": lambda params: f"ADX is stronger than {params.get('Level', 'N/A')} with period {params.get('Period', 'N/A')}",
    "Bears Power": lambda params: f"Bears Power indicator shows downward momentum with period {params.get('Period', 'N/A')}",
    "Bulls Power": lambda params: f"Bulls Power indicator shows upward momentum with period {params.get('Period', 'N/A')}",
    "Pin Bar": lambda params: f"Pin Bar pattern identified with strength {params.get('Strength', 'N/A')} and length {params.get('Length', 'N/A')}"
    # Add more interpretations as needed
}

# Mapping for indicator list indexes to parameters (this needs to be customized based on EAS documentation)
INDEX_MAPPING = {
    "Directional Indicators": {
        0: "Period",
        1: "Level"
    },
    "Bears Power": {
        0: "Period",
        1: "Level"
    },
    "Bulls Power": {
        0: "Period",
        1: "Level"
    },
    "Pin Bar": {
        0: "Strength",
        1: "Length"
    },
    "RSI": {
        0: "Period",
        1: "Level"
    },
    "Bollinger Bands": {
        0: "Period",
        1: "Deviations"
    },
    "Engulfing Pattern": {
        0: "Strength"
    }
    # Add more as needed
}

def get_parameter_description(indicator, list_idx, value):
    """
    Get a human-readable description of a parameter based on list index and value.
    
    Args:
        indicator: The indicator name
        list_idx: The index in the listIndexes array
        value: The corresponding value
        
    Returns:
        A string describing the parameter
    """
    # This would need to be expanded based on EAS documentation
    if indicator == "Directional Indicators":
        if list_idx == 0:  # First list index typically represents variation
            return f"ADX with period {value}"
        elif list_idx == 1:
            return f"ADX greater than {value}"
    elif indicator == "Bears Power":
        if list_idx == 0:
            return f"Bears Power with period {value}"
    elif indicator == "Pin Bar":
        if list_idx == 0:
            return f"Pin Bar with strength {value}"
        elif list_idx == 1:
            return f"Pin Bar length {value}"
            
    # Default fallback
    return f"Parameter {list_idx} = {value}"

def parse_eas_collection(json_path):
    """
    Parse an EAS Collection JSON file and extract key components.
    
    Args:
        json_path: Path to the EAS JSON strategy file
        
    Returns:
        Dictionary containing structured strategy information
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            collection = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {json_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Strategy file not found: {json_path}")

    # Check if it's a collection (array) and get the first strategy
    if isinstance(collection, list):
        if len(collection) == 0:
            raise ValueError("Strategy collection is empty")
        strategy_data = collection[0]
    else:
        strategy_data = collection

    # Extract strategy info
    symbol = strategy_data.get("symbol", "Unknown")
    period = strategy_data.get("period", "Unknown")
    
    # Get strategy properties
    properties = strategy_data.get("strategy", {}).get("properties", {})
    
    # Extract basic strategy information
    out = {
        "symbol": symbol,
        "timeframe": period,
        "entry_conditions": [],
        "exit_conditions": [],
        "stop_loss": properties.get("stopLoss", 0),
        "take_profit": properties.get("takeProfit", 0),
        "position_size": properties.get("entryLots", "Not specified"),
        "direction": "Long" if properties.get("tradeDirectionMode", 0) == 0 else "Short",
        "backtest_stats": strategy_data.get("backtestStats", {}),
        "magic_number": strategy_data.get("magicNumber", "Not specified"),
        "use_stop_loss": properties.get("useStopLoss", True),
        "use_take_profit": properties.get("useTakeProfit", True),
        "is_trailing_stop": properties.get("isTrailingStop", False),
        "opposite_entry_signal": properties.get("oppositeEntrySignal", False)
    }
    
    # Get entry and exit filters
    open_filters = strategy_data.get("strategy", {}).get("openFilters", [])
    close_filters = strategy_data.get("strategy", {}).get("closeFilters", [])
    
    # Process entry conditions
    for filter_item in open_filters:
        indicator_name = filter_item.get("name", "Unknown")
        list_indexes = filter_item.get("listIndexes", [])
        num_values = filter_item.get("numValues", [])
        
        # Try to interpret the values
        params = {}
        descriptions = []
        
        for i, idx in enumerate(list_indexes):
            if idx >= 0 and i < len(num_values):
                param_name = INDEX_MAPPING.get(indicator_name, {}).get(i, f"Param{i}")
                params[param_name] = num_values[i]
                descriptions.append(get_parameter_description(indicator_name, i, num_values[i]))
        
        # Create a human-readable logic interpretation
        logic_desc = " AND ".join(descriptions) if descriptions else "Uses unknown parameters"
        
        # Use more specific logic interpretation if available
        if indicator_name in LOGIC_INTERPRETATIONS:
            logic_desc = LOGIC_INTERPRETATIONS[indicator_name](params)
        
        out["entry_conditions"].append({
            "indicator": indicator_name,
            "algowizard_indicator": INDICATOR_MAPPING.get(indicator_name, indicator_name),
            "logic": logic_desc,
            "params": params
        })
    
    # Process exit conditions
    for filter_item in close_filters:
        indicator_name = filter_item.get("name", "Unknown")
        list_indexes = filter_item.get("listIndexes", [])
        num_values = filter_item.get("numValues", [])
        
        # Try to interpret the values
        params = {}
        descriptions = []
        
        for i, idx in enumerate(list_indexes):
            if idx >= 0 and i < len(num_values):
                param_name = INDEX_MAPPING.get(indicator_name, {}).get(i, f"Param{i}")
                params[param_name] = num_values[i]
                descriptions.append(get_parameter_description(indicator_name, i, num_values[i]))
        
        # Create a human-readable logic interpretation
        logic_desc = " AND ".join(descriptions) if descriptions else "Uses unknown parameters"
        
        # Use more specific logic interpretation if available
        if indicator_name in LOGIC_INTERPRETATIONS:
            logic_desc = LOGIC_INTERPRETATIONS[indicator_name](params)
        
        out["exit_conditions"].append({
            "indicator": indicator_name,
            "algowizard_indicator": INDICATOR_MAPPING.get(indicator_name, indicator_name),
            "logic": logic_desc,
            "params": params
        })

    return out

def create_strategy_diagram(strategy_dict):
    """
    Generate a simple ASCII diagram representing the strategy flow.
    
    Args:
        strategy_dict: Dictionary containing the parsed strategy
        
    Returns:
        String containing the strategy diagram
    """
    diagram = []
    
    # Add header
    diagram.append("+---------------------------------------+")
    diagram.append(f"| Strategy: {strategy_dict['symbol']} {strategy_dict['timeframe']} |")
    diagram.append("+---------------------------------------+")
    diagram.append("")
    
    # Add entry conditions
    diagram.append("+---------------------------------------+")
    diagram.append("| ENTRY CONDITIONS                      |")
    diagram.append("+---------------------------------------+")
    
    for i, cond in enumerate(strategy_dict['entry_conditions'], 1):
        params_str = ", ".join([f"{k}={v}" for k, v in cond['params'].items()])
        diagram.append(f"| {i}. {cond['indicator']} ({params_str}) |")
    
    diagram.append("+---------------------------------------+")
    diagram.append("                    |")
    diagram.append("                    V")
    
    # Add position info
    diagram.append("+---------------------------------------+")
    diagram.append(f"| OPEN {strategy_dict['direction'].upper()} POSITION             |")
    
    sl_tp_info = ""
    if strategy_dict.get("use_stop_loss", True):
        sl_tp_info += f"SL: {strategy_dict['stop_loss']} pips"
        if strategy_dict.get("is_trailing_stop", False):
            sl_tp_info += " (trailing)"
    if strategy_dict.get("use_take_profit", True):
        if sl_tp_info:
            sl_tp_info += ", "
        sl_tp_info += f"TP: {strategy_dict['take_profit']} pips"
    
    diagram.append(f"| {sl_tp_info} |")
    diagram.append("+---------------------------------------+")
    diagram.append("                    |")
    diagram.append("                    V")
    
    # Add exit conditions
    diagram.append("+---------------------------------------+")
    diagram.append("| EXIT CONDITIONS                       |")
    diagram.append("+---------------------------------------+")
    
    for i, cond in enumerate(strategy_dict['exit_conditions'], 1):
        params_str = ", ".join([f"{k}={v}" for k, v in cond['params'].items()])
        diagram.append(f"| {i}. {cond['indicator']} ({params_str}) |")
    
    diagram.append("+---------------------------------------+")
    diagram.append("                    |")
    diagram.append("                    V")
    diagram.append("+---------------------------------------+")
    diagram.append("| CLOSE POSITION                        |")
    diagram.append("+---------------------------------------+")
    
    return "\n".join(diagram)

def to_markdown(strategy_dict, output_path):
    """
    Generate a formatted markdown file from the parsed strategy information.
    
    Args:
        strategy_dict: Dictionary containing the parsed strategy
        output_path: Path where the markdown file will be saved
    """
    # Use plain text versions of emojis to avoid encoding issues
    lines = [
        f"# Strategy Breakdown - {strategy_dict['symbol']} {strategy_dict['timeframe']}",
        "",
        "## Strategy Parameters",
        f"**Direction**: {strategy_dict['direction']}",
        f"**Stop Loss**: {strategy_dict['stop_loss']} pips" + (" (Trailing)" if strategy_dict.get('is_trailing_stop', False) else ""),
        f"**Take Profit**: {strategy_dict['take_profit']} pips",
        f"**Position Size**: {strategy_dict['position_size']}",
        f"**Magic Number**: {strategy_dict['magic_number']}",
        f"**Opposite Entry Signal**: {'Yes' if strategy_dict.get('opposite_entry_signal', False) else 'No'}",
        ""
    ]
    
    # Add backtest stats if available
    backtest_stats = strategy_dict.get("backtest_stats", {})
    if backtest_stats:
        lines.extend([
            "## Backtest Statistics",
            f"**Profit Factor**: {backtest_stats.get('profitFactor', 'N/A')}",
            f"**Net Profit**: {backtest_stats.get('netBalance', 'N/A')}",
            f"**Max Drawdown**: {backtest_stats.get('maxDrawdownPercent', 'N/A')}%",
            f"**Win/Loss Ratio**: {backtest_stats.get('winLossRatio', 'N/A')}",
            f"**Total Trades**: {backtest_stats.get('countOfTrades', 'N/A')}",
            ""
        ])
    
    # Add strategy flow diagram
    lines.extend([
        "## Strategy Flow Diagram",
        "```",
        create_strategy_diagram(strategy_dict),
        "```",
        ""
    ])
    
    # Entry conditions section
    lines.append("## Entry Conditions:")
    lines.append("```") # Start of entry block for AlgoWizard

    for i, cond in enumerate(strategy_dict['entry_conditions'], 1):
        lines.append(f"Condition {i}:")
        lines.append(f"  Indicator: {cond['indicator']}")
        lines.append(f"  AlgoWizard: {cond['algowizard_indicator']}")
        lines.append(f"  Logic: {cond['logic']}")
        lines.append("  Parameters:")
        for key, val in cond["params"].items():
            lines.append(f"    * {key}: {val}")
        lines.append("")

    lines.append("```") # End of entry block
    lines.append("")
    
    # Exit conditions section
    lines.append("## Exit Conditions:")
    lines.append("```") # Start of exit block for AlgoWizard
    
    for i, cond in enumerate(strategy_dict['exit_conditions'], 1):
        lines.append(f"Condition {i}:")
        lines.append(f"  Indicator: {cond['indicator']}")
        lines.append(f"  AlgoWizard: {cond['algowizard_indicator']}")
        lines.append(f"  Logic: {cond['logic']}")
        lines.append("  Parameters:")
        for key, val in cond["params"].items():
            lines.append(f"    * {key}: {val}")
        lines.append("")

    lines.append("```") # End of exit block
    lines.append("")
    
    # AlgoWizard implementation notes
    lines.append("## AlgoWizard Implementation Notes")
    lines.append("1. Create a new strategy in AlgoWizard for EURUSD M30 timeframe")
    lines.append("2. Set up entry conditions:")
    
    for i, cond in enumerate(strategy_dict['entry_conditions'], 1):
        lines.append(f"   - Add {cond['algowizard_indicator']} indicator with parameters as described")
        
    lines.append("3. Set up exit conditions:")
    
    for i, cond in enumerate(strategy_dict['exit_conditions'], 1):
        lines.append(f"   - Add {cond['algowizard_indicator']} indicator with parameters as described")
        
    lines.append(f"4. Configure stop loss at {strategy_dict['stop_loss']} pips" + 
                 (" with trailing stop" if strategy_dict.get('is_trailing_stop', False) else ""))
    lines.append(f"5. Configure take profit at {strategy_dict['take_profit']} pips")
    lines.append(f"6. Set position size to {strategy_dict['position_size']} lots")
    
    # Create directory if one is specified
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write("\n".join(lines))
    except UnicodeEncodeError:
        # Fallback to ASCII encoding if UTF-8 fails
        with open(output_path, 'w', encoding='ascii', errors='replace') as out_file:
            out_file.write("\n".join(lines))

def main():
    """Main function to handle command-line execution"""
    parser = argparse.ArgumentParser(description='Parse EAS Collection JSON to AlgoWizard-friendly format')
    parser.add_argument('input', help='Path to input EAS Collection JSON strategy file')
    parser.add_argument('-o', '--output', help='Path to output markdown file (default: <input_name>_parsed.md)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Handle input path
    input_path = args.input
    
    # Generate default output path if not specified
    if not args.output:
        input_file = Path(input_path)
        output_path = str(input_file.with_name(f"{input_file.stem}_parsed.md"))
    else:
        output_path = args.output
    
    try:
        # Parse the strategy
        if args.verbose:
            print(f"Parsing strategy from {input_path}...")
        
        result = parse_eas_collection(input_path)
        
        # Generate markdown output
        to_markdown(result, output_path)
        
        print(f"Strategy successfully exported to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    return 0

# Run it
if __name__ == "__main__":
    sys.exit(main()) 