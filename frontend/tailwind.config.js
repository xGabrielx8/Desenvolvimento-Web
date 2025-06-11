/** @type {import('tailwindcss').Config} */
export default {
  // A configuração 'content' é a mais importante.
  // Ela diz ao Tailwind para procurar por classes de estilo em todos os
  // ficheiros .html, .js, .svelte, e .ts dentro da pasta 'src'.
  content: ['./src/**/*.{html,js,svelte,ts}'],
  
  theme: {
    extend: {},
  },
  plugins: [],
}


