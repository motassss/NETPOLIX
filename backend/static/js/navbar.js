import { BASE_URL, getAuthHeaders, logout } from "./config.js";
import { updateCartBadge } from "./carrito-module.js";
import { initMiListaDrawer } from "./mi-lista-drawer.js";

let profileLoaded = false;
let navbarReady = false;

export function initNavbar(options = {}) {
  const { withDrawer = true } = options;
  const navbar = document.getElementById("navbar");
  if (!navbar || navbarReady) return;
  navbarReady = true;

  window.addEventListener(
    "scroll",
    () => navbar.classList.toggle("scrolled", window.scrollY > 50),
    { passive: true }
  );

  document.getElementById("searchToggle")?.addEventListener("click", () => {
    const input = document.getElementById("searchInput");
    if (!input) return;
    input.classList.toggle("open");
    if (input.classList.contains("open")) input.focus();
  });

  document.getElementById("btnLogout")?.addEventListener("click", logout);

  const profile = document.getElementById("navProfile");
  const avatarBtn = document.getElementById("profileAvatar");

  avatarBtn?.addEventListener("click", (e) => {
    e.stopPropagation();
    profile?.classList.toggle("active");
  });

  document.addEventListener("click", (e) => {
    if (profile && !profile.contains(e.target)) profile.classList.remove("active");
  });

  document.getElementById("navMobileToggle")?.addEventListener("click", () => {
    document.getElementById("navbarLinks")?.classList.toggle("mobile-open");
  });

  populateNavProfile();
  updateCartBadge();
  if (withDrawer) initMiListaDrawer();
}

export async function populateNavProfile() {
  const cached = sessionStorage.getItem("netpolix_user");
  if (cached) applyProfile(JSON.parse(cached));

  try {
    const res = await fetch(`${BASE_URL}/auth/me`, { headers: getAuthHeaders() });
    if (!res.ok) return;
    const user = await res.json();
    sessionStorage.setItem("netpolix_user", JSON.stringify(user));
    applyProfile(user);
    profileLoaded = true;
  } catch {
    /* silent */
  }
}

function applyProfile(user) {
  const name = user.nombre || "Usuario";
  const email = user.cedula ? `C.C. ${user.cedula}` : "";
  const initial =
    name
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((p) => p[0].toUpperCase())
      .join("") || "U";

  const set = (id, text) => {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  };

  set("profileAvatar", initial);
  set("dropdownAvatar", initial);
  set("dropdownName", name);
  set("dropdownEmail", email);
}

window.logout = logout;
