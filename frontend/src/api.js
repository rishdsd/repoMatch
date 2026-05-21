import axios from "axios";

const BASE = "http://localhost:8000";

export async function sendAnswer(answers, latestStageId, latestAnswer) {
  const res = await axios.post(`${BASE}/chat`, {
    answers,
    latest_stage_id: latestStageId,
    latest_answer: latestAnswer
  });
  return res.data;
}