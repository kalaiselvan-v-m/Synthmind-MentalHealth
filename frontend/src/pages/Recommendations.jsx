import { useEffect, useState } from "react";
import API from "../api/api";

function Recommendations() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      const res = await API.get("/recommendations/1");
      setData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (!data) {
    return <div className="rec-page">Loading recommendations...</div>;
  }

  return (
    <div className="rec-page">
      <div className="rec-header">
        <h1>Personalized Recommendations</h1>
        <p>Small actions selected from your mood, emotion, and risk signals.</p>
      </div>

      <div className="rec-summary">
        <div className="rec-summary-card">
          <span>Current Emotion</span>
          <strong>{data.current_emotion}</strong>
        </div>

        <div className="rec-summary-card">
          <span>Latest Mood</span>
          <strong>{data.latest_mood}</strong>
        </div>

        <div className={`rec-summary-card risk-${data.risk_level.toLowerCase()}`}>
          <span>Risk Level</span>
          <strong>{data.risk_level}</strong>
        </div>
      </div>

      <div className="rec-list">
        {data.recommendations.map((rec, index) => (
          <div key={index} className="rec-premium-card">
            <div className="rec-icon">{index + 1}</div>
            <div>
              <h3>Suggested Action</h3>
              <p>{rec}</p>
            </div>
          </div>
        ))}
      </div>

      <p className="rec-note">{data.note}</p>
    </div>
  );
}

export default Recommendations;