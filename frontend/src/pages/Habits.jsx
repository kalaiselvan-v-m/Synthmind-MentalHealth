import { useEffect, useState } from "react";

function Habits() {
  const token = localStorage.getItem("token");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchHabits();
  }, []);

  const fetchHabits = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/habits", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const result = await res.json();

      if (!res.ok) {
        setError("Unable to load habit suggestions");
        return;
      }

      setData(result);
    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }
  };

  if (error) {
    return <div className="habits-page"><p>{error}</p></div>;
  }

  if (!data) {
    return <div className="habits-page"><p>Loading habits...</p></div>;
  }

  return (
    <div className="habits-page">
      <div className="habits-header">
        <h1>Habit Suggestions</h1>
        <p>Small routines based on your weekly emotional patterns.</p>
      </div>

      <div className="habits-summary">
        <div>
          <span>Weekly Trend</span>
          <strong>{data.trend}</strong>
        </div>
        <div>
          <span>Dominant Emotion</span>
          <strong>{data.dominantEmotion}</strong>
        </div>
        <div>
          <span>Heavy Moments</span>
          <strong>{data.negativeCount}</strong>
        </div>
      </div>

      <div className="habits-list">
        {data.habits.map((habit, index) => (
          <div key={index} className="habit-card">
            <div className="habit-top">
              <div>
                <span className="habit-category">{habit.category}</span>
                <h2>{habit.title}</h2>
              </div>

              <span className={`habit-difficulty ${habit.difficulty.toLowerCase()}`}>
                {habit.difficulty}
              </span>
            </div>

            <p className="habit-reason">{habit.reason}</p>

            <div className="habit-frequency">
              Frequency: {habit.frequency}
            </div>

            <div className="habit-steps">
              {habit.steps.map((step, stepIndex) => (
                <div key={stepIndex} className="habit-step">
                  <span>{stepIndex + 1}</span>
                  <p>{step}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <p className="habits-note">
        These habits support reflection and daily wellness. They are not medical advice.
      </p>
    </div>
  );
}

export default Habits;