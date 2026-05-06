import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
} from "recharts";

function WeeklyReport() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchReport();
  }, []);

  const fetchReport = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/weekly-report", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      if (!res.ok) {
        setError("Unable to load weekly report");
        return;
      }

      setReport(data);
    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }
  };

  if (error) {
    return <div className="weekly-page"><p>{error}</p></div>;
  }

  if (!report) {
    return <div className="weekly-page"><p>Loading weekly report...</p></div>;
  }

  const emotionPieData = Object.entries(report.emotionBreakdown || {}).map(
    ([name, value]) => ({ name, value })
  );

  return (
    <div className="weekly-page">
      <div className="weekly-header">
        <h1>Weekly Mental Report</h1>
        <p>Your emotional activity and patterns from the last 7 days.</p>
      </div>

      <div className="weekly-summary-grid">
        <div className="weekly-card">
          <span>Total Chats</span>
          <strong>{report.totalChats}</strong>
        </div>

        <div className="weekly-card">
          <span>Dominant Emotion</span>
          <strong>{report.dominantEmotion}</strong>
        </div>

        <div className="weekly-card">
          <span>Weekly Trend</span>
          <strong>{report.trend}</strong>
        </div>
      </div>

      <div className="weekly-ai-card">
        <h2>AI Summary</h2>
        <p>{report.summary}</p>
      </div>

      <div className="weekly-chart-grid">
        <div className="weekly-chart-card">
          <h2>Daily Emotion Flow</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={report.dailyEmotionCounts}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis dataKey="date" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Bar dataKey="positive" fill="#22c55e" />
              <Bar dataKey="negative" fill="#ef4444" />
              <Bar dataKey="neutral" fill="#60a5fa" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="weekly-chart-card">
          <h2>Emotion Breakdown</h2>
          {emotionPieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={emotionPieData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={95}
                  label
                >
                  {emotionPieData.map((_, index) => (
                    <Cell
                      key={index}
                      fill={["#7c3aed", "#2563eb", "#22c55e", "#ef4444", "#eab308"][index % 5]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="weekly-empty">No emotion data yet.</p>
          )}
        </div>
      </div>

      <div className="weekly-recommend-card">
        <h2>Personal Suggestions</h2>
        <div className="weekly-recommend-list">
          {report.recommendations.map((item, index) => (
            <div key={index} className="weekly-recommend-item">
              <span>{index + 1}</span>
              <p>{item}</p>
            </div>
          ))}
        </div>
      </div>

      <p className="weekly-note">
        This report supports self-reflection only. It is not a medical diagnosis.
      </p>
    </div>
  );
}

export default WeeklyReport;