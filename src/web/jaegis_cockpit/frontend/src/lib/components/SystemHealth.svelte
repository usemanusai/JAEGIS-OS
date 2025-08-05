<script>
  export let cpu = 0;
  export let memory = 0;
</script>

<div class="bg-gray-800 p-4 rounded-lg shadow-lg">
  <h2 class="text-xl font-bold mb-4 text-gray-200">System Health</h2>
  <div class="space-y-4">
    <div>
      <p class="text-gray-400">CPU Usage</p>
      <div class="w-full bg-gray-700 rounded-full h-4">
        <div class="bg-cyan-500 h-4 rounded-full" style="width: {cpu}%"></div>
      </div>
      <p class="text-right text-cyan-400 font-mono">{cpu.toFixed(1)}%</p>
    </div>
    <div>
      <p class="text-gray-400">Memory Usage</p>
      <div class="w-full bg-gray-700 rounded-full h-4">
        <div class="bg-purple-500 h-4 rounded-full" style="width: {memory}%"></div>
      </div>
      <p class="text-right text-purple-400 font-mono">{memory.toFixed(1)}%</p>
    </div>
  </div>
</div>
