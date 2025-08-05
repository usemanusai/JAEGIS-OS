import { readable } from 'svelte/store';
import { API_UTILS, WS_CONFIG } from './config.js';

export const systemStatus = readable({
    cpu_usage: 0,
    memory_usage: 0,
    latest_event: { event_type: 'connecting', details: {} },
    services_online: {},
    system_metrics: {},
    jaegis_status: {},
    agent_activity: {},
    nlds_activity: {},
    chat_status: {}
}, function start(set) {
    let ws;
    let reconnectAttempts = 0;
    let reconnectTimer;

    function connect() {
        try {
            ws = new WebSocket(API_UTILS.getWsUrl('/ws/system-status'));

            ws.onopen = () => {
                console.log("✅ JAEGIS Cockpit WebSocket connection established");
                reconnectAttempts = 0;
                if (reconnectTimer) {
                    clearTimeout(reconnectTimer);
                    reconnectTimer = null;
                }
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    set(data);
                } catch (error) {
                    console.error("❌ Error parsing WebSocket message:", error);
                }
            };

            ws.onclose = (event) => {
                console.log("🔌 JAEGIS Cockpit WebSocket connection closed");

                // Set disconnected state
                set({
                    cpu_usage: 0,
                    memory_usage: 0,
                    latest_event: { event_type: 'disconnected', details: { reason: event.reason || 'Connection closed' } },
                    services_online: {},
                    system_metrics: {},
                    jaegis_status: {},
                    agent_activity: {},
                    nlds_activity: {},
                    chat_status: {}
                });

                // Attempt to reconnect
                if (reconnectAttempts < WS_CONFIG.MAX_RECONNECT_ATTEMPTS) {
                    reconnectAttempts++;
                    console.log(`🔄 Attempting to reconnect... (${reconnectAttempts}/${WS_CONFIG.MAX_RECONNECT_ATTEMPTS})`);
                    reconnectTimer = setTimeout(connect, WS_CONFIG.RECONNECT_INTERVAL);
                } else {
                    console.error("❌ Max reconnection attempts reached. Please refresh the page.");
                }
            };

            ws.onerror = (error) => {
                console.error("❌ JAEGIS Cockpit WebSocket error:", error);
            };
        } catch (error) {
            console.error("❌ Failed to create WebSocket connection:", error);
        }
    }

    // Initial connection
    connect();

    return function stop() {
        if (reconnectTimer) {
            clearTimeout(reconnectTimer);
        }
        if (ws) {
            ws.close();
        }
    };
});
