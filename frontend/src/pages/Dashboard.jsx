import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div>
      <section className="hero">
        <h1>Welcome back 👋</h1>
        <p>Your AI-powered mental wellness dashboard.</p>
      </section>

      <section className="card-grid">
        <div className="glass-card">
          <p>Wellness Status</p>
          <h2>Active</h2>
          <p>Tracking enabled</p>
        </div>

        <div className="glass-card">
          <p>AI Support</p>
          <h2>24/7</h2>
          <p>Chat available anytime</p>
        </div>

        <div className="glass-card">
          <p>Care Plan</p>
          <h2>Ready</h2>
          <p>Personalized suggestions</p>
        </div>
      </section>

      <section className="action-grid">
        <Link to="/chat" className="action-card">
          <h2>Talk to SynthMind</h2>
          <p>Start an AI emotional support chat.</p>
        </Link>

        <Link to="/mood" className="action-card blue">
          <h2>Daily Mood Check-in</h2>
          <p>Record how you feel today.</p>
        </Link>
      </section>
    </div>
  );
}

export default Dashboard;