import { useState } from "react";
import API from "../api/api";

const moods = [
  { label: "Happy", emoji: "😊" },
  { label: "Normal", emoji: "😐" },
  { label: "Low", emoji: "😔" },
  { label: "Overwhelmed", emoji: "😵" }
];

function Mood() {
  const [selected, setSelected] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const saveMood = async () => {
    if (!selected || loading) return;

    setLoading(true);
    setMessage("");

    try {
      await API.post("/mood/checkin", {
        user_id: 1,
        mood: selected,
        note: ""
      });

      setMessage("Saved successfully ✨");
      setSelected("");
    } catch (err) {
      console.error(err);
      setMessage("Something went wrong ❌");
    }

    setLoading(false);
  };

  return (
    <div className="mood-page">

      {/* Header */}
      <div className="mood-header">
        <h1>How are you feeling today?</h1>
        <p>Take a moment to check in with yourself</p>
      </div>

      {/* Mood Cards */}
      <div className="mood-grid">
        {moods.map((m) => (
          <div
            key={m.label}
            className={`mood-card ${
              selected === m.label ? "selected" : ""
            }`}
            onClick={() => setSelected(m.label)}
          >
            <div className="mood-emoji">{m.emoji}</div>
            <div className="mood-label">{m.label}</div>
          </div>
        ))}
      </div>

      {/* Save Button */}
      <button
        className="mood-save-btn"
        onClick={saveMood}
        disabled={!selected || loading}
      >
        {loading ? "Saving..." : "Save Mood"}
      </button>

      {/* Feedback */}
      {message && <p className="mood-msg">{message}</p>}
    </div>
  );
}

export default Mood;