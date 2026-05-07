import { NavLink } from "react-router-dom";
import { MessageCircle, Home, Sprout, User, BookOpen } from "lucide-react";

function BottomNav() {
  const items = [
    { to: "/chat", label: "Chat", icon: <MessageCircle size={20} /> },
    { to: "/dashboard", label: "Home", icon: <Home size={20} /> },
    { to: "/mood", label: "Reflect", icon: <BookOpen size={20} /> },
    { to: "/habit-tracker", label: "Growth", icon: <Sprout size={20} /> },
    { to: "/profile", label: "Profile", icon: <User size={20} /> },
  ];

  return (
    <nav className="bottom-dock">
      {items.map((item) => (
        <NavLink key={item.to} to={item.to} className="dock-item">
          {item.icon}
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}

export default BottomNav;