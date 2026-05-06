import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Profile() {
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    const res = await fetch("http://127.0.0.1:8000/profile", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  const clearChat = async () => {
    await fetch("http://127.0.0.1:8000/profile/chat", {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    alert("Chat cleared");
    fetchProfile();
  };

  const clearJournal = async () => {
    await fetch("http://127.0.0.1:8000/profile/journal", {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    alert("Journal cleared");
    fetchProfile();
  };

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  if (loading) return <p>Loading...</p>;

  const profile = data.profile;

  return (
    <div className="profile-page">
      <h1>Your Profile</h1>

      <div className="profile-card">
        <h2>Mental Profile</h2>

        {profile ? (
          <>
            <p>Stress Score: {profile.stress_score}</p>
            <p>Wellness Score: {profile.wellness_score}</p>
            <p>Emotion: {profile.emotional_state}</p>
            <p>Support Level: {profile.support_level}</p>
            <p>Risk Level: {profile.risk_level}</p>
          </>
        ) : (
          <p>No onboarding data yet</p>
        )}
      </div>

      <div className="profile-card">
        <h2>Usage</h2>
        <p>Chats: {data.chatCount}</p>
        <p>Journal Entries: {data.journalCount}</p>
      </div>

      <div className="profile-actions">
        <button onClick={clearChat}>Clear Chat History</button>
        <button onClick={clearJournal}>Clear Journal</button>
        <button className="logout" onClick={logout}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default Profile;