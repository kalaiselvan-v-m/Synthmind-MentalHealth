import Badge from "./Badge";

function ChatBubble({ message }) {
  const isUser = message.sender === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[75%] rounded-2xl px-4 py-3 ${
        isUser
          ? "bg-purple-600 text-white rounded-br-sm"
          : "bg-white/10 border border-white/10 text-gray-100 rounded-bl-sm"
      }`}>
        <p className="leading-relaxed">{message.text}</p>

        {!isUser && (
          <div className="flex gap-2 mt-3 flex-wrap">
            {message.emotion && <Badge label={`Emotion: ${message.emotion}`} type="emotion" />}
            {message.risk && <Badge label={`Risk: ${message.risk}`} type={message.risk.toLowerCase()} />}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatBubble;