import { BASE_URL, getAuthHeaders } from "./config.js";
import { showToast } from "./toast.js";

let myList = new Set();

export async function loadMyList() {
  try {
    const res = await fetch(`${BASE_URL}/api/favoritos/`, { headers: getAuthHeaders() });
    if (!res.ok) return;
    const favs = await res.json();
    myList = new Set(favs.map((f) => f.video_isan));
  } catch {
    myList = new Set();
  }
}

export function isFavorite(isan) {
  return myList.has(isan);
}

export async function toggleFavorite(isan, btn = null) {
  const isFav = myList.has(isan);
  const method = isFav ? "DELETE" : "POST";

  const res = await fetch(`${BASE_URL}/api/favoritos/${encodeURIComponent(isan)}`, {
    method,
    headers: getAuthHeaders(),
  });

  if (!res.ok) {
    showToast("No se pudo actualizar Mi Lista", "error");
    return;
  }

  if (isFav) myList.delete(isan);
  else myList.add(isan);

  if (btn) {
    btn.textContent = myList.has(isan) ? "✓" : "+";
    btn.classList.toggle("is-fav", myList.has(isan));
  }

  showToast(myList.has(isan) ? "Agregada a Mi Lista" : "Quitada de Mi Lista", "info");
  return myList.has(isan);
}

export function getMyList() {
  return myList;
}
