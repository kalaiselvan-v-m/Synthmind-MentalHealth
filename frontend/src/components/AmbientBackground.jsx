function AmbientBackground() {
  return (
    <div className="inside-ambient-bg">
      <div className="ambient-blob blob-one"></div>
      <div className="ambient-blob blob-two"></div>
      <div className="ambient-blob blob-three"></div>

      <div className="ambient-fog fog-one"></div>
      <div className="ambient-fog fog-two"></div>

      <div className="ambient-stars">
        {Array.from({ length: 34 }).map((_, index) => (
          <span key={index}></span>
        ))}
      </div>

      <div className="ambient-depth-overlay"></div>
    </div>
  );
}

export default AmbientBackground;