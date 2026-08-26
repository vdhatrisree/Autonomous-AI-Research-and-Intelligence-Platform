import { useState } from "react";
import { sendChatMessage } from "../api/client";

function ChatBox({ sessionId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    const response = await sendChatMessage(sessionId, input);
    setMessages((prev) => [...prev, { role: "bot", text: response.response }]);
  };

  return (
    <div className="chat-box">
      <h3>Appended Notes — File No. {sessionId}</h3>
      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role}`}>{m.text}</div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Add a note to this file..."
      />
      <button onClick={handleSend}>Add Note</button>
    </div>
  );
}

export default ChatBox;