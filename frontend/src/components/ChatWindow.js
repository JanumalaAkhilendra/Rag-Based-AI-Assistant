import React, { useState } from "react";
import { chat } from "../api/api";
import Message from "./Message";

export default function ChatWindow({ role }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: "user", text: input }]);
    setLoading(true);
    try {
      const res = await chat(input, role);
      setMessages(msgs => [
        ...msgs,
        {
          sender: "assistant",
          text: res.data.answer,
          references: res.data.references
        }
      ]);
    } catch (e) {
      setMessages(msgs => [
        ...msgs,
        { sender: "assistant", text: "Error: " + e.message }
      ]);
    }
    setInput("");
    setLoading(false);
  };

  return (
    <>
      <div className="chat-box">
        {messages.map((msg, i) => (
          <Message key={i} {...msg} />
        ))}
        {loading && <div><i>Assistant is typing...</i></div>}
      </div>
      <div className="input-row">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Ask about your Gmail, WhatsApp, or Calendar..."
        />
        <button onClick={sendMessage} disabled={loading}>Send</button>
      </div>
    </>
  );
}
