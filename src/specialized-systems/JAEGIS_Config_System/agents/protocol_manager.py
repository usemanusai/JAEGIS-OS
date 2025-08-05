"""
JAEGIS Configuration Management System - Protocol Manager Agent
Agent responsible for workflow protocols and rules management
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

from ..core.config_schema import WorkflowProtocol, ProtocolRule, JAEGISConfiguration
from ..core.config_engine import ConfigurationEngine, ConfigurationChangeEvent
from ..core.agent_communication import (
    AgentCommunicationHub, AgentMessage, MessageType, MessagePriority,
    AgentInfo, ConfigurationBroadcaster
)
from ..core.security import SecurityManager, Permission

logger = logging.getLogger(__name__)

class RuleType(Enum):
    """Types of protocol rules"""
    VALIDATION = "validation"
    APPROVAL = "approval"
    NOTIFICATION = "notification"
    ESCALATION = "escalation"
    CONSTRAINT = "constraint"
    TRIGGER = "trigger"

class ProtocolStatus(Enum):
    """Protocol status states"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"

@dataclass
class ProtocolTemplate:
    """Template for creating new protocols"""
    template_id: str
    name: str
    description: str
    category: str
    default_rules: List[Dict[str, Any]]
    project_types: List[str]
    complexity_level: str = "medium"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class RuleTemplate:
    """Template for creating new rules"""
    template_id: str
    name: str
    description: str
    rule_type: RuleType
    condition_template: str
    action_template: str
    parameters: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "description": self.description,
            "rule_type": self.rule_type.value,
            "condition_template": self.condition_template,
            "action_template": self.action_template,
            "parameters": self.parameters
        }

