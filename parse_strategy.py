#!/usr/bin/env python3
"""
EAS Strategy Parser to AlgoWizard Translator

This script parses Expert Advisor Studio (EAS) JSON strategy files and
transforms them into a structured format compatible with StrategyQuant X AlgoWizard.
"""

import json
import os
import argparse
from pathlib import Path
import sys

# Mapping dictionary for translating EAS terms to AlgoWizard equivalents
INDICATOR_MAPPING = {
    "RSI": "RSI",
    "MA": "Moving Average",
    "Bollinger Bands": "Bollinger Bands",
    "MACD": "MACD",
    "Stochastic": "Stochastic",
    "ATR": "ATR",
    "Trailing Stop": "Trailing Stop",
    # Add more mappings as needed
}

LOGIC_MAPPING = {
    "crosses above": "crosses above",
    "crosses below": "crosses below",
    "is above": "is greater than",
    "is below": "is less than",
    # Add more mappings as needed
}

def parse_eas_strategy(json_path):
    """
    Parse an EAS strategy JSON file and extract key components.
    
    Args:
        json_path: Path to the EAS JSON strategy file
        
    Returns:
        Dictionary containing structured strategy information
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            strategy = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {json_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Strategy file not found: {json_path}")

    # Extract basic strategy information
    out = {
        "symbol": strategy.get("Symbol", ""),
        "timeframe": strategy.get("Period", ""),
        "entry_conditions": [],
        "exit_conditions": [],
        "stop_loss": strategy.get("StopLoss", 0),
        "take_profit": strategy.get("TakeProfit", 0),
        "position_size": strategy.get("EntryLots", "Not specified"),
        "direction": strategy.get("TradeDirection", "Long"),  # Add direction if available
        "optimization": strategy.get("Optimization", {}),
        "backtest": strategy.get("Backtest", {})
    }

    # Extract entry conditions with translations
    for rule in strategy.get("OpeningLogicConditions", []):
        indicator = rule.get("Indicator", "")
        logic = rule.get("LogicRule", "")
        
        # Translate EAS terms to AlgoWizard equivalents
        algowizard_indicator = INDICATOR_MAPPING.get(indicator, indicator)
        
        out["entry_conditions"].append({
            "indicator": indicator,
            "algowizard_indicator": algowizard_indicator,
            "logic": logic,
            "params": rule.get("Params", {})
        })

    # Extract exit conditions with translations
    for rule in strategy.get("ClosingLogicConditions", []):
        indicator = rule.get("Indicator", "")
        logic = rule.get("LogicRule", "")
        
        # Translate EAS terms to AlgoWizard equivalents
        algowizard_indicator = INDICATOR_MAPPING.get(indicator, indicator)
        
        out["exit_conditions"].append({
            "indicator": indicator,
            "algowizard_indicator": algowizard_indicator,
            "logic": logic,
            "params": rule.get("Params", {})
        })

    # Identify logical relationships between conditions
    if len(out["entry_conditions"]) > 1:
        out["entry_logic_relationship"] = find_logical_relationships(out["entry_conditions"])
    
    if len(out["exit_conditions"]) > 1:
        out["exit_logic_relationship"] = find_logical_relationships(out["exit_conditions"])

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
        diagram.append(f"| {i}. {cond['indicator']} - {cond['logic'][:30]:30} |")
    
    diagram.append("+---------------------------------------+")
    diagram.append("                    |")
    diagram.append("                    V")
    
    # Add position info
    diagram.append("+---------------------------------------+")
    diagram.append(f"| OPEN {strategy_dict['direction'].upper()} POSITION             |")
    diagram.append(f"| SL: {strategy_dict['stop_loss']} pips, TP: {strategy_dict['take_profit']} pips     |")
    diagram.append("+---------------------------------------+")
    diagram.append("                    |")
    diagram.append("                    V")
    
    # Add exit conditions
    diagram.append("+---------------------------------------+")
    diagram.append("| EXIT CONDITIONS                       |")
    diagram.append("+---------------------------------------+")
    
    for i, cond in enumerate(strategy_dict['exit_conditions'], 1):
        diagram.append(f"| {i}. {cond['indicator']} - {cond['logic'][:30]:30} |")
    
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
        f"**Stop Loss**: {strategy_dict['stop_loss']} pips",
        f"**Take Profit**: {strategy_dict['take_profit']} pips",
        f"**Position Size**: {strategy_dict['position_size']}",
        ""
    ]
    
    # Add backtest information if available
    backtest = strategy_dict.get("backtest", {})
    if backtest:
        lines.extend([
            "## Backtest Settings",
            f"**Period**: {backtest.get('Start', 'N/A')} to {backtest.get('End', 'N/A')}",
            f"**Initial Deposit**: {backtest.get('InitialDeposit', 'N/A')}",
            f"**Spread**: {backtest.get('Spread', 'N/A')} points",
            ""
        ])
    
    # Add optimization information if available
    optimization = strategy_dict.get("optimization", {})
    if optimization and optimization.get("Enabled", False):
        lines.extend([
            "## Optimization Parameters",
            f"**Criterion**: {optimization.get('Criterion', 'N/A')}",
            "**Parameters**:"
        ])
        
        for param in optimization.get("Parameters", []):
            lines.append(f"- {param.get('Name', 'Unknown')}: {param.get('Min', 'N/A')} to {param.get('Max', 'N/A')}, step {param.get('Step', 'N/A')}")
        lines.append("")
    
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
    if strategy_dict.get("entry_logic_relationship"):
        lines.append(f"**Logical Relationship**: {strategy_dict.get('entry_logic_relationship')}")
    lines.append("```") # Start of entry block for AlgoWizard

    for i, cond in enumerate(strategy_dict['entry_conditions'], 1):
        lines.append(f"Condition {i}:")
        lines.append(f"  EAS: {cond['indicator']} - {cond['logic']}")
        lines.append(f"  AlgoWizard: {cond['algowizard_indicator']} - {cond['logic']}")
        lines.append("  Parameters:")
        for key, val in cond["params"].items():
            lines.append(f"    * {key}: {val}")
        lines.append("")

    lines.append("```") # End of entry block
    lines.append("")
    
    # Exit conditions section
    lines.append("## Exit Conditions:")
    if strategy_dict.get("exit_logic_relationship"):
        lines.append(f"**Logical Relationship**: {strategy_dict.get('exit_logic_relationship')}")
    lines.append("```") # Start of exit block for AlgoWizard
    
    for i, cond in enumerate(strategy_dict['exit_conditions'], 1):
        lines.append(f"Condition {i}:")
        lines.append(f"  EAS: {cond['indicator']} - {cond['logic']}")
        lines.append(f"  AlgoWizard: {cond['algowizard_indicator']} - {cond['logic']}")
        lines.append("  Parameters:")
        for key, val in cond["params"].items():
            lines.append(f"    * {key}: {val}")
        lines.append("")

    lines.append("```") # End of exit block
    lines.append("")
    
    # AlgoWizard implementation notes
    lines.append("## AlgoWizard Implementation Notes")
    lines.append("1. Create a new strategy in AlgoWizard")
    lines.append("2. Set up the following blocks:")
    lines.append("   - Entry block with conditions as described above")
    lines.append("   - Exit block with conditions as described above")
    lines.append("   - Set stop loss and take profit values")
    lines.append("3. Configure position sizing")
    lines.append("4. Verify all indicator parameters match the EAS configuration")
    
    # Add optimization notes if present
    if optimization and optimization.get("Enabled", False):
        lines.append("5. Set up optimization parameters:")
        for param in optimization.get("Parameters", []):
            lines.append(f"   - {param.get('Name', 'Unknown')}: range {param.get('Min', 'N/A')} to {param.get('Max', 'N/A')}")

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

def find_logical_relationships(conditions):
    """
    Attempt to identify logical relationships (AND/OR) between conditions.
    This is a placeholder for more advanced parsing logic.
    
    Args:
        conditions: List of condition dictionaries
        
    Returns:
        String describing the logical relationship
    """
    if len(conditions) <= 1:
        return "Single condition, no logical relationship"
    
    # This is where we would implement more sophisticated logic parsing
    # For now, we'll assume AND relationship as that's most common
    return "All conditions must be true (AND relationship)"

def main():
    """Main function to handle command-line execution"""
    parser = argparse.ArgumentParser(description='Parse EAS strategy JSON to AlgoWizard-friendly format')
    parser.add_argument('input', help='Path to input EAS strategy JSON file')
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
        
        result = parse_eas_strategy(input_path)
        
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
