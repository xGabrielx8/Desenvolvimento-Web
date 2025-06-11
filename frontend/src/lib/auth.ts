import { writable } from 'svelte/store';
import { browser } from '$app/environment';
// Importa o tipo User que será usado na função login
import type { User } from '$lib/schemas';

// Define a "forma" completa do nosso estado de autenticação
interface AuthState {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null; // Garante que o usuário aqui tem o tipo completo
}

// Tenta carregar o estado salvo do localStorage, apenas se estiver no navegador
const initialValue = browser ? localStorage.getItem('auth') : null;
const initialState: AuthState = initialValue ? JSON.parse(initialValue) : {
    isAuthenticated: false,
    token: null,
    user: null,
};

// Cria a "loja" reativa com o estado inicial
export const authStore = writable<AuthState>(initialState);

// Salva qualquer mudança no estado de volta para o localStorage
if (browser) {
  authStore.subscribe((value) => {
    localStorage.setItem('auth', JSON.stringify(value));
  });
}

/**
 * Função de login CORRIGIDA
 * Agora ela aceita o objeto de usuário completo.
 */
export function login(token: string, user: User) {
  authStore.set({
    isAuthenticated: true,
    token,
    user, // Salva o usuário completo
  });
}

/**
 * Função de logout
 */
export function logout() {
  authStore.set({
    isAuthenticated: false,
    token: null,
    user: null,
  });
}

/**
 * Função que verifica o estado de login salvo quando a aplicação carrega
 */
export function initializeAuth() {
  const storedAuth = localStorage.getItem('auth');
  if (storedAuth) {
    authStore.set(JSON.parse(storedAuth));
  }
}
