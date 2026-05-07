import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  CheckCircle2,
  Flame,
  Sparkles,
  TrendingUp,
  Leaf,
  Bell,
} from "lucide-react";
import { sendNotification } from "../utils/reminder";

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

function HabitTracker() {
  const token = localStorage.getItem("token");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [celebration, setCelebration] = useState("");

  useEffect(() => {
    fetchProgress();
  }, []);

  const fetchProgress = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/habit-tracking", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const result = await res.json();

      if (!res.ok) {
        setError("Unable to load habit tracker");
        return;
      }

      setData(result);

      if (result.bestStreak >= 2 && result.totalCompletedToday === 0) {
        sendNotification(
          "🔥 Streak Alert",
          `You have a ${result.bestStreak}-day streak. Complete one habit today to keep it alive.`
        );
      }
    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }
  };

  const markDone = async (habit) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/habit-tracking/complete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          habit_title: habit.title,
          habit_category: habit.category,
        }),
      });

      const result = await res.json();

      if (res.ok) {
        setCelebration(result.message);

        sendNotification(
          "Habit Completed 🎉",
          `${habit.title} is done for today. Keep your streak going!`
        );

        setTimeout(() => setCelebration(""), 2500);
        fetchProgress();
      }
    } catch (err) {
      console.error(err);
      setCelebration("Could not mark habit as done");
      setTimeout(() => setCelebration(""), 2500);
    }
  };

  if (error) {
    return (
      <div className="habit-tracker-page synth-habit-page">
        <p>{error}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="habit-tracker-page synth-habit-page">
        <p>Loading habit tracker...</p>
      </div>
    );
  }

  return (
    <div className="habit-tracker-page synth-habit-page">
      {celebration && (
        <motion.div
          className="synth-streak-toast"
          initial={{ opacity: 0, y: -18, filter: "blur(8px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          exit={{ opacity: 0, y: -18, filter: "blur(8px)" }}
        >
          <Sparkles size={18} />
          <span>{celebration}</span>
        </motion.div>
      )}

      <motion.section
        className="synth-habit-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>Habit rhythm</p>

        <h1>
          Small rituals,
          <span> softly repeated.</span>
        </h1>

        <small>
          Track tiny wellness habits, protect your streaks, and build emotional
          consistency without pressure.
        </small>
      </motion.section>

      <motion.section
        className="synth-habit-summary"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-habit-stat">
          <CheckCircle2 size={20} />
          <span>Completed today</span>
          <strong>{data.totalCompletedToday}</strong>
        </div>

        <div className="synth-habit-stat">
          <Flame size={20} />
          <span>Best streak</span>
          <strong>{data.bestStreak} days</strong>
        </div>

        <div className="synth-habit-stat">
          <TrendingUp size={20} />
          <span>Weekly trend</span>
          <strong>{data.trend}</strong>
        </div>
      </motion.section>

      <motion.section
        className="synth-habit-list-header"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <p>Today’s care actions</p>
        <h2>Choose one gentle step.</h2>
      </motion.section>

      <div className="synth-habit-list">
        {data.habits.map((habit, index) => (
          <motion.article
            key={index}
            className={`synth-habit-card ${
              habit.completedToday ? "done" : ""
            }`}
            initial={{
              opacity: 0,
              y: 26,
              filter: "blur(10px)",
            }}
            whileInView={{
              opacity: 1,
              y: 0,
              filter: "blur(0px)",
            }}
            viewport={{ once: true, amount: 0.12 }}
            transition={{
              duration: 0.65,
              delay: index * 0.05,
              ease: [0.16, 1, 0.3, 1],
            }}
            whileHover={{
              y: -5,
              transition: {
                type: "spring",
                stiffness: 220,
                damping: 18,
              },
            }}
          >
            <div className="synth-habit-card-top">
              <div>
                <span className="synth-habit-category">{habit.category}</span>
                <h2>{habit.title}</h2>
              </div>

              <div className="synth-habit-badge">
                {habit.completedToday ? (
                  <>
                    <CheckCircle2 size={15} />
                    <span>Done</span>
                  </>
                ) : (
                  <>
                    <Bell size={15} />
                    <span>{habit.reward?.badge || "Not Started"}</span>
                  </>
                )}
              </div>
            </div>

            <div className="synth-habit-reward">
              <div className="synth-habit-reward-top">
                <div>
                  <span>{habit.reward?.level || "Not started"}</span>
                  <strong>{habit.reward?.progress || 0}% progress</strong>
                </div>

                <p>
                  <Flame size={15} />
                  {habit.streak} day streak
                </p>
              </div>

              <div className="synth-habit-progress">
                <div
                  style={{ width: `${habit.reward?.progress || 0}%` }}
                ></div>
              </div>

              <small>{habit.reward?.message}</small>
            </div>

            <p className="synth-habit-reason">{habit.reason}</p>

            <div className="synth-habit-steps">
              {habit.steps.map((step, stepIndex) => (
                <div key={stepIndex} className="synth-habit-step">
                  <span>{stepIndex + 1}</span>
                  <p>{step}</p>
                </div>
              ))}
            </div>

            <button
              className="synth-habit-done-btn"
              disabled={habit.completedToday}
              onClick={() => markDone(habit)}
            >
              {habit.completedToday ? (
                <>
                  <CheckCircle2 size={17} />
                  Completed today
                </>
              ) : (
                <>
                  <Leaf size={17} />
                  Mark as done
                </>
              )}
            </button>
          </motion.article>
        ))}
      </div>
    </div>
  );
}

export default HabitTracker;