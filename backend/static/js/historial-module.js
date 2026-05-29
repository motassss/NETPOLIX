import { BASE_URL, getAuthHeaders } from "./config.js";

export async function registrarVista(videoIsan) {
  const res = await fetch(`${BASE_URL}/api/historial/${encodeURIComponent(videoIsan)}`, {
    method: "POST",
    headers: getAuthHeaders(),
  });
  return res.ok;
}
