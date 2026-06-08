import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const refreshClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('user_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;
    const refreshToken = localStorage.getItem('refresh_token');

    if (
      status === 401 &&
      refreshToken &&
      !originalRequest._retry &&
      !originalRequest.url.includes('/auth/login/') &&
      !originalRequest.url.includes('/auth/register/') &&
      !originalRequest.url.includes('/auth/refresh/')
    ) {
      originalRequest._retry = true;
      try {
        const response = await refreshClient.post('/auth/refresh/', {
          refresh: refreshToken,
        });
        const access = response.data.access;
        localStorage.setItem('user_token', access);
        apiClient.defaults.headers.common.Authorization = `Bearer ${access}`;
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Token de refresh expirado — limpar sessão e redirecionar
        localStorage.removeItem('user_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_name');
        window.dispatchEvent(new Event('storage-update'));
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default {
  // Auth
  login(data) {
    return apiClient.post('/auth/login/', data);
  },
  register(data) {
    return apiClient.post('/auth/register/', data);
  },
  refresh(data) {
    return refreshClient.post('/auth/refresh/', data);
  },
  me() {
    return apiClient.get('/auth/me/');
  },
  updateMe(data) {
    return apiClient.patch('/auth/me/', data);
  },

  // Rios
  getRios() {
    return apiClient.get('/rios/');
  },
  getRio(id) {
    return apiClient.get(`/rios/${id}/`);
  },
  createRio(data) {
    return apiClient.post('/rios/', data);
  },
  updateRio(id, data) {
    return apiClient.put(`/rios/${id}/`, data);
  },
  deleteRio(id) {
    return apiClient.delete(`/rios/${id}/`);
  },
  toggleFavorite(id) {
    return apiClient.post(`/pontos-risco/${id}/favorite/`);
  },
  toggleAlert(id) {
    return apiClient.post(`/pontos-risco/${id}/alert/`);
  },
  getRioDescricaoGemini(id) {
    return apiClient.get(`/publico/rios/${id}/descricao-gemini/`);
  },

  // Pontos de Risco (por Rio)
  getPontosRisco(rioId) {
    return apiClient.get(`/rios/${rioId}/pontos-risco/`);
  },
  createPontoRisco(rioId, data) {
    return apiClient.post(`/rios/${rioId}/pontos-risco/`, { ...data, rio: rioId });
  },

  // Pontos de Risco (ponto específico)
  updatePontoRisco(pontoId, data) {
    return apiClient.put(`/pontos-risco/${pontoId}/`, data);
  },
  deletePontoRisco(pontoId) {
    return apiClient.delete(`/pontos-risco/${pontoId}/`);
  },

  // Usuarios
  getUsuarios() {
    return apiClient.get('/usuarios/');
  },
  getUsuario(id) {
    return apiClient.get(`/usuarios/${id}/`);
  },
  createUsuario(data) {
    return apiClient.post('/usuarios/', data);
  },
  updateUsuario(id, data) {
    return apiClient.patch(`/usuarios/${id}/`, data);
  },
  deleteUsuario(id) {
    return apiClient.delete(`/usuarios/${id}/`);
  },

  // Endpoints Públicos (sem autenticação, para /monitoramento)
  getRiosPublico() {
    return apiClient.get('/publico/rios/');
  },
  getPontosRiscoPublico(rioId) {
    return apiClient.get(`/publico/rios/${rioId}/pontos-risco/`);
  },
};
