import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { CalendarDays, HeartPulse, Smile, CloudMoon } from "lucide-react";
import API from "../api/api";

const fadeUp = {
  hidden: {
    opacity: 0,
    y: 32,
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
    return <div className="mood-page synth-mood-page"><p>{error}</p></div>;
  }

  if (!data) {
    return <div className="mood-page synth-mood-page"><p>Loading mood insights...</p></div>;
  }

  return (
    <div className="mood-page synth-mood-page">
      <motion.section
        className="synth-mood-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>Mood tracker</p>
        <h1>
          Notice your emotional
          <span> rhythm.</span>
        </h1>
        <small>
          Your mood calendar helps SynthMind understand patterns gently, without
          judging or forcing progress.
        </small>
      </motion.section>

      <motion.section
        className="synth-mood-summary"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-mood-stat">
          <Smile size={20} />
          <span>Dominant mood</span>
          <strong>{data.dominantMood}</strong>
        </div>

        <div className="synth-mood-stat">
          <HeartPulse size={20} />
          <span>Positive days</span>
          <strong>{data.positiveDays}</strong>
        </div>

        <div className="synth-mood-stat">
          <CloudMoon size={20} />
          <span>Low days</span>
          <strong>{data.negativeDays}</strong>
        </div>
      </motion.section>

      <motion.section
        className="synth-mood-calendar-card"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <div className="synth-mood-card-header">
          <div>
            <p>Recent calendar</p>
            <h2>Your emotional trail</h2>
          </div>
          <CalendarDays size={22} />
        </div>

        <div className="synth-mood-calendar">
          {data.days.map((day, index) => (
            <motion.div
              key={index}
              className={`synth-calendar-cell ${day.mood?.toLowerCase() || ""}`}
              title={`${day.date} - ${day.mood}`}
              initial={{ opacity: 0, scale: 0.7 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{
                duration: 0.35,
                delay: index * 0.015,
              }}
            >
              <span>{day.emoji}</span>
              <small>{index + 1}</small>
            </motion.div>
          ))}
        </div>
      </motion.section>

      <motion.section
        className="synth-mood-insight"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <p>Insight</p>
        <h2>What this pattern may mean</h2>
        <span>{data.insight}</span>
      </motion.section>
    </div>
  );
}

export default Mood;