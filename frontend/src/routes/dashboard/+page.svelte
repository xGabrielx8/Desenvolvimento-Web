<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { authStore, logout } from '$lib/auth';
    import type { User } from '$lib/schemas';
    import { apiClient } from '$lib/api';
    import type { Task } from '$lib/schemas';

    let currentUser: User | null = null;
    let tasks: Task[] = [];
    
    let newTaskTitle: string = "";
    let newTaskDescription: string = ""; 

    let errorMessage: string = "";
    let isLoadingTasks: boolean = true;
    let isAddingTask: boolean = false;

    // Protege a rota: Redireciona para o login se não estiver autenticado
    onMount(async () => {
        const state = $authStore;
        if (!state.isAuthenticated || !state.user) {
            goto('/login');
            return;
        }
        currentUser = state.user;
        await loadTasks();
    });

    async function loadTasks() {
        isLoadingTasks = true;
        errorMessage = "";
        try {
            const fetchedTasks: Task[] = await apiClient.get('/tasks/');
            tasks = fetchedTasks;
        } catch (error: any) {
            errorMessage = `Erro ao carregar tarefas: ${error.message}`;
            console.error("Failed to load tasks:", error);
            if (error.message.includes("401") || error.message.includes("credentials")) {
                handleLogout();
            }
        } finally {
            isLoadingTasks = false;
        }
    }

    async function addTask() {
        if (!newTaskTitle.trim()) return;
        isAddingTask = true;
        errorMessage = "";
        try {
            const newTask: Task = await apiClient.post('/tasks/', { 
                title: newTaskTitle, 
                description: newTaskDescription 
            });
            tasks = [...tasks, newTask];
            
            newTaskTitle = "";
            newTaskDescription = "";
        } catch (error: any) {
            errorMessage = `Erro ao adicionar tarefa: ${error.message}`;
            console.error("Failed to add task:", error);
        } finally {
            isAddingTask = false;
        }
    }

    async function toggleTaskCompletion(task: Task) {
        const originalStatus = task.completed;
        // Atualização otimista: muda o visual imediatamente
        tasks = tasks.map(t => t.id === task.id ? { ...t, completed: !t.completed } : t);

        try {
            // Constrói o endpoint correto com base no estado original da tarefa
            const endpoint = `/tasks/${task.id}/${!originalStatus ? 'complete' : 'incomplete'}`;
            await apiClient.patch(endpoint, {}); // Envia a requisição para o backend
        } catch (error: any) {
            errorMessage = `Erro ao atualizar tarefa: ${error.message}`;
            console.error("Failed to update task status:", error);
            // Reverte a mudança visual em caso de erro
            tasks = tasks.map(t => t.id === task.id ? { ...t, completed: originalStatus } : t);
        }
    }

    async function deleteTask(taskId: number) {
        const originalTasks = tasks;
        tasks = tasks.filter(t => t.id !== taskId);
        try {
            await apiClient.delete(`/tasks/${taskId}`);
        } catch (error: any) {
            errorMessage = `Erro ao deletar tarefa: ${error.message}`;
            console.error("Failed to delete task:", error);
            tasks = originalTasks;
        }
    }

    function handleLogout() {
        logout();
        goto('/login');
    }

</script>

