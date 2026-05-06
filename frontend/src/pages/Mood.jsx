import { useEffect, useState } from "react";
import API from "../api/api";

function Mood() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMoodData();
  }, []);

  const fetchMoodData = async () => {
    try {
      const res = await API.get("/mood/calendar/1");
      setData(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load mood insights");
    }
  };

  if (error) {
    return <div className="mood-page"><p>{error}</p></div>;
  }

  if (!data) {
    return <div className="mood-page"><p>Loading mood insights...</p></div>;
  }

  return (
    <div className="mood-page">

      {/* HEADER */}
      <div className="mood-header">
        <h1>Mood Insights</h1>
        <p>Understand your emotional patterns</p>
      </div>

      {/* SUMMARY */}
      <div className="mood-summary">
        <div>
          <span>Dominant Mood</span>
          <strong>{data.dominantMood}</strong>
        </div>

        <div>
          <span>Positive Days</span>
          <strong>{data.positiveDays}</strong>
        </div>

        <div>
          <span>Low Days</span>
          <strong>{data.negativeDays}</strong>
        </div>
      </div>

      {/* CALENDAR */}
      <div className="mood-calendar">
        {data.days.map((day, index) => (
          <div
            key={index}
            className="calendar-cell"
            title={`${day.date} - ${day.mood}`}
          >
            {day.emoji}
          </div>
        ))}
      </div>

      {/* INSIGHT */}
      <div className="mood-insight-box">
        <h3>Insight</h3>
        <p>{data.insight}</p>
      </div>

    </div>
  );
}

export default Mood;