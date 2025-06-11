<script lang="ts">

 import "../app.css"; // Importa o CSS global com Tailwind

 import { onMount } from 'svelte';

 import { initializeAuth } from '$lib/auth';



 // onMount só executa no navegador, depois que o componente é renderizado

 onMount(() => {

  // Esta função irá verificar o localStorage e atualizar o estado de login

  initializeAuth();

 });

</script>



<div class="min-h-screen bg-gray-100">

 <slot /> </div> 