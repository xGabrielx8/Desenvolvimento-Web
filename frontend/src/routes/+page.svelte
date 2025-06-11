<script lang="ts">

 import { onMount } from 'svelte';

 import { goto } from '$app/navigation';

 import { authStore } from '$lib/auth';



 onMount(() => {

 // Verifica se o usuário está autenticado ao montar a página raiz

 const state = $authStore; // Acessa o valor atual do store

 if (state.isAuthenticated) {

goto('/dashboard'); // Redireciona para o dashboard se autenticado

 } else {

 goto('/login'); // Redireciona para login se não autenticado
 }

});

</script>



<div class="flex justify-center items-center min-h-screen">
<p class="text-gray-500">Redirecionando...</p>

</div>