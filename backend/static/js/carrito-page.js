import { BASE_URL, requireAuth, getAuthHeaders, formatPrice } from "./config.js";
import { initNavbar } from "./navbar.js";
import { initModal } from "./modal.js";
import { removeFromCart, processPayment } from "./carrito-module.js";
import { loadRentas } from "./rentas.js";
import { showToast } from "./toast.js";

document.addEventListener("DOMContentLoaded", async () => {
  if (!requireAuth()) return;
  initNavbar({ withDrawer: true });
  initModal();
  await renderCart();
});

async function renderCart() {
  const container = document.getElementById("cartContent");
  try {
    const res = await fetch(`${BASE_URL}/api/carrito/`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error();
    const data = await res.json();
    const items = data.items || [];

    if (!items.length) {
      container.innerHTML = `
        <div class="cart-empty">
          <div class="cart-empty-icon">🎬</div>
          <h2>Tu carrito está vacío</h2>
          <p>Explora el catálogo y agrega películas para rentarlas.</p>
          <a href="/dashboard" class="btn-browse">Explorar catálogo</a>
        </div>`;
      return;
    }

    let subtotal = 0;
    const itemsHtml = items
      .map((item) => {
        const p = item.pelicula;
        const precio = p.precio_renta ?? 3.99;
        subtotal += precio;
        const genero = p.genero || (p.categorias?.[0] ?? "");
        return `
          <div class="cart-item" data-isan="${p.isan}">
            <img src="${p.imagen_url || "/static/img/placeholder.jpg"}" alt="${p.titulo_original}" class="cart-item-poster"
                 onerror="this.src='/static/img/placeholder.jpg'">
            <div class="cart-item-info">
              <h3>${p.titulo_original}</h3>
              <p>${genero} · ${p.anio_produccion || ""}</p>
              <span class="cart-item-price">${formatPrice(precio)} / 30 días</span>
            </div>
            <button class="cart-item-remove" data-isan="${p.isan}" aria-label="Eliminar">✕</button>
          </div>`;
      })
      .join("");

    container.innerHTML = `
      <div class="cart-layout">
        <div class="cart-items">${itemsHtml}</div>
        <div class="cart-summary">
          <h2>Resumen</h2>
          <div class="summary-line">
            <span>${items.length} película(s)</span>
            <span>${formatPrice(subtotal)}</span>
          </div>
          <div class="summary-line total">
            <strong>Total</strong>
            <strong>${formatPrice(subtotal)}</strong>
          </div>
          <button class="btn-checkout" id="btnCheckout">💳 Pagar y desbloquear</button>
          <p class="checkout-notice">
            Pago simulado. Las películas se desbloquean inmediatamente por 30 días.
          </p>
        </div>
      </div>`;

    container.querySelectorAll(".cart-item-remove").forEach((btn) => {
      btn.addEventListener("click", async () => {
        await removeFromCart(btn.dataset.isan);
        await renderCart();
      });
    });

    document.getElementById("btnCheckout")?.addEventListener("click", handleCheckout);
  } catch {
    container.innerHTML = '<p class="empty-msg">Error al cargar el carrito.</p>';
  }
}

async function handleCheckout() {
  const btn = document.getElementById("btnCheckout");
  if (!btn) return;
  btn.disabled = true;
  btn.textContent = "Procesando...";

  const data = await processPayment();
  btn.disabled = false;
  btn.textContent = "💳 Pagar y desbloquear";

  if (!data?.success) return;

  await loadRentas();
  showPaymentSuccess(data.peliculas_desbloqueadas || []);
  await renderCart();
}

function showPaymentSuccess(peliculas) {
  let overlay = document.getElementById("successOverlay");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "successOverlay";
    overlay.className = "success-overlay";
    document.body.appendChild(overlay);
  }

  const list = peliculas
    .map(
      (p) => `
      <div class="success-item">
        <img src="${p.imagen_url || "/static/img/placeholder.jpg"}" alt="">
        <span>${p.titulo}</span>
      </div>`
    )
    .join("");

  overlay.innerHTML = `
    <div class="success-modal">
      <div class="success-icon">🎉</div>
      <h2>¡Pago exitoso!</h2>
      <p>Se desbloquearon ${peliculas.length} película(s):</p>
      <div class="success-list">${list}</div>
      <a href="/dashboard" class="btn-browse">Ir al catálogo</a>
      <button class="btn-secondary-close" id="closeSuccess">Cerrar</button>
    </div>`;

  overlay.classList.remove("hidden");
  document.getElementById("closeSuccess")?.addEventListener("click", () => {
    overlay.classList.add("hidden");
  });
}
