import { formatPrice } from "./config.js";
import { isRented } from "./rentas.js";
import { isFavorite, toggleFavorite } from "./favoritos.js";
import { openModal, playMovie } from "./modal.js";
import { addToCart } from "./carrito-module.js";

export function renderMovieCard(movie) {
  const card = document.createElement("article");
  card.className = "movie-card";
  card.dataset.isan = movie.isan;

  const rented = isRented(movie.isan);
  const precio = movie.precio_renta ?? 3.99;

  const badge = rented
    ? `<span class="card-badge rented">✓ Rentada</span>`
    : `<span class="card-badge price">${formatPrice(precio)}</span>`;

  const ctaBtn = rented
    ? `<button type="button" class="card-cta card-cta-play">▶ Reproducir</button>`
    : `<button type="button" class="card-cta card-cta-rent">🛒 Rentar ${formatPrice(precio)}</button>`;

  card.innerHTML = `
    ${badge}
    <div class="card-poster-wrap">
      <img src="${movie.imagen_url || "/static/img/placeholder.jpg"}"
           alt="${movie.titulo_original}"
           loading="lazy"
           onerror="this.src='/static/img/placeholder.jpg'">
      <div class="card-hover-layer">
        <p class="card-title">${movie.titulo_original}</p>
        <p class="card-meta">${movie.anio_produccion || ""} · ${movie.duracion || ""} min</p>
        <div class="card-icon-row">
          <button type="button" class="card-icon-btn info-btn" title="Más info">ℹ</button>
          <button type="button" class="card-icon-btn fav-btn ${isFavorite(movie.isan) ? "is-fav" : ""}" title="Mi lista">${isFavorite(movie.isan) ? "✓" : "+"}</button>
        </div>
      </div>
    </div>
    <div class="card-footer">${ctaBtn}</div>`;

  card.querySelector(".info-btn")?.addEventListener("click", (e) => {
    e.stopPropagation();
    openModal(movie);
  });

  card.querySelector(".fav-btn")?.addEventListener("click", async (e) => {
    e.stopPropagation();
    await toggleFavorite(movie.isan, e.currentTarget);
  });

  card.querySelector(".card-cta-play")?.addEventListener("click", (e) => {
    e.stopPropagation();
    playMovie(movie);
  });

  card.querySelector(".card-cta-rent")?.addEventListener("click", async (e) => {
    e.stopPropagation();
    const ok = await addToCart(movie.isan);
    if (ok) openModal(movie);
  });

  card.querySelector(".card-poster-wrap")?.addEventListener("click", () => openModal(movie));

  return card;
}

export function renderCategorySection(title, movies) {
  const section = document.createElement("section");
  section.className = "category-section";
  section.innerHTML = `<h2 class="category-title">${title}</h2><div class="movies-row"></div>`;
  const row = section.querySelector(".movies-row");
  movies.forEach((m) => row.appendChild(renderMovieCard(m)));
  return section;
}
