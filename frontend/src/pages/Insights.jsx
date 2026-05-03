import { useEffect, useState } from "react";
import API from "../api/api";
import {
  Line
} from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function Insights() {
  const [data, setData] = useState([]);
  const [trend, setTrend] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await API.get("/analytics/timeline/1");
      setData(res.data.timeline);
      setTrend(res.data.trend_analysis);
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
        borderWidth: 2
      }
    ]
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Insights</h1>

      {/* Chart */}
      <div className="bg-white/10 p-4 rounded-xl">
        <Line data={chartData} />
      </div>

      {/* Trend Info */}
      <div className="mt-6 space-y-2">
        <p>Overall Trend: {trend.overall_trend}</p>
        <p>Mood Trend: {trend.mood_trend}</p>
        <p>Risk Trend: {trend.risk_trend}</p>
        <p>Dominant Emotion: {trend.dominant_emotion}</p>
        <p className="mt-3 text-green-400">{trend.insight}</p>
      </div>
    </div>
  );
}

export default Insights;