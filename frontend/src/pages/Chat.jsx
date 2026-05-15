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
  const [messages, setMessages] = useState(defaultMessages);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchChatHistory();

    const handleHistoryClear = () => {
      localStorage.removeItem("synthChatMessages");
      setMessages(defaultMessages);
    };

    window.addEventListener("chatHistoryCleared", handleHistoryClear);

    return () => {
      window.removeEventListener("chatHistoryCleared", handleHistoryClear);
    };
  }, []);

  useEffect(() => {
    localStorage.setItem("synthChatMessages", JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const fetchChatHistory = async () => {
    try {
      if (!token) {
        setMessages(defaultMessages);
        return;
      }

      const res = await fetch("http://127.0.0.1:8000/chat/history", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      if (!res.ok || !Array.isArray(data) || data.length === 0) {
        setMessages(defaultMessages);
        return;
      }

      const formattedMessages = data
        .reverse()
        .flatMap((chat) => [
          {
            sender: "user",
            text: chat.message,
          },
          {
            sender: "ai",
            text: chat.response,
            streaming: false,
          },
        ]);

      setMessages([defaultMessages[0], ...formattedMessages]);
    } catch (err) {
      console.error("History fetch error:", err);

      const saved = localStorage.getItem("synthChatMessages");

      if (saved) {
        const parsed = JSON.parse(saved).map((msg) => ({
          ...msg,
          streaming: false,
        }));

        setMessages(parsed);
      } else {
        setMessages(defaultMessages);
      }
    }
  };

  const updateLastAiMessage = (text, streaming) => {
    setMessages((prev) => {
      const updated = [...prev];

      updated[updated.length - 1] = {
        sender: "ai",
        text,
        streaming,
      };

      return updated;
    });
  };

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    if (!token) {
      alert("Please login first");
      return;
    }

    const currentMessage = message.trim();
    setMessage("");

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: currentMessage, streaming: false },
      { sender: "ai", text: "", streaming: true },
    ]);

    setLoading(true);

    let aiText = "";

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

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
            setLoading(false);

            updateLastAiMessage(
              aiText.trim() || "I’m here. say that again once?",
              false
            );
            break;
        }

        const chunk = decoder.decode(value, { stream: true });

        if (!chunk) continue;

        aiText += chunk;

        updateLastAiMessage(aiText, true);
      }
    } catch (err) {
      console.error(err);

      updateLastAiMessage(
        "I’m having trouble connecting right now. Please try again.",
        false
      );
    }
  };

  const clearLocalChat = async () => {
    try {
      if (token) {
        await fetch("http://127.0.0.1:8000/chat/history", {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      }

      localStorage.removeItem("synthChatMessages");
      setMessages(defaultMessages);
      window.dispatchEvent(new Event("chatHistoryCleared"));
    } catch (err) {
      console.error("Clear chat error:", err);
    }
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

        <button className="replika-status" onClick={clearLocalChat}>
          <span></span>
          Clear chat
        </button>
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
          msg.sender === "user"
            ? "user-bubble"
            : "ai-bubble"
        }`}
      >
        {msg.streaming && !msg.text ? (
          <div className="synthmind-thinking">
            <span></span>
            <span></span>
            <span></span>
          </div>
        ) : (
          msg.text || " "
        )}
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