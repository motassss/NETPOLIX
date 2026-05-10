import { auth } from './auth.js';

const BASE_URL = 'http://localhost:8000';

async function apiFetch(endpoint, options = {}) {
    const token = auth.obtenerToken();

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        auth.eliminarToken();
        window.location.href = '/pages/login.html';
        return;
    }

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error en la solicitud');
    }

    return response.json();
}

export const api = {
    auth: {
        async login(cedula, password) {
            const data = await apiFetch('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ cedula, password }),
            });
            auth.guardarToken(data.access_token);
            return data;
        },

        async registro(datos) {
            return apiFetch('/auth/registro', {
                method: 'POST',
                body: JSON.stringify(datos),
            });
        },

        logout() {
            auth.eliminarToken();
            window.location.href = '/pages/login.html';
        },
    },

    videos: {
        async listar(page = 0) {
            return apiFetch(`/videos/?skip=${page * 20}&limit=20`);
        },

        async verCalificacion(isan) {
            return apiFetch(`/videos/${isan}/clasificacion`);
        },

        async calificar(isan, puntuacion) {
            return apiFetch(`/videos/${isan}/calificar`, {
                method: 'POST',
                body: JSON.stringify({ puntuacion }),
            });
        },
    },
};
