<div class="min-h-screen bg-gray-900 text-white">
    <nav class="bg-gray-800 shadow-md">
        <div class="max-w-7xl mx-auto px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center space-x-8">
                    <a href="/" class="text-xl font-bold text-cyan-400">JAEGIS Cockpit</a>
                    <div class="flex space-x-4">
                        <a href="/" class="text-gray-300 hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">Dashboard</a>
                        <a href="/forge" class="text-gray-300 hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">A.C.I.D. Swarms</a>
                        <a href="/governance" class="text-gray-300 hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">Agent System</a>
                        <a href="/treasury" class="text-gray-300 hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">N.L.D.S. & Metrics</a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    <main>
        <slot />
    </main>
</div>
