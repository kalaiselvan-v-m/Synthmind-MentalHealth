import { useEffect, useState } from "react";
import API from "../api/api";

import {
  Laugh,
  Meh,
  Frown,
  CloudLightning,
} from "lucide-react";

const moods = [
  {
    label: "Happy",
    icon: <Laugh size={34} strokeWidth={1.8} />,
  },

  {
    label: "Normal",
    icon: <Meh size={34} strokeWidth={1.8} />,
  },

  {
    label: "Low",
    icon: <Frown size={34} strokeWidth={1.8} />,
  },

  {
    label: "Overwhelmed",
    icon: <CloudLightning size={34} strokeWidth={1.8} />,
  },
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
        <div className="mood-popup-header">
          <p>Daily emotional check-in</p>

          <h2>How are you feeling today?</h2>

          <span>
            A quick check-in helps SynthMind gently understand your emotional
            rhythm and support you better.
          </span>
        </div>

        <div className="mood-popup-options">
          {moods.map((mood) => (
            <button
              key={mood.label}
              className={selected === mood.label ? "selected" : ""}
              onClick={() => setSelected(mood.label)}
            >
              <div className="mood-popup-icon">
                {mood.icon}
              </div>

              <small>{mood.label}</small>
            </button>
          ))}
        </div>

        <div className="mood-popup-actions">
          <button
            className="mood-popup-skip"
            onClick={skipToday}
          >
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