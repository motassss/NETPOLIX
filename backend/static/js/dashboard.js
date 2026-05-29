import { BASE_URL, requireAuth, getAuthHeaders, formatPrice } from "./config.js";
import { initNavbar } from "./navbar.js";
import { initModal, openModal } from "./modal.js";
import { renderCategorySection } from "./cards.js";
import { loadRentas } from "./rentas.js";
import { loadMyList } from "./favoritos.js";
import { addToCart } from "./carrito-module.js";
import { checkRenta } from "./rentas.js";
import { playMovie } from "./modal.js";

const CATEGORIAS_A_MOSTRAR = [
  { key: "tendencias", label: "🔥 Tendencias", id: "cat-tendencias" },
  { key: "Accion", label: "💥 Acción", id: "cat-accion" },
  { key: "Ciencia Ficcion", label: "🚀 Ciencia Ficción", id: "cat-scifi" },
  { key: "Terror", label: "👻 Terror", id: "cat-terror" },
  { key: "Drama", label: "🎭 Drama", id: "cat-drama" },
  { key: "Comedia", label: "😄 Comedia", id: "cat-comedia" },
];

let heroMovie = null;

document.addEventListener("DOMContentLoaded", async () => {
  if (!requireAuth()) return;

  initNavbar({ withDrawer: true });
  initModal();

  await loadMyList();
  await loadRentas();
  await loadHero();
  await loadAllCategories();
  setupSearch();
  handleDeepLink();
  handleNavAnchors();
});

async function loadHero() {
  try {
    const res = await fetch(`${BASE_URL}/videos/tendencias`, { headers: getAuthHeaders() });
    const movies = await res.json();
    if (!movies.length) return;

    heroMovie = movies[0];
    const hero = document.querySelector(".hero");

    document.getElementById("heroTitle").textContent = heroMovie.titulo_original;
    document.getElementById("heroDesc").textContent = heroMovie.descripcion || "";
    document.getElementById("heroYear").textContent = heroMovie.anio_produccion || "";
    document.getElementById("heroDuration").textContent = heroMovie.duracion ? `${heroMovie.duracion} min` : "";

    const precio = heroMovie.precio_renta ?? 3.99;
    const priceEl = document.getElementById("heroPrice");
    if (priceEl) {
      priceEl.innerHTML = `${formatPrice(precio)} <span>/ 30 días</span>`;
    }

    if (heroMovie.imagen_url && hero) {
      hero.style.backgroundImage = `url('${heroMovie.imagen_url}')`;
    }

    await renderHeroButtons(heroMovie);
  } catch {
    /* silent */
  }
}

async function renderHeroButtons(movie) {
  const primary = document.getElementById("heroPrimary");
  const secondary = document.getElementById("heroSecondary");
  const precio = movie.precio_renta ?? 3.99;
  const status = await checkRenta(movie.isan);

  if (status.rentada) {
    primary.textContent = "▶ Reproducir ahora";
    primary.className = "hero-btn hero-btn-play";
    primary.onclick = () => playMovie(movie);
  } else {
    primary.textContent = `🛒 Rentar — ${formatPrice(precio)}`;
    primary.className = "hero-btn hero-btn-primary";
    primary.onclick = async () => {
      await addToCart(movie.isan);
      openModal(movie);
    };
  }

  secondary.textContent = "ⓘ Más info";
  secondary.className = "hero-btn hero-btn-secondary";
  secondary.onclick = () => openModal(movie);
}

async function loadAllCategories() {
  const container = document.getElementById("categorias-container");
  container.innerHTML = "";

  for (const cat of CATEGORIAS_A_MOSTRAR) {
    try {
      const endpoint =
        cat.key === "tendencias"
          ? `${BASE_URL}/videos/tendencias`
          : `${BASE_URL}/videos/categoria/${encodeURIComponent(cat.key)}`;

      const res = await fetch(endpoint, { headers: getAuthHeaders() });
      if (!res.ok) continue;
      const movies = await res.json();
      if (!movies.length) continue;

      const section = renderCategorySection(cat.label, movies);
      section.id = cat.id;
      container.appendChild(section);
    } catch {
      /* skip */
    }
  }
}

function setupSearch() {
  const input = document.getElementById("searchInput");
  if (!input) return;
  let timeout;
  input.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(async () => {
      const q = input.value.trim();
      if (!q) {
        await loadAllCategories();
        return;
      }
      try {
        const res = await fetch(`${BASE_URL}/videos/buscar?q=${encodeURIComponent(q)}`, {
          headers: getAuthHeaders(),
        });
        const movies = await res.json();
        const container = document.getElementById("categorias-container");
        container.innerHTML = "";
        if (!movies.length) {
          container.innerHTML = '<p class="empty-msg">No se encontraron resultados.</p>';
          return;
        }
        container.appendChild(renderCategorySection(`Resultados para "${q}"`, movies));
      } catch {
        /* silent */
      }
    }, 400);
  });
}

function handleNavAnchors() {
  const hash = window.location.hash;
  if (hash) {
    setTimeout(() => {
      document.querySelector(hash)?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 600);
  }
}

async function handleDeepLink() {
  const params = new URLSearchParams(window.location.search);
  const isan = params.get("modal");
  if (!isan) return;
  try {
    const res = await fetch(`${BASE_URL}/videos/${encodeURIComponent(isan)}`, {
      headers: getAuthHeaders(),
    });
    if (res.ok) openModal(await res.json());
  } catch {
    /* silent */
  }
}
