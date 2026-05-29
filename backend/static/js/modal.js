import { formatPrice, formatDate } from "./config.js";
import { checkRenta } from "./rentas.js";
import { addToCart } from "./carrito-module.js";
import { toggleFavorite, isFavorite } from "./favoritos.js";
import { registrarVista } from "./historial-module.js";
import { showToast } from "./toast.js";

let currentMovie = null;
let escHandler = null;
let modalInitialized = false;

export function initModal() {
  if (modalInitialized) return;
  modalInitialized = true;

  const modal = document.getElementById("movieModal");
  const backdrop = modal?.querySelector(".modal-backdrop");
  const closeBtn = modal?.querySelector(".modal-close");

  backdrop?.addEventListener("click", closeModal);
  closeBtn?.addEventListener("click", closeModal);

  escHandler = (e) => {
    if (e.key === "Escape") closeModal();
  };
  document.addEventListener("keydown", escHandler);
}

export async function openModal(movie) {
  initModal();
  currentMovie = movie;

  const rentaStatus = await checkRenta(movie.isan);
  renderModal(movie, rentaStatus);

  document.getElementById("movieModal")?.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function renderModal(movie, rentaStatus) {
  const img = document.getElementById("modalImg");
  const title = document.getElementById("modalTitle");
  const year = document.getElementById("modalYear");
  const duration = document.getElementById("modalDuration");
  const type = document.getElementById("modalType");
  const desc = document.getElementById("modalDesc");
  const actions = document.getElementById("modalActions");
  const notice = document.getElementById("modalNotice");
  const trailer = document.getElementById("modalTrailer");

  if (img) {
    img.src = movie.imagen_url || "/static/img/placeholder.jpg";
    img.alt = movie.titulo_original;
  }
  if (title) title.textContent = movie.titulo_original;
  if (year) year.textContent = movie.anio_produccion || "";
  if (duration) duration.textContent = movie.duracion ? `${movie.duracion} min` : "";
  if (type) type.textContent = movie.tipo || "Película";
  if (desc) desc.textContent = movie.descripcion || "Sin descripción disponible.";

  const precio = movie.precio_renta ?? 3.99;
  const cats = movie.categorias?.map((c) => c.nombre).join(", ") || "";

  if (trailer) {
    if (movie.trailer_url) {
      trailer.href = movie.trailer_url;
      trailer.classList.remove("hidden");
    } else {
      trailer.classList.add("hidden");
    }
  }

  if (!actions) return;

  if (rentaStatus.rentada) {
    actions.innerHTML = `
      <button class="btn-play active" id="modalPlayBtn">▶ Reproducir</button>
      <button class="btn-wishlist ${isFavorite(movie.isan) ? "is-fav" : ""}" id="modalFavBtn">
        ${isFavorite(movie.isan) ? "✓ En Mi Lista" : "+ Mi Lista"}
      </button>
      <div class="rental-expiry">
        Acceso hasta: <strong>${formatDate(rentaStatus.expira_en)}</strong>
      </div>`;
    if (notice) {
      notice.textContent = cats ? `Géneros: ${cats}` : "";
      notice.classList.remove("hidden");
    }

    document.getElementById("modalPlayBtn")?.addEventListener("click", () => playMovie(movie));
    document.getElementById("modalFavBtn")?.addEventListener("click", async () => {
      await toggleFavorite(movie.isan);
      const btn = document.getElementById("modalFavBtn");
      if (btn) {
        btn.textContent = isFavorite(movie.isan) ? "✓ En Mi Lista" : "+ Mi Lista";
        btn.classList.toggle("is-fav", isFavorite(movie.isan));
      }
    });
  } else {
    actions.innerHTML = `
      <div class="rental-price">
        <span class="price-tag">${formatPrice(precio)}</span>
        <span class="price-label">/ 30 días</span>
      </div>
      <button class="btn-rent" id="modalRentBtn">🛒 Agregar al carrito</button>
      <button class="btn-play locked" type="button" disabled>🔒 Renta para ver</button>`;
    if (notice) {
      notice.textContent = "Esta película requiere renta. Agrégala al carrito y completa el pago para desbloquearla.";
      notice.classList.remove("hidden");
    }

    document.getElementById("modalRentBtn")?.addEventListener("click", async () => {
      const ok = await addToCart(movie.isan);
      if (ok) {
        const btn = document.getElementById("modalRentBtn");
        if (btn) {
          btn.textContent = "✓ En el carrito";
          btn.disabled = true;
        }
      }
    });
  }
}

export function closeModal() {
  document.getElementById("movieModal")?.classList.add("hidden");
  document.body.style.overflow = "";
  currentMovie = null;
}

export async function playMovie(movie) {
  const m = movie || currentMovie;
  if (!m) return;

  const status = await checkRenta(m.isan);
  if (!status.rentada) {
    showToast("Debes rentar esta película primero", "error");
    return;
  }

  await registrarVista(m.isan);
  showPlayer(m);
}

function showPlayer(movie) {
  let overlay = document.getElementById("playerOverlay");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "playerOverlay";
    overlay.className = "player-overlay";
    overlay.innerHTML = `
      <div class="player-header">
        <span class="player-title" id="playerTitle"></span>
        <button class="player-close" id="playerClose" aria-label="Cerrar">✕</button>
      </div>
      <div class="player-screen">
        <div class="player-icon">▶</div>
        <p class="player-msg" id="playerMsg"></p>
      </div>`;
    document.body.appendChild(overlay);
    document.getElementById("playerClose")?.addEventListener("click", hidePlayer);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !overlay.classList.contains("hidden")) hidePlayer();
    });
  }

  document.getElementById("playerTitle").textContent = movie.titulo_original;
  document.getElementById("playerMsg").textContent =
    `Reproduciendo "${movie.titulo_original}". El reproductor completo estará disponible próximamente.`;
  overlay.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function hidePlayer() {
  document.getElementById("playerOverlay")?.classList.add("hidden");
  const modalOpen = !document.getElementById("movieModal")?.classList.contains("hidden");
  const drawerOpen = document.getElementById("miListaDrawer")?.classList.contains("active");
  if (!modalOpen && !drawerOpen) document.body.style.overflow = "";
}

window.closeModal = closeModal;
window.openModal = openModal;
window.playMovie = playMovie;
