import pytest
from tools.calculator import run as calc
from tools.clock import run as clock
from tools import TOOLS, TOOL_MAP


def test_calculator_addition():
    assert calc({"expression": "2 + 3"}) == "5"


def test_calculator_complex():
    assert calc({"expression": "2 + 3 * (4 - 1)"}) == "11"


def test_calculator_division():
    assert calc({"expression": "10 / 4"}) == "2.5"


def test_calculator_power():
    assert calc({"expression": "2 ** 10"}) == "1024"


def test_calculator_invalid():
    result = calc({"expression": "import os"})
    assert result.startswith("Error")


def test_calculator_division_by_zero():
    result = calc({"expression": "10 / 0"})
    assert result.startswith("Error")


def test_calculator_unary_negation():
    assert calc({"expression": "-5 + 3"}) == "-2"


def test_calculator_float_input():
    assert calc({"expression": "1.5 * 2"}) == "3.0"


def test_calculator_missing_key():
    with pytest.raises(KeyError):
        calc({})


def test_clock_returns_utc():
    result = clock({})
    assert "UTC" in result


def test_clock_format():
    result = clock({})
    # format: YYYY-MM-DD HH:MM:SS UTC
    parts = result.split()
    assert len(parts) == 3
    assert parts[2] == "UTC"
    assert len(parts[0]) == 10  # YYYY-MM-DD
    assert len(parts[1]) == 8   # HH:MM:SS


def test_tools_list_nonempty():
    assert len(TOOLS) > 0


def test_tool_map_keys_match_schemas():
    schema_names = {t["name"] for t in TOOLS}
    assert set(TOOL_MAP.keys()) == schema_names
