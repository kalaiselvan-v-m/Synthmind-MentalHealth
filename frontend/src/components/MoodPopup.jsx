import { useEffect, useState } from "react";
import API from "../api/api";

const moods = [
  { label: "Happy", emoji: "😊" },
  { label: "Normal", emoji: "😐" },
  { label: "Low", emoji: "😔" },
  { label: "Overwhelmed", emoji: "😵" },
];

function MoodPopup() {
  const [show, setShow] = useState(false);
  const [selected, setSelected] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const today = new Date().toDateString();
    const lastMoodDate = localStorage.getItem("lastMoodDate");

    if (lastMoodDate !== today) {
      setShow(true);
    }
  }, []);

  const getUserId = () => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    return user.user_id || user.id || 1;
  };

  const saveMood = async () => {
    if (!selected || loading) return;

    setLoading(true);

    try {
      await API.post("/mood/checkin", {
        user_id: getUserId(),
        mood: selected,
        note: "",
      });

      localStorage.setItem("lastMoodDate", new Date().toDateString());
      setShow(false);
    } catch (err) {
      console.error("Mood save failed:", err);
    }

    setLoading(false);
  };

  const skipToday = () => {
    localStorage.setItem("lastMoodDate", new Date().toDateString());
    setShow(false);
  };

  if (!show) return null;

  return (
    <div className="mood-popup-overlay">
      <div className="mood-popup-card">
        <h2>How are you feeling today?</h2>
        <p>A quick check-in helps SynthMind understand your emotional pattern.</p>

        <div className="mood-popup-options">
          {moods.map((mood) => (
            <button
              key={mood.label}
              className={selected === mood.label ? "selected" : ""}
              onClick={() => setSelected(mood.label)}
            >
              <span>{mood.emoji}</span>
              <small>{mood.label}</small>
            </button>
          ))}
        </div>

        <div className="mood-popup-actions">
          <button className="mood-popup-skip" onClick={skipToday}>
            Skip today
          </button>

          <button
            className="mood-popup-save"
            onClick={saveMood}
            disabled={!selected || loading}
          >
            {loading ? "Saving..." : "Save Mood"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default MoodPopup;