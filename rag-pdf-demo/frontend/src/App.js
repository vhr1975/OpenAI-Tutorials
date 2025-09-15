import React, { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const data = await response.json();
      setAnswer(data.answer);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", padding: 24 }}>
      <h1>OpenAI RAG PDF Demo</h1>
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
