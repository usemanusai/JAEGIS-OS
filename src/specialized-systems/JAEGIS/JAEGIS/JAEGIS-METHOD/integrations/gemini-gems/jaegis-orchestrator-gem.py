"""
JAEGIS Orchestrator Gem for Google Gemini
Main coordinator for JAEGIS methodology within Google's AI ecosystem
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import FunctionDeclaration, Tool

class JAEGISOrchestratorGem:
    """Main JAEGIS Method coordinator Gem for Gemini"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.sessions = {}
        self.jaegis_functions = self._setup_jaegis_functions()
        
    def _setup_jaegis_functions(self) -> List[FunctionDeclaration]:
        """Setup JAEGIS function declarations for Gemini"""
        
        return [
            FunctionDeclaration(
                name="jaegis_init_project",
                description="Initialize a new JAEGIS project with specified type and configuration",
                parameters={
                    "type": "objectproperties": {
                        "project_name": {
                            "type": "string",
                            "description": "Name_of_the_project_to_createproject_type": {
                            "type": "string",
                            "description": "Type of project (web-app, mobile-app, game, etc.)",
                            "enum": ["web-app", "mobile-app", "game", "api", "desktop-app", "generaldescription": {
                            "type": "string",
                            "description": "Brief description of the project"
                        }
                    },
                    "required": ["project_name", "project_type"]
                }
            ),
            FunctionDeclaration(
                name="jaegis_start_brainstorming",
                description="Start a psychology-backed brainstorming session for idea generation",
                parameters={
                    "type": "objectproperties": {
                        "session_id": {
                            "type": "string",
                            "description": "Session_ID_from_project_initializationtopic": {
                            "type": "string",
                            "description": "Topic_or_problem_to_brainstorm_abouttechniques": {
                            "type": "arrayitems": {"type": "string"},
                            "description": "Specific_brainstorming_techniques_to_useduration": {
                            "type": "integer",
                            "description": "Duration in minutes for brainstorming session",
                            "default": 30
                        }
                    },
                    "required": ["session_id", "topic"]
                }
            ),
            FunctionDeclaration(
                name="jaegis_create_prd",
                description="Create a Product Requirements Document using interactive templates",
                parameters={
                    "type": "objectproperties": {
                        "session_id": {
                            "type": "string",
                            "description": "Session_ID_from_project_initializationtemplate_type": {
                            "type": "string",
                            "description": "Type of PRD template to use",
                            "enum": ["standard", "comprehensive", "agile", "startupinteractive": {
                            "type": "boolean",
                            "description": "Whether to use interactive mode",
                            "default": True
                        }
                    },
                    "required": ["session_id"]
                }
            ),
            FunctionDeclaration(
                name="jaegis_design_architecture",
                description="Design technical architecture with AI guidance",
                parameters={
                    "type": "objectproperties": {
                        "session_id": {
                            "type": "string",
                            "description": "Session_ID_from_project_initializationarchitecture_type": {
                            "type": "string",
                            "description": "Type of architecture to design",
                            "enum": ["monolithic", "microservices", "serverless", "hybridtechnology_preferences": {
                            "type": "arrayitems": {"type": "string"},
                            "description": "Preferred technologies or frameworks"
                        }
                    },
                    "required": ["session_id"]
                }
            ),
            FunctionDeclaration(
                name="jaegis_get_session_status",
                description="Get current status and progress of a JAEGIS session",
                parameters={
                    "type": "objectproperties": {
                        "session_id": {
                            "type": "string",
                            "description": "Session ID to check status for"
                        }
                    },
                    "required": ["session_id"]
                }
            ),
            FunctionDeclaration(
                name="jaegis_get_templates",
                description="Get available JAEGIS templates for different purposes",
                parameters={
                    "type": "objectproperties": {
                        "template_type": {
                            "type": "string",
                            "description": "Type of templates to retrieve",
                            "enum": ["prd", "architecture", "brainstorming", "development", "all"]
                        }
                    }
                }
            )
        ]
    
    async def handle_function_call(self, function_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle function calls from Gemini"""
        
        if function_name == "jaegis_init_project":
            return await self._init_project(parameters)
        elif function_name == "jaegis_start_brainstorming":
            return await self._start_brainstorming(parameters)
        elif function_name == "jaegis_create_prd":
            return await self._create_prd(parameters)
        elif function_name == "jaegis_design_architecture":
            return await self._design_architecture(parameters)
        elif function_name == "jaegis_get_session_status":
            return await self._get_session_status(parameters)
        elif function_name == "jaegis_get_templates":
            return await self._get_templates(parameters)
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    async def _init_project(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize new JAEGIS project"""
        
        session_id = str(uuid.uuid4())
        project_name = params["project_name"]
        project_type = params["project_type"]
        description = params.get("description", "")
        
        session = JAEGISSession(
            session_id=session_id,
            project_name=project_name,
            project_type=project_type,
            description=description,
            created_at=datetime.now(),
            current_phase="initialization"
        )
        
        self.sessions[session_id] = session
        
        return {
            "session_id": session_id,
            "project_name": project_name,
            "project_type": project_type,
            "status": "initialized",
            "next_steps": [
                "Start brainstorming with jaegis_start_brainstorming",
                "Create PRD with jaegis_create_prd",
                "Design architecture with jaegis_design_architecture"
            ],
            "message": f"✅ JAEGIS project '{project_name}' initialized successfully! Ready to begin the JAEGIS methodology."
        }
    
    async def _start_brainstorming(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Start brainstorming session"""
        
        session_id = params["session_id"]
        topic = params["topic"]
        techniques = params.get("techniques", [])
        duration = params.get("duration", 30)
        
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Invalid session ID"}
        
        brainstorm_id = str(uuid.uuid4())
        
        # Generate initial ideas using psychology-backed techniques
        initial_ideas = await self._generate_brainstorm_ideas(topic, techniques)
        
        brainstorm_result = {
            "brainstorm_id": brainstorm_id,
            "topic": topic,
            "techniques_used": techniques or ["free_association", "stakeholder_perspective", "what_if_analysis"],
            "initial_ideas": initial_ideas,
            "duration": duration,
            "status": "active"
        }
        
        session.brainstorm_results = brainstorm_result
        session.current_phase = "brainstorming"
        
        return {
            "brainstorm_id": brainstorm_id,
            "initial_ideas": initial_ideas,
            "techniques_suggested": [
                "analogical_thinking",
                "reverse_brainstorming",
                "six_thinking_hats",
                "scamper_method"
            ],
            "message": f"🧠 Brainstorming session started for '{topic}'! Generated {len(initial_ideas)} initial ideas.",
            "next_action": "Continue developing these ideas or move to PRD creation"
        }
    
    async def _create_prd(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create Product Requirements Document"""
        
        session_id = params["session_id"]
        template_type = params.get("template_type", "standard")
        interactive = params.get("interactive", True)
        
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Invalid session ID"}
        
        prd_id = str(uuid.uuid4())
        
        # Generate PRD structure based on template type
        prd_sections = self._get_prd_template_sections(template_type)
        
        prd_result = {
            "prd_id": prd_id,
            "template_type": template_type,
            "sections": prd_sections,
            "tool_205": {section: False for section in prd_sections},
            "interactive_mode": interactive
        }
        
        session.prd_results = prd_result
        session.current_phase = "modeling"
        
        return {
            "prd_id": prd_id,
            "template_type": template_type,
            "sections": prd_sections,
            "current_section": prd_sections[0] if prd_sections else None,
            "message": f"📋 PRD creation started using {template_type} template! Let's begin with the first section.",
            "interactive_prompt": f"Let's start with '{prd_sections[0]}'. What should we include in this section based on your project?"
        }
    
    async def _design_architecture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Design technical architecture"""
        
        session_id = params["session_id"]
        architecture_type = params.get("architecture_type", "monolithic")
        tech_preferences = params.get("technology_preferences", [])
        
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Invalid session ID"}
        
        architecture_id = str(uuid.uuid4())
        
        # Generate architecture components based on type
        architecture_components = self._get_architecture_components(architecture_type, session.project_type)
        
        architecture_result = {
            "architecture_id": architecture_id,
            "architecture_type": architecture_type,
            "components": architecture_components,
            "technology_preferences": tech_preferences,
            "diagrams": ["system_overview", "component_diagram", "data_flow"],
            "status": "in_progress"
        }
        
        session.architecture_results = architecture_result
        session.current_phase = "architecture"
        
        return {
            "architecture_id": architecture_id,
            "architecture_type": architecture_type,
            "components": architecture_components,
            "recommended_technologies": self._get_tech_recommendations(session.project_type, architecture_type),
            "message": f"🏗️ Architecture design started using {architecture_type} pattern! Here are the main components.",
            "next_steps": [
                "Review and refine component definitions",
                "Select specific technologies",
                "Define data flow and APIs",
                "Create detailed diagrams"
            ]
        }
    
    async def _get_session_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get session status"""
        
        session_id = params["session_id"]
        session = self.sessions.get(session_id)
        
        if not session:
            return {"error": "Invalid session ID"}
        
        progress = self._calculate_session_progress(session)
        
        return {
            "session_id": session_id,
            "project_name": session.project_name,
            "project_type": session.project_type,
            "current_phase": session.current_phase,
            "progress": progress,
            "created_at": session.created_at.isoformat(),
            "phases_completed": progress["completed_phases"],
            "next_actions": self._get_next_actions(session),
            "message": f"📊 Project '{session.project_name}' is in {session.current_phase} phase ({progress['overall_progress']:.0%} complete)"
        }
    
    async def _get_templates(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get available templates"""
        
        template_type = params.get("template_type", "all")
        
        templates = {
            "prd": [
                {"name": "Standard_PRD", "id": "standard", "description": "Comprehensive product requirements"},
                {"name": "Agile_PRD", "id": "agile", "description": "Lightweight, iterative requirements"},
                {"name": "Startup_PRD", "id": "startup", "description": "MVP-focused requirements"}
            ],
            "architecture": [
                {"name": "Monolithic_Architecture", "id": "monolithic", "description": "Single deployable unit"},
                {"name": "Microservices_Architecture", "id": "microservices", "description": "Distributed services"},
                {"name": "Serverless_Architecture", "id": "serverless", "description": "Function-based architecture"}
            ],
            "brainstorming": [
                {"name": "Creative_Ideation", "id": "creative", "description": "Open-ended idea generation"},
                {"name": "Problem-Solution_Fit", "id": "problem_solution", "description": "Focused problem solving"},
                {"name": "Feature_Brainstorming", "id": "feature", "description": "Product feature ideation"}
            ]
        }
        
        if template_type == "all":
            return {"templatestemplates_else_return_templates": {template_type: templates.get(template_type, [])}}
    
    # Helper methods
    async def _generate_brainstorm_ideas(self, topic: str, techniques: List[str]) -> List[str]:
        """Generate initial brainstorming ideas"""
        
        # Mock implementation - in real version would use advanced elicitation
        ideas = [
            f"Innovative approach to {topic} using AI/ML",
            f"User-centric solution for {topic} challenges",
            f"Scalable platform addressing {topic} needs",
            f"Mobile-first approach to {topic}",
            f"Community-driven solution for {topic}"
        ]
        
        return ideas[:5]  # Return top 5 ideas
    
    def _get_prd_template_sections(self, template_type: str) -> List[str]:
        """Get PRD template sections"""
        
        templates = {
            "standard": [
                "Executive Summary",
                "User Personas",
                "Functional Requirements",
                "Technical Requirements",
                "Success Metrics",
                "Timeline and Milestones"
            ],
            "comprehensive": [
                "Executive Summary",
                "Market Analysis",
                "User Personas",
                "User Stories",
                "Functional Requirements",
                "Technical Requirements",
                "UI/UX Requirements",
                "Success Metrics",
                "Risk Assessment",
                "Timeline and Milestones"
            ],
            "agile": [
                "Product Vision",
                "User Stories",
                "Acceptance Criteria",
                "Definition of Done",
                "Success Metrics"
            ],
            "startup": [
                "Problem Statement",
                "Solution Overview",
                "MVP Features",
                "Success Metrics",
                "Go-to-Market Strategy"
            ]
        }
        
        return templates.get(template_type, templates["standard"])
    
    def _get_architecture_components(self, arch_type: str, project_type: str) -> List[Dict[str, str]]:
        """Get architecture components"""
        
        base_components = [
            {"name": "Frontend", "description": "User interface layer"},
            {"name": "Backend_API", "description": "Business logic and data processing"},
            {"name": "Database", "description": "Data storage and management"},
            {"name": "Authentication", "description": "User authentication and authorization"}
        ]
        
        if arch_type == "microservices":
            base_components.extend([
                {"name": "API_Gateway", "description": "Request routing and management"},
                {"name": "Service_Discovery", "description": "Service registration and discovery"},
                {"name": "Message_Queue", "description": "Asynchronous communication"}
            ])
        elif arch_type == "serverless":
            base_components.extend([
                {"name": "Function_Runtime", "description": "Serverless function execution"},
                {"name": "Event_Triggers", "description": "Event-driven function invocation"},
                {"name": "Managed_Services", "description": "Cloud-managed infrastructure"}
            ])
        
        return base_components
    
    def _get_tech_recommendations(self, project_type: str, arch_type: str) -> List[str]:
        """Get technology recommendations"""
        
        recommendations = {
            "web-app": ["React", "Node.js", "PostgreSQL", "Redis"],
            "mobile-app": ["React Native", "Firebase", "MongoDB"],
            "api": ["FastAPI", "PostgreSQL", "Docker", "Kubernetes"],
            "game": ["Unity", "C#", "SQLite", "Photon"]
        }
        
        return recommendations.get(project_type, ["Python", "JavaScript", "PostgreSQL"])
    
    def _calculate_session_progress(self, session: 'JAEGISSession') -> Dict[str, Any]:
        """Calculate session progress"""
        
        phases = ["initialization", "brainstorming", "modeling", "architecture", "development"]
        current_index = phases.index(session.current_phase) if session.current_phase in phases else 0
        
        return {
            "current_phase": session.current_phase,
            "completed_phases": phases[:current_index],
            "remaining_phases": phases[current_index + 1:],
            "overall_progress": current_index / len(phases)
        }
    
    def _get_next_actions(self, session: 'JAEGISSession') -> List[str]:
        """Get next recommended actions"""
        
        if session.current_phase == "initialization":
            return ["Start brainstorming session", "Define project scope"]
        elif session.current_phase == "brainstorming":
            return ["Create PRD", "Refine ideas"]
        elif session.current_phase == "modeling":
            return ["Design architecture", "Validate requirements"]
        elif session.current_phase == "architecture":
            return ["Begin development", "Set up infrastructure"]
        else:
            return ["Continue development", "Test and iterate"]

@dataclass
class JAEGISSession:
    """JAEGIS session data for Gemini Gems"""
    session_id: str
    project_name: str
    project_type: str
    description: str
    created_at: datetime
    current_phase: str = "initialization"
    brainstorm_results: Optional[Dict] = None
    prd_results: Optional[Dict] = None
    architecture_results: Optional[Dict] = None
    development_results: Optional[Dict] = None

# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_jaegis_gem():
        # Initialize the gem (requires Gemini API key)
        # gem = JAEGISOrchestratorGem("your-api-key-here")
        
        # Test function calls
        print("JAEGIS Orchestrator Gem - Function Definitions:")
        
        # Mock gem for testing
        class MockGem:
            def __init__(self):
                self.jaegis_functions = JAEGISOrchestratorGem("mock")._setup_jaegis_functions()
        
        mock_gem = MockGem()
        
        for func in mock_gem.jaegis_functions:
            print(f"\n📋 Function: {func.name}")
            print(f"   Description: {func.description}")
            print(f"   Parameters: {list(func.parameters.get('properties', {}).keys())}")
    
    asyncio.run(test_jaegis_gem())
