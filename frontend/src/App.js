import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import RoleSelector from "./components/RoleSelector";
import "./App.css";

function App() {
  const [role, setRole] = useState("me");

  return (
    <div className="container">
      <h2>Personal AI Assistant</h2>
      <RoleSelector role={role} setRole={setRole} />
      <ChatWindow role={role} />
    </div>
  );
}

export default App;
