const VIDEO_URL =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260406_094145_4a271a6c-3869-4f1c-8aa7-aeb0cb227994.mp4";

function CinematicVideoBackground() {
  return (
    <div className="cinematic-video-wrapper">
      <video
        autoPlay
        muted
        loop
        playsInline
        className="cinematic-video"
        src={VIDEO_URL}
      />

      {/* bottom blur fade */}
      <div className="cinematic-bottom-blur" />
    </div>
  );
}

export default CinematicVideoBackground;