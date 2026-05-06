import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Onboarding() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/onboarding/questions");

      const data = await res.json();

      if (!res.ok) {
        setError("Unable to load onboarding questions");
        setLoading(false);
        return;
      }

      setQuestions(data);
    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }

    setLoading(false);
  };

  const currentQuestion = questions[current];

  const selectAnswer = (option) => {
    if (!currentQuestion) return;

    if (currentQuestion.question_type === "multi_choice") {
      const existing = answers[currentQuestion.id] || [];

      if (existing.includes(option)) {
        setAnswers({
          ...answers,
          [currentQuestion.id]: existing.filter((item) => item !== option),
        });
      } else {
        setAnswers({
          ...answers,
          [currentQuestion.id]: [...existing, option],
        });
      }
    } else {
      setAnswers({
        ...answers,
        [currentQuestion.id]: option,
      });
    }
  };

  const saveAnswer = async () => {
    const answer = answers[currentQuestion.id];

    if (!answer || (Array.isArray(answer) && answer.length === 0)) {
      setError("Please select an answer");
      return;
    }

    setError("");
    setSaving(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/onboarding/answer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          question_id: currentQuestion.id,
          answer: answer,
        }),
      });

      if (!res.ok) {
        setError("Could not save answer");
        setSaving(false);
        return;
      }

      if (current < questions.length - 1) {
        setCurrent(current + 1);
      } else {
        await completeOnboarding();
      }
    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }

    setSaving(false);
  };

  const completeOnboarding = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/onboarding/complete", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        setError("Could not complete onboarding");
        return;
      }

      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }
  };

  if (loading) {
    return (
      <div className="onboarding-page">
        <div className="onboarding-card">
          <p>Loading onboarding...</p>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="onboarding-page">
        <div className="onboarding-card">
          <h1>No questions found</h1>
          <p>Please seed onboarding questions first.</p>
        </div>
      </div>
    );
  }

  const selectedAnswer = answers[currentQuestion.id];

  return (
    <div className="onboarding-page">
      <div className="onboarding-card">
        <div className="onboarding-progress">
          <span>
            Question {current + 1} of {questions.length}
          </span>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${((current + 1) / questions.length) * 100}%`,
              }}
            ></div>
          </div>
        </div>

        <h1>{currentQuestion.question_text}</h1>
        <p className="onboarding-subtitle">
          This helps SynthMind personalize your emotional wellness support.
        </p>

        <div className="onboarding-options">
          {currentQuestion.options.map((option) => {
            const selected =
              currentQuestion.question_type === "multi_choice"
                ? selectedAnswer?.includes(option)
                : selectedAnswer === option;

            return (
              <button
                key={option}
                className={`onboarding-option ${selected ? "selected" : ""}`}
                onClick={() => selectAnswer(option)}
              >
                {option}
              </button>
            );
          })}
        </div>

        {error && <div className="auth-error">{error}</div>}

        <div className="onboarding-actions">
          <button
            className="onboarding-back"
            disabled={current === 0 || saving}
            onClick={() => setCurrent(current - 1)}
          >
            Back
          </button>

          <button className="onboarding-next" onClick={saveAnswer} disabled={saving}>
            {saving
              ? "Saving..."
              : current === questions.length - 1
              ? "Complete"
              : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Onboarding;