function GlassCard({ children, className = "" }) {
  return (
    <div className={`glass rounded-3xl p-6 soft-glow ${className}`}>
      {children}
    </div>
  );
}

export default GlassCard;