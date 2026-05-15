import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useEffect } from "react";
import "./App.css";

import MoodPopup from "./components/MoodPopup";
import CinematicVideoBackground from "./components/CinematicVideoBackground";
import AppMenu from "./components/AppMenu";

import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Mood from "./pages/Mood";
import Insights from "./pages/Insights";
import Recommendations from "./pages/Recommendations";
import RecoveryPlan from "./pages/RecoveryPlan";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Onboarding from "./pages/Onboarding";
import WeeklyReport from "./pages/WeeklyReport";
import Journal from "./pages/Journal";
import Profile from "./pages/Profile";
import Habits from "./pages/Habits";
import HabitTracker from "./pages/HabitTracker";

import {
  requestNotificationPermission,
  sendNotification,
} from "./utils/reminder";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
}

function AppLayout() {
  useEffect(() => {
    requestNotificationPermission();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const lastVisit = localStorage.getItem("lastVisit");
      const now = Date.now();

      if (!lastVisit || now - lastVisit > 6 * 60 * 60 * 1000) {
        sendNotification(
          "SynthMind 🌿",
          "Take 2 minutes for your habit today."
        );
      }

      localStorage.setItem("lastVisit", now);
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchReminder = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const res = await fetch("http://127.0.0.1:8000/reminder", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json();

        if (res.ok && data.message) {
          sendNotification("SynthMind 🌿", data.message);
        }
      } catch (err) {
        console.error("Reminder fetch error:", err);
      }
    };

    fetchReminder();

    const timer = setInterval(fetchReminder, 1000 * 60 * 60 * 8);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="app no-sidebar-app">
      <CinematicVideoBackground />

      <MoodPopup />

      <AppMenu />

      <main className="main app-main">
        <Routes>
          {/* DEFAULT AFTER LOGIN */}
          <Route path="/" element={<Navigate to="/chat" replace />} />

          {/* MAIN PAGES */}
          <Route path="/chat" element={<Chat />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/mood" element={<Mood />} />
          <Route path="/habit-tracker" element={<HabitTracker />} />
          <Route path="/profile" element={<Profile />} />

          {/* SECONDARY PAGES */}
          <Route path="/insights" element={<Insights />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/recovery-plan" element={<RecoveryPlan />} />
          <Route path="/weekly-report" element={<WeeklyReport />} />
          <Route path="/journal" element={<Journal />} />
          <Route path="/habits" element={<Habits />} />
          <Route path="/onboarding" element={<Onboarding />} />

          {/* FALLBACK INSIDE APP */}
          <Route path="*" element={<Navigate to="/chat" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* PUBLIC LANDING FIRST */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* PROTECTED APP */}
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;