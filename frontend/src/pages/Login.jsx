import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import skyVideo from "../assets/videos/sky.mp4";

function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const checkOnboardingStatus = async (token) => {
    const res = await fetch("http://127.0.0.1:8000/onboarding/status", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) return false;

    const status = await res.json();
    return status.completed;
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Login failed");
        setLoading(false);
        return;
      }

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data));

      const completed = await checkOnboardingStatus(data.access_token);
      navigate(completed ? "/dashboard" : "/onboarding");
    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }

    setLoading(false);
  };

  return (
    <div className="auth-cinematic-page">
      <video
        autoPlay
        loop
        muted
        playsInline
        className="auth-bg-video"
        src={skyVideo}
      />

      <div className="auth-cinematic-overlay" />

      <Link to="/" className="auth-brand">
        SynthMind
      </Link>

      <div className="auth-cinematic-shell">
        <motion.div
          initial={{ opacity: 0, y: 40, filter: "blur(12px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
          className="auth-copy"
        >
          <p>Welcome back</p>
          <h1>Your emotional space is still here.</h1>
          <span>
            Continue your private wellness journey with an AI companion that
            remembers, reflects, and supports you gently.
          </span>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 50, filter: "blur(14px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 1, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
          className="auth-cinematic-card"
        >
          <div className="auth-card-header">
            <p>Login</p>
            <h2>Enter SynthMind</h2>
          </div>

          <form onSubmit={handleLogin} className="auth-form cinematic">
            <input
              name="email"
              type="email"
              placeholder="Email address"
              value={form.email}
              onChange={handleChange}
              required
            />

            <input
              name="password"
              type="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              required
            />

            {error && <div className="auth-error">{error}</div>}

            <button type="submit" disabled={loading}>
              {loading ? "Entering..." : "Continue"}
              <ArrowRight size={18} />
            </button>
          </form>

          <p className="auth-switch cinematic">
            New here? <Link to="/register">Create your space</Link>
          </p>
        </motion.div>
      </div>
    </div>
  );
}

export default Login;