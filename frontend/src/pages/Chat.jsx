import { useState, useRef, useEffect } from "react";
import chatBg from "../assets/images/chat-bg.jpg";

const greetings = [
  "hey, glad you came back.",
  "heyy. how’s your head feeling today?",
  "good to see you again honestly.",
  "yo. what’s been on your mind lately?",
  "hey :) how’s life treating you today?",
  "welcome back. how are you feeling rn?",
  "hey, what’s been going on lately?",
  "you made it back 😭 how are you doing?",
];

const createDefaultMessages = () => [
  {
    sender: "ai",
    text: greetings[new Date().getDate() % greetings.length],
    streaming: false,
    timestamp: new Date().toISOString(),
  },
];

function Chat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState(createDefaultMessages);
  const [loading, setLoading] = useState(false);

  const [crisisState, setCrisisState] = useState({
  visible: false,
  riskLevel: "LOW",
  response: "",
});
  
  const [groundingOpen, setGroundingOpen] = useState(false);

  const groundingSteps = [
    "Breathe in slowly for 4 seconds.",
    "Hold your breath gently for 4 seconds.",
    "Exhale slowly for 6 seconds.",
    "Relax your shoulders.",
    "Focus on one thing you can see nearby.",
  ];

  const [groundingStep, setGroundingStep] = useState(0);

  const chatEndRef = useRef(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchChatHistory();

    const handleHistoryClear = () => {
      localStorage.removeItem("synthChatMessages");
      setMessages(createDefaultMessages());
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
  if (!groundingOpen) return;

  if (groundingStep >= groundingSteps.length - 1)
    return;

  const timer = setTimeout(() => {
    setGroundingStep((prev) => prev + 1);
  }, 4000);

  return () => clearTimeout(timer);

}, [groundingStep, groundingOpen]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
  if (!groundingOpen) return;

  if (groundingStep >= groundingSteps.length - 1)
    return;

  const timer = setTimeout(() => {
    setGroundingStep((prev) => prev + 1);
  }, 4000);

  return () => clearTimeout(timer);

}, [groundingStep, groundingOpen]);

  const formatTime = (timestamp) => {
    if (!timestamp) return "";

    return new Date(timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const fetchChatHistory = async () => {
    try {
      if (!token) {
        setMessages(createDefaultMessages());
        return;
      }

      const res = await fetch("http://127.0.0.1:8000/chat/history", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      if (!res.ok || !Array.isArray(data) || data.length === 0) {
        setMessages(createDefaultMessages());
        return;
      }

      const formattedMessages = data
        .reverse()
        .flatMap((chat) => [
          {
            sender: "user",
            text: chat.message,
            streaming: false,
            timestamp: chat.created_at,
          },
          {
            sender: "ai",
            text: chat.response,
            streaming: false,
            timestamp: chat.created_at,
          },
        ]);

      setMessages([createDefaultMessages()[0], ...formattedMessages]);
    } catch (err) {
      console.error("History fetch error:", err);

      const saved = localStorage.getItem("synthChatMessages");

      if (saved) {
        const parsed = JSON.parse(saved).map((msg) => ({
          ...msg,
          streaming: false,
          timestamp: msg.timestamp || new Date().toISOString(),
        }));

        setMessages(parsed);
      } else {
        setMessages(createDefaultMessages());
      }
    }
  };

  const updateLastAiMessage = (text, streaming) => {
    setMessages((prev) => {
      const updated = [...prev];

      updated[updated.length - 1] = {
        ...updated[updated.length - 1],
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
    const now = new Date().toISOString();

    setMessage("");

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentMessage,
        streaming: false,
        timestamp: now,
      },
      {
        sender: "ai",
        text: "",
        streaming: true,
        timestamp: new Date().toISOString(),
      },
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

      const riskCheck = await fetch(
  "http://127.0.0.1:8000/chat/latest-meta",
  {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
);

const riskData = await riskCheck.json();

if (
  riskData.riskLevel === "HIGH" ||
  riskData.riskLevel === "CRITICAL"
) {
  setCrisisState({
    visible: true,
    riskLevel: riskData.riskLevel,
    response:
      riskData.riskLevel === "CRITICAL"
        ? "You seem like you may be in a really heavy moment right now."
        : "You seem emotionally overwhelmed right now.",
  });
}

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          updateLastAiMessage(
            aiText.trim() || "I’m here. say that again once?",
            false
          );
          setLoading(false);
          break;
        }

        const chunk = decoder.decode(value, { stream: true });

        if (chunk.startsWith("__CRISIS__")) {

          try {
            const jsonText = chunk
              .replace("__CRISIS__", "")
              .trim();

            const crisisData = JSON.parse(
              jsonText.replaceAll("'", '"')
            );

            setCrisisState({
              visible: true,
              riskLevel: crisisData.riskLevel,
              response: crisisData.response,
            });

          } catch (err) {
            console.error("Crisis parse error:", err);
          }

          continue;
        }

        if (!chunk) continue;

        for (let char of chunk) {
          aiText += char;
          updateLastAiMessage(aiText, true);

          await new Promise((resolve) => setTimeout(resolve, 8));
        }
      }
    } catch (err) {
      console.error(err);

      updateLastAiMessage(
        "I’m having trouble connecting right now. Please try again.",
        false
      );

      setLoading(false);
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
      setMessages(createDefaultMessages());
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

            <div className="chat-date-divider">
  {new Date().toLocaleDateString([], {
    weekday: "long",
    month: "long",
    day: "numeric",
  })}
</div>
            <div className="chat-message-wrapper">
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

            <div
              className={`chat-time ${
                msg.sender === "user"
                  ? "user-time"
                  : "ai-time"
              }`}
            >
              {formatTime(msg.timestamp)}
            </div>
          </div>
                    </div>
                  ))}

        <div ref={chatEndRef} />
      </main>

      {crisisState.visible && (
  <div className="synth-crisis-card">

    <div className="synth-crisis-glow"></div>

    <h3>
      {crisisState.riskLevel === "CRITICAL"
        ? "Stay with us for a second."
        : "You don’t have to carry this alone."}
    </h3>

    <p>
      {crisisState.response}
    </p>

    <div className="synth-crisis-actions">

      <button
       onClick={() => {
        setGroundingOpen(true);

        setGroundingStep(0);

        setCrisisState({
          ...crisisState,
          visible: false,
        });
      }}
      >
        Ground me
      </button>

      <button
        onClick={async () => {
          try {
            const res = await fetch(
              "http://127.0.0.1:8000/trusted-contact/notify-preview",
              {
                method: "POST",
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );

            const data = await res.json();

            alert(data.message);
          } catch (err) {
            console.error(err);
            alert("Unable to prepare trusted contact notification.");
          }
        }}
      >
        Notify trusted contact
      </button>

      <button
        onClick={() => {
          setGroundingOpen(true);

          setGroundingStep(0);

          setCrisisState({
            ...crisisState,
            visible: false,
          });
        }}
      >
        Not now
      </button>

    </div>

  </div>
)} 
{groundingOpen && (

  <div className="synth-grounding-overlay">

    <div className="synth-grounding-card">

      <div className="grounding-pulse"></div>

      <small>Grounding exercise</small>

      <h2>
        Take this one moment slowly.
      </h2>

      <p>
        {groundingSteps[groundingStep]}
      </p>

      <div className="grounding-progress">

        {groundingSteps.map((_, index) => (
          <span
            key={index}
            className={
              index <= groundingStep
                ? "active"
                : ""
            }
          />
        ))}

      </div>

      <button
        onClick={async () => {

          try {
            await fetch(
              "http://127.0.0.1:8000/crisis-support/grounding-complete",
              {
                method: "POST",
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );
          } catch (err) {
            console.error(err);
          }

          setGroundingOpen(false);
        }}
      >
        I feel a little calmer
      </button>

    </div>

  </div>

)}

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