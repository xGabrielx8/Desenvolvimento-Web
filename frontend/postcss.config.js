/** @type {import('postcss-load-config').Config} */
export default {
  plugins: {
    // Adiciona o plugin do Tailwind CSS para o PostCSS.
    // Esta é a forma correta de configurar para versões mais recentes.
    '@tailwindcss/postcss': {},
    
    // Adiciona o autoprefixer para garantir compatibilidade com navegadores mais antigos.
    autoprefixer: {},
  },
};
