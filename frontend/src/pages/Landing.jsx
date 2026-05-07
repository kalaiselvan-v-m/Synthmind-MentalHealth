import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  Sparkles,
  HeartHandshake,
  ShieldCheck,
} from "lucide-react";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

function WordsPullUp({ text, showAsterisk = false }) {
  const words = text.split(" ");

  return (
    <span className="inline-flex flex-wrap">
      {words.map((word, i) => {
        const isLast = i === words.length - 1;

        return (
          <motion.span
            key={i}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{
              duration: 0.6,
              delay: i * 0.08,
              ease: [0.16, 1, 0.3, 1],
            }}
            className="relative inline-block"
            style={{ marginRight: isLast ? 0 : "0.25em" }}
          >
            {word}

            {showAsterisk && isLast && (
              <span className="absolute top-[0.65em] -right-[0.3em] text-[0.31em]">
                *
              </span>
            )}
          </motion.span>
        );
      })}
    </span>
  );
}

function Reveal({ children, delay = 0 }) {
  return (
    <motion.div
      initial={{
        opacity: 0,
        y: 80,
        filter: "blur(12px)",
      }}
      whileInView={{
        opacity: 1,
        y: 0,
        filter: "blur(0px)",
      }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{
        duration: 1,
        delay,
        ease: [0.16, 1, 0.3, 1],
      }}
    >
      {children}
    </motion.div>
  );
}

const navItems = [
  { label: "About", href: "#about" },
  { label: "Companion", href: "#companion" },
  { label: "Features", href: "#features" },
  { label: "Safety", href: "#safety" },
];

