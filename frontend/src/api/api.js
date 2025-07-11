import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://127.0.0.1:8000";

export const chat = (query, role) =>
  axios.post(`${API_BASE}/chat`, { query, role });

export const ingest = (source) =>
  axios.post(`${API_BASE}/ingest`, { source });

export const getSources = () =>
  axios.get(`${API_BASE}/sources`);