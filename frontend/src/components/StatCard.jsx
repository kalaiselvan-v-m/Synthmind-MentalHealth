function StatCard({ title, value, subtitle }) {
  return (
    <div className="bg-white/10 rounded-2xl p-5 border border-white/10">
      <p className="text-gray-400 text-sm">{title}</p>
      <h2 className="text-3xl font-bold mt-2">{value}</h2>
      {subtitle && <p className="text-gray-400 mt-2">{subtitle}</p>}
    </div>
  );
}

export default StatCard;