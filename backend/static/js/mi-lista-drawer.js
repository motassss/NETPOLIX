import { BASE_URL, getAuthHeaders } from "./config.js";
import { openModal } from "./modal.js";
import { loadMyList, getMyList } from "./favoritos.js";
import { showToast } from "./toast.js";

let drawerBound = false;

export function initMiListaDrawer() {
  if (drawerBound) return;
  drawerBound = true;

  document.getElementById("btnMiLista")?.addEventListener("click", (e) => {
    e.preventDefault();
    openMiLista();
  });

  document.getElementById("drawerClose")?.addEventListener("click", closeMiLista);
  document.getElementById("drawerOverlay")?.addEventListener("click", closeMiLista);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.getElementById("miListaDrawer")?.classList.contains("active")) {
      closeMiLista();
    }
  });
}

export function openMiLista() {
  document.getElementById("miListaDrawer")?.classList.add("active");
  document.getElementById("drawerOverlay")?.classList.add("active");
  document.body.style.overflow = "hidden";
  loadMiListaDrawer();
}

export function closeMiLista() {
  document.getElementById("miListaDrawer")?.classList.remove("active");
  document.getElementById("drawerOverlay")?.classList.remove("active");
  document.body.style.overflow = "";
}

async function loadMiListaDrawer() {
  const content = document.getElementById("drawerContent");
  const empty = document.getElementById("drawerEmpty");
  if (!content || !empty) return;

  content.style.display = "flex";
  empty.classList.remove("visible");
  content.innerHTML = '<p class="drawer-loading">Cargando...</p>';

  await loadMyList();

  try {
    const res = await fetch(`${BASE_URL}/api/favoritos/`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error();
    const favoritos = await res.json();

    if (!favoritos.length) {
      content.style.display = "none";
      empty.classList.add("visible");
      return;
    }

    content.innerHTML = "";
    content.style.display = "flex";

    for (const fav of favoritos) {
      const vr = await fetch(`${BASE_URL}/videos/${encodeURIComponent(fav.video_isan)}`, {
        headers: getAuthHeaders(),
      });
      if (!vr.ok) continue;
      const movie = await vr.json();
      content.appendChild(renderDrawerCard(movie));
    }

    if (!content.children.length) {
      content.style.display = "none";
      empty.classList.add("visible");
    }
  } catch {
    content.innerHTML = '<p class="drawer-loading">Error al cargar</p>';
  }
}

function renderDrawerCard(movie) {
  const card = document.createElement("div");
  card.className = "drawer-movie-card";
  card.id = `drawer-card-${movie.isan}`;

  const genero = movie.categorias?.map((c) => c.nombre).join(", ") || "";

  card.innerHTML = `
    <img class="drawer-movie-poster" src="${movie.imagen_url || "/static/img/placeholder.jpg"}" alt="${movie.titulo_original}" onerror="this.src='/static/img/placeholder.jpg'">
    <div class="drawer-movie-info">
      <p class="drawer-movie-title">${movie.titulo_original}</p>
      <p class="drawer-movie-meta">${movie.anio_produccion || ""} · ${genero}</p>
      <div class="drawer-movie-actions">
        <button type="button" class="drawer-btn-ver">▶ Ver</button>
        <button type="button" class="drawer-btn-quitar">✕ Quitar</button>
      </div>
    </div>`;

  card.querySelector(".drawer-btn-ver")?.addEventListener("click", () => {
    closeMiLista();
    openModal(movie);
  });

  card.querySelector(".drawer-btn-quitar")?.addEventListener("click", () => {
    quitarDeLista(movie.isan, card);
  });

  return card;
}

async function quitarDeLista(isan, card) {
  card.style.opacity = "0";
  card.style.transform = "translateX(20px)";

  setTimeout(async () => {
    const res = await fetch(`${BASE_URL}/api/favoritos/${encodeURIComponent(isan)}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });

    if (res.ok) {
      getMyList().delete(isan);
      card.remove();
      showToast("Quitada de Mi Lista", "info");

      const content = document.getElementById("drawerContent");
      const empty = document.getElementById("drawerEmpty");
      if (content && !content.children.length) {
        content.style.display = "none";
        empty?.classList.add("visible");
      }
    } else {
      card.style.opacity = "1";
      card.style.transform = "";
      showToast("No se pudo quitar", "error");
    }
  }, 280);
}

window.openMiLista = openMiLista;
window.closeMiLista = closeMiLista;
