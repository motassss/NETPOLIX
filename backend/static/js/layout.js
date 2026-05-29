const ICON_SEARCH = `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>`;
const ICON_CART = `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>`;

export function getNavbarHTML(activePage = "inicio") {
  const links = [
    { id: "inicio", href: "/dashboard", label: "Inicio" },
    { id: "series", href: "/dashboard#cat-drama", label: "Series" },
    { id: "peliculas", href: "/dashboard#catalogo", label: "Películas" },
    { id: "novedades", href: "/dashboard#cat-tendencias", label: "Novedades" },
  ];

  const linksHtml = links
    .map(
      (l) =>
        `<a href="${l.href}" class="nav-link${activePage === l.id ? " active" : ""}" data-nav="${l.id}">${l.label}</a>`
    )
    .join("");

  return `
<nav class="navbar" id="navbar">
  <div class="navbar-left">
    <button type="button" class="nav-mobile-toggle" id="navMobileToggle" aria-label="Menú">☰</button>
    <a class="navbar-logo" href="/dashboard">NETPOLIX</a>
    <div class="navbar-links" id="navbarLinks">${linksHtml}</div>
  </div>
  <div class="navbar-right">
    <div class="nav-search">
      <button type="button" class="search-toggle" id="searchToggle" aria-label="Buscar">${ICON_SEARCH}</button>
      <input type="text" class="search-input" id="searchInput" placeholder="Títulos, personas, géneros" autocomplete="off">
    </div>
    <a href="/carrito" class="nav-cart" aria-label="Carrito">${ICON_CART}<span class="cart-badge" id="cartBadge">0</span></a>
    <button type="button" class="nav-mi-lista" id="btnMiLista">Mi Lista</button>
    <div class="nav-profile" id="navProfile">
      <button type="button" class="profile-avatar" id="profileAvatar" aria-haspopup="true" aria-expanded="false">U</button>
      <div class="profile-dropdown" id="profileDropdown">
        <div class="dropdown-header">
          <div class="dropdown-avatar" id="dropdownAvatar">U</div>
          <div>
            <p class="dropdown-name" id="dropdownName">Usuario</p>
            <p class="dropdown-email" id="dropdownEmail">—</p>
          </div>
        </div>
        <hr class="dropdown-divider">
        <a href="/perfil" class="dropdown-item">👤 Mi perfil</a>
        <a href="/carrito" class="dropdown-item">🛒 Mi carrito</a>
        <a href="/perfil#config" class="dropdown-item">⚙️ Configuración</a>
        <hr class="dropdown-divider">
        <button type="button" class="dropdown-item dropdown-logout" id="btnLogout">🚪 Cerrar sesión</button>
      </div>
    </div>
  </div>
</nav>`;
}

export function getDrawerHTML() {
  return `
<div class="drawer-overlay" id="drawerOverlay"></div>
<div class="mi-lista-drawer" id="miListaDrawer" role="dialog" aria-label="Mi Lista">
  <div class="drawer-header">
    <h2 class="drawer-title">❤️ Mi Lista</h2>
    <button type="button" class="drawer-close" id="drawerClose" aria-label="Cerrar">✕</button>
  </div>
  <div class="drawer-content" id="drawerContent"></div>
  <div class="drawer-empty" id="drawerEmpty">
    <div class="drawer-empty-icon">🎬</div>
    <p>Tu lista está vacía</p>
    <span>Agrega películas desde el catálogo</span>
  </div>
</div>`;
}

export function mountAppChrome({ activePage = "inicio", withDrawer = true } = {}) {
  const navMount = document.getElementById("navbar-mount");
  if (navMount) {
    navMount.outerHTML = getNavbarHTML(activePage);
  }

  if (withDrawer && !document.getElementById("miListaDrawer")) {
    document.body.insertAdjacentHTML("beforeend", getDrawerHTML());
  }
}
