import { useEffect, useState } from "react";
import API from "../api/api";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

function Insights() {
  const [data, setData] = useState([]);
  const [trend, setTrend] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await API.get("/analytics/timeline/1");
      setData(res.data.timeline || []);
      setTrend(res.data.trend_analysis || {});
    } catch (err) {
      console.error(err);
    }
  };

  const moodMap = {
    Happy: 4,
    Normal: 3,
    Low: 2,
    Overwhelmed: 1,
    Unknown: 0
  };

  const chartData = {
    labels: data.map((d) => d.date),
    datasets: [
      {
        label: "Mood Level",
        data: data.map((d) => moodMap[d.mood]),
        borderWidth: 3,
        tension: 0.4,
        pointRadius: 5,
        pointHoverRadius: 7
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#cbd5e1"
        }
      }
    },
    scales: {
      x: {
        ticks: { color: "#94a3b8" },
        grid: { color: "rgba(255,255,255,0.08)" }
      },
      y: {
        min: 0,
        max: 4,
        ticks: {
          color: "#94a3b8",
          stepSize: 1
        },
        grid: { color: "rgba(255,255,255,0.08)" }
      }
    }
  };

  return (
    <div className="insights-page">
      <div className="insights-header">
        <h1>Emotional Insights</h1>
        <p>Track your mood patterns, emotional signals, and wellness direction over time.</p>
      </div>

      <div className="insights-summary">
        <div className="insights-summary-card">
          <span>Overall Trend</span>
          <strong>{trend.overall_trend || "Unknown"}</strong>
        </div>

        <div className="insights-summary-card">
          <span>Mood Trend</span>
          <strong>{trend.mood_trend || "Unknown"}</strong>
        </div>

        <div className="insights-summary-card">
          <span>Dominant Emotion</span>
          <strong>{trend.dominant_emotion || "Unknown"}</strong>
        </div>
      </div>

      <div className="insights-chart-card">
        <div className="chart-card-header">
          <div>
            <h2>Mood Timeline</h2>
            <p>Happy = 4, Normal = 3, Low = 2, Overwhelmed = 1</p>
          </div>
        </div>

        {data.length > 0 ? (
          <Line data={chartData} options={chartOptions} />
        ) : (
          <p className="empty-insight">No timeline data available yet.</p>
        )}
      </div>

      <div className="insights-detail-grid">
        <div className="insights-detail-card">
          <h3>Risk Trend</h3>
          <p>{trend.risk_trend || "Unknown"}</p>
        </div>

        <div className="insights-detail-card">
          <h3>Negative Emotion Count</h3>
          <p>{trend.negative_emotion_count ?? 0}</p>
        </div>
      </div>

      <div className="insight-message-card">
        <h3>AI Insight</h3>
        <p>{trend.insight || "Start using chat and mood check-ins to generate insights."}</p>
      </div>
    </div>
  );
}

export default Insights;