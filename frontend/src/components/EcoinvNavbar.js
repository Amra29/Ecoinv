function renderNavbar(activePage = '') {
    const rol = localStorage.getItem("ecoinv_rol");
    const isSuperAdmin = rol === "SUPERADMIN";

    const navbarHTML = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="../admin/DashboardAdmin.html">
                <i class="bi bi-box-seam me-2"></i> Ecoinv♻
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    ${isSuperAdmin ? `
                        <li class="nav-item">
                            <a class="nav-link ${activePage === 'admin' ? 'active' : ''}" href="../admin/DashboardAdmin.html">Panel Distribuidora</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link ${activePage === 'gestion' ? 'active' : ''}" href="../admin/GestionUsuarios.html">Clientes y Administradores</a>
                        </li>
                    ` : `
                        <li class="nav-item">
                            <a class="nav-link ${activePage === 'cliente' ? 'active' : ''}" href="../client/DashboardCliente.html">Mi Inventario</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link ${activePage === 'escaneo' ? 'active' : ''}" href="../client/EscaneoToner.html">Escanear QR</a>
                        </li>
                    `}
                </ul>
                <div class="d-flex align-items-center text-white">
                    <span class="badge bg-light text-primary me-3">${rol || ''}</span>
                    <button class="btn btn-outline-light btn-sm" onclick="cerrarSesion()">Cerrar Sesión</button>
                </div>
            </div>
        </div>
    </nav>
    `;

    document.getElementById("navbar-container").innerHTML = navbarHTML;
}

function cerrarSesion() {
    localStorage.removeItem("ecoinv_token");
    localStorage.removeItem("ecoinv_rol");
    window.location.href = "../login/LoginView.html";
}