function Landing() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const blurValue = Math.min(scrollY / 180, 6);
  const darkOverlay = Math.min(scrollY / 1200, 0.45);

  return (
    <div className="relative overflow-x-hidden bg-black text-white">
      
      {/* FIXED CINEMATIC BACKGROUND */}
      <div className="fixed inset-0 z-0 overflow-hidden">
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 h-full w-full object-cover transition-all duration-300"
          style={{
            filter: `blur(${blurValue}px)`,
            transform: `scale(${1 + blurValue * 0.01})`,
          }}
          src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260405_170732_8a9ccda6-5cff-4628-b164-059c500a2b41.mp4"
        />

        <div
          className="absolute inset-0 transition-all duration-300"
          style={{
            background: `
              linear-gradient(
                to bottom,
                rgba(0,0,0,${0.25 + darkOverlay}),
                rgba(0,0,0,${0.15 + darkOverlay * 0.6}),
                rgba(0,0,0,${0.7 + darkOverlay})
              )
            `,
            backdropFilter: `blur(${blurValue * 0.35}px)`,
          }}
        />
      </div>

      {/* CONTENT */}
      <div className="relative z-10">

        {/* HERO */}
        <section className="relative h-screen w-full overflow-hidden p-2">
          <div className="relative h-full w-full overflow-hidden rounded-2xl md:rounded-[2rem]">

            {/* NAVBAR */}
            <nav className="absolute left-1/2 top-0 z-20 -translate-x-1/2">
              <div className="flex items-center gap-3 rounded-b-2xl border border-white/10 bg-black/40 px-4 py-2 backdrop-blur-2xl sm:gap-6 md:gap-12 md:rounded-b-3xl md:px-8 lg:gap-14">
                {navItems.map((item) => (
                  <a
                    key={item.label}
                    href={item.href}
                    className="text-[10px] font-light tracking-[0.15em] text-[#E1E0CC]/70 transition-all duration-300 hover:text-[#E1E0CC] sm:text-xs md:text-sm"
                  >
                    {item.label}
                  </a>
                ))}
              </div>
            </nav>

            {/* LOGIN / REGISTER */}
            <div className="absolute right-4 top-4 z-30 hidden gap-3 md:flex">
              <Link
                to="/login"
                className="rounded-full border border-white/10 bg-black/30 px-5 py-2 text-sm text-[#E1E0CC] backdrop-blur-xl transition-all duration-300 hover:border-cyan-200/20 hover:bg-black/50"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="rounded-full bg-[#E1E0CC] px-5 py-2 text-sm font-medium text-black transition-all duration-300 hover:scale-105"
              >
                Register
              </Link>
            </div>

            {/* HERO CONTENT */}
            <div className="absolute bottom-0 left-0 right-0 px-4 pb-6 sm:px-6 md:px-10">
              <div className="grid grid-cols-12 items-end gap-4">
                
                <div className="col-span-12 lg:col-span-8">
                  <h1
                    className="font-medium leading-[0.82] tracking-[-0.08em] text-[22vw] sm:text-[20vw] md:text-[17vw] lg:text-[13vw] xl:text-[12vw]"
                    style={{ color: "#F5F1E8" }}
                  >
                    <WordsPullUp text="SynthMind" showAsterisk />
                  </h1>
                </div>

                <div className="col-span-12 flex flex-col gap-6 pb-6 lg:col-span-4 lg:pb-10">
                  <motion.p
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{
                      duration: 0.8,
                      delay: 0.5,
                      ease: [0.16, 1, 0.3, 1],
                    }}
                    className="max-w-md text-sm leading-relaxed text-white/60 md:text-base"
                  >
                    An emotionally intelligent AI companion that listens,
                    remembers, reflects, and gently supports your wellness
                    journey.
                  </motion.p>

                  <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{
                      duration: 0.8,
                      delay: 0.7,
                      ease: [0.16, 1, 0.3, 1],
                    }}
                  >
                    <Link
                      to="/register"
                      className="group inline-flex items-center gap-2 rounded-full bg-[#F5F1E8] py-1 pl-5 pr-1 text-sm font-medium text-black transition-all duration-300 hover:gap-4"
                    >
                      Begin Journey

                      <span className="flex h-10 w-10 items-center justify-center rounded-full bg-black transition-all duration-300 group-hover:scale-110">
                        <ArrowRight
                          className="h-4 w-4"
                          style={{ color: "#F5F1E8" }}
                        />
                      </span>
                    </Link>
                  </motion.div>
                </div>

              </div>
            </div>
          </div>
        </section>

        {/* ABOUT */}
        <section
          id="about"
          className="mx-auto flex min-h-screen max-w-6xl flex-col justify-center px-6 py-32"
        >
          <Reveal>
            <p className="mb-6 text-sm uppercase tracking-[0.35em] text-cyan-200/60">
              About
            </p>

            <h2 className="max-w-5xl text-5xl font-medium leading-[1.05] tracking-[-0.05em] text-[#F5F1E8] md:text-7xl">
              A calm emotional space designed for reflection, support, and growth.
            </h2>

            <p className="mt-10 max-w-2xl text-lg leading-relaxed text-white/50">
              SynthMind combines emotional intelligence, adaptive AI memory,
              mood understanding, and supportive conversations to create a
              deeply personal wellness experience.
            </p>
          </Reveal>
        </section>

        {/* COMPANION */}
        <section
          id="companion"
          className="mx-auto grid min-h-screen max-w-6xl items-center gap-20 px-6 py-32 md:grid-cols-2"
        >
          <Reveal>
            <div>
              <p className="mb-6 text-sm uppercase tracking-[0.35em] text-cyan-200/60">
                Companion
              </p>

              <h2 className="text-5xl font-medium leading-[1.05] tracking-[-0.05em] text-[#F5F1E8] md:text-7xl">
                More than a chatbot.
              </h2>
            </div>
          </Reveal>

          <div className="space-y-6">
            {[
              {
                icon: <Brain size={22} />,
                title: "Emotional Memory",
                desc: "SynthMind remembers emotional patterns and adapts support over time.",
              },
              {
                icon: <Sparkles size={22} />,
                title: "Adaptive Personality",
                desc: "Conversation tone evolves based on your emotional state and comfort.",
              },
              {
                icon: <HeartHandshake size={22} />,
                title: "Gentle Wellness Support",
                desc: "Designed to create calm, reflection, and emotional openness.",
              },
            ].map((item, index) => (
              <Reveal delay={index * 0.15} key={item.title}>
                <div className="group relative overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.03] p-8 backdrop-blur-2xl transition-all duration-500 hover:border-cyan-300/20 hover:bg-white/[0.05]">
                  
                  <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/0 via-cyan-400/0 to-cyan-400/5 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

                  <div className="relative z-10">
                    <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-200">
                      {item.icon}
                    </div>

                    <h3 className="mb-3 text-2xl font-medium tracking-tight text-[#F5F1E8]">
                      {item.title}
                    </h3>

                    <p className="leading-relaxed text-white/55">
                      {item.desc}
                    </p>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </section>

        {/* FEATURES */}
        <section
          id="features"
          className="mx-auto min-h-screen max-w-6xl px-6 py-32"
        >
          <Reveal>
            <p className="mb-6 text-sm uppercase tracking-[0.35em] text-cyan-200/60">
              Features
            </p>

            <h2 className="mb-20 text-5xl font-medium leading-[1.05] tracking-[-0.05em] text-[#F5F1E8] md:text-7xl">
              Built for emotional wellness.
            </h2>
          </Reveal>

          <div className="grid gap-8 md:grid-cols-2">
            {[
              {
                title: "Mood Tracking",
                desc: "Track emotional patterns through calm daily reflections.",
              },
              {
                title: "AI Journal",
                desc: "Emotion-aware journaling with adaptive AI insight generation.",
              },
              {
                title: "Habit Growth",
                desc: "Build gentle wellness routines with emotional awareness.",
              },
              {
                title: "Weekly Insights",
                desc: "Understand emotional shifts through reflective summaries.",
              },
            ].map((card, index) => (
              <Reveal delay={index * 0.1} key={card.title}>
                <div className="group relative overflow-hidden rounded-[2.5rem] border border-white/10 bg-white/[0.03] p-10 backdrop-blur-2xl transition-all duration-500 hover:-translate-y-2 hover:border-cyan-300/20 hover:bg-white/[0.05]">
                  
                  <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/0 to-cyan-400/10 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

                  <div className="relative z-10">
                    <h3 className="mb-5 text-4xl font-medium tracking-tight text-[#F5F1E8]">
                      {card.title}
                    </h3>

                    <p className="max-w-sm text-lg leading-relaxed text-white/55">
                      {card.desc}
                    </p>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </section>

        {/* SAFETY */}
        <section
          id="safety"
          className="mx-auto flex min-h-screen max-w-6xl flex-col justify-center px-6 py-32"
        >
          <Reveal>
            <p className="mb-6 text-sm uppercase tracking-[0.35em] text-cyan-200/60">
              Safety
            </p>

            <h2 className="max-w-5xl text-5xl font-medium leading-[1.05] tracking-[-0.05em] text-[#F5F1E8] md:text-7xl">
              Supportive AI designed with emotional safety in mind.
            </h2>
          </Reveal>

          <div className="mt-20 grid gap-8 md:grid-cols-3">
            {[
              {
                title: "Crisis Awareness",
                desc: "Detects emotionally critical conversations and responds supportively.",
              },
              {
                title: "Emotion Sensitive AI",
                desc: "Responses adapt carefully to emotional tone and intensity.",
              },
              {
                title: "Private Experience",
                desc: "Designed to feel personal, safe, and emotionally respectful.",
              },
            ].map((item, index) => (
              <Reveal delay={index * 0.12} key={item.title}>
                <div className="group rounded-[2rem] border border-white/10 bg-white/[0.03] p-8 backdrop-blur-2xl transition-all duration-500 hover:border-cyan-300/20 hover:bg-white/[0.05]">
                  
                  <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-200">
                    <ShieldCheck size={22} />
                  </div>

                  <h3 className="mb-3 text-2xl font-medium tracking-tight text-[#F5F1E8]">
                    {item.title}
                  </h3>

                  <p className="leading-relaxed text-white/55">
                    {item.desc}
                  </p>
                </div>
              </Reveal>
            ))}
          </div>
        </section>

        {/* FINAL CTA */}
        <section className="relative overflow-hidden px-6 py-40 text-center">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-500/10 to-transparent blur-3xl" />

          <Reveal>
            <div className="relative z-10">
              <h2 className="text-5xl font-medium leading-[1] tracking-[-0.06em] text-[#F5F1E8] md:text-8xl">
                Your emotional space awaits.
              </h2>

              <Link
                to="/register"
                className="mt-12 inline-flex items-center gap-3 rounded-full bg-[#F5F1E8] px-8 py-4 text-lg font-medium text-black transition-all duration-300 hover:scale-105"
              >
                Begin Journey
                <ArrowRight className="h-5 w-5" />
              </Link>
            </div>
          </Reveal>
        </section>

      </div>
    </div>
  );
}

export default Landing;