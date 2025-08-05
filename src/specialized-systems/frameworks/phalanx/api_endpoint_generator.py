"""
P.H.A.L.A.N.X. API Endpoint Generator
RESTful API generation with documentation, authentication, and CRUD operations
Part of the JAEGIS A.E.G.I.S. Protocol Suite
"""

import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTTPMethod(Enum):
    """HTTP methods for API endpoints"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"

class AuthType(Enum):
    """Authentication types"""
    NONE = "none"
    JWT = "jwt"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"
    BEARER = "bearer"

class ResponseFormat(Enum):
    """Response format types"""
    JSON = "json"
    XML = "xml"
    HTML = "html"
    TEXT = "text"
    BINARY = "binary"

class ValidationRule(Enum):
    """Validation rule types"""
    REQUIRED = "required"
    EMAIL = "email"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    PATTERN = "pattern"
    NUMERIC = "numeric"
    BOOLEAN = "boolean"
    DATE = "date"
    UUID = "uuid"

@dataclass
class APIParameter:
    """API parameter definition"""
    name: str
    param_type: str  # query, path, body, header
    data_type: str
    required: bool = False
    default: Optional[Any] = None
    description: Optional[str] = None
    validation_rules: List[ValidationRule] = None
    example: Optional[Any] = None

@dataclass
class APIResponse:
    """API response definition"""
    status_code: int
    description: str
    schema: Dict[str, Any]
    examples: Dict[str, Any] = None
    headers: Dict[str, str] = None

@dataclass
class APIEndpoint:
    """API endpoint definition"""
    endpoint_id: str
    path: str
    method: HTTPMethod
    summary: str
    description: str
    parameters: List[APIParameter]
    responses: List[APIResponse]
    auth_type: AuthType = AuthType.NONE
    tags: List[str] = None
    deprecated: bool = False
    rate_limit: Optional[int] = None

@dataclass
class APIDocumentation:
    """API documentation structure"""
    title: str
    version: str
    description: str
    base_url: str
    endpoints: List[APIEndpoint]
    auth_config: Dict[str, Any]
    schemas: Dict[str, Any]
    metadata: Dict[str, Any]

class PHALANXAPIGenerator:
    """
    P.H.A.L.A.N.X. API Endpoint Generator
    
    Generates RESTful API endpoints with comprehensive documentation,
    authentication, validation, and CRUD operations.
    """
    
    def __init__(self, config_path: str = "config/phalanx/api_config.json"):
        self.config_path = Path(config_path)
        
        # API templates and patterns
        self.endpoint_templates = {}
        self.crud_patterns = {}
        self.auth_patterns = {}
        self.validation_patterns = {}
        
        # Generated APIs storage
        self.generated_apis: Dict[str, APIDocumentation] = {}
        
        # Load templates and patterns
        self._load_endpoint_templates()
        self._load_crud_patterns()
        self._load_auth_patterns()
        self._load_validation_patterns()
        
        logger.info("P.H.A.L.A.N.X. API Endpoint Generator initialized")
    
    def _load_endpoint_templates(self):
        """Load endpoint templates for common patterns"""
        
        # CRUD endpoint templates
        self.endpoint_templates["crud"] = {
            "list": {
                "method": HTTPMethod.GET,
                "path": "/{resource}",
                "summary": "List {resource}",
                "description": "Retrieve a list of {resource} with optional filtering and pagination",
                "parameters": [
                    {"name": "page", "param_type": "query", "data_type": "integer", "default": 1},
                    {"name": "limit", "param_type": "query", "data_type": "integer", "default": 20},
                    {"name": "sort", "param_type": "query", "data_type": "string"},
                    {"name": "filter", "param_type": "query", "data_type": "string"}
                ]
            },
            "create": {
                "method": HTTPMethod.POST,
                "path": "/{resource}",
                "summary": "Create {resource}",
                "description": "Create a new {resource}",
                "parameters": [
                    {"name": "body", "param_type": "body", "data_type": "object", "required": True}
                ]
            },
            "get": {
                "method": HTTPMethod.GET,
                "path": "/{resource}/{id}",
                "summary": "Get {resource}",
                "description": "Retrieve a specific {resource} by ID",
                "parameters": [
                    {"name": "id", "param_type": "path", "data_type": "string", "required": True}
                ]
            },
            "update": {
                "method": HTTPMethod.PUT,
                "path": "/{resource}/{id}",
                "summary": "Update {resource}",
                "description": "Update a specific {resource}",
                "parameters": [
                    {"name": "id", "param_type": "path", "data_type": "string", "required": True},
                    {"name": "body", "param_type": "body", "data_type": "object", "required": True}
                ]
            },
            "patch": {
                "method": HTTPMethod.PATCH,
                "path": "/{resource}/{id}",
                "summary": "Partially update {resource}",
                "description": "Partially update a specific {resource}",
                "parameters": [
                    {"name": "id", "param_type": "path", "data_type": "string", "required": True},
                    {"name": "body", "param_type": "body", "data_type": "object", "required": True}
                ]
            },
            "delete": {
                "method": HTTPMethod.DELETE,
                "path": "/{resource}/{id}",
                "summary": "Delete {resource}",
                "description": "Delete a specific {resource}",
                "parameters": [
                    {"name": "id", "param_type": "path", "data_type": "string", "required": True}
                ]
            }
        }
        
        # Authentication endpoints
        self.endpoint_templates["auth"] = {
            "login": {
                "method": HTTPMethod.POST,
                "path": "/auth/login",
                "summary": "User login",
                "description": "Authenticate user and return access token",
                "parameters": [
                    {"name": "email", "param_type": "body", "data_type": "string", "required": True},
                    {"name": "password", "param_type": "body", "data_type": "string", "required": True}
                ]
            },
            "register": {
                "method": HTTPMethod.POST,
                "path": "/auth/register",
                "summary": "User registration",
                "description": "Register a new user account",
                "parameters": [
                    {"name": "email", "param_type": "body", "data_type": "string", "required": True},
                    {"name": "password", "param_type": "body", "data_type": "string", "required": True},
                    {"name": "name", "param_type": "body", "data_type": "string", "required": True}
                ]
            },
            "refresh": {
                "method": HTTPMethod.POST,
                "path": "/auth/refresh",
                "summary": "Refresh token",
                "description": "Refresh access token using refresh token",
                "parameters": [
                    {"name": "refresh_token", "param_type": "body", "data_type": "string", "required": True}
                ]
            },
            "logout": {
                "method": HTTPMethod.POST,
                "path": "/auth/logout",
                "summary": "User logout",
                "description": "Logout user and invalidate tokens",
                "auth_type": AuthType.JWT
            }
        }
        
        logger.info(f"Loaded {len(self.endpoint_templates)} endpoint template categories")
    
    def _load_crud_patterns(self):
        """Load CRUD operation patterns"""
        
        self.crud_patterns = {
            "standard_responses": {
                "list": [
                    {"status_code": 200, "description": "Successful response", "schema": {"type": "array"}},
                    {"status_code": 400, "description": "Bad request"},
                    {"status_code": 401, "description": "Unauthorized"},
                    {"status_code": 500, "description": "Internal server error"}
                ],
                "create": [
                    {"status_code": 201, "description": "Resource created successfully"},
                    {"status_code": 400, "description": "Validation error"},
                    {"status_code": 401, "description": "Unauthorized"},
                    {"status_code": 409, "description": "Resource already exists"},
                    {"status_code": 500, "description": "Internal server error"}
                ],
                "get": [
                    {"status_code": 200, "description": "Successful response"},
                    {"status_code": 404, "description": "Resource not found"},
                    {"status_code": 401, "description": "Unauthorized"},
                    {"status_code": 500, "description": "Internal server error"}
                ],
                "update": [
                    {"status_code": 200, "description": "Resource updated successfully"},
                    {"status_code": 400, "description": "Validation error"},
                    {"status_code": 401, "description": "Unauthorized"},
                    {"status_code": 404, "description": "Resource not found"},
                    {"status_code": 500, "description": "Internal server error"}
                ],
                "delete": [
                    {"status_code": 204, "description": "Resource deleted successfully"},
                    {"status_code": 401, "description": "Unauthorized"},
                    {"status_code": 404, "description": "Resource not found"},
                    {"status_code": 500, "description": "Internal server error"}
                ]
            }
        }
        
        logger.info("Loaded CRUD patterns")
    
    def _load_auth_patterns(self):
        """Load authentication patterns"""
        
        self.auth_patterns = {
            AuthType.JWT: {
                "header": "Authorization",
                "scheme": "Bearer",
                "description": "JWT token authentication",
                "example": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            },
            AuthType.API_KEY: {
                "header": "X-API-Key",
                "description": "API key authentication",
                "example": "your-api-key-here"
            },
            AuthType.BASIC: {
                "header": "Authorization",
                "scheme": "Basic",
                "description": "Basic authentication",
                "example": "Basic dXNlcm5hbWU6cGFzc3dvcmQ="
            }
        }
        
        logger.info(f"Loaded {len(self.auth_patterns)} authentication patterns")
    
    def _load_validation_patterns(self):
        """Load validation patterns"""
        
        self.validation_patterns = {
            "email": {
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "message": "Must be a valid email address"
            },
            "password": {
                "min_length": 8,
                "pattern": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]",
                "message": "Password must contain at least 8 characters with uppercase, lowercase, number, and special character"
            },
            "uuid": {
                "pattern": r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
                "message": "Must be a valid UUID"
            },
            "phone": {
                "pattern": r"^\+?[1-9]\d{1,14}$",
                "message": "Must be a valid phone number"
            }
        }
        
        logger.info(f"Loaded {len(self.validation_patterns)} validation patterns")
    
    async def generate_api(self, 
                          schema: Dict[str, Any], 
                          config: Dict[str, Any] = None) -> APIDocumentation:
        """Generate API endpoints from database schema"""
        
        api_id = f"api_{int(datetime.now().timestamp())}"
        logger.info(f"Generating API {api_id}")
        
        try:
            # Extract configuration
            api_config = config or {}
            
            # Generate endpoints for each table/resource
            endpoints = []
            schemas = {}
            
            for table_name, table_schema in schema.get("tables", {}).items():
                # Generate CRUD endpoints for each table
                crud_endpoints = self._generate_crud_endpoints(table_name, table_schema, api_config)
                endpoints.extend(crud_endpoints)
                
                # Generate schema definitions
                resource_schema = self._generate_resource_schema(table_name, table_schema)
                schemas[table_name] = resource_schema
            
            # Generate authentication endpoints if auth is enabled
            if api_config.get("auth_enabled", True):
                auth_endpoints = self._generate_auth_endpoints(api_config)
                endpoints.extend(auth_endpoints)
            
            # Generate additional endpoints based on features
            feature_endpoints = self._generate_feature_endpoints(api_config.get("features", []))
            endpoints.extend(feature_endpoints)
            
            # Create API documentation
            api_doc = APIDocumentation(
                title=api_config.get("title", "Generated API"),
                version=api_config.get("version", "1.0.0"),
                description=api_config.get("description", "Auto-generated RESTful API"),
                base_url=api_config.get("base_url", "http://localhost:3000/api"),
                endpoints=endpoints,
                auth_config=self._generate_auth_config(api_config),
                schemas=schemas,
                metadata={
                    "generated_at": datetime.now().isoformat(),
                    "generator": "P.H.A.L.A.N.X. API Generator",
                    "total_endpoints": len(endpoints)
                }
            )
            
            # Store generated API
            self.generated_apis[api_id] = api_doc
            
            logger.info(f"Generated API with {len(endpoints)} endpoints")
            return api_doc
            
        except Exception as e:
            logger.error(f"Error generating API: {e}")
            raise
    
    def _generate_crud_endpoints(self, resource: str, table_schema: Dict[str, Any], config: Dict[str, Any]) -> List[APIEndpoint]:
        """Generate CRUD endpoints for a resource"""
        endpoints = []
        
        # Determine which CRUD operations to generate
        crud_operations = config.get("crud_operations", ["list", "create", "get", "update", "delete"])
        
        for operation in crud_operations:
            if operation in self.endpoint_templates["crud"]:
                template = self.endpoint_templates["crud"][operation]
                
                endpoint = APIEndpoint(
                    endpoint_id=f"{resource}_{operation}",
                    path=template["path"].replace("{resource}", resource),
                    method=template["method"],
                    summary=template["summary"].replace("{resource}", resource.title()),
                    description=template["description"].replace("{resource}", resource),
                    parameters=self._generate_parameters(template["parameters"], resource, table_schema),
                    responses=self._generate_responses(operation, resource, table_schema),
                    auth_type=config.get("default_auth", AuthType.JWT) if operation != "list" else AuthType.NONE,
                    tags=[resource],
                    rate_limit=config.get("rate_limit", 100)
                )
                
                endpoints.append(endpoint)
        
        return endpoints
    
    def _generate_parameters(self, template_params: List[Dict], resource: str, table_schema: Dict[str, Any]) -> List[APIParameter]:
        """Generate parameters for an endpoint"""
        parameters = []
        
        for param_template in template_params:
            param = APIParameter(
                name=param_template["name"],
                param_type=param_template["param_type"],
                data_type=param_template["data_type"],
                required=param_template.get("required", False),
                default=param_template.get("default"),
                description=param_template.get("description"),
                validation_rules=self._get_validation_rules(param_template["name"], param_template["data_type"]),
                example=self._generate_parameter_example(param_template["name"], param_template["data_type"])
            )
            parameters.append(param)
        
        return parameters
    
    def _generate_responses(self, operation: str, resource: str, table_schema: Dict[str, Any]) -> List[APIResponse]:
        """Generate responses for an endpoint"""
        responses = []
        
        if operation in self.crud_patterns["standard_responses"]:
            response_templates = self.crud_patterns["standard_responses"][operation]
            
            for template in response_templates:
                response = APIResponse(
                    status_code=template["status_code"],
                    description=template["description"],
                    schema=self._generate_response_schema(operation, resource, table_schema, template["status_code"]),
                    examples=self._generate_response_examples(operation, resource, template["status_code"])
                )
                responses.append(response)
        
        return responses
    
    def _generate_auth_endpoints(self, config: Dict[str, Any]) -> List[APIEndpoint]:
        """Generate authentication endpoints"""
        endpoints = []
        
        auth_operations = config.get("auth_operations", ["login", "register", "refresh", "logout"])
        
        for operation in auth_operations:
            if operation in self.endpoint_templates["auth"]:
                template = self.endpoint_templates["auth"][operation]
                
                endpoint = APIEndpoint(
                    endpoint_id=f"auth_{operation}",
                    path=template["path"],
                    method=template["method"],
                    summary=template["summary"],
                    description=template["description"],
                    parameters=self._generate_parameters(template.get("parameters", []), "auth", {}),
                    responses=self._generate_auth_responses(operation),
                    auth_type=template.get("auth_type", AuthType.NONE),
                    tags=["authentication"]
                )
                
                endpoints.append(endpoint)
        
        return endpoints
    
    def _generate_feature_endpoints(self, features: List[str]) -> List[APIEndpoint]:
        """Generate endpoints for specific features"""
        endpoints = []
        
        feature_endpoint_map = {
            "search": {
                "path": "/search",
                "method": HTTPMethod.GET,
                "summary": "Global search",
                "description": "Search across all resources"
            },
            "upload": {
                "path": "/upload",
                "method": HTTPMethod.POST,
                "summary": "File upload",
                "description": "Upload files to the server"
            },
            "health": {
                "path": "/health",
                "method": HTTPMethod.GET,
                "summary": "Health check",
                "description": "Check API health status"
            }
        }
        
        for feature in features:
            if feature in feature_endpoint_map:
                template = feature_endpoint_map[feature]
                
                endpoint = APIEndpoint(
                    endpoint_id=f"feature_{feature}",
                    path=template["path"],
                    method=template["method"],
                    summary=template["summary"],
                    description=template["description"],
                    parameters=[],
                    responses=[
                        APIResponse(
                            status_code=200,
                            description="Successful response",
                            schema={"type": "object"}
                        )
                    ],
                    auth_type=AuthType.NONE if feature == "health" else AuthType.JWT,
                    tags=[feature]
                )
                
                endpoints.append(endpoint)
        
        return endpoints
    
    def _generate_resource_schema(self, resource: str, table_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON schema for a resource"""
        properties = {}
        required = []
        
        for field_name, field_info in table_schema.get("fields", {}).items():
            field_type = field_info.get("type", "string")
            
            # Map database types to JSON schema types
            json_type = self._map_db_type_to_json_type(field_type)
            
            properties[field_name] = {
                "type": json_type,
                "description": field_info.get("description", f"{field_name} field")
            }
            
            # Add format for specific types
            if field_type == "email":
                properties[field_name]["format"] = "email"
            elif field_type == "uuid":
                properties[field_name]["format"] = "uuid"
            elif field_type == "date":
                properties[field_name]["format"] = "date"
            elif field_type == "datetime":
                properties[field_name]["format"] = "date-time"
            
            # Add to required if not nullable
            if not field_info.get("nullable", True):
                required.append(field_name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }
    
    def _generate_auth_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate authentication configuration"""
        auth_type = config.get("auth_type", "jwt")
        
        auth_config = {
            "type": auth_type,
            "description": f"{auth_type.upper()} authentication"
        }
        
        if auth_type in self.auth_patterns:
            auth_config.update(self.auth_patterns[AuthType(auth_type)])
        
        return auth_config
    
    def _get_validation_rules(self, param_name: str, data_type: str) -> List[ValidationRule]:
        """Get validation rules for a parameter"""
        rules = []
        
        # Add type-specific validation
        if data_type == "string":
            if "email" in param_name.lower():
                rules.append(ValidationRule.EMAIL)
            elif "password" in param_name.lower():
                rules.extend([ValidationRule.REQUIRED, ValidationRule.MIN_LENGTH])
        elif data_type == "integer":
            rules.append(ValidationRule.NUMERIC)
        elif data_type == "boolean":
            rules.append(ValidationRule.BOOLEAN)
        
        return rules
    
    def _generate_parameter_example(self, param_name: str, data_type: str) -> Any:
        """Generate example value for a parameter"""
        examples = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user@example.com",
            "password": "SecurePass123!",
            "name": "John Doe",
            "page": 1,
            "limit": 20,
            "sort": "created_at:desc"
        }
        
        if param_name in examples:
            return examples[param_name]
        
        # Generate based on data type
        type_examples = {
            "string": "example_string",
            "integer": 42,
            "boolean": True,
            "array": ["item1", "item2"],
            "object": {"key": "value"}
        }
        
        return type_examples.get(data_type, "example_value")
    
    def _generate_response_schema(self, operation: str, resource: str, table_schema: Dict[str, Any], status_code: int) -> Dict[str, Any]:
        """Generate response schema"""
        if status_code == 200:
            if operation == "list":
                return {
                    "type": "object",
                    "properties": {
                        "data": {"type": "array", "items": {"$ref": f"#/components/schemas/{resource}"}},
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer"},
                                "limit": {"type": "integer"},
                                "total": {"type": "integer"},
                                "pages": {"type": "integer"}
                            }
                        }
                    }
                }
            else:
                return {"$ref": f"#/components/schemas/{resource}"}
        elif status_code == 201:
            return {"$ref": f"#/components/schemas/{resource}"}
        elif status_code >= 400:
            return {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "message": {"type": "string"},
                    "details": {"type": "object"}
                }
            }
        
        return {"type": "object"}
    
    def _generate_response_examples(self, operation: str, resource: str, status_code: int) -> Dict[str, Any]:
        """Generate response examples"""
        if status_code == 200 and operation == "list":
            return {
                "application/json": {
                    "data": [{"id": "123", "name": "Example"}],
                    "pagination": {"page": 1, "limit": 20, "total": 1, "pages": 1}
                }
            }
        elif status_code in [200, 201]:
            return {
                "application/json": {"id": "123", "name": "Example"}
            }
        elif status_code >= 400:
            return {
                "application/json": {
                    "error": "Error occurred",
                    "message": "Detailed error message"
                }
            }
        
        return {}
    
    def _generate_auth_responses(self, operation: str) -> List[APIResponse]:
        """Generate responses for authentication endpoints"""
        if operation == "login":
            return [
                APIResponse(
                    status_code=200,
                    description="Login successful",
                    schema={
                        "type": "object",
                        "properties": {
                            "access_token": {"type": "string"},
                            "refresh_token": {"type": "string"},
                            "expires_in": {"type": "integer"},
                            "user": {"type": "object"}
                        }
                    }
                ),
                APIResponse(
                    status_code=401,
                    description="Invalid credentials",
                    schema={"type": "object", "properties": {"error": {"type": "string"}}}
                )
            ]
        elif operation == "register":
            return [
                APIResponse(
                    status_code=201,
                    description="Registration successful",
                    schema={"type": "object", "properties": {"user": {"type": "object"}}}
                ),
                APIResponse(
                    status_code=400,
                    description="Validation error",
                    schema={"type": "object", "properties": {"error": {"type": "string"}}}
                )
            ]
        
        return [
            APIResponse(
                status_code=200,
                description="Successful response",
                schema={"type": "object"}
            )
        ]
    
    def _map_db_type_to_json_type(self, db_type: str) -> str:
        """Map database type to JSON schema type"""
        type_mapping = {
            "string": "string",
            "text": "string",
            "integer": "integer",
            "bigint": "integer",
            "float": "number",
            "decimal": "number",
            "boolean": "boolean",
            "date": "string",
            "datetime": "string",
            "timestamp": "string",
            "json": "object",
            "uuid": "string",
            "array": "array"
        }
        
        return type_mapping.get(db_type.lower(), "string")
    
    def generate_openapi_spec(self, api_doc: APIDocumentation) -> Dict[str, Any]:
        """Generate OpenAPI 3.0 specification"""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": api_doc.title,
                "version": api_doc.version,
                "description": api_doc.description
            },
            "servers": [
                {"url": api_doc.base_url, "description": "API server"}
            ],
            "paths": {},
            "components": {
                "schemas": api_doc.schemas,
                "securitySchemes": self._generate_security_schemes(api_doc.auth_config)
            }
        }
        
        # Generate paths
        for endpoint in api_doc.endpoints:
            if endpoint.path not in spec["paths"]:
                spec["paths"][endpoint.path] = {}
            
            spec["paths"][endpoint.path][endpoint.method.value.lower()] = {
                "summary": endpoint.summary,
                "description": endpoint.description,
                "tags": endpoint.tags or [],
                "parameters": [self._parameter_to_openapi(p) for p in endpoint.parameters if p.param_type != "body"],
                "responses": {str(r.status_code): self._response_to_openapi(r) for r in endpoint.responses}
            }
            
            # Add request body for POST/PUT/PATCH
            body_params = [p for p in endpoint.parameters if p.param_type == "body"]
            if body_params and endpoint.method in [HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH]:
                spec["paths"][endpoint.path][endpoint.method.value.lower()]["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object"}
                        }
                    }
                }
            
            # Add security if required
            if endpoint.auth_type != AuthType.NONE:
                spec["paths"][endpoint.path][endpoint.method.value.lower()]["security"] = [
                    {endpoint.auth_type.value: []}
                ]
        
        return spec
    
    def _generate_security_schemes(self, auth_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security schemes for OpenAPI"""
        schemes = {}
        
        auth_type = auth_config.get("type", "jwt")
        
        if auth_type == "jwt":
            schemes["jwt"] = {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        elif auth_type == "api_key":
            schemes["api_key"] = {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key"
            }
        
        return schemes
    
    def _parameter_to_openapi(self, param: APIParameter) -> Dict[str, Any]:
        """Convert parameter to OpenAPI format"""
        openapi_param = {
            "name": param.name,
            "in": param.param_type,
            "required": param.required,
            "schema": {"type": param.data_type}
        }
        
        if param.description:
            openapi_param["description"] = param.description
        
        if param.example:
            openapi_param["example"] = param.example
        
        return openapi_param
    
    def _response_to_openapi(self, response: APIResponse) -> Dict[str, Any]:
        """Convert response to OpenAPI format"""
        openapi_response = {
            "description": response.description
        }
        
        if response.schema:
            openapi_response["content"] = {
                "application/json": {
                    "schema": response.schema
                }
            }
        
        if response.examples:
            openapi_response["content"]["application/json"]["examples"] = response.examples
        
        return openapi_response
    
    def get_generated_apis(self) -> List[APIDocumentation]:
        """Get all generated APIs"""
        return list(self.generated_apis.values())
    
    def get_api_by_id(self, api_id: str) -> Optional[APIDocumentation]:
        """Get API by ID"""
        return self.generated_apis.get(api_id)

# Export main class
__all__ = ['PHALANXAPIGenerator', 'APIDocumentation', 'APIEndpoint', 'HTTPMethod', 'AuthType']
