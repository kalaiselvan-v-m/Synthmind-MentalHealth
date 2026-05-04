import { useEffect, useState } from "react";
import API from "../api/api";

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

  if (!data) return <div className="recovery-page">Loading plan...</div>;

  const tasks = [
    ["Breathing", data.breathing_exercise],
    ["CBT Task", data.cbt_task],
    ["Journaling", data.journaling_task],
    ["Sleep Tip", data.sleep_tip],
    ["Habit Goal", data.habit_goal],
  ];

  return (
    <div className="recovery-page">
      <div className="recovery-header">
        <h1>Recovery Plan</h1>
        <p>Your personalized daily wellness routine generated from mood, emotion, and risk signals.</p>
      </div>

      <div className="recovery-summary">
        <div className={`recovery-summary-card risk-${data.risk_level.toLowerCase()}`}>
          <span>Risk Level</span>
          <strong>{data.risk_level}</strong>
        </div>

        <div className="recovery-summary-card">
          <span>Overall Trend</span>
          <strong>{data.overall_trend}</strong>
        </div>

        <div className="recovery-summary-card">
          <span>Dominant Emotion</span>
          <strong>{data.dominant_emotion}</strong>
        </div>
      </div>

      <section className="recovery-section">
        <h2>Daily Routine</h2>

        <div className="routine-list">
          {data.daily_routine.map((item, i) => (
            <div key={i} className="routine-item">
              <div className="routine-number">{i + 1}</div>
              <p>{item}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="recovery-section">
        <h2>Care Tasks</h2>

        <div className="care-task-grid">
          {tasks.map(([title, value], i) => (
            <div key={i} className="care-task-card">
              <h3>{title}</h3>
              <p>{value}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="recovery-section">
        <h2>Suggested Activities</h2>

        <div className="activity-list">
          {data.recommended_activities.map((rec, i) => (
            <div key={i} className="activity-card">
              {rec}
            </div>
          ))}
        </div>
      </section>

      <div className="therapy-card">
        <h3>Therapy Suggestion</h3>
        <p>{data.therapy_suggestion}</p>
      </div>

      <p className="recovery-note">{data.note}</p>
    </div>
  );
}

export default RecoveryPlan;