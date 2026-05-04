import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-hero">
        <h1>Welcome back 👋</h1>
        <p>Your AI-powered mental wellness dashboard</p>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <p>Status</p>
          <h2>Active</h2>
          <p>Tracking enabled</p>
        </div>

        <div className="dashboard-card">
          <p>AI Support</p>
          <h2>24/7</h2>
          <p>Always available</p>
        </div>

        <div className="dashboard-card">
          <p>Care Plan</p>
          <h2>Ready</h2>
          <p>Personalized suggestions</p>
        </div>
      </div>

      <div className="dashboard-actions">
        <Link to="/chat" className="dashboard-action">
          <h3>Start AI Chat</h3>
          <p>Talk with SynthMind</p>
        </Link>

        <Link to="/mood" className="dashboard-action">
          <h3>Track Mood</h3>
          <p>Daily check-in</p>
        </Link>
      </div>
    </div>
  );
}

export default Dashboard;