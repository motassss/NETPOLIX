import { BASE_URL, getAuthHeaders } from "./config.js";
import { showToast } from "./toast.js";

export async function updateCartBadge() {
  const badge = document.getElementById("cartBadge") || document.getElementById("cart-count");
  if (!badge) return 0;

  try {
    const res = await fetch(`${BASE_URL}/api/carrito/`, { headers: getAuthHeaders() });
    if (!res.ok) return 0;
    const data = await res.json();
    const count = data.count ?? data.items?.length ?? 0;
    badge.textContent = count;
    badge.style.display = count > 0 ? "flex" : "none";
    return count;
  } catch {
    return 0;
  }
}

export async function addToCart(videoIsan) {
  const res = await fetch(`${BASE_URL}/api/carrito/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ video_isan: videoIsan }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    showToast(data.detail || "No se pudo agregar al carrito", "error");
    return false;
  }
  showToast("Agregada al carrito", "success");
  await updateCartBadge();
  return true;
}

export async function removeFromCart(videoIsan) {
  const res = await fetch(`${BASE_URL}/api/carrito/${encodeURIComponent(videoIsan)}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    showToast("No se pudo eliminar", "error");
    return false;
  }
  showToast("Eliminada del carrito", "info");
  await updateCartBadge();
  return true;
}

export async function processPayment() {
  const res = await fetch(`${BASE_URL}/api/rentas/pagar`, {
    method: "POST",
    headers: getAuthHeaders(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    showToast(data.detail || "Error al procesar el pago", "error");
    return null;
  }
  await updateCartBadge();
  return data;
}
