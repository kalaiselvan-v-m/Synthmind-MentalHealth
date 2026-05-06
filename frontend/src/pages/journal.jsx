import { useEffect, useState } from "react";

function Journal() {
  const token = localStorage.getItem("token");

  const [content, setContent] = useState("");
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    const res = await fetch("http://127.0.0.1:8000/journal", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();

    if (!res.ok) {
    console.error(data);
    setEntries([]);
    return;
    }

    setEntries(Array.isArray(data) ? data : []);
  };

  const submitEntry = async () => {
    if (!content.trim()) return;

    setLoading(true);

    await fetch("http://127.0.0.1:8000/journal", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content }),
    });

    setContent("");
    fetchEntries();
    setLoading(false);
  };

  return (
    <div className="journal-page">
      <h1>AI Journal</h1>

      <div className="journal-input">
        <textarea
          placeholder="Write how you feel..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />

        <button onClick={submitEntry} disabled={loading}>
          {loading ? "Saving..." : "Save Entry"}
        </button>
      </div>

      <div className="journal-list">
        {entries.map((entry) => (
          <div key={entry.id} className="journal-card">
            <p>{entry.content}</p>

            <div className="journal-meta">
              <span>Emotion: {entry.emotion}</span>
              <span>{new Date(entry.created_at).toLocaleString()}</span>
            </div>

            <div className="journal-ai">
              <strong>AI Insight:</strong>
              <p>{entry.ai_summary}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Journal;