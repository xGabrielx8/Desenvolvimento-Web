/**
 * Define a estrutura (schema) dos dados que vêm da API.
 * Isso ajuda o TypeScript a entender os dados e evitar erros.
 */

export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string; // A API retorna a data como uma string no formato ISO
  owner_id: number;
}

export interface User {
  id: number;
  email: string;
  is_active: boolean;
}
