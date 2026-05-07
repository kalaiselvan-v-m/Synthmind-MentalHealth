import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar ocean-sidebar">
      <div className="logo-wrap">
        <div className="mini-orb"></div>
        <div>
          <div className="logo">SynthMind</div>
          <p>Ocean Night</p>
        </div>
      </div>

      <nav className="nav">
        <NavLink to="/dashboard">Home</NavLink>
        <NavLink to="/chat">AI Chat</NavLink>
        <NavLink to="/mood">Reflect</NavLink>
        <NavLink to="/journal">Journal</NavLink>
        <NavLink to="/habit-tracker">Growth</NavLink>
        <NavLink to="/weekly-report">Weekly Report</NavLink>
        <NavLink to="/profile">Profile</NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;