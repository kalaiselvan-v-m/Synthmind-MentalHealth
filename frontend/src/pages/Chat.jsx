import { useState, useRef, useEffect } from "react";
import API from "../api/api";

function Chat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hi, I’m SynthMind. What’s on your mind today?",
      emotion: "neutral",
      risk: "Low",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const currentMessage = message;
    setMessage("");

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentMessage,
      },
    ]);

    setLoading(true);

    try {
      const res = await API.post("/chat/send", {
        user_id: 1,
        message: currentMessage,
        mode: "guidance",
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: res.data.reply,
          emotion: res.data.emotion,
          risk: res.data.riskLevel,
        },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "I’m having trouble connecting right now. Please try again.",
          emotion: "neutral",
          risk: "Low",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="chatgpt-page">
      <div className="chatgpt-topbar">
        <div>
          <h1>SynthMind AI</h1>
          <p>Private emotional support assistant</p>
        </div>

        <div className="chatgpt-online">
          <span></span>
          Online
        </div>
      </div>

      <div className="chatgpt-window">
        <div className="chatgpt-messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chatgpt-message-row ${
                msg.sender === "user" ? "chatgpt-user-row" : "chatgpt-ai-row"
              }`}
            >
              {msg.sender === "ai" && (
                <div className="chatgpt-avatar chatgpt-ai-avatar">S</div>
              )}

              <div className="chatgpt-message-content">
                <div
                  className={`chatgpt-bubble ${
                    msg.sender === "user"
                      ? "chatgpt-user-bubble"
                      : "chatgpt-ai-bubble"
                  }`}
                >
                  {msg.text}
                </div>

                {msg.sender === "ai" && msg.emotion && (
                  <div className="chatgpt-meta">
                    <span className="chatgpt-pill emotion">
                      Emotion: {msg.emotion}
                    </span>
                    <span
                      className={`chatgpt-pill ${
                        msg.risk === "High"
                          ? "risk-high"
                          : msg.risk === "Medium"
                          ? "risk-medium"
                          : "risk-low"
                      }`}
                    >
                      Risk: {msg.risk}
                    </span>
                  </div>
                )}
              </div>

              {msg.sender === "user" && (
                <div className="chatgpt-avatar chatgpt-user-avatar">You</div>
              )}
            </div>
          ))}

          {loading && (
            <div className="chatgpt-message-row chatgpt-ai-row">
              <div className="chatgpt-avatar chatgpt-ai-avatar">S</div>
              <div className="chatgpt-typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        <div className="chatgpt-input-wrapper">
          <div className="chatgpt-input-box">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Message SynthMind..."
              rows="1"
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage} disabled={loading || !message.trim()}>
              ↑
            </button>
          </div>

          <p className="chatgpt-disclaimer">
            SynthMind can support reflection, but it is not a medical diagnosis tool.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Chat;