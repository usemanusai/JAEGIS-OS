"""
P.H.A.L.A.N.X. Live Editor Interface
Real-time application editing, component modification, and instant preview system
Part of the JAEGIS A.E.G.I.S. Protocol Suite
"""

import json
import logging
import asyncio
import websockets
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EditType(Enum):
    """Types of edits supported by the live editor"""
    COMPONENT_UPDATE = "component_update"
    STYLE_CHANGE = "style_change"
    PROP_MODIFICATION = "prop_modification"
    LAYOUT_CHANGE = "layout_change"
    CODE_EDIT = "code_edit"
    ASSET_UPDATE = "asset_update"

class PreviewMode(Enum):
    """Preview modes for the live editor"""
    DESKTOP = "desktop"
    TABLET = "tablet"
    MOBILE = "mobile"
    CUSTOM = "custom"

@dataclass
class EditOperation:
    """Represents a single edit operation"""
    operation_id: str
    edit_type: EditType
    target_component: str
    changes: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[str] = None
    preview_mode: PreviewMode = PreviewMode.DESKTOP

@dataclass
class LiveSession:
    """Represents a live editing session"""
    session_id: str
    app_id: str
    user_id: str
    connected_at: datetime
    last_activity: datetime
    preview_mode: PreviewMode
    active_component: Optional[str] = None
    websocket: Optional[Any] = None

@dataclass
class ComponentState:
    """Current state of a component in the live editor"""
    component_id: str
    component_type: str
    props: Dict[str, Any]
    styles: Dict[str, Any]
    children: List[str]
    parent: Optional[str]
    position: Dict[str, Any]
    version: int

