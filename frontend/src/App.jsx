import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";

import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Mood from "./pages/Mood";
import Insights from "./pages/Insights";
import Recommendations from "./pages/Recommendations";
import RecoveryPlan from "./pages/RecoveryPlan";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />
        <main className="main">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/mood" element={<Mood />} />
            <Route path="/insights" element={<Insights />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/recovery-plan" element={<RecoveryPlan />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;