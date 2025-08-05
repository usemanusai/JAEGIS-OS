"""
JAEGIS Configuration Management System - Quality Assurance Rules Manager
Interface for managing QA rules and validation criteria
"""

import logging
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import re
import json

from ..core.config_schema import ProtocolRule
from ..core.security import SecurityManager, Permission

logger = logging.getLogger(__name__)

class QACategory(Enum):
    """Categories of QA rules"""
    CODE_QUALITY = "code_quality"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    COMPLIANCE = "compliance"
    ACCESSIBILITY = "accessibility"
    USABILITY = "usability"

class QASeverity(Enum):
    """Severity levels for QA rules"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class QAScope(Enum):
    """Scope of QA rule application"""
    FILE = "file"
    MODULE = "module"
    PROJECT = "project"
    GLOBAL = "global"

@dataclass
class QARule:
    """Quality Assurance rule definition"""
    rule_id: str
    name: str
    description: str
    category: QACategory
    severity: QASeverity
    scope: QAScope
    condition: str
    validation_logic: str
    error_message: str
    fix_suggestion: str = ""
    enabled: bool = True
    auto_fix: bool = False
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "severity": self.severity.value,
            "scope": self.scope.value,
            "condition": self.condition,
            "validation_logic": self.validation_logic,
            "error_message": self.error_message,
            "fix_suggestion": self.fix_suggestion,
            "enabled": self.enabled,
            "auto_fix": self.auto_fix,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QARule':
        """Create from dictionary"""
        return cls(
            rule_id=data["rule_id"],
            name=data["name"],
            description=data["description"],
            category=QACategory(data["category"]),
            severity=QASeverity(data["severity"]),
            scope=QAScope(data["scope"]),
            condition=data["condition"],
            validation_logic=data["validation_logic"],
            error_message=data["error_message"],
            fix_suggestion=data.get("fix_suggestion", ""),
            enabled=data.get("enabled", True),
            auto_fix=data.get("auto_fix", False),
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            modified_at=datetime.fromisoformat(data.get("modified_at", datetime.now().isoformat()))
        )

@dataclass
class QAViolation:
    """QA rule violation"""
    violation_id: str
    rule_id: str
    file_path: str
    line_number: Optional[int]
    column_number: Optional[int]
    message: str
    severity: QASeverity
    context: Dict[str, Any]
    detected_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution_note: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "violation_id": self.violation_id,
            "rule_id": self.rule_id,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "column_number": self.column_number,
            "message": self.message,
            "severity": self.severity.value,
            "context": self.context,
            "detected_at": self.detected_at.isoformat(),
            "resolved": self.resolved,
            "resolution_note": self.resolution_note
        }

@dataclass
class QARuleSet:
    """Collection of QA rules for specific contexts"""
    ruleset_id: str
    name: str
    description: str
    rules: List[str]  # Rule IDs
    project_types: List[str]
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "ruleset_id": self.ruleset_id,
            "name": self.name,
            "description": self.description,
            "rules": self.rules,
            "project_types": self.project_types,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat()
        }

class QualityAssuranceRulesManager:
    """Manager for QA rules and validation criteria"""
    
    def __init__(self, security_manager: SecurityManager):
        self.security_manager = security_manager
        
        # Storage
        self.qa_rules: Dict[str, QARule] = {}
        self.qa_rulesets: Dict[str, QARuleSet] = {}
        self.violations: List[QAViolation] = []
        
        # Statistics
        self.rule_execution_stats: Dict[str, Dict[str, int]] = {}
        self.violation_trends: Dict[str, List[int]] = {}
        
        # Initialize default rules
        self._initialize_default_rules()
        self._initialize_default_rulesets()
        
        logger.info("Quality Assurance Rules Manager initialized")
    
    def _initialize_default_rules(self):
        """Initialize default QA rules"""
        default_rules = [
            {
                "rule_id": "code_complexity",
                "name": "Code_Complexity_Check",
                "description": "Checks for overly complex functions and methods",
                "category": QACategory.CODE_QUALITY,
                "severity": QASeverity.WARNING,
                "scope": QAScope.FILE,
                "condition": "function_detected",
                "validation_logic": "cyclomatic_complexity > 10",
                "error_message": "Function complexity exceeds recommended threshold (10)",
                "fix_suggestion": "Consider breaking down the function into smaller, more focused functions",
                "tags": ["complexity", "maintainability"]
            },
            {
                "rule_id": "security_hardcoded_secrets",
                "name": "Hardcoded_Secrets_Detection",
                "description": "Detects hardcoded passwords, API keys, and other secrets",
                "category": QACategory.SECURITY,
                "severity": QASeverity.CRITICAL,
                "scope": QAScope.FILE,
                "condition": "code_content_scan",
                "validation_logic": "contains_pattern(r'(password|api_key|secret)\\s*=\\s*[\"\\'][^\"\\'\n]+[\"\\']')",
                "error_message": "Hardcoded secret detected in source code",
                "fix_suggestion": "Move secrets to environment variables or secure configuration",
                "tags": ["security", "secrets"]
            },
            {
                "rule_id": "documentation_missing",
                "name": "Missing_Documentation",
                "description": "Checks for missing function and class documentation",
                "category": QACategory.DOCUMENTATION,
                "severity": QASeverity.WARNING,
                "scope": QAScope.FILE,
                "condition": "function_or_class_detected",
                "validation_logic": "missing_docstring",
                "error_message": "Function or class is missing documentation",
                "fix_suggestion": "Add docstring explaining the purpose, parameters, and return value",
                "tags": ["documentation", "maintainability"]
            },
            {
                "rule_id": "performance_inefficient_loop",
                "name": "Inefficient_Loop_Detection",
                "description": "Detects potentially inefficient loop patterns",
                "category": QACategory.PERFORMANCE,
                "severity": QASeverity.WARNING,
                "scope": QAScope.FILE,
                "condition": "loop_detected",
                "validation_logic": "nested_loop_depth > 3 OR loop_contains_expensive_operation",
                "error_message": "Potentially inefficient loop pattern detected",
                "fix_suggestion": "Consider optimizing loop logic or using more efficient algorithms",
                "tags": ["performance", "optimization"]
            },
            {
                "rule_id": "testing_missing_tests",
                "name": "Missing_Test_Coverage",
                "description": "Checks for functions without corresponding tests",
                "category": QACategory.TESTING,
                "severity": QASeverity.ERROR,
                "scope": QAScope.MODULE,
                "condition": "public_function_detected",
                "validation_logic": "no_corresponding_test_found",
                "error_message": "Public function lacks test coverage",
                "fix_suggestion": "Create unit tests for this function",
                "tags": ["testing", "coverage"]
            },
            {
                "rule_id": "accessibility_missing_alt_text",
                "name": "Missing_Alt_Text",
                "description": "Checks for images without alt text in web content",
                "category": QACategory.ACCESSIBILITY,
                "severity": QASeverity.ERROR,
                "scope": QAScope.FILE,
                "condition": "html_img_tag_detected",
                "validation_logic": "img_tag_missing_alt_attribute",
                "error_message": "Image element is missing alt text for accessibility",
                "fix_suggestion": "Add descriptive alt text to the image element",
                "tags": ["accessibility", "web"]
            }
        ]
        
        for rule_data in default_rules:
            rule = QARule(
                rule_id=rule_data["rule_id"],
                name=rule_data["name"],
                description=rule_data["description"],
                category=rule_data["category"],
                severity=rule_data["severity"],
                scope=rule_data["scope"],
                condition=rule_data["condition"],
                validation_logic=rule_data["validation_logic"],
                error_message=rule_data["error_message"],
                fix_suggestion=rule_data["fix_suggestion"],
                tags=rule_data["tags"]
            )
            self.qa_rules[rule.rule_id] = rule
    
    def _initialize_default_rulesets(self):
        """Initialize default rule sets"""
        default_rulesets = [
            {
                "ruleset_id": "web_development",
                "name": "Web_Development_QA_Rules",
                "description": "Quality assurance rules for web development projects",
                "rules": ["code_complexity", "security_hardcoded_secrets", "documentation_missing", "accessibility_missing_alt_text"],
                "project_types": ["web_application", "frontend"]
            },
            {
                "ruleset_id": "api_development",
                "name": "API_Development_QA_Rules",
                "description": "Quality assurance rules for API development",
                "rules": ["code_complexity", "security_hardcoded_secrets", "documentation_missing", "testing_missing_tests"],
                "project_types": ["api_service", "backend"]
            },
            {
                "ruleset_id": "enterprise_system",
                "name": "Enterprise_System_QA_Rules",
                "description": "Comprehensive QA rules for enterprise systems",
                "rules": list(self.qa_rules.keys()),  # All rules
                "project_types": ["enterprise_system", "data_analysis"]
            }
        ]
        
        for ruleset_data in default_rulesets:
            ruleset = QARuleSet(
                ruleset_id=ruleset_data["ruleset_id"],
                name=ruleset_data["name"],
                description=ruleset_data["description"],
                rules=ruleset_data["rules"],
                project_types=ruleset_data["project_types"]
            )
            self.qa_rulesets[ruleset.ruleset_id] = ruleset
    
    def create_qa_rule(self, session_id: str, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new QA rule"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            # Generate rule ID if not provided
            rule_id = rule_data.get("rule_id", str(uuid.uuid4()))
            
            # Validate required fields
            required_fields = ["name", "description", "category", "severity", "scope", "condition", "validation_logic", "error_message"]
            for field in required_fields:
                if field not in rule_data:
                    return {"success": False, "error": f"Missing required field: {field}"}
            
            # Create rule
            rule = QARule(
                rule_id=rule_id,
                name=rule_data["name"],
                description=rule_data["description"],
                category=QACategory(rule_data["category"]),
                severity=QASeverity(rule_data["severity"]),
                scope=QAScope(rule_data["scope"]),
                condition=rule_data["condition"],
                validation_logic=rule_data["validation_logic"],
                error_message=rule_data["error_message"],
                fix_suggestion=rule_data.get("fix_suggestion", ""),
                enabled=rule_data.get("enabled", True),
                auto_fix=rule_data.get("auto_fix", False),
                tags=rule_data.get("tags", [])
            )
            
            # Validate rule logic
            validation_result = self._validate_rule_logic(rule)
            if not validation_result["valid"]:
                return {"success": False, "error": f"Invalid rule logic: {validation_result['error']}"}
            
            # Store rule
            self.qa_rules[rule_id] = rule
            
            return {
                "success": True,
                "rule_id": rule_id,
                "message": f"QA rule '{rule.name}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating QA rule: {e}")
            return {"success": False, "error": str(e)}
    
    def update_qa_rule(self, session_id: str, rule_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing QA rule"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        if rule_id not in self.qa_rules:
            return {"success": False, "error": "QA rule not found"}
        
        try:
            rule = self.qa_rules[rule_id]
            
            # Update fields
            if "name" in updates:
                rule.name = updates["name"]
            if "description" in updates:
                rule.description = updates["description"]
            if "category" in updates:
                rule.category = QACategory(updates["category"])
            if "severity" in updates:
                rule.severity = QASeverity(updates["severity"])
            if "scope" in updates:
                rule.scope = QAScope(updates["scope"])
            if "condition" in updates:
                rule.condition = updates["condition"]
            if "validation_logic" in updates:
                rule.validation_logic = updates["validation_logic"]
            if "error_message" in updates:
                rule.error_message = updates["error_message"]
            if "fix_suggestion" in updates:
                rule.fix_suggestion = updates["fix_suggestion"]
            if "enabled" in updates:
                rule.enabled = updates["enabled"]
            if "auto_fix" in updates:
                rule.auto_fix = updates["auto_fix"]
            if "tags" in updates:
                rule.tags = updates["tags"]
            
            rule.modified_at = datetime.now()
            
            # Validate updated rule
            validation_result = self._validate_rule_logic(rule)
            if not validation_result["valid"]:
                return {"success": False, "error": f"Invalid rule logic: {validation_result['error']}"}
            
            return {
                "success": True,
                "message": f"QA rule '{rule.name}' updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating QA rule: {e}")
            return {"success": False, "error": str(e)}
    
    def delete_qa_rule(self, session_id: str, rule_id: str) -> Dict[str, Any]:
        """Delete a QA rule"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        if rule_id not in self.qa_rules:
            return {"success": False, "error": "QA rule not found"}
        
        try:
            rule_name = self.qa_rules[rule_id].name
            
            # Remove from all rulesets
            for ruleset in self.qa_rulesets.values():
                if rule_id in ruleset.rules:
                    ruleset.rules.remove(rule_id)
            
            # Delete rule
            del self.qa_rules[rule_id]
            
            return {
                "success": True,
                "message": f"QA rule '{rule_name}' deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting QA rule: {e}")
            return {"success": False, "error": str(e)}
    
    def get_qa_rules(self, session_id: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get QA rules with optional filtering"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.READ_CONFIG):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            rules = list(self.qa_rules.values())
            
            # Apply filters
            if filters:
                if "category" in filters:
                    category = QACategory(filters["category"])
                    rules = [r for r in rules if r.category == category]
                
                if "severity" in filters:
                    severity = QASeverity(filters["severity"])
                    rules = [r for r in rules if r.severity == severity]
                
                if "enabled" in filters:
                    enabled = filters["enabled"]
                    rules = [r for r in rules if r.enabled == enabled]
                
                if "tags" in filters:
                    required_tags = filters["tags"]
                    if isinstance(required_tags, str):
                        required_tags = [required_tags]
                    rules = [r for r in rules if any(tag in r.tags for tag in required_tags)]
                
                if "search" in filters:
                    search_term = filters["search"].lower()
                    rules = [r for r in rules 
                           if search_term in r.name.lower() or search_term in r.description.lower()]
            
            return {
                "success": True,
                "rules": [rule.to_dict() for rule in rules],
                "total_count": len(rules)
            }
            
        except Exception as e:
            logger.error(f"Error getting QA rules: {e}")
            return {"success": False, "error": str(e)}
    
    def create_ruleset(self, session_id: str, ruleset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new QA ruleset"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.MANAGE_PROTOCOLS):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            ruleset_id = ruleset_data.get("ruleset_id", str(uuid.uuid4()))
            
            # Validate rule IDs
            rule_ids = ruleset_data.get("rules", [])
            invalid_rules = [rid for rid in rule_ids if rid not in self.qa_rules]
            if invalid_rules:
                return {"success": False, "error": f"Invalid rule IDs: {', '.join(invalid_rules)}"}
            
            ruleset = QARuleSet(
                ruleset_id=ruleset_id,
                name=ruleset_data["name"],
                description=ruleset_data.get("description", ""),
                rules=rule_ids,
                project_types=ruleset_data.get("project_types", []),
                enabled=ruleset_data.get("enabled", True)
            )
            
            self.qa_rulesets[ruleset_id] = ruleset
            
            return {
                "success": True,
                "ruleset_id": ruleset_id,
                "message": f"QA ruleset '{ruleset.name}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating QA ruleset: {e}")
            return {"success": False, "error": str(e)}
    
    def get_rulesets(self, session_id: str) -> Dict[str, Any]:
        """Get all QA rulesets"""
        # Check permissions
        if not self.security_manager.require_permission(session_id, Permission.READ_CONFIG):
            return {"success": False, "error": "Insufficient permissions"}
        
        try:
            rulesets = []
            for ruleset in self.qa_rulesets.values():
                ruleset_dict = ruleset.to_dict()
                ruleset_dict["rule_count"] = len(ruleset.rules)
                rulesets.append(ruleset_dict)
            
            return {
                "success": True,
                "rulesets": rulesets,
                "total_count": len(rulesets)
            }
            
        except Exception as e:
            logger.error(f"Error getting QA rulesets: {e}")
            return {"success": False, "error": str(e)}
    
    def validate_content(self, content: str, file_path: str, ruleset_id: Optional[str] = None) -> Dict[str, Any]:
        """Validate content against QA rules"""
        violations = []
        
        # Determine which rules to apply
        if ruleset_id and ruleset_id in self.qa_rulesets:
            rule_ids = self.qa_rulesets[ruleset_id].rules
            rules_to_apply = [self.qa_rules[rid] for rid in rule_ids if rid in self.qa_rules]
        else:
            rules_to_apply = [rule for rule in self.qa_rules.values() if rule.enabled]
        
        # Apply each rule
        for rule in rules_to_apply:
            try:
                rule_violations = self._apply_rule(rule, content, file_path)
                violations.extend(rule_violations)
                
                # Update statistics
                if rule.rule_id not in self.rule_execution_stats:
                    self.rule_execution_stats[rule.rule_id] = {"executions": 0, "violations": 0}
                
                self.rule_execution_stats[rule.rule_id]["executions"] += 1
                self.rule_execution_stats[rule.rule_id]["violations"] += len(rule_violations)
                
            except Exception as e:
                logger.error(f"Error applying rule {rule.rule_id}: {e}")
        
        return {
            "success": True,
            "violations": [v.to_dict() for v in violations],
            "violation_count": len(violations),
            "rules_applied": len(rules_to_apply)
        }
    
    def _apply_rule(self, rule: QARule, content: str, file_path: str) -> List[QAViolation]:
        """Apply a single rule to content"""
        violations = []
        
        # This is a simplified implementation
        # In production, you'd have more sophisticated rule engines
        
        if rule.rule_id == "security_hardcoded_secrets":
            # Check for hardcoded secrets
            pattern = r'(password|api_key|secret|token)\s*=\s*["\'][^"\'\n]+["\']'
            matches = re.finditer(pattern, content, re.IGNORECASE)
            
            for match in matches:
                line_number = content[:match.start()].count('\n') + 1
                violation = QAViolation(
                    violation_id=str(uuid.uuid4()),
                    rule_id=rule.rule_id,
                    file_path=file_path,
                    line_number=line_number,
                    column_number=match.start() - content.rfind('\n', 0, match.start()),
                    message=rule.error_message,
                    severity=rule.severity,
                    context={"matched_text": match.group()}
                )
                violations.append(violation)
        
        elif rule.rule_id == "documentation_missing":
            # Check for missing docstrings
            func_pattern = r'def\s+\w+\s*\([^)]*\):'
            matches = re.finditer(func_pattern, content)
            
            for match in matches:
                # Simple check: look for docstring after function definition
                func_end = match.end()
                next_lines = content[func_end:func_end+200]  # Check next 200 chars
                if '"""' not in next_lines and "'''" not in next_lines:
                    line_number = content[:match.start()].count('\n') + 1
                    violation = QAViolation(
                        violation_id=str(uuid.uuid4()),
                        rule_id=rule.rule_id,
                        file_path=file_path,
                        line_number=line_number,
                        column_number=None,
                        message=rule.error_message,
                        severity=rule.severity,
                        context={"function_signature": match.group()}
                    )
                    violations.append(violation)
        
        return violations
    
    def _validate_rule_logic(self, rule: QARule) -> Dict[str, Any]:
        """Validate rule logic syntax"""
        try:
            # Basic validation - in production, you'd have more sophisticated validation
            if not rule.validation_logic.strip():
                return {"valid": False, "error": "Validation logic cannot be empty"}
            
            # Check for basic syntax issues
            if rule.validation_logic.count('(') != rule.validation_logic.count(')'):
                return {"valid": False, "error": "Unbalanced parentheses in validation logic"}
            
            return {"valid": True}
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def get_qa_statistics(self) -> Dict[str, Any]:
        """Get QA system statistics"""
        total_rules = len(self.qa_rules)
        enabled_rules = len([r for r in self.qa_rules.values() if r.enabled])
        total_rulesets = len(self.qa_rulesets)
        
        # Category distribution
        category_counts = {}
        for rule in self.qa_rules.values():
            category = rule.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Severity distribution
        severity_counts = {}
        for rule in self.qa_rules.values():
            severity = rule.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "total_rules": total_rules,
            "enabled_rules": enabled_rules,
            "total_rulesets": total_rulesets,
            "category_distribution": category_counts,
            "severity_distribution": severity_counts,
            "total_violations": len(self.violations),
            "rule_execution_stats": self.rule_execution_stats
        }
