import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Brain,
  HeartHandshake,
  ShieldAlert,
  Sparkles,
  MessageCircle,
  NotebookPen,
  Trash2,
  LogOut,
  Activity,
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

function Profile() {
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    const res = await fetch("http://127.0.0.1:8000/profile", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  const clearChat = async () => {
    await fetch("http://127.0.0.1:8000/profile/chat", {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    fetchProfile();
  };

  const clearJournal = async () => {
    await fetch("http://127.0.0.1:8000/profile/journal", {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    fetchProfile();
  };

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  if (loading) {
    return (
      <div className="profile-page synth-profile-page">
        <p>Loading profile...</p>
      </div>
    );
  }

  const profile = data.profile;

  return (
    <div className="profile-page synth-profile-page">
      <motion.section
        className="synth-profile-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>Your emotional profile</p>

        <h1>
          A softer look
          <span> at your wellbeing.</span>
        </h1>

        <small>
          Review emotional patterns, wellness signals, activity history, and
          your personalized support profile.
        </small>
      </motion.section>

      <motion.section
        className="synth-profile-grid"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-profile-stat">
          <Brain size={20} />
          <span>Stress score</span>
          <strong>{profile?.stress_score ?? "--"}</strong>
        </div>

        <div className="synth-profile-stat">
          <Sparkles size={20} />
          <span>Wellness score</span>
          <strong>{profile?.wellness_score ?? "--"}</strong>
        </div>

        <div className="synth-profile-stat">
          <ShieldAlert size={20} />
          <span>Risk level</span>
          <strong>{profile?.risk_level ?? "Unknown"}</strong>
        </div>
      </motion.section>

      <motion.section
        className="synth-profile-main-grid"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <div className="synth-profile-card">
          <div className="synth-profile-card-header">
            <HeartHandshake size={20} />

            <div>
              <p>Mental profile</p>
              <h2>Your emotional support profile</h2>
            </div>
          </div>

          {profile ? (
            <div className="synth-profile-info-grid">
              <div>
                <span>Emotional state</span>
                <strong>{profile.emotional_state}</strong>
              </div>

              <div>
                <span>Support level</span>
                <strong>{profile.support_level}</strong>
              </div>

              <div>
                <span>Stress score</span>
                <strong>{profile.stress_score}</strong>
              </div>

              <div>
                <span>Wellness score</span>
                <strong>{profile.wellness_score}</strong>
              </div>

              <div>
                <span>Risk level</span>
                <strong>{profile.risk_level}</strong>
              </div>
            </div>
          ) : (
            <p className="synth-profile-empty">
              No onboarding data available yet.
            </p>
          )}
        </div>

        <div className="synth-profile-card">
          <div className="synth-profile-card-header">
            <Activity size={20} />

            <div>
              <p>Usage activity</p>
              <h2>Your recent activity</h2>
            </div>
          </div>

          <div className="synth-usage-grid">
            <div className="synth-usage-box">
              <MessageCircle size={18} />
              <span>Total chats</span>
              <strong>{data.chatCount}</strong>
            </div>

            <div className="synth-usage-box">
              <NotebookPen size={18} />
              <span>Journal entries</span>
              <strong>{data.journalCount}</strong>
            </div>
          </div>
        </div>
      </motion.section>

      <motion.section
        className="synth-profile-actions"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <button onClick={clearChat}>
          <Trash2 size={18} />
          Clear chat history
        </button>

        <button onClick={clearJournal}>
          <Trash2 size={18} />
          Clear journal
        </button>

        <button className="logout-btn" onClick={logout}>
          <LogOut size={18} />
          Logout
        </button>
      </motion.section>
    </div>
  );
}

export default Profile;