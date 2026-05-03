import { useState, useRef, useEffect } from "react";
import API from "../api/api";

function Chat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hi, I’m SynthMind. You can talk to me about what’s on your mind.",
      emotion: "neutral",
      risk: "Low"
    }
  ]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const currentMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentMessage
      }
    ]);

    setMessage("");
    setLoading(true);

    try {
      const res = await API.post("/chat/send", {
        user_id: 1,
        message: currentMessage,
        mode: "guidance"
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: res.data.reply,
          emotion: res.data.emotion,
          risk: res.data.riskLevel
        }
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "I’m having trouble connecting right now. Please try again."
        }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="chat-page">
      <div className="chat-header">
        <div>
          <h1>SynthMind AI</h1>
          <p>Private emotional support chat</p>
        </div>

        <div className="chat-status">
          <span className="status-dot"></span>
          Online
        </div>
      </div>

      <div className="chat-shell">
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message-row ${
                msg.sender === "user" ? "user-row" : "ai-row"
              }`}
            >
              {msg.sender === "ai" && (
                <div className="avatar ai-avatar">S</div>
              )}

              <div
                className={`message-bubble ${
                  msg.sender === "user" ? "user-bubble" : "ai-bubble"
                }`}
              >
                <p>{msg.text}</p>

                {msg.sender === "ai" && msg.emotion && (
                  <div className="message-tags">
                    <span className="tag emotion-tag">
                      Emotion: {msg.emotion}
                    </span>
                    <span
                      className={`tag ${
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
                <div className="avatar user-avatar">You</div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message-row ai-row">
              <div className="avatar ai-avatar">S</div>
              <div className="typing-bubble">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        <div className="chat-input-area">
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
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;