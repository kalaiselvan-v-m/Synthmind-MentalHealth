import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  MessageCircle,
  SmilePlus,
  BookOpenText,
  Flame,
  HeartHandshake,
  Moon,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import EmotionalInsights from "../components/EmotionalInsights";

const fadeUp = {
  hidden: {
    opacity: 0,
    y: 36,
    filter: "blur(12px)",
  },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: {
      duration: 0.8,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

const cardHover = {
  y: -6,
  scale: 1.01,
  transition: {
    type: "spring",
    stiffness: 220,
    damping: 18,
  },
};

function Dashboard() {
  return (
    <div className="dashboard-page synth-dashboard">
      <motion.section
        className="synth-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p className="synth-kicker">Your private emotional space</p>

        <h1>
          Welcome back to a softer place
          <span> for your mind.</span>
        </h1>

        <p>
          Check in with yourself, talk to SynthMind, notice emotional patterns,
          and continue small healing routines without pressure.
        </p>
      </motion.section>

      <motion.section
        className="synth-home-grid"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <motion.div whileHover={cardHover}>
          <Link to="/chat" className="synth-primary-card">
            <div className="synth-card-icon">
              <MessageCircle size={24} />
            </div>

            <div>
              <p>Start here</p>
              <h2>What’s on your mind today?</h2>
              <span>
                Open a calm conversation with SynthMind and share whatever feels
                heavy, confusing, or important.
              </span>
            </div>
          </Link>
        </motion.div>

        <div className="synth-status-stack">
          {[
            {
              icon: <ShieldCheck size={20} />,
              label: "Safety",
              value: "Active",
              text: "Support checks are enabled",
            },
            {
              icon: <Moon size={20} />,
              label: "Companion",
              value: "24/7",
              text: "Available whenever you return",
            },
            {
              icon: <Sparkles size={20} />,
              label: "Care Plan",
              value: "Ready",
              text: "Personalized suggestions prepared",
            },
          ].map((item, index) => (
            <motion.div
              key={item.label}
              className="synth-mini-card"
              whileHover={cardHover}
              initial={{ opacity: 0, y: 24, filter: "blur(10px)" }}
              whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              viewport={{ once: true }}
              transition={{
                duration: 0.65,
                delay: index * 0.08,
                ease: [0.16, 1, 0.3, 1],
              }}
            >
              {item.icon}
              <p>{item.label}</p>
              <h3>{item.value}</h3>
              <span>{item.text}</span>
            </motion.div>
          ))}
        </div>
      </motion.section>

      <motion.section
        className="synth-section-heading"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.3 }}
      >
        <p>Gentle next steps</p>
        <h2>Choose one small action.</h2>
      </motion.section>

      <motion.section
        className="synth-action-grid"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.15 }}
      >
        {[
          {
            to: "/mood",
            icon: <SmilePlus size={22} />,
            title: "Mood check-in",
            text: "Name how you feel right now.",
          },
          {
            to: "/journal",
            icon: <BookOpenText size={22} />,
            title: "Reflect in journal",
            text: "Write what you could not say out loud.",
          },
          {
            to: "/habit-tracker",
            icon: <Flame size={22} />,
            title: "Habit rhythm",
            text: "Continue small routines without pressure.",
          },
          {
            to: "/recovery-plan",
            icon: <HeartHandshake size={22} />,
            title: "Recovery plan",
            text: "Follow your personalized care path.",
          },
        ].map((item, index) => (
          <motion.div
            key={item.title}
            whileHover={cardHover}
            initial={{ opacity: 0, y: 24, filter: "blur(10px)" }}
            whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            viewport={{ once: true }}
            transition={{
              duration: 0.65,
              delay: index * 0.07,
              ease: [0.16, 1, 0.3, 1],
            }}
          >
            <Link to={item.to} className="synth-action-card">
              {item.icon}
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </Link>
          </motion.div>
        ))}
      </motion.section>

      <motion.section
        className="synth-weekly-card"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
        whileHover={cardHover}
      >
        <div>
          <p>Weekly reflection</p>
          <h2>Patterns, not pressure.</h2>
          <span>
            Review your recent emotional trends, mood changes, and gentle
            recommendations from SynthMind.
          </span>
        </div>

        <Link to="/weekly-report">View weekly report</Link>
      </motion.section>

      <motion.div
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.15 }}
      >
        <EmotionalInsights />
      </motion.div>
    </div>
  );
}

export default Dashboard;