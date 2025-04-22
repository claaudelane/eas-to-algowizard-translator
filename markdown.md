# 🧠 EAS Strategy Parser to AlgoWizard Translator

## 🎯 Goal

Build a Python script that parses `.json` strategies exported from **Expert Advisor Studio (EAS)** and structures them into a readable format that can be easily rebuilt in **StrategyQuant X AlgoWizard**, preserving the logic, indicators, and parameters.

---

## ✅ Why This Is Useful

- **EAS** allows high-speed mining with no license limits.
- **SQX (AlgoWizard)** enables deeper robustness validation via Monte Carlo, FWO, and Multi-Market.
- This tool bridges both by translating mined EAS logic into AlgoWizard-ready templates.

---

## 🔁 Workflow Overview

1. **Export** strategy from EAS as `.json`
2. **Run** the parser script
3. **Extract** logic: entries, exits, indicators, SL/TP
4. **Render** the result as a structured object
5. **Copy logic** manually into AlgoWizard blocks

---

## 📁 Folder Structure

```
/eas-strategy-parser/
├── sample/                 # Sample EAS JSON strategy files
│   └── EURUSD_M5.json
├── output/                 # Generated markdown files
│   └── EURUSD_M5_parsed.md
├── parse_strategy.py       # Main parser script
└── README.md               # Project documentation
```

---

## 💻 Usage Instructions

```bash
# Basic usage
python parse_strategy.py sample/EURUSD_M5.json

# Specify output file
python parse_strategy.py sample/EURUSD_M5.json -o custom_output.md

# Enable verbose output
python parse_strategy.py sample/EURUSD_M5.json -v
```

---

## 📋 Features

- ✅ Extracts entry and exit conditions from EAS JSON
- ✅ Maps EAS indicators to AlgoWizard equivalents
- ✅ Preserves indicator parameters
- ✅ Includes stop loss and take profit values
- ✅ Detects logical relationships between conditions
- ✅ Generates ASCII strategy flow diagram
- ✅ Provides implementation guidelines for AlgoWizard
- ✅ Handles optimization parameters

---

## 📈 Example Output

The script generates a markdown file with:

1. Strategy overview (symbol, timeframe, SL/TP)
2. Visual flow diagram of the strategy
3. Detailed entry conditions with parameters
4. Detailed exit conditions with parameters 
5. Implementation notes for AlgoWizard

---

## 🚀 Future Enhancements

- Add support for more indicator types
- Improve logical relationship detection
- Add direct export to AlgoWizard format
- Create a GUI interface
- Add batch processing for multiple strategies

---

## 📚 Resources

- [Expert Advisor Studio Documentation](https://www.expertadvisorstudio.com/documentation/)
- [StrategyQuant X AlgoWizard Guide](https://www.strategyquant.com/algowizard/)
- [Python Documentation](https://docs.python.org/3/)
