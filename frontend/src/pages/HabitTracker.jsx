import { useEffect, useState } from "react";
import { sendNotification } from "../utils/reminder";

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
      <div className="habit-tracker-page">
        <p>{error}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="habit-tracker-page">
        <p>Loading habit tracker...</p>
      </div>
    );
  }

  return (
    <div className="habit-tracker-page">
      {celebration && <div className="streak-toast">🎉 {celebration}</div>}

      <div className="habit-tracker-header">
        <h1>Habit Tracker</h1>
        <p>Track small wellness habits and build daily streaks.</p>
      </div>

      <div className="habit-tracker-summary">
        <div>
          <span>Completed Today</span>
          <strong>{data.totalCompletedToday}</strong>
        </div>

        <div>
          <span>Best Streak</span>
          <strong>🔥 {data.bestStreak} days</strong>
        </div>

        <div>
          <span>Weekly Trend</span>
          <strong>{data.trend}</strong>
        </div>
      </div>

      <div className="habit-tracker-list">
        {data.habits.map((habit, index) => (
          <div
            key={index}
            className={`habit-track-card ${
              habit.completedToday ? "done" : ""
            }`}
          >
            <div className="habit-track-top">
              <div>
                <span className="habit-category">{habit.category}</span>
                <h2>{habit.title}</h2>
              </div>

              <div className="habit-reward-badge">
                {habit.reward?.badge || "○ Not Started"}
              </div>
            </div>

            <div className="habit-reward-box">
              <div className="habit-reward-info">
                <span>{habit.reward?.level || "Not started"}</span>
                <strong>🔥 {habit.streak} day streak</strong>
              </div>

              <div className="habit-progress-bar">
                <div
                  className="habit-progress-fill"
                  style={{ width: `${habit.reward?.progress || 0}%` }}
                ></div>
              </div>

              <p>{habit.reward?.message}</p>
            </div>

            <p className="habit-reason">{habit.reason}</p>

            <div className="habit-steps">
              {habit.steps.map((step, stepIndex) => (
                <div key={stepIndex} className="habit-step">
                  <span>{stepIndex + 1}</span>
                  <p>{step}</p>
                </div>
              ))}
            </div>

            <button
              className="habit-done-btn"
              disabled={habit.completedToday}
              onClick={() => markDone(habit)}
            >
              {habit.completedToday ? "Completed Today ✓" : "Mark as Done"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HabitTracker;