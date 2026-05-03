function Badge({ label, type = "default" }) {
  const colors = {
    low: "bg-green-500/20 text-green-300 border-green-500/30",
    medium: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
    high: "bg-red-500/20 text-red-300 border-red-500/30",
    emotion: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    default: "bg-purple-500/20 text-purple-300 border-purple-500/30",
  };

  return (
    <span className={`px-3 py-1 rounded-full border text-xs capitalize ${colors[type] || colors.default}`}>
      {label}
    </span>
  );
}

export default Badge;