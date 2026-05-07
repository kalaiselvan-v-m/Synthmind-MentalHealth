import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  BookOpenText,
  Feather,
  Sparkles,
  Clock3,
  HeartPulse,
} from "lucide-react";

const fadeUp = {
  hidden: {
    opacity: 0,
    y: 28,
    filter: "blur(10px)",
  },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: {
      duration: 0.75,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

function Journal() {
  const token = localStorage.getItem("token");

  const [content, setContent] = useState("");
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/journal", {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await res.json();

      if (!res.ok) {
        console.error(data);
        setEntries([]);
        return;
      }

      setEntries(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setEntries([]);
    }
  };

  const submitEntry = async () => {
    if (!content.trim()) return;

    setLoading(true);

    try {
      await fetch("http://127.0.0.1:8000/journal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content }),
      });

      setContent("");
      fetchEntries();
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="journal-page synth-journal-page">
      <motion.section
        className="synth-journal-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>AI Journal</p>

        <h1>
          Write what your mind
          <span> could not say.</span>
        </h1>

        <small>
          Use this space to release thoughts, track emotions, and let SynthMind
          reflect back gentle insights from your writing.
        </small>
      </motion.section>

      <motion.section
        className="synth-journal-compose"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-compose-header">
          <div>
            <p>Today’s reflection</p>
            <h2>What are you carrying right now?</h2>
          </div>

          <Feather size={22} />
        </div>

        <textarea
          placeholder="Start writing freely..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />

        <div className="synth-compose-footer">
          <span>{content.trim().length} characters</span>

          <button onClick={submitEntry} disabled={loading || !content.trim()}>
            {loading ? "Saving..." : "Save reflection"}
          </button>
        </div>
      </motion.section>

      <motion.section
        className="synth-journal-list-header"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <p>Your entries</p>
        <h2>Recent reflections</h2>
      </motion.section>

      <div className="synth-journal-list">
        {entries.length === 0 && (
          <motion.div
            className="synth-empty-journal"
            variants={fadeUp}
            initial="hidden"
            animate="visible"
          >
            <BookOpenText size={26} />
            <h3>No journal entries yet</h3>
            <p>
              Your first reflection will appear here after you save an entry.
            </p>
          </motion.div>
        )}

        {entries.map((entry, index) => (
          <motion.article
            key={entry.id}
            className="synth-journal-card"
            initial={{
              opacity: 0,
              y: 24,
              filter: "blur(10px)",
            }}
            whileInView={{
              opacity: 1,
              y: 0,
              filter: "blur(0px)",
            }}
            viewport={{ once: true, amount: 0.15 }}
            transition={{
              duration: 0.65,
              delay: index * 0.05,
              ease: [0.16, 1, 0.3, 1],
            }}
            whileHover={{
              y: -5,
              transition: {
                type: "spring",
                stiffness: 220,
                damping: 18,
              },
            }}
          >
            <div className="synth-journal-card-top">
              <div className="synth-journal-date">
                <Clock3 size={15} />
                <span>{new Date(entry.created_at).toLocaleString()}</span>
              </div>

              <div className="synth-journal-emotion">
                <HeartPulse size={15} />
                <span>{entry.emotion || "Reflective"}</span>
              </div>
            </div>

            <p className="synth-journal-content">{entry.content}</p>

            <div className="synth-journal-ai">
              <div>
                <Sparkles size={16} />
                <strong>AI Insight</strong>
              </div>

              <p>{entry.ai_summary || "SynthMind is still learning from this entry."}</p>
            </div>
          </motion.article>
        ))}
      </div>
    </div>
  );
}

export default Journal;