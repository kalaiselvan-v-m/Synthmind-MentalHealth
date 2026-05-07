import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeft, ArrowRight, CheckCircle2, Sparkles } from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 28, filter: "blur(10px)" },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: { duration: 0.75, ease: [0.16, 1, 0.3, 1] },
  },
};

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

      setAnswers({
        ...answers,
        [currentQuestion.id]: existing.includes(option)
          ? existing.filter((item) => item !== option)
          : [...existing, option],
      });
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
          answer,
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
      <div className="onboarding-page synth-onboarding-page">
        <div className="synth-onboarding-card">
          <p>Loading onboarding...</p>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="onboarding-page synth-onboarding-page">
        <div className="synth-onboarding-card">
          <h1>No questions found</h1>
          <p>Please seed onboarding questions first.</p>
        </div>
      </div>
    );
  }

  const selectedAnswer = answers[currentQuestion.id];
  const progress = ((current + 1) / questions.length) * 100;

  return (
    <div className="onboarding-page synth-onboarding-page">
      <motion.div
        className="synth-onboarding-card"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-onboarding-top">
          <div>
            <p>Personal setup</p>
            <span>
              Question {current + 1} of {questions.length}
            </span>
          </div>

          <Sparkles size={22} />
        </div>

        <div className="synth-onboarding-progress">
          <div style={{ width: `${progress}%` }}></div>
        </div>

        <motion.div
          key={currentQuestion.id}
          initial={{ opacity: 0, y: 18, filter: "blur(8px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 0.45 }}
          className="synth-question-area"
        >
          <h1>{currentQuestion.question_text}</h1>

          <p>
            This helps SynthMind personalize your emotional wellness support.
          </p>

          <div className="synth-onboarding-options">
            {currentQuestion.options.map((option) => {
              const selected =
                currentQuestion.question_type === "multi_choice"
                  ? selectedAnswer?.includes(option)
                  : selectedAnswer === option;

              return (
                <button
                  key={option}
                  className={selected ? "selected" : ""}
                  onClick={() => selectAnswer(option)}
                >
                  <span>{option}</span>
                  {selected && <CheckCircle2 size={18} />}
                </button>
              );
            })}
          </div>
        </motion.div>

        {error && <div className="auth-error">{error}</div>}

        <div className="synth-onboarding-actions">
          <button
            className="synth-onboarding-back"
            disabled={current === 0 || saving}
            onClick={() => setCurrent(current - 1)}
          >
            <ArrowLeft size={17} />
            Back
          </button>

          <button
            className="synth-onboarding-next"
            onClick={saveAnswer}
            disabled={saving}
          >
            {saving
              ? "Saving..."
              : current === questions.length - 1
              ? "Complete"
              : "Next"}

            <ArrowRight size={17} />
          </button>
        </div>
      </motion.div>
    </div>
  );
}

export default Onboarding;