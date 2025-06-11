<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { authStore } from "$lib/auth";

    let email = "";
    let password = "";
    let confirmPassword = "";
    let errorMessage = "";
    let successMessage = "";
    let isLoading = false;

    // Se já estiver logado, redireciona para o dashboard
    onMount(() => {
        if ($authStore.isAuthenticated) {
            goto('/dashboard');
        }
    });

    async function handleRegister() {
        if (password !== confirmPassword) {
            errorMessage = "As senhas não coincidem.";
            return;
        }

        isLoading = true;
        errorMessage = "";
        successMessage = "";

        try {
            const response = await fetch('http://localhost:8000/users/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "Erro ao se cadastrar.");
            }

            successMessage = "Cadastro realizado com sucesso! Redirecionando para login...";
            
            setTimeout(() => {
                goto('/login');
            }, 2000);

        } catch (error: any) {
            errorMessage = error.message || "Ocorreu um erro inesperado.";
            console.error("Registration failed:", error);
        } finally {
            isLoading = false;
        }
    }
</script>

<!-- Visual Dark Mode para a página de Cadastro -->
<div class="min-h-screen font-sans bg-slate-900 text-slate-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
        <!-- A ALTERAÇÃO ESTÁ AQUI: o padding 'p-8' foi trocado por 'p-6 sm:p-8' para melhor ajuste em telas pequenas -->
        <div class="bg-slate-800/50 backdrop-blur-xl shadow-2xl rounded-3xl px-4 py-6 sm:px-8 sm:py-8 border border-slate-700">
            <h1 class="text-4xl font-bold text-cyan-400 text-center mb-8">Cadastro</h1>
            
            <form on:submit|preventDefault={handleRegister} class="space-y-4">
                <div>
                    <label for="email" class="block text-sm font-medium text-slate-300 mb-1">Email</label>
                    <input id="email" type="email"
                           bind:value={email}
                           placeholder="seu@email.com"
                           required
                           class="w-full px-4 py-3 bg-slate-800 text-white border border-slate-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition shadow-sm">
                </div>
                
                <div>
                    <label for="password" class="block text-sm font-medium text-slate-300 mb-1">Senha</label>
                    <input id="password" type="password"
                           bind:value={password}
                           placeholder="Crie uma senha forte"
                           required
                           minlength="6"
                           class="w-full px-4 py-3 bg-slate-800 text-white border border-slate-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition shadow-sm">
                </div>

                <div>
                    <label for="confirmPassword" class="block text-sm font-medium text-slate-300 mb-1">Confirmar Senha</label>
                    <input id="confirmPassword" type="password"
                           bind:value={confirmPassword}
                           placeholder="Confirme sua senha"
                           required
                           minlength="6"
                           class="w-full px-4 py-3 bg-slate-800 text-white border border-slate-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition shadow-sm">
                </div>

                {#if errorMessage}
                    <div class="p-3 text-sm text-red-300 bg-red-900/50 rounded-xl border border-red-800" role="alert">
                        {errorMessage}
                    </div>
                {/if}
                
                {#if successMessage}
                    <div class="p-3 text-sm text-emerald-300 bg-emerald-900/50 rounded-xl border border-emerald-800" role="alert">
                        {successMessage}
                    </div>
                {/if}

                <button type="submit"
                        disabled={isLoading}
                        class="w-full px-6 py-3 mt-4 text-white font-bold bg-cyan-600 rounded-full hover:bg-cyan-500 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02] shadow-lg hover:shadow-cyan-500/30">
                    {#if isLoading}Criando conta...{:else}Cadastrar{/if}
                </button>

                <div class="text-center pt-2">
                    <a href="/login" class="text-sm text-cyan-400 hover:text-cyan-300 hover:underline">
                        Já tem conta? Faça login
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>
