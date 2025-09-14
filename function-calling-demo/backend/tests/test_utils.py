import pytest
from backend import utils

def test_log_info(capsys):
    utils.log_info("Hello test")
    captured = capsys.readouterr()
    assert "Hello test" in captured.out

def test_log_error(capsys):
    utils.log_error("Error test")
    captured = capsys.readouterr()
    assert "Error test" in captured.out
