import { useEffect, useState } from "react";
import { motion } from "framer-motion";
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
import {
  MessageCircle,
  Sparkles,
  TrendingUp,
  Brain,
  Wand2,
} from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 28, filter: "blur(10px)" },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: { duration: 0.75, ease: [0.16, 1, 0.3, 1] },
  },
};

const chartColors = ["#fff7ed", "#fbbf24", "#fb923c", "#c084fc", "#86efac"];

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
        headers: { Authorization: `Bearer ${token}` },
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
    return <div className="weekly-page synth-weekly-page"><p>{error}</p></div>;
  }

  if (!report) {
    return (
      <div className="weekly-page synth-weekly-page">
        <p>Loading weekly report...</p>
      </div>
    );
  }

  const emotionPieData = Object.entries(report.emotionBreakdown || {}).map(
    ([name, value]) => ({ name, value })
  );

  return (
    <div className="weekly-page synth-weekly-page">
      <motion.section
        className="synth-weekly-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>Weekly reflection</p>

        <h1>
          Your emotional story
          <span> of the week.</span>
        </h1>

        <small>
          A calm summary of your chats, emotional flow, dominant patterns, and
          suggested next steps from SynthMind.
        </small>
      </motion.section>

      <motion.section
        className="synth-weekly-summary"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-weekly-stat">
          <MessageCircle size={20} />
          <span>Total chats</span>
          <strong>{report.totalChats}</strong>
        </div>

        <div className="synth-weekly-stat">
          <Brain size={20} />
          <span>Dominant emotion</span>
          <strong>{report.dominantEmotion}</strong>
        </div>

        <div className="synth-weekly-stat">
          <TrendingUp size={20} />
          <span>Weekly trend</span>
          <strong>{report.trend}</strong>
        </div>
      </motion.section>

      <motion.section
        className="synth-weekly-ai-card"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <Sparkles size={22} />
        <div>
          <p>AI summary</p>
          <h2>What SynthMind noticed</h2>
          <span>{report.summary}</span>
        </div>
      </motion.section>

      <motion.section
        className="synth-weekly-chart-grid"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.15 }}
      >
        <div className="synth-weekly-chart-card">
          <div className="synth-weekly-chart-header">
            <p>Daily emotion flow</p>
            <h2>Positive, neutral, and difficult signals</h2>
          </div>

          <div className="synth-weekly-chart-area">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={report.dailyEmotionCounts}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="date" stroke="rgba(255,237,213,0.48)" />
                <YAxis stroke="rgba(255,237,213,0.48)" />
                <Tooltip
                  contentStyle={{
                    background: "rgba(5,5,5,0.88)",
                    border: "1px solid rgba(255,214,165,0.16)",
                    borderRadius: "14px",
                    color: "#fff7ed",
                  }}
                />
                <Bar dataKey="positive" fill="#86efac" radius={[8, 8, 0, 0]} />
                <Bar dataKey="negative" fill="#fb7185" radius={[8, 8, 0, 0]} />
                <Bar dataKey="neutral" fill="#fbbf24" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="synth-weekly-chart-card">
          <div className="synth-weekly-chart-header">
            <p>Emotion breakdown</p>
            <h2>What showed up most</h2>
          </div>

          <div className="synth-weekly-chart-area">
            {emotionPieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={emotionPieData}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={92}
                    label
                  >
                    {emotionPieData.map((_, index) => (
                      <Cell key={index} fill={chartColors[index % chartColors.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: "rgba(5,5,5,0.88)",
                      border: "1px solid rgba(255,214,165,0.16)",
                      borderRadius: "14px",
                      color: "#fff7ed",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="weekly-empty">No emotion data yet.</p>
            )}
          </div>
        </div>
      </motion.section>

      <motion.section
        className="synth-weekly-recommend-card"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <div className="synth-weekly-chart-header">
          <p>Personal suggestions</p>
          <h2>Next week, gently.</h2>
        </div>

        <div className="synth-weekly-recommend-list">
          {report.recommendations.map((item, index) => (
            <motion.div
              key={index}
              className="synth-weekly-recommend-item"
              initial={{ opacity: 0, y: 18, filter: "blur(8px)" }}
              whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              viewport={{ once: true }}
              transition={{ duration: 0.55, delay: index * 0.05 }}
            >
              <span><Wand2 size={15} /></span>
              <p>{item}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>

      <p className="synth-weekly-note">
        This report supports self-reflection only. It is not a medical diagnosis.
      </p>
    </div>
  );
}

export default WeeklyReport;