<script>
  import { systemStatus } from '$lib/ws.js';
  import SystemHealth from '$lib/components/SystemHealth.svelte';
  import EventStream from '$lib/components/EventStream.svelte';
</script>

<div class="p-8 max-w-7xl mx-auto space-y-8">
    <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white mb-2">JAEGIS Cockpit</h1>
        <p class="text-gray-400">Real-Time Operational Dashboard for the JAEGIS Ecosystem</p>
        <div class="flex justify-center space-x-6 mt-4 text-sm">
            <div class="flex items-center">
                <div class="w-3 h-3 bg-green-400 rounded-full mr-2"></div>
                <span class="text-gray-300">A.C.I.D. Swarms</span>
            </div>
            <div class="flex items-center">
                <div class="w-3 h-3 bg-blue-400 rounded-full mr-2"></div>
                <span class="text-gray-300">Agent System</span>
            </div>
            <div class="flex items-center">
                <div class="w-3 h-3 bg-purple-400 rounded-full mr-2"></div>
                <span class="text-gray-300">N.L.D.S.</span>
            </div>
            <div class="flex items-center">
                <div class="w-3 h-3 bg-cyan-400 rounded-full mr-2"></div>
                <span class="text-gray-300">Enhanced Chat</span>
            </div>
        </div>
    </div>

    <!-- Real-time System Status -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div class="bg-gray-800 rounded-lg p-4 text-center">
            <h3 class="text-lg font-bold text-white mb-2">JAEGIS Core</h3>
            <div class="text-2xl font-bold {$systemStatus.services_online?.jaegis_core ? 'text-green-400' : 'text-red-400'}">
                {$systemStatus.services_online?.jaegis_core ? 'ONLINE' : 'OFFLINE'}
            </div>
            <p class="text-gray-400 text-sm mt-1">Core System Status</p>
        </div>

        <div class="bg-gray-800 rounded-lg p-4 text-center">
            <h3 class="text-lg font-bold text-white mb-2">Agent System</h3>
            <div class="text-2xl font-bold {$systemStatus.services_online?.agent_system ? 'text-green-400' : 'text-red-400'}">
                {$systemStatus.services_online?.agent_system ? 'ONLINE' : 'OFFLINE'}
            </div>
            <p class="text-gray-400 text-sm mt-1">Agent Coordination</p>
        </div>

        <div class="bg-gray-800 rounded-lg p-4 text-center">
            <h3 class="text-lg font-bold text-white mb-2">N.L.D.S.</h3>
            <div class="text-2xl font-bold {$systemStatus.services_online?.nlds_system ? 'text-green-400' : 'text-red-400'}">
                {$systemStatus.services_online?.nlds_system ? 'ONLINE' : 'OFFLINE'}
            </div>
            <p class="text-gray-400 text-sm mt-1">Language Processing</p>
        </div>

        <div class="bg-gray-800 rounded-lg p-4 text-center">
            <h3 class="text-lg font-bold text-white mb-2">Chat System</h3>
            <div class="text-2xl font-bold {$systemStatus.services_online?.chat_system ? 'text-green-400' : 'text-red-400'}">
                {$systemStatus.services_online?.chat_system ? 'ONLINE' : 'OFFLINE'}
            </div>
            <p class="text-gray-400 text-sm mt-1">Enhanced Chat Interface</p>
        </div>
    </div>

    <!-- System Health and Live Events -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-1">
            <SystemHealth cpu={$systemStatus.system_metrics?.cpu_usage || 0} memory={$systemStatus.system_metrics?.memory_usage || 0} />
        </div>
        <div class="lg:col-span-2">
            <EventStream event={$systemStatus.jaegis_status || { event_type: 'system_status', details: { status: 'monitoring' } }} />
        </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-gray-800 rounded-lg p-4">
            <h3 class="text-lg font-bold text-white mb-2">A.C.I.D. Activity</h3>
            <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                    <span class="text-gray-400">Active Swarms:</span>
                    <span class="text-green-400">{$systemStatus.agent_activity?.active_swarms || 0}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Queued Tasks:</span>
                    <span class="text-yellow-400">{$systemStatus.agent_activity?.queued_tasks || 0}</span>
                </div>
            </div>
        </div>

        <div class="bg-gray-800 rounded-lg p-4">
            <h3 class="text-lg font-bold text-white mb-2">N.L.D.S. Processing</h3>
            <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                    <span class="text-gray-400">Requests Processed:</span>
                    <span class="text-blue-400">{$systemStatus.nlds_activity?.total_requests || 0}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Languages Detected:</span>
                    <span class="text-purple-400">{$systemStatus.nlds_activity?.languages_count || 0}</span>
                </div>
            </div>
        </div>

        <div class="bg-gray-800 rounded-lg p-4">
            <h3 class="text-lg font-bold text-white mb-2">Chat System</h3>
            <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                    <span class="text-gray-400">Active Sessions:</span>
                    <span class="text-cyan-400">{$systemStatus.chat_status?.active_sessions || 0}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Total Messages:</span>
                    <span class="text-green-400">{$systemStatus.chat_status?.total_messages || 0}</span>
                </div>
            </div>
        </div>
    </div>
</div>
