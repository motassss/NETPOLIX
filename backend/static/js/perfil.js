import { auth } from "./auth.js";
import { BASE_URL, getAuthHeaders, requireAuth, formatPrice, formatDate, logout } from "./config.js";
import { initNavbar } from "./navbar.js";
import { openMiLista } from "./mi-lista-drawer.js";
import { showToast } from "./toast.js";

document.addEventListener("DOMContentLoaded", () => {
  if (!requireAuth()) return;
  initNavbar({ withDrawer: true });
  document.getElementById("btnVerMiLista")?.addEventListener("click", openMiLista);
  cargarPerfil();
  cargarRentas();
  cargarHistorial();
  cargarFavoritos();
});

window.logout = logout;
window.limpiarHistorial = limpiarHistorial;
window.toggleForm = toggleForm;
window.cambiarNombre = cambiarNombre;
window.cambiarPassword = cambiarPassword;

async function cargarPerfil() {
  try {
    const res = await fetch(`${BASE_URL}/auth/me`, { headers: getAuthHeaders() });
    if (!res.ok) {
      window.location.href = "/login";
      return;
    }
    const data = await res.json();

    const iniciales = data.nombre
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((p) => p[0].toUpperCase())
      .join("");

    document.getElementById("perfilAvatar").textContent = iniciales || "U";
    document.getElementById("perfilNombre").textContent = data.nombre;
    document.getElementById("perfilCedula").textContent = `C.C. ${data.cedula}`;
    document.getElementById("perfilBadge").textContent = data.is_admin ? "Admin" : "Usuario";

    if (data.fecha_ingreso) {
      document.getElementById("perfilIngreso").textContent = formatDate(data.fecha_ingreso);
    }

    document.getElementById("statFavoritos").textContent = data.total_favoritos;
    document.getElementById("statVistas").textContent = data.total_vistas;
    document.getElementById("statRentas").textContent = data.total_rentas ?? 0;
    document.getElementById("statGasto").textContent = formatPrice(data.gasto_total ?? 0);

    if (data.ultima_vista) {
      const vr = await fetch(`${BASE_URL}/videos/${encodeURIComponent(data.ultima_vista.video_isan)}`, {
        headers: getAuthHeaders(),
      });
      if (vr.ok) {
        const vm = await vr.json();
        document.getElementById("statUltimaVistaTitulo").textContent = vm.titulo_original;
      }
      document.getElementById("statUltimaVistaFecha").textContent = new Date(
        data.ultima_vista.fecha_hora
      ).toLocaleDateString("es-CO", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    }

    document.getElementById("configNombreActual").textContent = data.nombre;
  } catch {
    window.location.href = "/login";
  }
}

async function cargarRentas() {
  const container = document.getElementById("rentasRow");
  if (!container) return;

  try {
    const res = await fetch(`${BASE_URL}/api/rentas/`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error();
    const rentas = await res.json();

    if (!rentas.length) {
      container.innerHTML =
        '<p class="empty-inline">No tienes rentas activas. <a href="/dashboard">Explorar catálogo</a></p>';
      return;
    }

    container.innerHTML = "";
    rentas.forEach((r) => {
      const p = r.pelicula;
      const card = document.createElement("div");
      card.className = "renta-card";
      card.innerHTML = `
        <img src="${p.imagen_url || "/static/img/placeholder.jpg"}" alt="${p.titulo_original}"
             onerror="this.src='/static/img/placeholder.jpg'">
        <div class="renta-card-info">
          <h4>${p.titulo_original}</h4>
          <span class="renta-expiry-tag">Hasta ${formatDate(r.expira_en)}</span>
        </div>`;
      card.addEventListener("click", () => {
        window.location.href = `/dashboard?modal=${p.isan}`;
      });
      container.appendChild(card);
    });
  } catch {
    container.innerHTML = '<p class="empty-inline">Error al cargar rentas</p>';
  }
}

async function cargarHistorial() {
  const container = document.getElementById("historialRow");
  try {
    const res = await fetch(`${BASE_URL}/api/historial/`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error();
    const registros = await res.json();

    if (!registros.length) {
      container.innerHTML = '<p class="empty-inline">No has visto películas rentadas aún.</p>';
      return;
    }

    const vistos = new Map();
    registros.forEach((r) => {
      if (!vistos.has(r.video_isan)) vistos.set(r.video_isan, r);
    });

    container.innerHTML = "";
    for (const r of Array.from(vistos.values()).slice(0, 12)) {
      const movie = r.pelicula;
      if (movie) container.appendChild(renderCardPerfil(movie));
      else {
        const vr = await fetch(`${BASE_URL}/videos/${encodeURIComponent(r.video_isan)}`, {
          headers: getAuthHeaders(),
        });
        if (vr.ok) container.appendChild(renderCardPerfil(await vr.json()));
      }
    }
  } catch {
    container.innerHTML = '<p class="empty-inline">Error al cargar historial</p>';
  }
}

async function cargarFavoritos() {
  const container = document.getElementById("favoritosRow");
  try {
    const res = await fetch(`${BASE_URL}/api/favoritos/`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error();
    const favs = await res.json();

    if (!favs.length) {
      container.innerHTML =
        '<p class="empty-inline">Tu lista está vacía. <a href="/dashboard">Explorar películas</a></p>';
      return;
    }

    container.innerHTML = "";
    for (const f of favs.slice(0, 12)) {
      const vr = await fetch(`${BASE_URL}/videos/${encodeURIComponent(f.video_isan)}`, {
        headers: getAuthHeaders(),
      });
      if (vr.ok) container.appendChild(renderCardPerfil(await vr.json()));
    }
  } catch {
    container.innerHTML = '<p class="empty-inline">Error al cargar favoritos</p>';
  }
}

function renderCardPerfil(movie) {
  const card = document.createElement("div");
  card.className = "movie-card";
  card.innerHTML = `
    <img src="${movie.imagen_url || "/static/img/placeholder.jpg"}"
         alt="${movie.titulo_original}"
         onerror="this.src='/static/img/placeholder.jpg'">
    <div class="card-overlay">
      <div class="card-title">${movie.titulo_original}</div>
      <div class="card-meta">${movie.anio_produccion || ""} · ${movie.duracion || ""} min</div>
    </div>`;
  card.addEventListener("click", () => {
    window.location.href = `/dashboard?modal=${movie.isan}`;
  });
  return card;
}

function toggleForm(id) {
  document.getElementById(id)?.classList.toggle("hidden");
}

async function cambiarNombre() {
  const input = document.getElementById("inputNuevoNombre");
  const nombre = input.value.trim();
  if (!nombre) {
    showToast("El nombre no puede estar vacío", "error");
    return;
  }

  const res = await fetch(`${BASE_URL}/auth/me/nombre`, {
    method: "PATCH",
    headers: getAuthHeaders(),
    body: JSON.stringify({ nombre }),
  });

  if (res.ok) {
    document.getElementById("perfilNombre").textContent = nombre;
    document.getElementById("configNombreActual").textContent = nombre;
    toggleForm("nombreForm");
    input.value = "";
    showToast("Nombre actualizado", "success");
  } else {
    const err = await res.json();
    showToast(err.detail || "Error al actualizar", "error");
  }
}

async function cambiarPassword() {
  const actual = document.getElementById("inputPasswordActual").value;
  const nuevo = document.getElementById("inputPasswordNuevo").value;
  const confirmar = document.getElementById("inputPasswordConfirmar").value;

  if (!actual || !nuevo || !confirmar) {
    showToast("Todos los campos son obligatorios", "error");
    return;
  }
  if (nuevo !== confirmar) {
    showToast("Las contraseñas no coinciden", "error");
    return;
  }
  if (nuevo.length < 6) {
    showToast("Mínimo 6 caracteres", "error");
    return;
  }

  const res = await fetch(`${BASE_URL}/auth/me/password`, {
    method: "PATCH",
    headers: getAuthHeaders(),
    body: JSON.stringify({ password_actual: actual, password_nuevo: nuevo }),
  });

  if (res.ok) {
    toggleForm("passwordForm");
    document.getElementById("inputPasswordActual").value = "";
    document.getElementById("inputPasswordNuevo").value = "";
    document.getElementById("inputPasswordConfirmar").value = "";
    showToast("Contraseña actualizada", "success");
  } else {
    const err = await res.json();
    showToast(err.detail || "Error al actualizar", "error");
  }
}

async function limpiarHistorial() {
  if (!confirm("¿Limpiar todo el historial?")) return;

  const res = await fetch(`${BASE_URL}/api/historial/`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (res.ok) {
    document.getElementById("historialRow").innerHTML =
      '<p class="empty-inline">No has visto películas rentadas aún.</p>';
    document.getElementById("statVistas").textContent = "0";
    showToast("Historial eliminado", "success");
  }
}

// Theme toggle
document.getElementById("themeToggle")?.addEventListener("change", (e) => {
  document.body.classList.toggle("theme-light", e.target.checked);
  localStorage.setItem("netpolix_theme", e.target.checked ? "light" : "dark");
});

if (localStorage.getItem("netpolix_theme") === "light") {
  document.body.classList.add("theme-light");
  const toggle = document.getElementById("themeToggle");
  if (toggle) toggle.checked = true;
}
