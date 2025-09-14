import pytest
from backend import openai_client

def test_call_openai_api_no_functions():
    payload = {"message": "Hello", "functions": []}
    result = openai_client.call_openai_api(payload)
    assert "function_call" in result
    assert "response" in result
