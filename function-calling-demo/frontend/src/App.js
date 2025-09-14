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
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Send message to backend
  const sendMessage = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setError(null);
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, user_id: 'user123' })
      });
      const data = await res.json();
      // If backend returns error field, show it nicely
      if (data.error) {
        setError(data.error);
        setResponse(null);
      } else {
        setError(null);
        setResponse({
          response: data.response,
          function_call: data.function_call
        });
      }
    } catch (err) {
      setError('Network error: ' + err.message);
      setResponse(null);
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
        {error ? (
          <div style={{ color: 'red', background: '#ffeaea', padding: 10, borderRadius: 4 }}>
            <strong>Error:</strong>
            <pre style={{ margin: 0 }}>{typeof error === 'string' ? error : JSON.stringify(error, null, 2)}</pre>
          </div>
        ) : response ? (
          <div style={{ background: '#f4f4f4', padding: 10, borderRadius: 4 }}>
            <strong>Response:</strong>
            <div>{response.response}</div>
            {response.function_call && (
              <div style={{ marginTop: 8 }}>
                <strong>Function Call:</strong>
                <pre style={{ margin: 0 }}>{JSON.stringify(response.function_call, null, 2)}</pre>
              </div>
            )}
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default App;