<!-- Visual Dark Mode inspirado na imagem -->
<div class="min-h-screen font-sans bg-slate-900 text-slate-100">
    <div class="max-w-3xl mx-auto p-4 sm:p-8">
        <div class="bg-slate-800/50 backdrop-blur-xl shadow-2xl rounded-3xl p-6 sm:p-8 border border-slate-700">
            
            <!-- Cabeçalho -->
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 border-b border-slate-700 pb-6">
                <h1 class="text-4xl font-bold text-cyan-400">Minhas Tarefas</h1>
                <div class="flex items-center mt-4 sm:mt-0">
                    {#if currentUser}
                        <span class="text-slate-400 mr-8">Olá, <span class="font-medium text-slate-200">{currentUser.email}</span></span>
                    {/if}
                    <button on:click={handleLogout} class="px-5 py-2 bg-slate-700 text-slate-200 font-semibold rounded-full hover:bg-slate-600 transition-colors duration-300">
                        Sair
                    </button>
                </div>
            </div>

            <!-- Formulário para adicionar nova tarefa -->
            <form on:submit|preventDefault={addTask} class="mb-8 p-6 bg-slate-900/60 rounded-2xl space-y-4 border border-slate-700 shadow-inner">
                <div>
                    <label for="task-title" class="block text-sm font-medium text-slate-300 mb-1">Título da Tarefa</label>
                    <input id="task-title" type="text"
                           bind:value={newTaskTitle}
                           placeholder="O que precisa ser feito?"
                           required
                           class="w-full px-4 py-3 bg-slate-800 text-white border border-slate-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition shadow-sm">
                </div>
                
                <div>
                    <label for="task-description" class="block text-sm font-medium text-slate-300 mb-1">Descrição (Opcional)</label>
                    <textarea id="task-description"
                              bind:value={newTaskDescription}
                              placeholder="Adicione mais detalhes..."
                              rows="3"
                              class="w-full px-4 py-3 bg-slate-800 text-white border border-slate-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition shadow-sm"></textarea>
                </div>

                <button type="submit"
                        disabled={isAddingTask}
                        class="w-full px-6 py-3 text-white font-bold bg-cyan-600 rounded-full hover:bg-cyan-500 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02] shadow-lg hover:shadow-cyan-500/30">
                    {#if isAddingTask}Adicionando...{:else}Adicionar Tarefa{/if}
                </button>
            </form>

            {#if errorMessage}
                <div class="mb-4 p-4 text-sm text-red-300 bg-red-900/50 rounded-xl border border-red-800" role="alert">
                    <span class="font-medium">Erro:</span> {errorMessage}
                </div>
            {/if}

            <!-- Lista de Tarefas -->
            <div class="space-y-3">
                <h2 class="text-2xl font-bold text-slate-300 border-b border-slate-700 pb-2 mb-4">Sua Lista</h2>
                {#if isLoadingTasks}
                    <p class="text-slate-400 text-center py-8">Carregando tarefas...</p>
                {:else if tasks.length === 0}
                    <div class="text-center py-10 px-4 bg-slate-800/50 rounded-2xl border-dashed border-2 border-slate-700">
                        <p class="text-sm text-slate-500 mt-1">Adicione sua primeira tarefa no formulário acima.</p>
                    </div>
                {:else}
                    {#each tasks as task (task.id)}
                        <div class="flex items-start justify-between p-4 border border-slate-700 rounded-2xl {task.completed ? 'bg-slate-800/30' : 'bg-slate-800'} hover:shadow-2xl hover:border-cyan-500/50 transition-all duration-300">
                            <div class="flex items-start flex-grow">
                                <input type="checkbox"
                                       checked={task.completed} 
                                       on:change={() => toggleTaskCompletion(task)}
                                       class="mt-1 h-6 w-6 text-cyan-500 focus:ring-cyan-400 bg-slate-700 border-slate-600 rounded-md cursor-pointer">
                                <div class="ml-4 flex-grow">
                                    <span class="font-medium {task.completed ? 'line-through text-slate-500' : 'text-slate-100'}">{task.title}</span>
                                    {#if task.description}
                                        <p class="text-sm text-slate-400 mt-1">{task.description}</p>
                                    {/if}
                                </div>
                            </div>
                            <button on:click={() => deleteTask(task.id)}
                                    class="ml-4 flex-shrink-0 w-8 h-8 flex items-center justify-center bg-slate-700 text-slate-400 text-sm font-bold rounded-full hover:bg-red-500 hover:text-white transition-colors duration-300">
                                X
                            </button>
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    </div>
</div>
