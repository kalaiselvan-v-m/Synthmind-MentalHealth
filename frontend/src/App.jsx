import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useEffect } from "react";
import "./App.css";

import Sidebar from "./components/Sidebar";
import MoodPopup from "./components/MoodPopup";

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

// ✅ Reminder utilities
import {
  requestNotificationPermission,
  sendNotification,
} from "./utils/reminder";


function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");

  return token ? children : <Navigate to="/login" />;
}


function AppLayout() {

  // 🔔 Request notification permission
  useEffect(() => {
    requestNotificationPermission();
  }, []);


  // 🔔 Basic inactivity reminder
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


  // 🔥 Smart reminder from backend
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

    // run once immediately
    fetchReminder();

    // then repeat every 8 hrs
    const timer = setInterval(fetchReminder, 1000 * 60 * 60 * 8);

    return () => clearInterval(timer);
  }, []);


  return (
    <div className="app">

      {/* ✅ Daily Mood Popup */}
      <MoodPopup />

      <Sidebar />

      <main className="main">
        <Routes>

          <Route
            path="/"
            element={<Navigate to="/dashboard" />}
          />

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/chat"
            element={<Chat />}
          />

          <Route
            path="/mood"
            element={<Mood />}
          />

          <Route
            path="/insights"
            element={<Insights />}
          />

          <Route
            path="/recommendations"
            element={<Recommendations />}
          />

          <Route
            path="/recovery-plan"
            element={<RecoveryPlan />}
          />

          <Route
            path="/onboarding"
            element={<Onboarding />}
          />

          <Route
            path="/weekly-report"
            element={<WeeklyReport />}
          />

          <Route
            path="/journal"
            element={<Journal />}
          />

          <Route
            path="/profile"
            element={<Profile />}
          />

          <Route
            path="/habits"
            element={<Habits />}
          />

          <Route
            path="/habit-tracker"
            element={<HabitTracker />}
          />

        </Routes>
      </main>
    </div>
  );
}


function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

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