import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import API from "../api/api";
import {
  HeartHandshake,
  Sparkles,
  SmilePlus,
  ShieldCheck,
  Wand2,
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

function Recommendations() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      const res = await API.get("/recommendations/1");
      setData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (!data) {
    return (
      <div className="rec-page synth-rec-page">
        Loading recommendations...
      </div>
    );
  }

  return (
    <div className="rec-page synth-rec-page">
      <motion.section
        className="synth-rec-hero"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <p>Personalized care</p>

        <h1>
          Gentle suggestions,
          <span> shaped by you.</span>
        </h1>

        <small>
          SynthMind recommends small actions based on your mood, emotions, and
          current wellness signals.
        </small>
      </motion.section>

      <motion.section
        className="synth-rec-summary"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
      >
        <div className="synth-rec-stat">
          <SmilePlus size={20} />
          <span>Current emotion</span>
          <strong>{data.current_emotion || "Unknown"}</strong>
        </div>

        <div className="synth-rec-stat">
          <Sparkles size={20} />
          <span>Latest mood</span>
          <strong>{data.latest_mood || "Unknown"}</strong>
        </div>

        <div className="synth-rec-stat">
          <ShieldCheck size={20} />
          <span>Risk level</span>
          <strong>{data.risk_level || "Unknown"}</strong>
        </div>
      </motion.section>

      <motion.section
        className="synth-rec-list-header"
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        <p>Next small steps</p>
        <h2>Recommended for now.</h2>
      </motion.section>

      <div className="synth-rec-list">
        {data.recommendations.map((rec, index) => (
          <motion.article
            key={index}
            className="synth-rec-card"
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
            viewport={{ once: true, amount: 0.12 }}
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
            <div className="synth-rec-number">
              <Wand2 size={18} />
            </div>

            <div>
              <span>Suggested action {index + 1}</span>
              <p>{rec}</p>
            </div>
          </motion.article>
        ))}
      </div>

      {data.note && (
        <motion.section
          className="synth-rec-note"
          variants={fadeUp}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
        >
          <HeartHandshake size={20} />
          <p>{data.note}</p>
        </motion.section>
      )}
    </div>
  );
}

export default Recommendations;