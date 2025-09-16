import React, { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pdfFile, setPdfFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setAnswer("");
    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || `Error: ${response.status}`);
        setAnswer("");
      } else if (data.answer) {
        setAnswer(data.answer);
      } else {
        setError("No answer returned.");
      }
    } catch (err) {
      setError("Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePdfChange = (e) => {
    setPdfFile(e.target.files[0]);
    setUploadStatus("");
  };

  const handlePdfUpload = async (e) => {
    e.preventDefault();
    if (!pdfFile) return;
    setUploadStatus("Uploading...");
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", pdfFile);
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const data = await response.json();
      setUploadStatus(`Success! PDF '${data.file_id}' uploaded.`);
      setPdfFile(null);
      // Reset file input visually
      document.getElementById("pdf-upload").value = "";
      setTimeout(() => setUploadStatus(""), 3000);
    } catch (err) {
      setError(err.message);
      setUploadStatus("");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", padding: 24 }}>
      <h1>OpenAI RAG PDF Demo</h1>

      {/* PDF Upload Section */}
      <form onSubmit={handlePdfUpload} style={{ marginBottom: 24 }}>
        <label htmlFor="pdf-upload">Upload a PDF:</label>
        <input
          id="pdf-upload"
          type="file"
          accept="application/pdf"
          onChange={handlePdfChange}
          style={{ marginLeft: 8 }}
        />
        <button type="submit" disabled={!pdfFile} style={{ marginLeft: 8 }}>
          Upload
        </button>
        {uploadStatus && <span style={{ marginLeft: 12 }}>{uploadStatus}</span>}
      </form>

      {/* Question Section */}
      <form onSubmit={handleSubmit}>
        <label htmlFor="question">Ask a question about the PDFs:</label>
        <input
          id="question"
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "100%", margin: "12px 0", padding: 8 }}
          required
        />
        <button type="submit" disabled={loading || !question}>
          {loading ? "Loading..." : "Submit"}
        </button>
        {uploadStatus && <span style={{ marginLeft: 12, color: 'green' }}>{uploadStatus}</span>}
        {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      </form>
      {answer && (
        <div style={{ marginTop: 24, background: "#f6f8fa", padding: 16, borderRadius: 8 }}>
          <strong>Answer:</strong>
          <div>{answer}</div>
        </div>
      )}
      {error && (
        <div style={{ marginTop: 24, color: "red" }}>
          <strong>{error}</strong>
        </div>
      )}
    </div>
  );
}

export default App;