class PHALANXLiveEditor:
    """
    P.H.A.L.A.N.X. Live Editor Interface
    
    Provides real-time application editing capabilities with instant preview,
    collaborative editing, and seamless integration with the A.E.G.I.S. ecosystem.
    """
    
    def __init__(self, port: int = 8765, host: str = "localhost"):
        self.host = host
        self.port = port
        
        # Session management
        self.active_sessions: Dict[str, LiveSession] = {}
        self.component_states: Dict[str, ComponentState] = {}
        self.edit_history: List[EditOperation] = []
        
        # WebSocket server
        self.websocket_server = None
        self.connected_clients: Dict[str, Any] = {}
        
        # Integration with other A.E.G.I.S. components
        self.aura_integration = True  # A.U.R.A. for component generation
        self.phalanx_integration = True  # P.H.A.L.A.N.X. app generator
        
        # Live editing configuration
        self.config = {
            "auto_save_interval": 5,  # seconds
            "max_undo_history": 50,
            "collaboration_enabled": True,
            "hot_reload_enabled": True,
            "preview_debounce": 300  # milliseconds
        }
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {
            "component_updated": [],
            "style_changed": [],
            "layout_modified": [],
            "session_started": [],
            "session_ended": []
        }
        
        logger.info("P.H.A.L.A.N.X. Live Editor Interface initialized")
    
    async def start_server(self):
        """Start the WebSocket server for live editing"""
        logger.info(f"Starting live editor server on {self.host}:{self.port}")
        
        self.websocket_server = await websockets.serve(
            self.handle_websocket_connection,
            self.host,
            self.port
        )
        
        logger.info("Live editor server started successfully")
    
    async def stop_server(self):
        """Stop the WebSocket server"""
        if self.websocket_server:
            self.websocket_server.close()
            await self.websocket_server.wait_closed()
            logger.info("Live editor server stopped")
    
    async def handle_websocket_connection(self, websocket, path):
        """Handle new WebSocket connections"""
        client_id = str(uuid.uuid4())
        self.connected_clients[client_id] = websocket
        
        logger.info(f"New client connected: {client_id}")
        
        try:
            await self.send_welcome_message(websocket, client_id)
            
            async for message in websocket:
                await self.handle_message(client_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_id}")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
        finally:
            if client_id in self.connected_clients:
                del self.connected_clients[client_id]
            await self.cleanup_client_session(client_id)
    
    async def send_welcome_message(self, websocket, client_id: str):
        """Send welcome message to new client"""
        welcome_message = {
            "type": "welcome",
            "client_id": client_id,
            "server_info": {
                "version": "1.0.0",
                "features": ["live_editing", "collaboration", "hot_reload"],
                "supported_frameworks": ["react", "vue", "svelte", "angular"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
        await websocket.send(json.dumps(welcome_message))
    
    async def handle_message(self, client_id: str, message: str):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "start_session":
                await self.handle_start_session(client_id, data)
            elif message_type == "edit_component":
                await self.handle_edit_component(client_id, data)
            elif message_type == "update_styles":
                await self.handle_update_styles(client_id, data)
            elif message_type == "change_preview_mode":
                await self.handle_change_preview_mode(client_id, data)
            elif message_type == "save_changes":
                await self.handle_save_changes(client_id, data)
            elif message_type == "undo_operation":
                await self.handle_undo_operation(client_id, data)
            elif message_type == "get_component_state":
                await self.handle_get_component_state(client_id, data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message from client {client_id}")
        except Exception as e:
            logger.error(f"Error handling message from client {client_id}: {e}")
    
    async def handle_start_session(self, client_id: str, data: Dict):
        """Handle session start request"""
        app_id = data.get("app_id")
        user_id = data.get("user_id", "anonymous")
        preview_mode = PreviewMode(data.get("preview_mode", "desktop"))
        
        session = LiveSession(
            session_id=str(uuid.uuid4()),
            app_id=app_id,
            user_id=user_id,
            connected_at=datetime.now(),
            last_activity=datetime.now(),
            preview_mode=preview_mode,
            websocket=self.connected_clients[client_id]
        )
        
        self.active_sessions[client_id] = session
        
        # Load application state
        app_state = await self.load_application_state(app_id)
        
        response = {
            "type": "session_started",
            "session_id": session.session_id,
            "app_state": app_state,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.send_to_client(client_id, response)
        await self.trigger_event("session_started", session)
        
        logger.info(f"Started editing session for app {app_id}")
    
    async def handle_edit_component(self, client_id: str, data: Dict):
        """Handle component edit request"""
        if client_id not in self.active_sessions:
            await self.send_error(client_id, "No active session")
            return
        
        session = self.active_sessions[client_id]
        component_id = data.get("component_id")
        changes = data.get("changes", {})
        
        # Create edit operation
        operation = EditOperation(
            operation_id=str(uuid.uuid4()),
            edit_type=EditType.COMPONENT_UPDATE,
            target_component=component_id,
            changes=changes,
            timestamp=datetime.now(),
            user_id=session.user_id
        )
        
        # Apply changes
        await self.apply_edit_operation(operation)
        
        # Broadcast to all clients editing the same app
        await self.broadcast_to_app(session.app_id, {
            "type": "component_updated",
            "operation": asdict(operation),
            "component_state": await self.get_component_state(component_id)
        })
        
        await self.trigger_event("component_updated", operation)
    
    async def handle_update_styles(self, client_id: str, data: Dict):
        """Handle style update request"""
        if client_id not in self.active_sessions:
            await self.send_error(client_id, "No active session")
            return
        
        session = self.active_sessions[client_id]
        component_id = data.get("component_id")
        styles = data.get("styles", {})
        
        # Create edit operation
        operation = EditOperation(
            operation_id=str(uuid.uuid4()),
            edit_type=EditType.STYLE_CHANGE,
            target_component=component_id,
            changes={"styles": styles},
            timestamp=datetime.now(),
            user_id=session.user_id
        )
        
        # Apply changes
        await self.apply_edit_operation(operation)
        
        # Broadcast style changes
        await self.broadcast_to_app(session.app_id, {
            "type": "styles_updated",
            "component_id": component_id,
            "styles": styles,
            "timestamp": datetime.now().isoformat()
        })
        
        await self.trigger_event("style_changed", operation)
    
    async def handle_change_preview_mode(self, client_id: str, data: Dict):
        """Handle preview mode change"""
        if client_id not in self.active_sessions:
            await self.send_error(client_id, "No active session")
            return
        
        session = self.active_sessions[client_id]
        new_mode = PreviewMode(data.get("preview_mode"))
        session.preview_mode = new_mode
        session.last_activity = datetime.now()
        
        response = {
            "type": "preview_mode_changed",
            "preview_mode": new_mode.value,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.send_to_client(client_id, response)
    
    async def handle_save_changes(self, client_id: str, data: Dict):
        """Handle save changes request"""
        if client_id not in self.active_sessions:
            await self.send_error(client_id, "No active session")
            return
        
        session = self.active_sessions[client_id]
        
        # Save current state
        saved = await self.save_application_state(session.app_id)
        
        response = {
            "type": "changes_saved",
            "success": saved,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.send_to_client(client_id, response)
    
    async def handle_undo_operation(self, client_id: str, data: Dict):
        """Handle undo operation request"""
        if client_id not in self.active_sessions:
            await self.send_error(client_id, "No active session")
            return
        
        session = self.active_sessions[client_id]
        
        # Find last operation for this session
        last_operation = None
        for operation in reversed(self.edit_history):
            if operation.user_id == session.user_id:
                last_operation = operation
                break
        
        if last_operation:
            await self.revert_edit_operation(last_operation)
            
            response = {
                "type": "operation_undone",
                "operation_id": last_operation.operation_id,
                "timestamp": datetime.now().isoformat()
            }
        else:
            response = {
                "type": "undo_failed",
                "reason": "No operations to undo",
                "timestamp": datetime.now().isoformat()
            }
        
        await self.send_to_client(client_id, response)
    
    async def apply_edit_operation(self, operation: EditOperation):
        """Apply an edit operation to the component state"""
        component_id = operation.target_component
        
        if component_id not in self.component_states:
            # Create new component state
            self.component_states[component_id] = ComponentState(
                component_id=component_id,
                component_type="unknown",
                props={},
                styles={},
                children=[],
                parent=None,
                position={},
                version=1
            )
        
        component_state = self.component_states[component_id]
        
        # Apply changes based on edit type
        if operation.edit_type == EditType.COMPONENT_UPDATE:
            if "props" in operation.changes:
                component_state.props.update(operation.changes["props"])
            if "children" in operation.changes:
                component_state.children = operation.changes["children"]
        
        elif operation.edit_type == EditType.STYLE_CHANGE:
            if "styles" in operation.changes:
                component_state.styles.update(operation.changes["styles"])
        
        elif operation.edit_type == EditType.LAYOUT_CHANGE:
            if "position" in operation.changes:
                component_state.position.update(operation.changes["position"])
        
        # Increment version
        component_state.version += 1
        
        # Add to history
        self.edit_history.append(operation)
        
        # Trim history if too long
        if len(self.edit_history) > self.config["max_undo_history"]:
            self.edit_history = self.edit_history[-self.config["max_undo_history"]:]
    
    async def revert_edit_operation(self, operation: EditOperation):
        """Revert an edit operation"""
        # This would implement the reverse of apply_edit_operation
        # For now, we'll just remove it from history
        if operation in self.edit_history:
            self.edit_history.remove(operation)
    
    async def get_component_state(self, component_id: str) -> Optional[Dict]:
        """Get current state of a component"""
        if component_id in self.component_states:
            return asdict(self.component_states[component_id])
        return None
    
    async def load_application_state(self, app_id: str) -> Dict:
        """Load application state from storage"""
        # This would load from database or file system
        # For now, return a mock state
        return {
            "app_id": app_id,
            "components": {},
            "layout": {"type": "vertical"},
            "theme": {"primary_color": "#3b82f6"}
        }
    
    async def save_application_state(self, app_id: str) -> bool:
        """Save application state to storage"""
        # This would save to database or file system
        logger.info(f"Saving application state for {app_id}")
        return True
    
    async def broadcast_to_app(self, app_id: str, message: Dict):
        """Broadcast message to all clients editing the same app"""
        for client_id, session in self.active_sessions.items():
            if session.app_id == app_id:
                await self.send_to_client(client_id, message)
    
    async def send_to_client(self, client_id: str, message: Dict):
        """Send message to a specific client"""
        if client_id in self.connected_clients:
            try:
                await self.connected_clients[client_id].send(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to client {client_id}: {e}")
    
    async def send_error(self, client_id: str, error_message: str):
        """Send error message to client"""
        error_response = {
            "type": "error",
            "message": error_message,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_to_client(client_id, error_response)
    
    async def cleanup_client_session(self, client_id: str):
        """Clean up when client disconnects"""
        if client_id in self.active_sessions:
            session = self.active_sessions[client_id]
            await self.trigger_event("session_ended", session)
            del self.active_sessions[client_id]
    
    def add_event_handler(self, event_type: str, handler: Callable):
        """Add event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def trigger_event(self, event_type: str, data: Any):
        """Trigger event handlers"""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event_type}: {e}")
    
    def get_active_sessions(self) -> List[LiveSession]:
        """Get all active sessions"""
        return list(self.active_sessions.values())
    
    def get_edit_history(self, app_id: Optional[str] = None) -> List[EditOperation]:
        """Get edit history, optionally filtered by app"""
        if app_id:
            return [op for op in self.edit_history 
                   if any(session.app_id == app_id 
                         for session in self.active_sessions.values())]
        return self.edit_history.copy()

# Export main class
__all__ = ['PHALANXLiveEditor', 'EditOperation', 'LiveSession', 'ComponentState', 'EditType', 'PreviewMode']
