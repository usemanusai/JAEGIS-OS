<script>
  export let title;
  export let value;
  export let icon;
  export let color = 'blue';
  export let subtitle = '';
  export let trend = null; // 'up', 'down', or null
  
  function getColorClasses(color) {
    const colors = {
      blue: 'text-blue-600 bg-blue-100',
      green: 'text-green-600 bg-green-100',
      yellow: 'text-yellow-600 bg-yellow-100',
      red: 'text-red-600 bg-red-100',
      gray: 'text-gray-600 bg-gray-100'
    };
    return colors[color] || colors.blue;
  }
  
  function getTrendColor(trend) {
    if (trend === 'up') return 'text-green-600';
    if (trend === 'down') return 'text-red-600';
    return 'text-gray-400';
  }
</script>

<div class="card">
  <div class="flex items-center">
    <div class="flex-shrink-0">
      <div class="w-8 h-8 rounded-md flex items-center justify-center {getColorClasses(color)}">
        <svelte:component this={icon} class="h-5 w-5" />
      </div>
    </div>
    
    <div class="ml-4 flex-1">
      <div class="flex items-baseline">
        <p class="text-2xl font-semibold text-gray-900">{value}</p>
        {#if trend}
          <span class="ml-2 text-sm {getTrendColor(trend)}">
            {trend === 'up' ? '↗' : '↘'}
          </span>
        {/if}
      </div>
      <p class="text-sm font-medium text-gray-600">{title}</p>
      {#if subtitle}
        <p class="text-xs text-gray-500 mt-1">{subtitle}</p>
      {/if}
    </div>
  </div>
</div>
