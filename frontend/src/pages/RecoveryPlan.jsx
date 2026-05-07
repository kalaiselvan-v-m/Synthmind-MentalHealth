import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import API from "../api/api";
import {
  Brain,
  HeartHandshake,
  Moon,
  NotebookPen,
  ShieldCheck,
  Sparkles,
  Wind,
  Activity,
  Leaf,
  TrendingUp,
} from "lucide-react";

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

function RecoveryPlan() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchPlan();
  }, []);

  const fetchPlan = async () => {
    try {
      const res = await API.get("/recovery-plan/1");
      setData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (!data) {
    return <div className="recovery-page synth-recovery-page">Loading plan...</div>;
  }

  const tasks = [
    {
      title: "Breathing",
      value: data.breathing_exercise,
      icon: <Wind size={20} />,
    },
    {
      title: "CBT Task",
      value: data.cbt_task,
      icon: <Brain size={20} />,
    },
    {
      title: "Journaling",
      value: data.journaling_task,
      icon: <NotebookPen size={20} />,
    },
    {
      title: "Sleep Tip",
      value: data.sleep_tip,
      icon: <Moon size={20} />,
    },
    {
      title: "Habit Goal",
      value: data.habit_goal,
      icon: <Leaf size={20} />,
    },
  ];

  return (
    <div className="recovery-page synth-recovery-page">
      <motion.section
        className="synth-recovery-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>Recovery plan</p>

        <h1>
          A calm roadmap
          <span> for today.</span>
        </h1>

        <small>
          Your care plan is shaped from mood, emotion, and risk signals so your
          next steps feel gentle, practical, and personal.
        </small>
      </motion.section>

      <motion.section
        className="synth-recovery-summary"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-recovery-stat">
          <ShieldCheck size={20} />
          <span>Risk level</span>
          <strong>{data.risk_level}</strong>
        </div>

        <div className="synth-recovery-stat">
          <TrendingUp size={20} />
          <span>Overall trend</span>
          <strong>{data.overall_trend}</strong>
        </div>

        <div className="synth-recovery-stat">
          <Sparkles size={20} />
          <span>Dominant emotion</span>
          <strong>{data.dominant_emotion}</strong>
        </div>
      </motion.section>

      <motion.section
        className="synth-recovery-section"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <div className="synth-recovery-section-title">
          <p>Daily routine</p>
          <h2>Follow these tiny steps.</h2>
        </div>

        <div className="synth-routine-list">
          {data.daily_routine.map((item, index) => (
            <motion.div
              key={index}
              className="synth-routine-item"
              initial={{ opacity: 0, y: 20, filter: "blur(8px)" }}
              whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              viewport={{ once: true }}
              transition={{ duration: 0.55, delay: index * 0.05 }}
              whileHover={{ y: -4 }}
            >
              <div>{index + 1}</div>
              <p>{item}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>

      <motion.section
        className="synth-recovery-section"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <div className="synth-recovery-section-title">
          <p>Care tasks</p>
          <h2>Your support toolkit.</h2>
        </div>

        <div className="synth-care-grid">
          {tasks.map((task, index) => (
            <motion.article
              key={task.title}
              className="synth-care-card"
              initial={{ opacity: 0, y: 22, filter: "blur(8px)" }}
              whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.05 }}
              whileHover={{ y: -5 }}
            >
              <div className="synth-care-icon">{task.icon}</div>
              <span>{task.title}</span>
              <p>{task.value}</p>
            </motion.article>
          ))}
        </div>
      </motion.section>

      <motion.section
        className="synth-recovery-section"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <div className="synth-recovery-section-title">
          <p>Suggested activities</p>
          <h2>Small things that may help.</h2>
        </div>

        <div className="synth-activity-list">
          {data.recommended_activities.map((rec, index) => (
            <motion.div
              key={index}
              className="synth-activity-card"
              initial={{ opacity: 0, y: 18, filter: "blur(8px)" }}
              whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              viewport={{ once: true }}
              transition={{ duration: 0.55, delay: index * 0.05 }}
            >
              <Activity size={17} />
              <span>{rec}</span>
            </motion.div>
          ))}
        </div>
      </motion.section>

      <motion.section
        className="synth-therapy-card"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <HeartHandshake size={22} />

        <div>
          <p>Therapy suggestion</p>
          <h2>Professional support note</h2>
          <span>{data.therapy_suggestion}</span>
        </div>
      </motion.section>

      {data.note && <p className="synth-recovery-note">{data.note}</p>}
    </div>
  );
}

export default RecoveryPlan;