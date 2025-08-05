<script>
  import { Settings, Save, RefreshCw, Database, Wifi, Shield } from 'lucide-svelte';
  
  let settings = {
    api: {
      backend_url: 'http://localhost:8090',
      timeout: 30,
      retry_attempts: 3
    },
    dashboard: {
      refresh_interval: 5,
      max_events: 100,
      auto_refresh: true
    },
    notifications: {
      budget_alerts: true,
      job_failures: true,
      approval_requests: true
    }
  };
  
  let saving = false;
  let saved = false;
  
  async function saveSettings() {
    saving = true;
    
    try {
      // Simulate saving settings
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // In a real implementation, this would save to localStorage or API
      localStorage.setItem('jaegis_cockpit_settings', JSON.stringify(settings));
      
      saved = true;
      setTimeout(() => saved = false, 3000);
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      saving = false;
    }
  }
  
  function resetSettings() {
    settings = {
      api: {
        backend_url: 'http://localhost:8090',
        timeout: 30,
        retry_attempts: 3
      },
      dashboard: {
        refresh_interval: 5,
        max_events: 100,
        auto_refresh: true
      },
      notifications: {
        budget_alerts: true,
        job_failures: true,
        approval_requests: true
      }
    };
  }
  
  // Load settings on mount
  if (typeof window !== 'undefined') {
    const savedSettings = localStorage.getItem('jaegis_cockpit_settings');
    if (savedSettings) {
      try {
        settings = { ...settings, ...JSON.parse(savedSettings) };
      } catch (error) {
        console.error('Failed to load settings:', error);
      }
    }
  }
</script>

<svelte:head>
  <title>Settings - JAEGIS Cockpit</title>
</svelte:head>

<div class="space-y-6">
  <!-- Header -->
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Settings</h1>
      <p class="text-gray-600">Configure your JAEGIS Cockpit preferences</p>
    </div>
    
    <div class="flex space-x-3">
      <button 
        class="btn-secondary"
        on:click={resetSettings}
      >
        <RefreshCw class="h-4 w-4 mr-2" />
        Reset
      </button>
      
      <button 
        class="btn-primary"
        on:click={saveSettings}
        disabled={saving}
      >
        {#if saving}
          <div class="spinner h-4 w-4 mr-2"></div>
        {:else}
          <Save class="h-4 w-4 mr-2" />
        {/if}
        {saved ? 'Saved!' : 'Save'}
      </button>
    </div>
  </div>
  
  <!-- Settings Sections -->
  <div class="space-y-6">
    <!-- API Settings -->
    <div class="card">
      <div class="card-header">
        <div class="flex items-center">
          <Wifi class="h-5 w-5 text-jaegis-primary mr-2" />
          <h3 class="card-title">API Configuration</h3>
        </div>
      </div>
      
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Backend URL
          </label>
          <input
            type="url"
            bind:value={settings.api.backend_url}
            class="w-full border-gray-300 rounded-md shadow-sm focus:ring-jaegis-primary focus:border-jaegis-primary"
            placeholder="http://localhost:8090"
          />
          <p class="text-xs text-gray-500 mt-1">
            URL of the JAEGIS Cockpit backend API
          </p>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Timeout (seconds)
            </label>
            <input
              type="number"
              bind:value={settings.api.timeout}
              min="5"
              max="120"
              class="w-full border-gray-300 rounded-md shadow-sm focus:ring-jaegis-primary focus:border-jaegis-primary"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Retry Attempts
            </label>
            <input
              type="number"
              bind:value={settings.api.retry_attempts}
              min="0"
              max="10"
              class="w-full border-gray-300 rounded-md shadow-sm focus:ring-jaegis-primary focus:border-jaegis-primary"
            />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Dashboard Settings -->
    <div class="card">
      <div class="card-header">
        <div class="flex items-center">
          <Database class="h-5 w-5 text-jaegis-primary mr-2" />
          <h3 class="card-title">Dashboard Configuration</h3>
        </div>
      </div>
      
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <label class="text-sm font-medium text-gray-700">
              Auto Refresh
            </label>
            <p class="text-xs text-gray-500">
              Automatically refresh dashboard data
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              bind:checked={settings.dashboard.auto_refresh}
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-jaegis-primary/25 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-jaegis-primary"></div>
          </label>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Refresh Interval (seconds)
            </label>
            <input
              type="number"
              bind:value={settings.dashboard.refresh_interval}
              min="1"
              max="300"
              disabled={!settings.dashboard.auto_refresh}
              class="w-full border-gray-300 rounded-md shadow-sm focus:ring-jaegis-primary focus:border-jaegis-primary disabled:bg-gray-100"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Max Events
            </label>
            <input
              type="number"
              bind:value={settings.dashboard.max_events}
              min="10"
              max="1000"
              class="w-full border-gray-300 rounded-md shadow-sm focus:ring-jaegis-primary focus:border-jaegis-primary"
            />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Notification Settings -->
    <div class="card">
      <div class="card-header">
        <div class="flex items-center">
          <Shield class="h-5 w-5 text-jaegis-primary mr-2" />
          <h3 class="card-title">Notifications</h3>
        </div>
      </div>
      
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <label class="text-sm font-medium text-gray-700">
              Budget Alerts
            </label>
            <p class="text-xs text-gray-500">
              Notify when budget thresholds are exceeded
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              bind:checked={settings.notifications.budget_alerts}
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-jaegis-primary/25 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-jaegis-primary"></div>
          </label>
        </div>
        
        <div class="flex items-center justify-between">
          <div>
            <label class="text-sm font-medium text-gray-700">
              Job Failures
            </label>
            <p class="text-xs text-gray-500">
              Notify when forge jobs fail
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              bind:checked={settings.notifications.job_failures}
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-jaegis-primary/25 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-jaegis-primary"></div>
          </label>
        </div>
        
        <div class="flex items-center justify-between">
          <div>
            <label class="text-sm font-medium text-gray-700">
              Approval Requests
            </label>
            <p class="text-xs text-gray-500">
              Notify when new items need approval
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              bind:checked={settings.notifications.approval_requests}
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-jaegis-primary/25 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-jaegis-primary"></div>
          </label>
        </div>
      </div>
    </div>
    
    <!-- System Information -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">System Information</h3>
      </div>
      
      <div class="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p class="text-gray-500">JAEGIS Version</p>
          <p class="text-gray-900 font-mono">v2.1.1</p>
        </div>
        <div>
          <p class="text-gray-500">Cockpit Version</p>
          <p class="text-gray-900 font-mono">v1.0.0</p>
        </div>
        <div>
          <p class="text-gray-500">Backend API</p>
          <p class="text-gray-900 font-mono">{settings.api.backend_url}</p>
        </div>
        <div>
          <p class="text-gray-500">Build Date</p>
          <p class="text-gray-900 font-mono">{new Date().toLocaleDateString()}</p>
        </div>
      </div>
    </div>
  </div>
</div>
