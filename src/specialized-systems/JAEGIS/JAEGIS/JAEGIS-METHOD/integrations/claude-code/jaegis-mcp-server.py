"""
JAEGIS MCP Server for Claude Code Integration
Implements Model Context Protocol server for seamless JAEGIS integration with Claude Code
"""

import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid
from datetime import datetime

# MCP Protocol Implementation
class MCPServer:
    """Model Context Protocol server for JAEGIS integration"""
    
    def __init__(self, jaegis_engine):
        self.jaegis_engine = jaegis_engine
        self.sessions = {}
        self.logger = logging.getLogger(__name__)
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request"""
        
        method = request.get('method')
        params = request.get('params', {})
        request_id = request.get('id')
        
        try:
            if method == 'jaegis/init':
                result = await self.handle_init(params)
            elif method == 'jaegis/brainstorm':
                result = await self.handle_brainstorm(params)
            elif method == 'jaegis/prd':
                result = await self.handle_prd(params)
            elif method == 'jaegis/architecture':
                result = await self.handle_architecture(params)
            elif method == 'jaegis/develop':
                result = await self.handle_develop(params)
            elif method == 'jaegis/status':
                result = await self.handle_status(params)
            elif method == 'jaegis/templates':
                result = await self.handle_templates(params)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'result': result
            }
            
        except Exception as e:
            self.logger.error(f"Error handling request {method}: {e}")
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {
                    'code': -32603,
                    'message': str(e)
                }
            }
    
    async def handle_init(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize new JAEGIS project"""
        
        project_type = params.get('project_type', 'general')
        project_name = params.get('project_name', f'jaegis-project-{uuid.uuid4().hex[:8]}')
        working_directory = params.get('working_directory', '.')
        
        # Create new JAEGIS session
        session_id = str(uuid.uuid4())
        session = JAEGISSession(
            session_id=session_id,
            project_name=project_name,
            project_type=project_type,
            working_directory=Path(working_directory),
            created_at=datetime.now()
        )
        
        self.sessions[session_id] = session
        
        # Initialize project structure
        project_structure = await self.jaegis_engine.initialize_project(
            project_name=project_name,
            project_type=project_type,
            working_directory=working_directory
        )
        
        return {
            'session_id': session_id,
            'project_name': project_name,
            'project_type': project_type,
            'project_structure': project_structure,
            'next_steps': [
                'Run `jaegis brainstorm` to start ideation',
                'Use `jaegis prd` to create product requirements',
                'Execute `jaegis architecture` for technical design'
            ]
        }
    
    async def handle_brainstorm(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle brainstorming session"""
        
        session_id = params.get('session_id')
        topic = params.get('topic', '')
        techniques = params.get('techniques', [])
        duration = params.get('duration', 30)  # minutes
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Invalid session ID")
        
        # Start brainstorming session
        brainstorm_result = await self.jaegis_engine.start_brainstorming(
            session_id=session_id,
            topic=topic,
            techniques=techniques,
            duration=duration
        )
        
        # Update session
        session.current_phase = 'brainstorming'
        session.brainstorm_results = brainstorm_result
        
        return {
            'session_id': session_id,
            'brainstorm_id': brainstorm_result['brainstorm_id'],
            'initial_ideas': brainstorm_result['initial_ideas'],
            'suggested_techniques': brainstorm_result['suggested_techniques'],
            'interaction_prompt': brainstorm_result['interaction_prompt'],
            'files_created': brainstorm_result.get('files_created', [])
        }
    
    async def handle_prd(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle PRD creation"""
        
        session_id = params.get('session_id')
        template_type = params.get('template_type', 'standard')
        interactive = params.get('interactive', True)
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Invalid session ID")
        
        # Generate PRD
        prd_result = await self.jaegis_engine.create_prd(
            session_id=session_id,
            template_type=template_type,
            interactive=interactive,
            brainstorm_context=session.brainstorm_results
        )
        
        # Update session
        session.current_phase = 'modeling'
        session.prd_results = prd_result
        
        return {
            'session_id': session_id,
            'prd_id': prd_result['prd_id'],
            'template_sections': prd_result['template_sections'],
            'current_section': prd_result['current_section'],
            'interaction_prompt': prd_result['interaction_prompt'],
            'files_created': prd_result.get('files_created', []),
            'progress': prd_result['progress']
        }
    
    async def handle_architecture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle architecture design"""
        
        session_id = params.get('session_id')
        architecture_type = params.get('architecture_type', 'standard')
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Invalid session ID")
        
        # Generate architecture
        arch_result = await self.jaegis_engine.create_architecture(
            session_id=session_id,
            architecture_type=architecture_type,
            prd_context=session.prd_results
        )
        
        # Update session
        session.current_phase = 'architecture'
        session.architecture_results = arch_result
        
        return {
            'session_id': session_id,
            'architecture_id': arch_result['architecture_id'],
            'architecture_sections': arch_result['architecture_sections'],
            'current_section': arch_result['current_section'],
            'interaction_prompt': arch_result['interaction_prompt'],
            'files_created': arch_result.get('files_created', []),
            'diagrams_generated': arch_result.get('diagrams_generated', [])
        }
    
    async def handle_develop(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle development phase"""
        
        session_id = params.get('session_id')
        feature = params.get('feature', '')
        development_approach = params.get('approach', 'iterative')
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Invalid session ID")
        
        # Start development
        dev_result = await self.jaegis_engine.start_development(
            session_id=session_id,
            feature=feature,
            approach=development_approach,
            architecture_context=session.architecture_results
        )
        
        # Update session
        session.current_phase = 'development'
        session.development_results = dev_result
        
        return {
            'session_id': session_id,
            'development_id': dev_result['development_id'],
            'development_plan': dev_result['development_plan'],
            'current_task': dev_result['current_task'],
            'interaction_prompt': dev_result['interaction_prompt'],
            'files_created': dev_result.get('files_created', []),
            'code_generated': dev_result.get('code_generated', [])
        }
    
    async def handle_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get session status"""
        
        session_id = params.get('session_id')
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Invalid session ID")
        
        return {
            'session_id': session_id,
            'project_name': session.project_name,
            'current_phase': session.current_phase,
            'progress': session.get_progress(),
            'files_created': session.get_created_files(),
            'next_actions': session.get_next_actions()
        }
    
    async def handle_templates(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get available templates"""
        
        template_type = params.get('type', 'all')
        
        templates = await self.jaegis_engine.get_available_templates(template_type)
        
        return {
            'templates': templates,
            'categories': list(set(t['category'] for t in templates))
        }

@dataclass
class JAEGISSession:
    """JAEGIS session data"""
    session_id: str
    project_name: str
    project_type: str
    working_directory: Path
    created_at: datetime
    current_phase: str = 'initialization'
    brainstorm_results: Optional[Dict] = None
    prd_results: Optional[Dict] = None
    architecture_results: Optional[Dict] = None
    development_results: Optional[Dict] = None
    
    def get_progress(self) -> Dict[str, Any]:
        """Get session progress"""
        phases = ['initialization', 'brainstorming', 'modeling', 'architecture', 'development']
        current_index = phases.index(self.current_phase) if self.current_phase in phases else 0
        
        return {
            'current_phase': self.current_phase,
            'completed_phases': phases[:current_index],
            'remaining_phases': phases[current_index + 1:],
            'overall_progress': current_index / len(phases)
        }
    
    def get_created_files(self) -> List[str]:
        """Get list of created files"""
        files = []
        
        if self.brainstorm_results:
            files.extend(self.brainstorm_results.get('files_created', []))
        if self.prd_results:
            files.extend(self.prd_results.get('files_created', []))
        if self.architecture_results:
            files.extend(self.architecture_results.get('files_created', []))
        if self.development_results:
            files.extend(self.development_results.get('files_created', []))
        
        return files
    
    def get_next_actions(self) -> List[str]:
        """Get suggested next actions"""
        if self.current_phase == 'initialization':
            return ['Start brainstorming with `jaegis brainstorm`']
        elif self.current_phase == 'brainstorming':
            return ['Create PRD with `jaegis prd`']
        elif self.current_phase == 'modeling':
            return ['Design architecture with `jaegis architecture`']
        elif self.current_phase == 'architecture':
            return ['Begin development with `jaegis develop`']
        else:
            return ['Continue development or start new feature']

class JAEGISEngine:
    """Mock JAEGIS engine for demonstration"""
    
    async def initialize_project(self, project_name: str, project_type: str, working_directory: str) -> Dict[str, Any]:
        """Initialize JAEGIS project"""
        
        # Create project structure
        project_path = Path(working_directory) / project_name
        project_path.mkdir(exist_ok=True)
        
        # Create basic directories
        (project_path / 'docs').mkdir(exist_ok=True)
        (project_path / 'brainstorming').mkdir(exist_ok=True)
        (project_path / 'architecture').mkdir(exist_ok=True)
        (project_path / 'development').mkdir(exist_ok=True)
        
        # Create initial files
        readme_content = f"""# {project_name}

JAEGIS Project - {project_type}

## Project Structure
- `docs/` - Project documentation
- `brainstorming/` - Brainstorming session results
- `architecture/` - Technical architecture documents
- `development/` - Development artifacts

## Next Steps
1. Run brainstorming session
2. Create Product Requirements Document
3. Design technical architecture
4. Begin development
"""
        
        with open(project_path / 'README.md', 'w') as f:
            f.write(readme_content)
        
        return {
            'project_path': str(project_path),
            'directories_created': ['docs', 'brainstorming', 'architecture', 'development'],
            'files_created': ['README.md']
        }
    
    async def start_brainstorming(self, session_id: str, topic: str, techniques: List[str], duration: int) -> Dict[str, Any]:
        """Start brainstorming session"""
        
        brainstorm_id = str(uuid.uuid4())
        
        # Mock brainstorming results
        initial_ideas = [
            f"Idea 1 for {topic}: Innovative approach using AI",
            f"Idea 2 for {topic}: User-centric design solution",
            f"Idea 3 for {topic}: Scalable architecture pattern"
        ]
        
        suggested_techniques = [
            "stakeholder_perspective_taking",
            "what_if_analysis",
            "analogical_thinking"
        ]
        
        return {
            'brainstorm_id': brainstorm_id,
            'initial_ideas': initial_ideas,
            'suggested_techniques': suggested_techniques,
            'interaction_prompt': f"Let's explore {topic} together. What specific aspects would you like to brainstorm about?",
            'files_created': [f'brainstorming/session_{brainstorm_id}.md']
        }
    
    async def create_prd(self, session_id: str, template_type: str, interactive: bool, brainstorm_context: Dict) -> Dict[str, Any]:
        """Create PRD"""
        
        prd_id = str(uuid.uuid4())
        
        template_sections = [
            'Executive Summary',
            'User Personas',
            'Functional Requirements',
            'Technical Requirements',
            'Success Metrics'
        ]
        
        return {
            'prd_id': prd_id,
            'template_sections': template_sections,
            'current_section': template_sections[0],
            'interaction_prompt': "Let's start with the Executive Summary. What problem does your product solve?",
            'files_created': [f'docs/prd_{prd_id}.md'],
            'progress': {'completed_sections': 0, 'total_sections': len(template_sections)}
        }
    
    async def create_architecture(self, session_id: str, architecture_type: str, prd_context: Dict) -> Dict[str, Any]:
        """Create architecture"""
        
        architecture_id = str(uuid.uuid4())
        
        architecture_sections = [
            'System Overview',
            'Component Architecture',
            'Data Architecture',
            'Security Architecture',
            'Deployment Architecture'
        ]
        
        return {
            'architecture_id': architecture_id,
            'architecture_sections': architecture_sections,
            'current_section': architecture_sections[0],
            'interaction_prompt': "Let's design the system architecture. What are the main components of your system?",
            'files_created': [f'architecture/architecture_{architecture_id}.md'],
            'diagrams_generated': [f'architecture/system_diagram_{architecture_id}.mermaid']
        }
    
    async def start_development(self, session_id: str, feature: str, approach: str, architecture_context: Dict) -> Dict[str, Any]:
        """Start development"""
        
        development_id = str(uuid.uuid4())
        
        development_plan = [
            'Setup development environment',
            'Implement core functionality',
            'Add user interface',
            'Integrate with external services',
            'Testing and validation'
        ]
        
        return {
            'development_id': development_id,
            'development_plan': development_plan,
            'current_task': development_plan[0],
            'interaction_prompt': f"Let's start developing {feature}. What's the first component we should build?",
            'files_created': [f'development/plan_{development_id}.md'],
            'code_generated': []
        }
    
    async def get_available_templates(self, template_type: str) -> List[Dict[str, Any]]:
        """Get available templates"""
        
        templates = [
            {
                'id': 'standard_prd',
                'name': 'Standard_PRD_Template',
                'category': 'prd',
                'description': 'Comprehensive product requirements document template'
            },
            {
                'id': 'web_app_architecture',
                'name': 'Web_Application_Architecture',
                'category': 'architecture',
                'description': 'Architecture template for web applications'
            },
            {
                'id': 'mobile_app_architecture',
                'name': 'Mobile_Application_Architecture',
                'category': 'architecture',
                'description': 'Architecture template for mobile applications'
            }
        ]
        
        if template_type != 'all':
            templates = [t for t in templates if t['category'] == template_type]
        
        return templates

# CLI Integration
class JAEGISCLI:
    """Command-line interface for JAEGIS Claude Code integration"""
    
    def __init__(self):
        self.mcp_server = MCPServer(JAEGISEngine())
    
    async def execute_command(self, command: str, args: List[str]) -> str:
        """Execute JAEGIS command"""
        
        if command == 'init':
            project_type = args[0] if args else 'general'
            request = {
                'method': 'jaegis/init',
                'params': {'project_type': project_type},
                'id': str(uuid.uuid4())
            }
        elif command == 'brainstorm':
            topic = ' '.join(args) if args else 'project ideas'
            request = {
                'method': 'jaegis/brainstorm',
                'params': {'topic': topic},
                'id': str(uuid.uuid4())
            }
        else:
            return f"Unknown command: {command}"
        
        response = await self.mcp_server.handle_request(request)
        
        if 'error' in response:
            return f"Error: {response['error']['message']}"
        
        return json.dumps(response['result'], indent=2)

# Server startup
async def start_mcp_server(host: str = "localhost", port: int = 8000):
    """Start MCP server for Claude Code integration"""

    from aiohttp import web, web_runner

    jaegis_engine = JAEGISEngine()
    mcp_server = MCPServer(jaegis_engine)

    async def handle_mcp_request(request):
        """Handle HTTP MCP requests"""
        try:
            data = await request.json()
            response = await mcp_server.handle_request(data)
            return web.json_response(response)
        except Exception as e:
            return web.json_response({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': str(e)
                }
            }, status=500)

    app = web.Application()
    app.router.add_post('/mcp', handle_mcp_request)

    runner = web_runner.AppRunner(app)
    await runner.setup()

    site = web_runner.TCPSite(runner, host, port)
    await site.start()

    print(f"JAEGIS MCP Server started on {host}:{port}")
    print("Ready for Claude Code integration!")

    # Keep server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down server...")
        await runner.cleanup()

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        # Start MCP server
        asyncio.run(start_mcp_server())
    else:
        # CLI mode
        async def main():
            cli = JAEGISCLI()

            if len(sys.argv) < 2:
                print("Usage: python jaegis-mcp-server.py <command> [args...]")
                print("       python jaegis-mcp-server.py server  # Start MCP server")
                return

            command = sys.argv[1]
            args = sys.argv[2:]

            result = await cli.execute_command(command, args)
            print(result)

        asyncio.run(main())
