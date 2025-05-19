import os
from pathlib import Path

import parse_strategy
import parse_collection


def test_parse_eas_strategy_sample():
    res = parse_strategy.parse_eas_strategy('sample/EURUSD_M5.json')
    assert res['symbol'] == 'EURUSD'
    assert res['timeframe'] == 'M5'
    assert len(res['entry_conditions']) == 3
    assert res['entry_conditions'][0]['indicator'] == 'RSI'
    assert res['exit_conditions'][0]['indicator'] == 'Trailing Stop'


def test_parse_eas_collection_sample():
    res = parse_collection.parse_eas_collection('Strategy Collection 1 EURUSD M30.json')
    assert res['symbol'] == 'EURUSD'
    assert res['timeframe'] == 'M30'
    assert len(res['entry_conditions']) == 2
    assert res['entry_conditions'][0]['indicator'] == 'Directional Indicators'
    assert res['exit_conditions'][0]['indicator'] == 'Pin Bar'


def test_to_markdown_no_directory(tmp_path, monkeypatch):
    res = parse_strategy.parse_eas_strategy('sample/EURUSD_M5.json')
    monkeypatch.chdir(tmp_path)
    output_file = 'output.md'
    parse_strategy.to_markdown(res, output_file)
    assert (tmp_path / output_file).exists()
