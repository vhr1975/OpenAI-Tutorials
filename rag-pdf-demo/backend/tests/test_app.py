def test_ragqa_stub():
    from backend.main import RAGQA
    ragqa = RAGQA()
    assert hasattr(ragqa, 'retrieve')
    assert hasattr(ragqa, 'answer')
    assert hasattr(ragqa, 'run')
