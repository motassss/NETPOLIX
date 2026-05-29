export const BASE_URL = window.location.origin;
export const TOKEN_KEY = "netpolix_token";

export function getAuthHeaders() {
  const token = localStorage.getItem(TOKEN_KEY);
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}

export function requireAuth() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) {
    window.location.href = "/login";
    return false;
  }
  return true;
}

export function logout() {
  try {
    fetch(`${BASE_URL}/auth/logout`, { method: "POST" }).catch(() => {});
  } catch {
    /* no endpoint required */
  }

  localStorage.clear();
  sessionStorage.clear();

  document.cookie.split(";").forEach((c) => {
    const name = c.split("=")[0].trim();
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
  });

  window.location.href = "/login";
}

export function formatPrice(amount) {
  return `$${Number(amount).toFixed(2)}`;
}

export function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("es-CO", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}
