def test_pdf_ingestor_stub():
    from backend.ingest import PDFIngestor
    ingestor = PDFIngestor()
    assert hasattr(ingestor, 'load_pdfs')
    assert hasattr(ingestor, 'chunk_text')
    assert hasattr(ingestor, 'generate_embeddings')
    assert hasattr(ingestor, 'build_vectorstore')
    assert hasattr(ingestor, 'run')
