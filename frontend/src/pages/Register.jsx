import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import skyVideo from "../assets/videos/sky.mp4";

function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Register failed");
        setLoading(false);
        return;
      }

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data));

      navigate("/onboarding");
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

      <Link to="/" className="auth-brand cream">
        SynthMind
      </Link>

      <div className="auth-cinematic-shell">
        <motion.div
          initial={{ opacity: 0, y: 40, filter: "blur(12px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
          className="auth-copy cream"
        >
          <p>Begin journey</p>

          <h1>Create a calm space that grows with you.</h1>

          <span>
            Start with a private emotional wellness space shaped around your
            mood, reflections, habits, and support needs.
          </span>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 50, filter: "blur(14px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ duration: 1, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
          className="auth-cinematic-card cream"
        >
          <div className="auth-card-header cream">
            <p>Register</p>
            <h2>Start SynthMind</h2>
          </div>

          <form onSubmit={handleRegister} className="auth-form cinematic cream">
            <input
              name="name"
              type="text"
              placeholder="Your name"
              value={form.name}
              onChange={handleChange}
              required
            />

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
              placeholder="Create password"
              value={form.password}
              onChange={handleChange}
              required
            />

            {error && <div className="auth-error">{error}</div>}

            <button type="submit" disabled={loading}>
              {loading ? "Creating..." : "Create space"}
              <ArrowRight size={18} />
            </button>
          </form>

          <p className="auth-switch cinematic cream">
            Already have an account? <Link to="/login">Enter your space</Link>
          </p>
        </motion.div>
      </div>
    </div>
  );
}

export default Register;