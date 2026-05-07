import { useEffect, useState } from "react";
import { Brain, TrendingUp, HeartPulse, NotebookText } from "lucide-react";

function EmotionalInsights() {
  const token = localStorage.getItem("token");
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/emotional-insights", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const result = await res.json();

      if (res.ok) {
        setData(result);
      }
    } catch (err) {
      console.error("Insights error:", err);
    }
  };

  if (!data) return null;

  return (
    <section className="synth-insights-section">
      <div className="synth-insights-header">
        <div>
          <p>Emotional intelligence</p>
          <h2>What SynthMind noticed</h2>
        </div>

        <Brain size={26} />
      </div>

      <div className="synth-insights-summary">
        <div>
          <TrendingUp size={18} />
          <span>Trend</span>
          <strong>{data.trend}</strong>
        </div>

        <div>
          <HeartPulse size={18} />
          <span>Dominant emotion</span>
          <strong>{data.dominantEmotion}</strong>
        </div>

        <div>
          <NotebookText size={18} />
          <span>Journal entries</span>
          <strong>{data.totalJournals}</strong>
        </div>
      </div>

      <div className="synth-insights-list">
        {data.insights.map((item, index) => (
          <article key={index} className="synth-insight-card">
            <span>{item.title}</span>
            <p>{item.message}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

export default EmotionalInsights;