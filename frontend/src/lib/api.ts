import { authStore } from '$lib/auth';
import { get } from 'svelte/store';

const BASE_URL = 'http://localhost:8000'; // A URL base da sua API

/**
 * Função central para fazer requisições à API.
 * Ela automaticamente adiciona o token de autenticação, se existir.
 */
async function request(path: string, options: RequestInit = {}) {
  // Pega o estado mais recente da loja de autenticação
  const { token } = get(authStore);

  // Cria os cabeçalhos da requisição
  const headers = new Headers(options.headers || {});

  // Se o token existir, o adiciona ao cabeçalho 'Authorization'
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  // Define o Content-Type como JSON, a menos que o corpo seja um FormData
  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  // Constrói a URL final e faz a chamada fetch.
  // Esta é a linha que estava corrompida no seu arquivo.
  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });

  // Trata a resposta da API
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'A requisição à API falhou' }));
    throw new Error(errorData.detail || 'Erro desconhecido da API');
  }

  // Se a resposta for "No Content" (ex: em um delete), não tenta converter para JSON
  if (response.status === 204) {
    return;
  }

  return response.json();
}

/**
 * Exporta um objeto 'apiClient' com métodos fáceis de usar (get, post, etc.)
 * que seus componentes podem chamar.
 */
export const apiClient = {
  get: (path: string) => request(path, { method: 'GET' }),
  post: (path: string, data: unknown) => request(path, { method: 'POST', body: JSON.stringify(data) }),
  patch: (path: string, data: unknown) => request(path, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (path: string) => request(path, { method: 'DELETE' }),
};
