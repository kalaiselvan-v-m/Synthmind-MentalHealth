import { useState, useRef, useEffect } from "react";
import chatBg from "../assets/images/chat-bg.jpg";

const defaultMessages = [
  {
    sender: "ai",
    text: "Hi, I’m SynthMind. What’s on your mind today?",
  },
];

function Chat() {
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("synthChatMessages");
    return saved ? JSON.parse(saved) : defaultMessages;
  });

  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    localStorage.setItem("synthChatMessages", JSON.stringify(messages));
  }, [messages]);

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
      { sender: "ai", text: "", streaming: true },
    ]);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: currentMessage,
          mode: "guidance",
        }),
      });

      if (!response.ok || !response.body) {
        throw new Error("Chat stream failed");
      }

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
            sender: "ai",
            text: aiText,
            streaming: true,
          };

          return updated;
        });
      }

      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          sender: "ai",
          text: aiText,
          streaming: false,
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
          streaming: false,
        };

        return updated;
      });
    }

    setLoading(false);
  };

  const clearLocalChat = () => {
    localStorage.removeItem("synthChatMessages");
    setMessages(defaultMessages);
  };

  return (
    <div className="replika-chat-page">
      <img src={chatBg} alt="" className="replika-chat-bg" />
      <div className="replika-chat-overlay" />

      <header className="replika-chat-header">
        <div>
          <h1>SynthMind</h1>
          <p>Private emotional companion</p>
        </div>

        <div className="replika-status" onClick={clearLocalChat}>
          <span></span>
          Online
        </div>
      </header>

      <main className="replika-chat-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`replika-message-row ${
              msg.sender === "user" ? "user" : "ai"
            }`}
          >
            <div
              className={`replika-bubble ${
                msg.sender === "user" ? "user-bubble" : "ai-bubble"
              }`}
            >
              {msg.text || " "}

              {msg.streaming && <span className="typing-cursor">▋</span>}
            </div>
          </div>
        ))}

        <div ref={chatEndRef} />
      </main>

      <footer className="replika-chat-input-area">
        <div className="replika-input-pill">
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

        <p>SynthMind supports reflection, not medical diagnosis.</p>
      </footer>
    </div>
  );
}

export default Chat;