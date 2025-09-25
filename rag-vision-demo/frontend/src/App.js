
import React from "react";

function App() {
  const [imageFile, setImageFile] = React.useState(null);
  const [uploadStatus, setUploadStatus] = React.useState("");
  const [question, setQuestion] = React.useState("");
  const [answer, setAnswer] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [fileId, setFileId] = React.useState("");

  const handleImageChange = (e) => {
    setImageFile(e.target.files[0]);
    setUploadStatus("");
    setError("");
    setFileId("");
    setAnswer("");
  };

  const handleImageUpload = async (e) => {
    e.preventDefault();
    if (!imageFile) return;
    setUploadStatus("Uploading...");
    setError("");
    setAnswer("");
    try {
      const formData = new FormData();
      formData.append("file", imageFile);
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || `Error: ${response.status}`);
        setUploadStatus("");
      } else {
        setUploadStatus(`Success! Image '${data.file_id}' uploaded.`);
        setFileId(data.file_id);
      }
    } catch (err) {
      setError("Network error: " + err.message);
      setUploadStatus("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setAnswer("");
    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_id: fileId, question }),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || `Error: ${response.status}`);
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

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", padding: 24, fontFamily: 'Inter, Arial, sans-serif' }}>
      <h1 style={{ marginBottom: 24 }}>RAG Vision Demo</h1>

      {/* Image Upload Section */}
      <form onSubmit={handleImageUpload} style={{ marginBottom: 24 }}>
        <label htmlFor="image-upload">Upload an image:</label>
        <input
          id="image-upload"
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          style={{ marginLeft: 8 }}
        />
        <button type="submit" disabled={!imageFile} style={{ marginLeft: 8 }}>
          Upload
        </button>
        {uploadStatus && <span style={{ marginLeft: 12, color: 'green' }}>{uploadStatus}</span>}
        {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      </form>

      {/* Question Section */}
      <form onSubmit={handleSubmit}>
        <label htmlFor="question">Ask a question about the image:</label>
        <input
          id="question"
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "100%", margin: "12px 0", padding: 8 }}
          required
          disabled={!fileId}
        />
        <button type="submit" disabled={loading || !question.trim() || !fileId} style={{ marginLeft: 8 }}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
      {answer && (
        <div style={{ marginTop: 24, background: "#f4f4f4", padding: 16, borderRadius: 6 }}>
          <strong>Answer:</strong>
          <div>{answer}</div>
        </div>
      )}
      {error && (
        <div style={{ color: "red", marginTop: 16 }}>{error}</div>
      )}
    </div>
  );
}

export default App;
