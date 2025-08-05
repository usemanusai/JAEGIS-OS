<script>
  import { Activity, Clock, CheckCircle, AlertTriangle, Users, Zap } from 'lucide-svelte';
  import { formatDistanceToNow } from 'date-fns';
  
  export let events = [];
  
  function getEventIcon(eventType) {
    switch (eventType) {
      case 'task_received': return Clock;
      case 'agent_assigned': return Users;
      case 'tool_used': return Zap;
      case 'mission_success': return CheckCircle;
      case 'mission_failure': return AlertTriangle;
      case 'prediction_generated': return Activity;
      case 'prediction_error_calculated': return Activity;
      default: return Activity;
    }
  }
  
  function getEventColor(eventType) {
    switch (eventType) {
      case 'task_received': return 'text-blue-600 bg-blue-100';
      case 'agent_assigned': return 'text-purple-600 bg-purple-100';
      case 'tool_used': return 'text-orange-600 bg-orange-100';
      case 'mission_success': return 'text-green-600 bg-green-100';
      case 'mission_failure': return 'text-red-600 bg-red-100';
      case 'prediction_generated': return 'text-cyan-600 bg-cyan-100';
      case 'prediction_error_calculated': return 'text-indigo-600 bg-indigo-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }
  
  function formatEventType(eventType) {
    return eventType
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
  
  function getEventDescription(event) {
    switch (event.event_type) {
      case 'task_received':
        return `New task: "${event.details?.objective || 'Unknown objective'}"`;
      case 'agent_assigned':
        const agentIds = event.details?.agent_ids || [];
        return `Assigned ${agentIds.length} agent${agentIds.length !== 1 ? 's' : ''} to task`;
      case 'tool_used':
        return `Used tool: ${event.details?.tool_name || 'Unknown tool'}`;
      case 'mission_success':
        return `Mission completed successfully`;
      case 'mission_failure':
        return `Mission failed: ${event.details?.error || 'Unknown error'}`;
      case 'prediction_generated':
        return `Generated prediction for task`;
      case 'prediction_error_calculated':
        const errorScore = event.details?.error_score;
        return `Prediction error: ${errorScore ? (errorScore * 100).toFixed(1) + '%' : 'Unknown'}`;
      default:
        return 'Event occurred';
    }
  }
  
  function formatTimestamp(timestamp) {
    try {
      const date = new Date(timestamp);
      return formatDistanceToNow(date, { addSuffix: true });
    } catch {
      return 'Unknown time';
    }
  }
</script>

<div class="card">
  <div class="card-header">
    <div class="flex items-center">
      <Activity class="h-5 w-5 text-jaegis-primary mr-2" />
      <h3 class="card-title">Live Event Stream</h3>
    </div>
    <div class="text-sm text-gray-500">
      {events.length} recent events
    </div>
  </div>
  
  <div class="space-y-1 max-h-96 overflow-y-auto scrollbar-thin">
    {#if events.length > 0}
      {#each events as event, index}
        <div class="flex items-start space-x-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
          <!-- Event icon -->
          <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center {getEventColor(event.event_type)}">
            <svelte:component this={getEventIcon(event.event_type)} class="h-4 w-4" />
          </div>
          
          <!-- Event content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-900">
                {formatEventType(event.event_type)}
              </p>
              <p class="text-xs text-gray-500">
                {formatTimestamp(event.timestamp)}
              </p>
            </div>
            
            <p class="text-sm text-gray-600 mt-1">
              {getEventDescription(event)}
            </p>
            
            <!-- Event metadata -->
            {#if event.details && Object.keys(event.details).length > 0}
              <div class="mt-2">
                <details class="group">
                  <summary class="text-xs text-gray-400 cursor-pointer hover:text-gray-600">
                    View details
                  </summary>
                  <div class="mt-1 p-2 bg-gray-100 rounded text-xs text-mono text-gray-700">
                    <pre>{JSON.stringify(event.details, null, 2)}</pre>
                  </div>
                </details>
              </div>
            {/if}
          </div>
        </div>
        
        <!-- Divider (except for last item) -->
        {#if index < events.length - 1}
          <div class="border-t border-gray-100"></div>
        {/if}
      {/each}
    {:else}
      <div class="text-center py-8">
        <Activity class="h-12 w-12 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">No recent events</p>
        <p class="text-sm text-gray-400 mt-1">Events will appear here as they occur</p>
      </div>
    {/if}
  </div>
  
  {#if events.length > 0}
    <div class="border-t border-gray-200 pt-4 mt-4">
      <div class="flex items-center justify-between text-sm">
        <span class="text-gray-500">
          Showing {Math.min(events.length, 10)} of {events.length} events
        </span>
        <button class="text-jaegis-primary hover:text-jaegis-secondary font-medium">
          View all events →
        </button>
      </div>
    </div>
  {/if}
</div>
