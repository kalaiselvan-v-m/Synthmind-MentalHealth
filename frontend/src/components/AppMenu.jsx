import {
  AnimatePresence,
  motion,
  useAnimationControls,
} from "framer-motion";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Menu,
  X,
  MessageCircle,
  Home,
  User,
  Heart,
  BarChart3,
  BookOpen,
  CalendarDays,
  Sparkles,
  HeartHandshake,
  Settings,
  LogOut,
} from "lucide-react";

const ITEMS = [
  { label: "Chat", path: "/chat", icon: <MessageCircle size={20} /> },
  { label: "Home", path: "/dashboard", icon: <Home size={20} /> },
  { label: "Mood", path: "/mood", icon: <Heart size={20} /> },
  { label: "Profile", path: "/profile", icon: <User size={20} /> },
  {label: "Habits",path: "/habit-tracker",icon: <Heart size={20} />,},
  { label: "Insights", path: "/insights", icon: <BarChart3 size={20} /> },
  { label: "Journal", path: "/journal", icon: <BookOpen size={20} /> },
  { label: "Reports", path: "/weekly-report", icon: <CalendarDays size={20} /> },
  { label: "Reccomendations", path: "/recommendations", icon: <Sparkles size={20} /> },
  {label: "Recovery",path: "/recovery-plan",icon: <HeartHandshake size={20} />,},
  { label: "Settings", path: "/profile", icon: <Settings size={20} /> },
  { label: "Logout", path: "/login", icon: <LogOut size={20} /> },
];

function AppMenu() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const animate = useAnimationControls();
  const shakeAnimation = useAnimationControls();

  const radius = 185;

  const closeAnimation = async () => {
    shakeAnimation.start({
      translateX: [0, 2, -2, 0, 2, -2, 0],
      transition: { duration: 0.07, repeat: Infinity },
    });

    await animate.start({
      scale: [1, 1.08, 1.15, 1],
      rotate: -360,
      filter: ["blur(0px)", "blur(2px)", "blur(0px)"],
      transition: { duration: 0.55, ease: [0.16, 1, 0.3, 1] },
    });

    shakeAnimation.stop();
    shakeAnimation.start({ translateX: 0, transition: { duration: 0 } });
    animate.start({ rotate: 0, scale: 1, filter: "blur(0px)" });
  };

  const handleNavigate = (path) => {
    if (path === "/login") {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    }

    navigate(path);
    setOpen(false);
  };

  return (
    <>
      {!open && (
        <motion.button
          layoutId="menu-button"
          className="center-orb-trigger"
          onClick={() => setOpen(true)}
          whileTap={{ scale: 0.92 }}
        >
          <Menu size={22} />
        </motion.button>
      )}

      <AnimatePresence>
        {open && (
          <motion.div
            className="center-orb-overlay"
            initial={{ opacity: 0, backdropFilter: "blur(0px)" }}
            animate={{ opacity: 1, backdropFilter: "blur(22px)" }}
            exit={{ opacity: 0, backdropFilter: "blur(0px)" }}
          >
            <motion.div
              animate={animate}
              className="center-orb-menu"
              initial={{ scale: 0.65, opacity: 0, filter: "blur(16px)" }}
              animate={{ scale: 1, opacity: 1, filter: "blur(0px)" }}
              exit={{ scale: 0.65, opacity: 0, filter: "blur(16px)" }}
              transition={{ type: "spring", stiffness: 180, damping: 22 }}
            >
              <motion.div animate={shakeAnimation}>
                <motion.button
                  layoutId="menu-button"
                  className="center-orb-close"
                  onClick={async () => {
                    setOpen(false);
                    await closeAnimation();
                  }}
                  whileTap={{ scale: 0.9 }}
                >
                  <X size={22} />
                </motion.button>
              </motion.div>

              {ITEMS.map((item, index) => {
                 const angle =
                (index / ITEMS.length) * Math.PI * 2 - Math.PI / 2;

                const x = Math.cos(angle) * radius;
                const y = Math.sin(angle) * radius;

                const labelRadius = radius + 78;

                const labelX = Math.cos(angle) * labelRadius;
                const labelY = Math.sin(angle) * labelRadius;

                return (
                    <div
                    key={item.label}
                    className="orb-item-wrap"
                    >
                    <motion.button
                        className="center-orb-item named"
                        initial={{
                        x: 0,
                        y: 0,
                        opacity: 0,
                        scale: 0.2,
                        }}
                        animate={{
                        x,
                        y,
                        opacity: 1,
                        scale: 1,
                        }}
                        exit={{
                        x: 0,
                        y: 0,
                        opacity: 0,
                        scale: 0.2,
                        }}
                        transition={{
                        type: "spring",
                        stiffness: 260,
                        damping: 20,
                        delay: index * 0.025,
                        }}
                        whileHover={{
                        scale: 1.08,
                        }}
                        onClick={() => handleNavigate(item.path)}
                    >
                        <div className="orb-icon-shell">
                        {item.icon}
                        </div>
                    </motion.button>

                    <motion.span
                        className="orb-name"
                        initial={{
                        x: 0,
                        y: 0,
                        opacity: 0,
                        scale: 0.6,
                        }}
                        animate={{
                        x: labelX,
                        y: labelY,
                        opacity: 1,
                        scale: 1,
                        }}
                        exit={{
                        x: 0,
                        y: 0,
                        opacity: 0,
                        scale: 0.6,
                        }}
                        transition={{
                        type: "spring",
                        stiffness: 240,
                        damping: 22,
                        delay: index * 0.025,
                        }}
                    >
                        {item.label}
                    </motion.span>
                    </div>
                );
              })}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export default AppMenu;