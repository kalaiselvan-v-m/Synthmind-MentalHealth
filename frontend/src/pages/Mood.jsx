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

  const saveMood = async () => {
    if (!selected) return;

    try {
      await API.post("/mood/checkin", {
        user_id: 1,
        mood: selected,
        note: ""
      });

      setMessage("Mood saved successfully ✅");
      setSelected("");
    } catch (err) {
      console.error(err);
      setMessage("Error saving mood ❌");
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Daily Mood Check-in</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {moods.map((m) => (
          <button
            key={m.label}
            onClick={() => setSelected(m.label)}
            className={`p-5 rounded-xl text-center border ${
              selected === m.label
                ? "bg-purple-600"
                : "bg-white/10 hover:bg-white/20"
            }`}
          >
            <div className="text-3xl">{m.emoji}</div>
            <div className="mt-2">{m.label}</div>
          </button>
        ))}
      </div>

      <button
        onClick={saveMood}
        className="mt-6 px-6 py-3 bg-green-600 rounded-xl hover:bg-green-700"
      >
        Save Mood
      </button>

      {message && <p className="mt-4 text-sm">{message}</p>}
    </div>
  );
}

export default Mood;