# 🧠 EAS Strategy Parser to AlgoWizard Translator

A Python tool that parses Expert Advisor Studio (EAS) exported strategies and formats them for easy rebuilding in StrategyQuant X AlgoWizard.

## 🎯 Purpose

This tool bridges the gap between EAS and AlgoWizard by:
- Extracting trading logic from EAS JSON exports
- Translating indicators and parameters
- Structuring entry/exit rules in AlgoWizard-compatible format
- Providing clear documentation for manual implementation

## 📋 Requirements

- Python 3.6+
- No additional packages required (uses standard library only)

## 🚀 Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed

## 💻 Usage

```bash
# Basic usage
python parse_strategy.py sample/EURUSD_M5.json

# Specify output file
python parse_strategy.py sample/EURUSD_M5.json -o custom_output.md

# Enable verbose output
python parse_strategy.py sample/EURUSD_M5.json -v
```

## 📂 Project Structure

```
/eas-to-algowizard-translator/
├── sample/                 # Sample EAS JSON strategy files
│   └── EURUSD_M5.json
├── output/                 # Generated markdown files
│   └── EURUSD_M5_parsed.md
├── parse_collection.py     # Parser for strategy collections
├── parse_strategy.py       # Main parser script
└── README.md               # Project documentation
```

## 🔄 Workflow

1. **Export** strategy from EAS as `.json`
2. **Run** the parser script
3. **View** the generated markdown with structured strategy information
4. **Implement** in AlgoWizard using the translated instructions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📄 License

MIT 