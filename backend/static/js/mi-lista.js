import { requireAuth, getAuthHeaders, BASE_URL, logout } from "./config.js";
import { initNavbar } from "./navbar.js";

document.addEventListener("DOMContentLoaded", () => {
  if (!requireAuth()) return;
  initNavbar();
  cargarMiLista();
});

window.logout = logout;

async function cargarMiLista() {
  const grid = document.getElementById("miListaGrid");
  const contador = document.getElementById("listaContador");

  try {
    const res = await fetch(`${BASE_URL}/api/favoritos/`, { headers: getAuthHeaders() });
    if (!res.ok) {
      grid.innerHTML = '<div class="estado-vacio">Error al cargar la lista</div>';
      return;
    }
    const favs = await res.json();

    contador.textContent = `(${favs.length})`;

    if (!favs.length) {
      grid.innerHTML = `<div class="estado-vacio">
        <p>Tu lista está vacía.</p>
        <a href="/dashboard">Explorar películas</a>
      </div>`;
      return;
    }

    grid.innerHTML = "";

    for (const f of favs) {
      const vr = await fetch(`${BASE_URL}/videos/${encodeURIComponent(f.video_isan)}`, {
        headers: getAuthHeaders(),
      });
      if (vr.ok) {
        grid.appendChild(renderMiListaCard(await vr.json()));
      }
    }
  } catch {
    grid.innerHTML = '<div class="estado-vacio">Error al cargar la lista</div>';
  }
}

function renderMiListaCard(movie) {
  const card = document.createElement("div");
  card.className = "movie-card";
  card.dataset.isan = movie.isan;
  card.innerHTML = `
    <img src="${movie.imagen_url || "/static/img/placeholder.jpg"}"
         alt="${movie.titulo_original}"
         onerror="this.src='/static/img/placeholder.jpg'">
    <div class="card-overlay">
      <div class="card-title">${movie.titulo_original}</div>
      <div class="card-meta">${movie.anio_produccion || ""} · ${movie.duracion || ""} min</div>
      <button class="card-btn quitar-btn" type="button">Quitar</button>
    </div>`;

  card.querySelector(".quitar-btn")?.addEventListener("click", async (e) => {
    e.stopPropagation();
    await quitarDeLista(movie.isan, card);
  });

  card.addEventListener("click", () => {
    window.location.href = `/dashboard?modal=${movie.isan}`;
  });

  return card;
}

async function quitarDeLista(isan, cardElement) {
  const res = await fetch(`${BASE_URL}/api/favoritos/${encodeURIComponent(isan)}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (res.ok) {
    cardElement.style.transition = "opacity 0.3s ease, transform 0.3s ease";
    cardElement.style.opacity = "0";
    cardElement.style.transform = "scale(0.8)";
    setTimeout(() => {
      cardElement.remove();
      actualizarContador();
    }, 300);
  }
}

function actualizarContador() {
  const grid = document.getElementById("miListaGrid");
  const contador = document.getElementById("listaContador");
  const cards = grid.querySelectorAll(".movie-card");
  contador.textContent = `(${cards.length})`;

  if (cards.length === 0) {
    grid.innerHTML = `<div class="estado-vacio">
      <p>Tu lista está vacía.</p>
      <a href="/dashboard">Explorar películas</a>
    </div>`;
  }
}
