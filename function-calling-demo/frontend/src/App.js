// =============================================================
// Function Calling Demo Frontend (App.js)
// -------------------------------------------------------------
// This React component provides a simple chat UI for beginners.
// It sends user messages to the FastAPI backend and displays responses.
// Key Concepts:
// - How to send POST requests to the backend
// - How to display backend responses
// - How to handle loading and errors
// =============================================================

import React, { useState } from 'react';
import './App.css';

function App() {
  // State for user message and backend response
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  // Send message to backend
  const sendMessage = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, user_id: 'user123' })
      });
      const data = await res.json();
      setResponse(data.response || JSON.stringify(data.function_call));
    } catch (err) {
      setResponse('Error: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 500, margin: 'auto', padding: 20 }}>
      <h2>Function Calling Demo</h2>
      <form onSubmit={sendMessage} style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Ask something..."
          style={{ flex: 1 }}
        />
        <button type="submit" disabled={loading || !message.trim()}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
      <div style={{ marginTop: 20 }}>
        <strong>Response:</strong>
        <pre style={{ background: '#f4f4f4', padding: 10 }}>{response}</pre>
      </div>
    </div>
  );
}

export default App;
