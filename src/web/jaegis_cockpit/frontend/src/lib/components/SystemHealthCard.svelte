<script>
  import { Activity, Cpu, HardDrive, Wifi } from 'lucide-svelte';
  
  export let systemStatus;
  
  function formatBytes(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  }
  
  function getHealthColor(status) {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-100';
      case 'degraded': return 'text-yellow-600 bg-yellow-100';
      case 'unavailable': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }
  
  function getProgressColor(percentage) {
    if (percentage > 80) return 'progress-error';
    if (percentage > 60) return 'progress-warning';
    return 'progress-success';
  }
</script>

<div class="card">
  <div class="card-header">
    <div class="flex items-center">
      <Activity class="h-5 w-5 text-jaegis-primary mr-2" />
      <h3 class="card-title">System Health</h3>
    </div>
  </div>
  
  <div class="space-y-6">
    <!-- CPU Usage -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center">
          <Cpu class="h-4 w-4 text-gray-500 mr-2" />
          <span class="text-sm font-medium text-gray-700">CPU Usage</span>
        </div>
        <span class="text-sm text-gray-900 font-mono">
          {systemStatus.system_metrics.cpu_percent.toFixed(1)}%
        </span>
      </div>
      <div class="progress-bar">
        <div 
          class="{getProgressColor(systemStatus.system_metrics.cpu_percent)}"
          style="width: {systemStatus.system_metrics.cpu_percent}%"
        ></div>
      </div>
    </div>
    
    <!-- Memory Usage -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center">
          <HardDrive class="h-4 w-4 text-gray-500 mr-2" />
          <span class="text-sm font-medium text-gray-700">Memory Usage</span>
        </div>
        <span class="text-sm text-gray-900 font-mono">
          {formatBytes(systemStatus.system_metrics.memory.used)} / {formatBytes(systemStatus.system_metrics.memory.total)}
        </span>
      </div>
      <div class="progress-bar">
        <div 
          class="{getProgressColor(systemStatus.system_metrics.memory.percent)}"
          style="width: {systemStatus.system_metrics.memory.percent}%"
        ></div>
      </div>
      <div class="text-xs text-gray-500 mt-1">
        {systemStatus.system_metrics.memory.percent.toFixed(1)}% used
      </div>
    </div>
    
    <!-- Disk Usage -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center">
          <HardDrive class="h-4 w-4 text-gray-500 mr-2" />
          <span class="text-sm font-medium text-gray-700">Disk Usage</span>
        </div>
        <span class="text-sm text-gray-900 font-mono">
          {formatBytes(systemStatus.system_metrics.disk.used)} / {formatBytes(systemStatus.system_metrics.disk.total)}
        </span>
      </div>
      <div class="progress-bar">
        <div 
          class="{getProgressColor(systemStatus.system_metrics.disk.percent)}"
          style="width: {systemStatus.system_metrics.disk.percent}%"
        ></div>
      </div>
      <div class="text-xs text-gray-500 mt-1">
        {systemStatus.system_metrics.disk.percent.toFixed(1)}% used
      </div>
    </div>
    
    <!-- Service Health -->
    <div>
      <h4 class="text-sm font-medium text-gray-700 mb-3">Service Status</h4>
      <div class="grid grid-cols-2 gap-3">
        {#each Object.entries(systemStatus.jaegis_metrics.service_health) as [service, status]}
          <div class="flex items-center justify-between p-2 bg-gray-50 rounded">
            <div class="flex items-center">
              <Wifi class="h-4 w-4 text-gray-400 mr-2" />
              <span class="text-sm text-gray-700 capitalize">{service}</span>
            </div>
            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium {getHealthColor(status)}">
              {status}
            </span>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>
