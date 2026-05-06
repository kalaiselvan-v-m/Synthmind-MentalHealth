import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">SynthMind</div>

      <nav className="nav">
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/chat">AI Chat</NavLink>
        <NavLink to="/mood">Mood Tracker</NavLink>
        <NavLink to="/insights">Insights</NavLink>
        <NavLink to="/recommendations">Recommendations</NavLink>
        <NavLink to="/recovery-plan">Recovery Plan</NavLink>
        <NavLink to="/weekly-report">Weekly Report</NavLink>
        <NavLink to="/journal">Journal</NavLink>
        <NavLink to="/profile">Profile</NavLink>
        <NavLink to="/habits">Habits</NavLink>
        <NavLink to="/habit-tracker">Habit Tracker</NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;