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
    return <p>Loading recommendations...</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Recommendations</h1>

      {/* Info */}
      <div className="mb-6 space-y-2">
        <p>Emotion: {data.current_emotion}</p>
        <p>Mood: {data.latest_mood}</p>
        <p>Risk: {data.risk_level}</p>
      </div>

      {/* Recommendation cards */}
      <div className="grid gap-4">
        {data.recommendations.map((rec, index) => (
          <div
            key={index}
            className="bg-white/10 p-4 rounded-xl border border-white/10"
          >
            {rec}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recommendations;