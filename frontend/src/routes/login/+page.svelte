<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { authStore, login } from "$lib/auth";
    import type { User } from "$lib/schemas";

    let email = "";
    let password = "";
    let errorMessage = "";
    let isLoading = false;

    // Se já estiver logado, redireciona para o dashboard
    onMount(() => {
        if ($authStore.isAuthenticated) {
            goto('/dashboard');
        }
    });

    async function handleLogin() {
        isLoading = true;
        errorMessage = "";
        try {
            // Passo 1: Busca o token
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const tokenResponse = await fetch('http://localhost:8000/token', {
                method: 'POST',
                body: formData,
            });

            if (!tokenResponse.ok) {
                throw new Error("Email ou senha incorretos.");
            }
            const tokenData = await tokenResponse.json();
            const accessToken = tokenData.access_token;

            // Passo 2: Busca os dados completos do usuário
            const userResponse = await fetch('http://localhost:8000/users/me', {
                headers: { 'Authorization': `Bearer ${accessToken}` }
            });

            if (!userResponse.ok) {
                throw new Error("Não foi possível carregar os dados do usuário.");
            }
            const userData: User = await userResponse.json();

            // Passo 3: Salva tudo e redireciona
            login(accessToken, userData);
            goto('/dashboard');

        } catch (error: any) {
            errorMessage = error.message || "Ocorreu um erro inesperado.";
            console.error("Login failed:", error);
        } finally {
            isLoading = false;
        }
    }
</script>

<!-- Visual Dark Mode para a página de Login -->
<div class="min-h-screen font-sans bg-slate-900 text-slate-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
        <!-- A ALTERAÇÃO ESTÁ AQUI: padding aumentado para p-8 -->
        <div class="bg-slate-800/50 backdrop-blur-xl shadow-2xl rounded-3xl p-8 border border-slate-700">
            <h1 class="text-4xl font-bold text-cyan-400 text-center mb-8">Login</h1>
            
            <form on:submit|preventDefault={handleLogin} class="space-y-6">
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
                           placeholder="Sua senha"
                           required
                           class="w-full px-4 py-3 bg-slate-800 text-white border border-slate-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition shadow-sm">
                </div>

                {#if errorMessage}
                    <div class="p-3 text-sm text-red-300 bg-red-900/50 rounded-xl border border-red-800" role="alert">
                        {errorMessage}
                    </div>
                {/if}

                <button type="submit"
                        disabled={isLoading}
                        class="w-full px-6 py-3 text-white font-bold bg-cyan-600 rounded-full hover:bg-cyan-500 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02] shadow-lg hover:shadow-cyan-500/30">
                    {#if isLoading}Carregando...{:else}Entrar{/if}
                </button>

                <div class="text-center pt-2">
                    <a href="/register" class="text-sm text-cyan-400 hover:text-cyan-300 hover:underline">
                        Não tem conta? Cadastre-se
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>
