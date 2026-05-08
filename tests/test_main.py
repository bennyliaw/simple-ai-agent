import argparse
import pytest
from main import temperature_arg, _model_temp_label


def test_temperature_arg_valid_zero():
    assert temperature_arg("0.0") == 0.0


def test_temperature_arg_valid_one():
    assert temperature_arg("1.0") == 1.0


def test_temperature_arg_valid_mid():
    assert temperature_arg("0.5") == 0.5


def test_temperature_arg_too_high():
    with pytest.raises(argparse.ArgumentTypeError):
        temperature_arg("1.5")


def test_temperature_arg_too_low():
    with pytest.raises(argparse.ArgumentTypeError):
        temperature_arg("-0.1")


def test_temperature_arg_non_numeric():
    with pytest.raises(argparse.ArgumentTypeError):
        temperature_arg("abc")


def test_model_temp_label_no_temperature():
    assert _model_temp_label("granite4.1:3b", None) == "granite4.1:3b"


def test_model_temp_label_with_temperature():
    assert _model_temp_label("granite4.1:3b", 0.3) == "granite4.1:3b (temp=0.3)"
