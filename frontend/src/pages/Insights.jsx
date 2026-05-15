import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import API from "../api/api";
import { Line } from "react-chartjs-2";

import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

import {
  Activity,
  Brain,
  HeartPulse,
  ShieldAlert,
  TrendingUp,
  Waves,
  Sparkles,
} from "lucide-react";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

const fadeUp = {
  hidden: {
    opacity: 0,
    y: 28,
    filter: "blur(10px)",
  },

  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",

    transition: {
      duration: 0.75,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

function Insights() {
  const [data, setData] = useState([]);
  const [trend, setTrend] = useState({});
  const [emotionalInsights, setEmotionalInsights] = useState({});

  useEffect(() => {
    fetchData();
    fetchEmotionalInsights();
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

  const fetchEmotionalInsights = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await API.get("/emotional-insights" , {
         headers: {
          Authorization: `Bearer ${token}`,
         },
      });
      console.log("Emotional Insights:", res.data);

      setEmotionalInsights(res.data || {});
    } catch (err) {
      console.error(err);
    }
  };

  const moodMap = {
    Happy: 4,
    Normal: 3,
    Low: 2,
    Overwhelmed: 1,
    Unknown: 0,
  };

  const chartData = {
    labels: data.map((d) => d.date),

    datasets: [
      {
        label: "Mood Level",

        data: data.map((d) => moodMap[d.mood] ?? 0),

        borderWidth: 3,
        tension: 0.42,
        pointRadius: 4,
        pointHoverRadius: 7,

        borderColor: "rgba(255, 214, 165, 0.95)",

        pointBackgroundColor: "#fff7ed",

        pointBorderColor: "rgba(255, 196, 122, 0.9)",

        pointBorderWidth: 2,

        fill: false,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,

    plugins: {
      legend: {
        labels: {
          color: "rgba(255, 237, 213, 0.68)",

          font: {
            family: "Geist",
            size: 12,
          },
        },
      },

      tooltip: {
        backgroundColor: "rgba(5, 5, 5, 0.88)",

        titleColor: "#fff7ed",

        bodyColor: "rgba(255, 237, 213, 0.72)",

        borderColor: "rgba(255, 214, 165, 0.16)",

        borderWidth: 1,

        padding: 12,
      },
    },

    scales: {
      x: {
        ticks: {
          color: "rgba(255, 237, 213, 0.48)",

          font: {
            family: "Geist",
            size: 11,
          },
        },

        grid: {
          color: "rgba(255,255,255,0.055)",
        },
      },

      y: {
        min: 0,
        max: 4,

        ticks: {
          color: "rgba(255, 237, 213, 0.48)",

          stepSize: 1,

          callback: (value) => {
            const labels = {
              1: "Overwhelmed",
              2: "Low",
              3: "Normal",
              4: "Happy",
            };

            return labels[value] || "";
          },
        },

        grid: {
          color: "rgba(255,255,255,0.055)",
        },
      },
    },
  };

  return (
    <div className="insights-page synth-insights-page">

      <motion.section
        className="synth-insights-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>Emotional intelligence</p>

        <h1>
          Patterns, not
          <span> pressure.</span>
        </h1>

        <small>
          SynthMind brings together your mood signals, emotional trends,
          and reflection patterns so you can understand yourself with more clarity.
        </small>
      </motion.section>

      <motion.section
        className="synth-insights-grid"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >

        <div className="synth-insight-stat">
          <TrendingUp size={20} />

          <span>Overall trend</span>

          <strong>
            {emotionalInsights.trend || trend.overall_trend || "Unknown"}
          </strong>
        </div>

        <div className="synth-insight-stat">
          <Waves size={20} />

          <span>Dominant emotion</span>

          <strong>
            {emotionalInsights.dominantEmotion || "Unknown"}
          </strong>
        </div>

        <div className="synth-insight-stat">
          <Brain size={20} />

          <span>Total chats</span>

          <strong>
            {emotionalInsights.totalChats ?? 0}
          </strong>
        </div>

        <div className="synth-insight-stat">
          <HeartPulse size={20} />

          <span>Total journals</span>

          <strong>
            {emotionalInsights.totalJournals ?? 0}
          </strong>
        </div>

      </motion.section>

      <motion.section
        className="synth-chart-card"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >

        <div className="synth-chart-header">

          <div>
            <p>Mood timeline</p>

            <h2>Your emotional wave</h2>

            <span>
              Happy = 4 · Normal = 3 · Low = 2 · Overwhelmed = 1
            </span>
          </div>

          <Activity size={22} />
        </div>

        <div className="synth-chart-area">

          {data.length > 0 ? (
            <Line data={chartData} options={chartOptions} />
          ) : (
            <div className="synth-empty-chart">

              <Activity size={24} />

              <h3>No timeline data yet</h3>

              <p>
                Start using mood check-ins and journal reflections
                to generate your emotional timeline.
              </p>

            </div>
          )}

        </div>
      </motion.section>

      <motion.section
        className="synth-detail-grid"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >

        <div className="synth-detail-card">
          <ShieldAlert size={20} />

          <span>Risk trend</span>

          <strong>
            {trend.risk_trend || "Unknown"}
          </strong>
        </div>

        <div className="synth-detail-card">
          <HeartPulse size={20} />

          <span>Negative emotion count</span>

          <strong>
            {trend.negative_emotion_count ?? 0}
          </strong>
        </div>

      </motion.section>

      <motion.section
        className="synth-ai-insight-message"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >

        <p>AI observation</p>

        <h2>What SynthMind noticed</h2>

        <span>
          {trend.insight ||
            "Start using chat, journal, and mood check-ins to generate deeper emotional insights."}
        </span>

      </motion.section>

      <motion.section
  className="synth-journey-section"
  variants={fadeUp}
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true, amount: 0.2 }}
>

  <div className="synth-chart-header">

    <div>
      <p>Emotional journey</p>

      <h2>Your recent emotional flow</h2>
    </div>

    <Waves size={20} />
  </div>

  <div className="synth-journey-grid">

    {(emotionalInsights.emotionJourney || []).map((item, index) => (
      <div
        className="synth-journey-card"
        key={index}
      >

        <small>{item.date}</small>

        <h3  className={`emotion-${item.dominantEmotion}`}
        >{item.dominantEmotion}</h3>

        <p>{item.summary}</p>

      </div>
    ))}

  </div>

</motion.section>

      <motion.section
        className="synth-insights-cards"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >

        <div className="synth-chart-header">

          <div>
            <p>Behavioral reflections</p>
            <h2>Emotional insights</h2>
          </div>

          <Sparkles size={20} />
        </div>

        <div className="synth-insights-card-grid">

          {(emotionalInsights.insights || []).map((item, index) => (
            <div
              className="synth-emotional-card"
              key={index}
            >
              <small>{item.title}</small>

              <p>{item.message}</p>
            </div>
          ))}

        </div>

      </motion.section>

    </div>
  );
}

export default Insights;