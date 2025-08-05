<script>
    import { onMount } from 'svelte';
    import { API_UTILS, API_CONFIG } from '$lib/config.js';

    let systemStatus = null;
    let nldsStats = null;
    let chatMetrics = null;
    let supportedLanguages = [];
    let error = null;
    let loading = true;

    async function fetchRealSystemMetrics() {
        try {
            // Fetch system status using centralized config
            const statusResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.SYSTEM_STATUS)
            );
            systemStatus = await statusResponse.json();

            // Fetch N.L.D.S. statistics using centralized config
            const nldsResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.NLDS_STATS)
            );
            nldsStats = await nldsResponse.json();

            // Fetch supported languages using centralized config
            const languagesResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.NLDS_LANGUAGES)
            );
            const languagesData = await languagesResponse.json();
            supportedLanguages = languagesData.supported_languages || [];

            // Fetch chat metrics using centralized config
            const chatResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.CHAT_SESSIONS)
            );
            chatMetrics = await chatResponse.json();

            loading = false;
        } catch (e) {
            error = e.message;
            loading = false;
            console.error("❌ Failed to fetch system metrics:", e);
        }
    }

    onMount(fetchRealSystemMetrics);

    function getServiceStatusColor(isOnline) {
        return isOnline ? 'text-green-400' : 'text-red-400';
    }

    function getSuccessRateColor(rate) {
        if (rate >= 95) return 'text-green-400';
        if (rate >= 80) return 'text-yellow-400';
        return 'text-red-400';
    }

    function formatUptime(uptimeStr) {
        if (!uptimeStr || uptimeStr === 'N/A') return 'N/A';
        return uptimeStr.split('.')[0]; // Remove microseconds
    }
</script>

<div class="p-8 max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold text-white mb-6">System Metrics & N.L.D.S.</h1>
    <p class="text-gray-400 mb-8">Real-time system performance, N.L.D.S. language processing statistics, and enhanced chat system monitoring.</p>

    {#if loading}
        <div class="text-center p-8">
            <p class="text-gray-400">Loading system metrics...</p>
        </div>
    {:else if error}
        <div class="bg-red-900 border border-red-500 text-red-200 p-4 rounded-lg mb-6">
            <p><strong>Error:</strong> Failed to load system metrics.</p>
            <p class="font-mono mt-2">{error}</p>
        </div>
    {:else}
        <!-- System Status Overview -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-white mb-4">JAEGIS System Status</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-gray-800 rounded-lg p-4">
                    <h3 class="text-lg font-bold text-white mb-2">Core Services</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-400">JAEGIS Core:</span>
                            <span class="{getServiceStatusColor(systemStatus?.services?.jaegis_core)}">
                                {systemStatus?.services?.jaegis_core ? 'Online' : 'Offline'}
                            </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Agent System:</span>
                            <span class="{getServiceStatusColor(systemStatus?.services?.agent_system)}">
                                {systemStatus?.services?.agent_system ? 'Online' : 'Offline'}
                            </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">N.L.D.S.:</span>
                            <span class="{getServiceStatusColor(systemStatus?.services?.nlds_system)}">
                                {systemStatus?.services?.nlds_system ? 'Online' : 'Offline'}
                            </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Chat System:</span>
                            <span class="{getServiceStatusColor(systemStatus?.services?.chat_system)}">
                                {systemStatus?.services?.chat_system ? 'Online' : 'Offline'}
                            </span>
                        </div>
                    </div>
                </div>

                <div class="bg-gray-800 rounded-lg p-4">
                    <h3 class="text-lg font-bold text-white mb-2">System Resources</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-400">CPU Usage:</span>
                            <span class="text-white">{systemStatus?.system_info?.cpu_usage?.toFixed(1) || 'N/A'}%</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Memory Usage:</span>
                            <span class="text-white">{systemStatus?.system_info?.memory_usage?.toFixed(1) || 'N/A'}%</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Uptime:</span>
                            <span class="text-white">{formatUptime(systemStatus?.system_info?.uptime)}</span>
                        </div>
                    </div>
                </div>

                <div class="bg-gray-800 rounded-lg p-4">
                    <h3 class="text-lg font-bold text-white mb-2">N.L.D.S. Processing</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-400">Total Requests:</span>
                            <span class="text-white">{nldsStats?.processing_stats?.total_requests || 0}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Success Rate:</span>
                            <span class="{getSuccessRateColor(nldsStats?.processing_stats?.success_rate || 0)}">
                                {nldsStats?.processing_stats?.success_rate?.toFixed(1) || 0}%
                            </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Languages:</span>
                            <span class="text-white">{nldsStats?.processing_stats?.languages_detected_count || 0}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Avg Confidence:</span>
                            <span class="text-white">{(nldsStats?.processing_stats?.average_confidence * 100)?.toFixed(1) || 0}%</span>
                        </div>
                    </div>
                </div>

                <div class="bg-gray-800 rounded-lg p-4">
                    <h3 class="text-lg font-bold text-white mb-2">Chat System</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-400">Total Sessions:</span>
                            <span class="text-white">{chatMetrics?.count || 0}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Active Sessions:</span>
                            <span class="text-green-400">{chatMetrics?.sessions?.filter(s => s.status === 'active').length || 0}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">July 2025 Models:</span>
                            <span class="text-cyan-400">Available</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- N.L.D.S. Language Support -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-white mb-4">N.L.D.S. Language Support ({supportedLanguages.length})</h2>
            {#if supportedLanguages.length === 0}
                <div class="bg-gray-800 rounded-lg p-6 text-center">
                    <p class="text-gray-400">No language data available.</p>
                </div>
            {:else}
                <div class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <table class="w-full text-left text-sm text-gray-300">
                        <thead class="bg-gray-900 text-xs text-gray-400 uppercase">
                            <tr>
                                <th class="p-4">Language</th>
                                <th class="p-4">Family</th>
                                <th class="p-4">Status</th>
                                <th class="p-4">Confidence Threshold</th>
                                <th class="p-4">Special Handling</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each supportedLanguages as lang (lang.language)}
                                <tr class="border-t border-gray-700 hover:bg-gray-700/50">
                                    <td class="p-4 font-bold text-white">{lang.language}</td>
                                    <td class="p-4 text-gray-400">{lang.family}</td>
                                    <td class="p-4 {lang.supported ? 'text-green-400' : 'text-red-400'}">
                                        {lang.supported ? 'Supported' : 'Not Supported'}
                                    </td>
                                    <td class="p-4">{(lang.confidence_threshold * 100).toFixed(0)}%</td>
                                    <td class="p-4">
                                        {#if lang.special_handling}
                                            <span class="text-cyan-400">Yes</span>
                                        {:else}
                                            <span class="text-gray-400">No</span>
                                        {/if}
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>

        <!-- Recent N.L.D.S. Activity -->
        {#if nldsStats?.processing_stats?.languages_detected}
            <div>
                <h2 class="text-2xl font-bold text-white mb-4">Recently Detected Languages</h2>
                <div class="bg-gray-800 rounded-lg p-6">
                    <div class="flex flex-wrap gap-2">
                        {#each nldsStats.processing_stats.languages_detected as language}
                            <span class="bg-blue-600 text-white px-3 py-1 rounded-full text-sm">{language}</span>
                        {/each}
                    </div>
                    <p class="text-gray-400 text-sm mt-4">
                        System uptime: {formatUptime(nldsStats?.processing_stats?.uptime)}
                    </p>
                </div>
            </div>
        {/if}
    {/if}
</div>
