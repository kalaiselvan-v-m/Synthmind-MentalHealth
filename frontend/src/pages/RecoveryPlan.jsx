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

  if (!data) return <p>Loading plan...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Recovery Plan</h1>

      <div className="space-y-2 mb-6">
        <p>Risk: {data.risk_level}</p>
        <p>Trend: {data.overall_trend}</p>
        <p>Emotion: {data.dominant_emotion}</p>
      </div>

      {/* Daily Routine */}
      <h2 className="text-xl font-semibold mb-2">Daily Routine</h2>
      <ul className="mb-6 list-disc ml-6">
        {data.daily_routine.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>

      {/* Tasks */}
      <div className="space-y-4">
        <div className="bg-white/10 p-4 rounded-xl">
          <strong>Breathing:</strong> {data.breathing_exercise}
        </div>

        <div className="bg-white/10 p-4 rounded-xl">
          <strong>CBT Task:</strong> {data.cbt_task}
        </div>

        <div className="bg-white/10 p-4 rounded-xl">
          <strong>Journaling:</strong> {data.journaling_task}
        </div>

        <div className="bg-white/10 p-4 rounded-xl">
          <strong>Sleep Tip:</strong> {data.sleep_tip}
        </div>

        <div className="bg-white/10 p-4 rounded-xl">
          <strong>Goal:</strong> {data.habit_goal}
        </div>
      </div>

      {/* Suggestions */}
      <h2 className="text-xl font-semibold mt-6 mb-2">
        Suggested Activities
      </h2>

      <div className="grid gap-3">
        {data.recommended_activities.map((rec, i) => (
          <div key={i} className="bg-purple-600 p-3 rounded-xl">
            {rec}
          </div>
        ))}
      </div>

      <p className="mt-6 text-green-400">{data.therapy_suggestion}</p>
    </div>
  );
}

export default RecoveryPlan;