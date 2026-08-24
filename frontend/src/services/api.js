const API_BASE_URL = "http://127.0.0.1:8000/api";

const api = {
    // Helper central para peticiones HTTP
    async request(endpoint, options = {}) {
        const token = localStorage.getItem("ecoinv_token");
        const headers = {
            "Content-Type": "application/json",
            ...options.headers
        };

        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Sesión expirada o token inválido
            localStorage.removeItem("ecoinv_token");
            localStorage.removeItem("ecoinv_rol");
            window.location.href = "../login/LoginView.html";
            return;
        }

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Error al procesar la solicitud");
        }

        return data;
    },

    // Autenticación
    async login(email, password) {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Credenciales incorrectas");
        return data;
    },

    // Inventario y Escaneo
    getToners: () => api.request("/toners/"),
    getModelos: () => api.request("/toners/modelos"),
    generarLoteQR: (payload) => api.request("/toners/generar-lote", {
        method: "POST",
        body: JSON.stringify(payload)
    }),
    getIncidencias: () => api.request("/incidencias/"),
    getEmpresas: () => api.request("/empresas/"),
    crearEmpresa: (payload) => api.request("/empresas/", {
        method: "POST",
        body: JSON.stringify(payload)
    }),
    eliminarEmpresa: (id) => api.request(`/empresas/${id}`, { method: "DELETE" }),

    // Gestión de usuarios (clientes y super admins)
    getUsuarios: () => api.request("/usuarios/"),
    crearUsuarioCliente: (payload) => api.request("/usuarios/clientes", {
        method: "POST",
        body: JSON.stringify(payload)
    }),
    crearSuperAdmin: (payload) => api.request("/usuarios/superadmins", {
        method: "POST",
        body: JSON.stringify(payload)
    }),
    eliminarUsuario: (id) => api.request(`/usuarios/${id}`, { method: "DELETE" }),
    
    procesarEscaneo: (payload) => api.request("/escaneo/procesar", {
        method: "POST",
        body: JSON.stringify(payload)
    })
};