class ProtocolManagerAgent:
    """Agent responsible for managing workflow protocols and rules"""
    
    def __init__(self, config_engine: ConfigurationEngine,
                 communication_hub: AgentCommunicationHub,
                 security_manager: SecurityManager):
        self.agent_id = "protocol_manager"
        self.agent_name = "Protocol Manager Agent"
        self.config_engine = config_engine
        self.communication_hub = communication_hub
        self.security_manager = security_manager
        self.broadcaster = ConfigurationBroadcaster(communication_hub)
        
        # Protocol management
        self.protocol_templates: Dict[str, ProtocolTemplate] = {}
        self.rule_templates: Dict[str, RuleTemplate] = {}
        self.protocol_history: List[Dict[str, Any]] = []
        
        # Performance tracking
        self.rule_execution_stats: Dict[str, Dict[str, int]] = {}
        self.protocol_usage_stats: Dict[str, int] = {}
        
        # Initialize templates
        self._initialize_default_templates()
        
        # Register with communication hub
        agent_info = AgentInfo(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            agent_type="protocol_manager",
            tier="tier_1_orchestrator",
            capabilities=[
                "protocol_management",
                "rule_creation",
                "workflow_validation",
                "approval_workflows",
                "quality_assurance"
            ]
        )
        self.communication_hub.register_agent(agent_info)
        
        # Register configuration change listener
        self.config_engine.add_change_listener(self._on_configuration_change)
        
        logger.info("Protocol Manager Agent initialized")
    
    def _initialize_default_templates(self):
        """Initialize default protocol and rule templates"""
        # Protocol templates
        self.protocol_templates = {
            "web_development": ProtocolTemplate(
                template_id="web_development",
                name="Web Development Protocol",
                description="Standard protocol for web application development projects",
                category="development",
                default_rules=[
                    {
                        "name": "Code_Review_Required",
                        "condition": "code_change_detected",
                        "action": "require_code_review",
                        "priority": 1
                    },
                    {
                        "name": "Security_Scan",
                        "condition": "deployment_requested",
                        "action": "run_security_scan",
                        "priority": 2
                    }
                ],
                project_types=["web_application", "api_service"],
                complexity_level="medium"
            ),
            "enterprise_system": ProtocolTemplate(
                template_id="enterprise_system",
                name="Enterprise System Protocol",
                description="Comprehensive protocol for enterprise-grade system development",
                category="enterprise",
                default_rules=[
                    {
                        "name": "Architecture_Review",
                        "condition": "design_phase_complete",
                        "action": "require_architecture_review",
                        "priority": 1
                    },
                    {
                        "name": "Compliance_Check",
                        "condition": "before_deployment",
                        "action": "run_compliance_validation",
                        "priority": 1
                    },
                    {
                        "name": "Performance_Testing",
                        "condition": "testing_phase",
                        "action": "require_performance_tests",
                        "priority": 2
                    }
                ],
                project_types=["enterprise_system", "data_analysis"],
                complexity_level="high"
            ),
            "prototype": ProtocolTemplate(
                template_id="prototype",
                name="Prototype Development Protocol",
                description="Lightweight protocol for rapid prototyping",
                category="prototype",
                default_rules=[
                    {
                        "name": "Quick_Validation",
                        "condition": "feature_complete",
                        "action": "basic_validation_check",
                        "priority": 3
                    }
                ],
                project_types=["prototype", "proof_of_concept"],
                complexity_level="low"
            )
        }
        
        # Rule templates
        self.rule_templates = {
            "code_review": RuleTemplate(
                template_id="code_review",
                name="Code Review Rule",
                description="Requires code review before merging changes",
                rule_type=RuleType.APPROVAL,
                condition_template="code_change_detected AND file_count > {min_files}",
                action_template="require_approval_from({reviewers})",
                parameters=["min_files", "reviewers"]
            ),
            "security_scan": RuleTemplate(
                template_id="security_scan",
                name="Security Scan Rule",
                description="Runs security scan before deployment",
                rule_type=RuleType.VALIDATION,
                condition_template="deployment_requested AND environment == '{target_env}'",
                action_template="run_security_scan(level={scan_level})",
                parameters=["target_env", "scan_level"]
            ),
            "notification": RuleTemplate(
                template_id="notification",
                name="Notification Rule",
                description="Sends notifications based on conditions",
                rule_type=RuleType.NOTIFICATION,
                condition_template="event_type == '{event}' AND severity >= {min_severity}",
                action_template="send_notification(recipients={recipients}, message='{message}')",
                parameters=["event", "min_severity", "recipients", "message"]
            ),
            "escalation": RuleTemplate(
                template_id="escalation",
                name="Escalation Rule",
                description="Escalates issues based on conditions",
                rule_type=RuleType.ESCALATION,
                condition_template="issue_age > {max_age} AND priority >= {min_priority}",
                action_template="escalate_to({escalation_target})",
                parameters=["max_age", "min_priority", "escalation_target"]
            )
        }
    
    async def create_protocol(self, session_id: str, protocol_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow protocol"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            # Generate protocol ID if not provided
            protocol_id = protocol_data.get("protocol_id", str(uuid.uuid4()))
            
            # Create protocol object
            protocol = WorkflowProtocol(
                protocol_id=protocol_id,
                name=protocol_data["name"],
                description=protocol_data.get("description", ""),
                project_types=protocol_data.get("project_types", []),
                agent_constraints=protocol_data.get("agent_constraints", {}),
                approval_required=protocol_data.get("approval_required", False),
                escalation_rules=protocol_data.get("escalation_rules", [])
            )
            
            # Add rules if provided
            if "rules" in protocol_data:
                for rule_data in protocol_data["rules"]:
                    rule = ProtocolRule(
                        rule_id=rule_data.get("rule_id", str(uuid.uuid4())),
                        name=rule_data["name"],
                        description=rule_data.get("description", ""),
                        condition=rule_data["condition"],
                        action=rule_data["action"],
                        priority=rule_data.get("priority", 1),
                        enabled=rule_data.get("enabled", True)
                    )
                    protocol.add_rule(rule)
            
            # Add to configuration
            success = self.config_engine.add_protocol(protocol)
            
            if success:
                # Record in history
                user = self.security_manager.validate_session(session_id)
                self._record_protocol_action("created", protocol, user.user_id if user else "unknown")
                
                # Broadcast change
                await self.broadcaster.broadcast_protocol_change(
                    protocol_id, "added", protocol.to_dict()
                )
                
                return {
                    "success": True,
                    "protocol_id": protocol_id,
                    "message": f"Protocol '{protocol.name}' created successfully"
                }
            else:
                return {"success": False, "error": "Failed to create protocol"}
                
        except Exception as e:
            logger.error(f"Error creating protocol: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_protocol(self, session_id: str, protocol_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing protocol"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            # Get current configuration
            current_config = self.config_engine.get_current_config()
            
            # Find existing protocol
            existing_protocol = None
            for protocol in current_config.protocols:
                if protocol.protocol_id == protocol_id:
                    existing_protocol = protocol
                    break
            
            if not existing_protocol:
                return {"success": False, "error": "Protocol not found"}
            
            # Create updated protocol
            updated_protocol = WorkflowProtocol(
                protocol_id=protocol_id,
                name=updates.get("name", existing_protocol.name),
                description=updates.get("description", existing_protocol.description),
                rules=existing_protocol.rules.copy(),
                project_types=updates.get("project_types", existing_protocol.project_types),
                agent_constraints=updates.get("agent_constraints", existing_protocol.agent_constraints),
                approval_required=updates.get("approval_required", existing_protocol.approval_required),
                escalation_rules=updates.get("escalation_rules", existing_protocol.escalation_rules),
                created_at=existing_protocol.created_at,
                version=existing_protocol.version
            )
            
            # Update rules if provided
            if "rules" in updates:
                updated_protocol.rules = []
                for rule_data in updates["rules"]:
                    rule = ProtocolRule(
                        rule_id=rule_data.get("rule_id", str(uuid.uuid4())),
                        name=rule_data["name"],
                        description=rule_data.get("description", ""),
                        condition=rule_data["condition"],
                        action=rule_data["action"],
                        priority=rule_data.get("priority", 1),
                        enabled=rule_data.get("enabled", True)
                    )
                    updated_protocol.add_rule(rule)
            
            # Update in configuration
            success = self.config_engine.update_protocol(updated_protocol)
            
            if success:
                # Record in history
                user = self.security_manager.validate_session(session_id)
                self._record_protocol_action("updated", updated_protocol, user.user_id if user else "unknown")
                
                # Broadcast change
                await self.broadcaster.broadcast_protocol_change(
                    protocol_id, "updated", updated_protocol.to_dict()
                )
                
                return {
                    "success": True,
                    "message": f"Protocol '{updated_protocol.name}' updated successfully"
                }
            else:
                return {"success": False, "error": "Failed to update protocol"}
                
        except Exception as e:
            logger.error(f"Error updating protocol: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_protocol(self, session_id: str, protocol_id: str) -> Dict[str, Any]:
        """Delete a protocol"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            # Get protocol name for logging
            current_config = self.config_engine.get_current_config()
            protocol_name = "Unknown"
            for protocol in current_config.protocols:
                if protocol.protocol_id == protocol_id:
                    protocol_name = protocol.name
                    break
            
            # Remove from configuration
            success = self.config_engine.remove_protocol(protocol_id)
            
            if success:
                # Record in history
                user = self.security_manager.validate_session(session_id)
                self._record_protocol_action("deleted", None, user.user_id if user else "unknown", 
                                           {"protocol_id": protocol_id, "protocol_name": protocol_name})
                
                # Broadcast change
                await self.broadcaster.broadcast_protocol_change(
                    protocol_id, "removed", {"protocol_id": protocol_id}
                )
                
                return {
                    "success": True,
                    "message": f"Protocol '{protocol_name}' deleted successfully"
                }
            else:
                return {"success": False, "error": "Failed to delete protocol"}
                
        except Exception as e:
            logger.error(f"Error deleting protocol: {e}")
            return {"success": False, "error": str(e)}
    
    def get_protocols(self, session_id: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get list of protocols with optional filtering"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.READ_CONFIG):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            current_config = self.config_engine.get_current_config()
            protocols = current_config.protocols
            
            # Apply filters if provided
            if filters:
                if "project_type" in filters:
                    project_type = filters["project_type"]
                    protocols = [p for p in protocols if project_type in p.project_types]
                
                if "status" in filters:
                    # This would filter by status if we had a status field
                    pass
                
                if "search" in filters:
                    search_term = filters["search"].lower()
                    protocols = [p for p in protocols 
                               if search_term in p.name.lower() or search_term in p.description.lower()]
            
            # Convert to dict format
            protocol_list = []
            for protocol in protocols:
                protocol_dict = protocol.to_dict()
                protocol_dict["rule_count"] = len(protocol.rules)
                protocol_dict["usage_count"] = self.protocol_usage_stats.get(protocol.protocol_id, 0)
                protocol_list.append(protocol_dict)
            
            return {
                "success": True,
                "protocols": protocol_list,
                "total_count": len(protocol_list)
            }
            
        except Exception as e:
            logger.error(f"Error getting protocols: {e}")
            return {"success": False, "error": str(e)}
    
    def get_protocol_templates(self) -> Dict[str, Any]:
        """Get available protocol templates"""
        return {
            "success": True,
            "templates": [template.to_dict() for template in self.protocol_templates.values()]
        }
    
    def get_rule_templates(self) -> Dict[str, Any]:
        """Get available rule templates"""
        return {
            "success": True,
            "templates": [template.to_dict() for template in self.rule_templates.values()]
        }
    
    async def create_protocol_from_template(self, session_id: str, template_id: str, 
                                          customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Create a protocol from a template"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        template = self.protocol_templates.get(template_id)
        if not template:
            return {"success": False, "error": "Template not found"}
        
        try:
            # Create protocol data from template
            protocol_data = {
                "name": customizations.get("name", template.name),
                "description": customizations.get("description", template.description),
                "project_types": customizations.get("project_types", template.project_types),
                "rules": []
            }
            
            # Add default rules from template
            for rule_template in template.default_rules:
                rule_data = {
                    "name": rule_template["name"],
                    "condition": rule_template["condition"],
                    "action": rule_template["action"],
                    "priority": rule_template["priority"]
                }
                protocol_data["rules"].append(rule_data)
            
            # Add custom rules if provided
            if "additional_rules" in customizations:
                protocol_data["rules"].extend(customizations["additional_rules"])
            
            # Create the protocol
            result = await self.create_protocol(session_id, protocol_data)
            
            if result["success"]:
                # Update template usage stats
                if template_id not in self.protocol_usage_stats:
                    self.protocol_usage_stats[template_id] = 0
                self.protocol_usage_stats[template_id] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Error creating protocol from template: {e}")
            return {"success": False, "error": str(e)}
    
    def validate_protocol(self, protocol_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate protocol configuration"""
        errors = []
        warnings = []
        
        # Required fields
        if not protocol_data.get("name"):
            errors.append("Protocol name is required")
        
        if not protocol_data.get("description"):
            warnings.append("Protocol description is recommended")
        
        # Validate rules
        rules = protocol_data.get("rules", [])
        for i, rule in enumerate(rules):
            if not rule.get("name"):
                errors.append(f"Rule {i+1}: Name is required")
            
            if not rule.get("condition"):
                errors.append(f"Rule {i+1}: Condition is required")
            
            if not rule.get("action"):
                errors.append(f"Rule {i+1}: Action is required")
            
            # Validate condition syntax (basic check)
            condition = rule.get("condition", "")
            if condition and not self._validate_condition_syntax(condition):
                warnings.append(f"Rule {i+1}: Condition syntax may be invalid")
        
        # Check for duplicate rule names
        rule_names = [rule.get("name", "") for rule in rules]
        duplicates = [name for name in rule_names if rule_names.count(name) > 1 and name]
        if duplicates:
            errors.append(f"Duplicate rule names found: {', '.join(set(duplicates))}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _validate_condition_syntax(self, condition: str) -> bool:
        """Basic validation of condition syntax"""
        # This is a simplified validation - in production, you'd want more robust parsing
        allowed_operators = ["AND", "OR", "NOT", "==", "!=", ">", "<", ">=", "<="]
        allowed_functions = ["contains", "starts_with", "ends_with", "matches"]
        
        # Check for basic syntax issues
        if not condition.strip():
            return False
        
        # Check for balanced parentheses
        open_count = condition.count("(")
        close_count = condition.count(")")
        if open_count != close_count:
            return False
        
        return True
    
    def _record_protocol_action(self, action: str, protocol: Optional[WorkflowProtocol], 
                               user_id: str, additional_data: Optional[Dict[str, Any]] = None):
        """Record protocol action in history"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_id": user_id,
            "protocol_id": protocol.protocol_id if protocol else None,
            "protocol_name": protocol.name if protocol else None
        }
        
        if additional_data:
            record.update(additional_data)
        
        self.protocol_history.append(record)
        
        # Keep only last 1000 records
        if len(self.protocol_history) > 1000:
            self.protocol_history = self.protocol_history[-1000:]
    
    def get_protocol_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get protocol change history"""
        return self.protocol_history[-limit:]
    
    async def _on_configuration_change(self, event: ConfigurationChangeEvent):
        """Handle configuration change events"""
        if event.parameter_name.startswith("protocol"):
            logger.info(f"Protocol configuration change: {event.parameter_name}")
    
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get agent statistics"""
        current_config = self.config_engine.get_current_config()
        
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "total_protocols": len(current_config.protocols),
            "total_rules": sum(len(p.rules) for p in current_config.protocols),
            "available_templates": len(self.protocol_templates),
            "protocol_actions": len(self.protocol_history),
            "most_used_template": max(self.protocol_usage_stats.keys(), 
                                    key=lambda k: self.protocol_usage_stats[k]) if self.protocol_usage_stats else None
        }
