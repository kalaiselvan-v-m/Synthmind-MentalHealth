import { useState, useRef, useEffect } from "react";

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

  const token = localStorage.getItem("token"); // 🔥 JWT

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    if (!token) {
      alert("Please login first");
      return;
    }

    const currentMessage = message;
    setMessage("");

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: currentMessage },
      {
        sender: "ai",
        text: "",
        emotion: "streaming",
        risk: "Low",
      },
    ]);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // 🔥 JWT added
        },
        body: JSON.stringify({
          message: currentMessage,
          mode: "guidance",
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let aiText = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        aiText += chunk;

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            text: aiText,
          };
          return updated;
        });
      }

      // 🔥 FIXED: JWT meta call (no user_id now)
      const metaRes = await fetch("http://127.0.0.1:8000/chat/latest-meta", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const meta = await metaRes.json();

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          emotion: meta.emotion || "neutral",
          risk: meta.riskLevel || "Low",
        };
        return updated;
      });

    } catch (err) {
      console.error(err);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          sender: "ai",
          text: "I’m having trouble connecting right now. Please try again.",
          emotion: "neutral",
          risk: "Low",
        };
        return updated;
      });
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
                  {msg.text || " "}

                  {msg.emotion === "streaming" && (
                    <span className="typing-cursor">▋</span>
                  )}
                </div>

                {msg.sender === "ai" &&
                  msg.emotion &&
                  msg.emotion !== "streaming" && (
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
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
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