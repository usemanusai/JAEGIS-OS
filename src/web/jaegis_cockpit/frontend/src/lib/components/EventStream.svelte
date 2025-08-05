<script>
  export let event = { event_type: 'loading', details: {} };
</script>

<div class="bg-gray-800 p-4 rounded-lg shadow-lg">
  <h2 class="text-xl font-bold mb-2 text-gray-200">C.O.R.I. Live Event</h2>
  <div class="bg-gray-900 p-3 rounded font-mono text-sm text-green-400 overflow-x-auto">
    <pre>{JSON.stringify(event, null, 2)}</pre>
  </div>
</div>
