import axios from "axios";

const client = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export async function doResearch(question) {
  const response = await client.post("/research", { question });
  return response.data;
}

export async function listSessions() {
  const response = await client.get("/sessions");
  return response.data;
}

export async function sendChatMessage(sessionId, message) {
  const response = await client.post("/chat", { session_id: sessionId, message });
  return response.data;
}