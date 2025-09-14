def test_ragqa_stub():
    from backend.app import RAGQA
    ragqa = RAGQA()
    assert hasattr(ragqa, 'retrieve')
    assert hasattr(ragqa, 'answer')
    assert hasattr(ragqa, 'run')
