import React from "react";

export default function Message({ sender, text, references }) {
  return (
    <div className={`message ${sender}`}>
      <b>{sender}:</b> {text}
      {references && references.length > 0 && (
        <ul className="references">
          {references.map((ref, i) => (
            <li key={i}>
              {ref.source}
              {ref.sender && ` | ${ref.sender}`}
              {ref.date && ` | ${ref.date}`}
              {ref.summary && ` | ${ref.summary}`}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
