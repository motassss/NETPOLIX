import { BASE_URL, getAuthHeaders } from "./config.js";

let rentaIds = new Set();

export async function loadRentas() {
  try {
    const res = await fetch(`${BASE_URL}/api/rentas/`, { headers: getAuthHeaders() });
    if (!res.ok) return [];
    const rentas = await res.json();
    rentaIds = new Set(rentas.map((r) => r.video_isan));
    return rentas;
  } catch {
    return [];
  }
}

export function getRentaIds() {
  return rentaIds;
}

export function isRented(videoIsan) {
  return rentaIds.has(videoIsan);
}

export async function checkRenta(videoIsan) {
  try {
    const res = await fetch(`${BASE_URL}/api/rentas/verificar/${encodeURIComponent(videoIsan)}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) return { rentada: false, expira_en: null };
    const data = await res.json();
    if (data.rentada) rentaIds.add(videoIsan);
    return data;
  } catch {
    return { rentada: false, expira_en: null };
  }
}
