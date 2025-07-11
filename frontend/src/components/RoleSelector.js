import React from "react";
const roles = ["me", "teacher", "mom"];

export default function RoleSelector({ role, setRole }) {
  return (
    <select className="select-role" value={role} onChange={e => setRole(e.target.value)}>
      {roles.map(r => <option key={r} value={r}>{r}</option>)}
    </select>
  );
}
