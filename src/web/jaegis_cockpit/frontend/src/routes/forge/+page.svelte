<script>
    import { onMount } from 'svelte';
    import { API_UTILS, API_CONFIG } from '$lib/config.js';

    let swarms = [];
    let tasks = [];
    let error = null;
    let loading = true;

    async function fetchRealACIDData() {
        try {
            // Fetch real A.C.I.D. swarms using centralized config
            const swarmsResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.ACID_SWARMS)
            );
            const swarmsData = await swarmsResponse.json();
            swarms = swarmsData.swarms || [];

            // Fetch real A.C.I.D. task queue using centralized config
            const tasksResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.ACID_TASKS)
            );
            const tasksData = await tasksResponse.json();
            tasks = tasksData.tasks || [];

            loading = false;
        } catch (e) {
            error = e.message;
            loading = false;
            console.error("❌ Failed to fetch A.C.I.D. data:", e);
        }
    }

    onMount(fetchRealACIDData);

    function getSwarmStatusColor(strategy) {
        switch (strategy?.toLowerCase()) {
            case 'sequential': return 'text-blue-400';
            case 'parallel': return 'text-green-400';
            case 'hierarchical': return 'text-purple-400';
            case 'consensus': return 'text-yellow-400';
            default: return 'text-gray-400';
        }
    }

    function getTaskComplexityColor(complexity) {
        switch (complexity?.toLowerCase()) {
            case 'simple': return 'text-green-400';
            case 'moderate': return 'text-yellow-400';
            case 'complex': return 'text-orange-400';
            case 'critical': return 'text-red-400';
            default: return 'text-gray-400';
        }
    }
</script>

<div class="p-8 max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold text-white mb-6">A.C.I.D. Swarm Orchestrator</h1>
    <p class="text-gray-400 mb-8">Live monitoring of Autonomous Code Intelligence & Development swarms and task execution.</p>

    {#if loading}
        <div class="text-center p-8">
            <p class="text-gray-400">Loading A.C.I.D. system data...</p>
        </div>
    {:else if error}
        <div class="bg-red-900 border border-red-500 text-red-200 p-4 rounded-lg mb-6">
            <p><strong>Error:</strong> Failed to load A.C.I.D. system data.</p>
            <p class="font-mono mt-2">{error}</p>
        </div>
    {:else}
        <!-- Active Swarms Section -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-white mb-4">Active Swarms ({swarms.length})</h2>
            {#if swarms.length === 0}
                <div class="bg-gray-800 rounded-lg p-6 text-center">
                    <p class="text-gray-400">No active swarms currently running.</p>
                    <p class="text-gray-500 text-sm mt-2">Swarms will appear here when tasks are being executed.</p>
                </div>
            {:else}
                <div class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <table class="w-full text-left text-sm text-gray-300">
                        <thead class="bg-gray-900 text-xs text-gray-400 uppercase">
                            <tr>
                                <th class="p-4">Swarm ID</th>
                                <th class="p-4">Task ID</th>
                                <th class="p-4">Strategy</th>
                                <th class="p-4">Agents</th>
                                <th class="p-4">Created</th>
                                <th class="p-4">Est. Completion</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each swarms as swarm (swarm.swarm_id)}
                                <tr class="border-t border-gray-700 hover:bg-gray-700/50">
                                    <td class="p-4 font-mono text-cyan-400">{swarm.swarm_id}</td>
                                    <td class="p-4 font-mono">{swarm.task_id}</td>
                                    <td class="p-4 font-bold {getSwarmStatusColor(swarm.coordination_strategy)}">{swarm.coordination_strategy}</td>
                                    <td class="p-4">{swarm.selected_agents?.length || 0} agents</td>
                                    <td class="p-4">{new Date(swarm.created_at).toLocaleString()}</td>
                                    <td class="p-4">{new Date(swarm.estimated_completion).toLocaleString()}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>

        <!-- Task Queue Section -->
        <div>
            <h2 class="text-2xl font-bold text-white mb-4">Task Queue ({tasks.length})</h2>
            {#if tasks.length === 0}
                <div class="bg-gray-800 rounded-lg p-6 text-center">
                    <p class="text-gray-400">No tasks currently queued.</p>
                    <p class="text-gray-500 text-sm mt-2">Tasks will appear here when submitted to the A.C.I.D. system.</p>
                </div>
            {:else}
                <div class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <table class="w-full text-left text-sm text-gray-300">
                        <thead class="bg-gray-900 text-xs text-gray-400 uppercase">
                            <tr>
                                <th class="p-4">Task ID</th>
                                <th class="p-4">Description</th>
                                <th class="p-4">Complexity</th>
                                <th class="p-4">Priority</th>
                                <th class="p-4">Duration (min)</th>
                                <th class="p-4">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each tasks as task (task.task_id)}
                                <tr class="border-t border-gray-700 hover:bg-gray-700/50">
                                    <td class="p-4 font-mono text-cyan-400">{task.task_id}</td>
                                    <td class="p-4">{task.description}</td>
                                    <td class="p-4 font-bold {getTaskComplexityColor(task.complexity)}">{task.complexity}</td>
                                    <td class="p-4">{task.priority}/10</td>
                                    <td class="p-4">{task.estimated_duration}</td>
                                    <td class="p-4 text-yellow-400">{task.status}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>
    {/if}
</div>
