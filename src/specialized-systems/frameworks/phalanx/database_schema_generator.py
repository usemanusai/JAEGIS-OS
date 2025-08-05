"""
P.H.A.L.A.N.X. Database Schema Generator
Intelligent database schema creation with optimized table structures, relationships, and indexing
Part of the JAEGIS A.E.G.I.S. Protocol Suite
"""

import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseType(Enum):
    """Supported database types"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    SUPABASE = "supabase"
    FIREBASE = "firebase"

class FieldType(Enum):
    """Database field types"""
    STRING = "string"
    TEXT = "text"
    INTEGER = "integer"
    BIGINT = "bigint"
    FLOAT = "float"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TIMESTAMP = "timestamp"
    JSON = "json"
    UUID = "uuid"
    ENUM = "enum"
    ARRAY = "array"
    FOREIGN_KEY = "foreign_key"

class RelationshipType(Enum):
    """Database relationship types"""
    ONE_TO_ONE = "one_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_MANY = "many_to_many"
    POLYMORPHIC = "polymorphic"

class IndexType(Enum):
    """Database index types"""
    PRIMARY = "primary"
    UNIQUE = "unique"
    INDEX = "index"
    COMPOSITE = "composite"
    PARTIAL = "partial"
    FULL_TEXT = "full_text"
    GIN = "gin"  # PostgreSQL specific
    BTREE = "btree"
    HASH = "hash"

@dataclass
class DatabaseField:
    """Database field definition"""
    name: str
    field_type: FieldType
    nullable: bool = True
    default: Optional[Any] = None
    max_length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    enum_values: Optional[List[str]] = None
    foreign_table: Optional[str] = None
    foreign_key: Optional[str] = None
    constraints: List[str] = None
    description: Optional[str] = None

@dataclass
class DatabaseIndex:
    """Database index definition"""
    name: str
    index_type: IndexType
    fields: List[str]
    unique: bool = False
    partial_condition: Optional[str] = None
    description: Optional[str] = None

@dataclass
class DatabaseRelationship:
    """Database relationship definition"""
    name: str
    relationship_type: RelationshipType
    source_table: str
    target_table: str
    source_field: str
    target_field: str
    cascade_delete: bool = False
    cascade_update: bool = False
    description: Optional[str] = None

@dataclass
class DatabaseTable:
    """Database table definition"""
    name: str
    fields: List[DatabaseField]
    indexes: List[DatabaseIndex]
    relationships: List[DatabaseRelationship]
    description: Optional[str] = None
    timestamps: bool = True
    soft_deletes: bool = False

@dataclass
class DatabaseSchema:
    """Complete database schema"""
    schema_id: str
    name: str
    database_type: DatabaseType
    tables: List[DatabaseTable]
    global_indexes: List[DatabaseIndex]
    constraints: List[str]
    metadata: Dict[str, Any]
    created_at: datetime

class PHALANXDatabaseGenerator:
    """
    P.H.A.L.A.N.X. Database Schema Generator
    
    Generates intelligent database schemas with optimized table structures,
    relationships, and indexing strategies based on application requirements.
    """
    
    def __init__(self, config_path: str = "config/phalanx/database_config.json"):
        self.config_path = Path(config_path)
        
        # Schema templates and patterns
        self.schema_templates = {}
        self.field_patterns = {}
        self.relationship_patterns = {}
        self.optimization_rules = {}
        
        # Generated schemas storage
        self.generated_schemas: Dict[str, DatabaseSchema] = {}
        
        # Load templates and patterns
        self._load_schema_templates()
        self._load_field_patterns()
        self._load_relationship_patterns()
        self._load_optimization_rules()
        
        logger.info("P.H.A.L.A.N.X. Database Schema Generator initialized")
    
    def _load_schema_templates(self):
        """Load common schema templates"""
        
        # E-commerce template
        self.schema_templates["ecommerce"] = {
            "tables": ["users", "products", "categories", "orders", "order_items", "payments", "reviews"],
            "common_fields": {
                "users": ["id", "email", "password_hash", "first_name", "last_name", "phone", "address"],
                "products": ["id", "name", "description", "price", "sku", "stock_quantity", "category_id"],
                "orders": ["id", "user_id", "total_amount", "status", "shipping_address", "billing_address"]
            },
            "relationships": [
                {"source": "products", "target": "categories", "type": "many_to_one"},
                {"source": "orders", "target": "users", "type": "many_to_one"},
                {"source": "order_items", "target": "orders", "type": "many_to_one"},
                {"source": "order_items", "target": "products", "type": "many_to_one"}
            ]
        }
        
        # Blog/CMS template
        self.schema_templates["blog"] = {
            "tables": ["users", "posts", "categories", "tags", "comments", "media"],
            "common_fields": {
                "users": ["id", "username", "email", "password_hash", "role", "bio"],
                "posts": ["id", "title", "slug", "content", "excerpt", "author_id", "status", "published_at"],
                "comments": ["id", "post_id", "author_id", "content", "parent_id", "approved"]
            },
            "relationships": [
                {"source": "posts", "target": "users", "type": "many_to_one"},
                {"source": "comments", "target": "posts", "type": "many_to_one"},
                {"source": "comments", "target": "users", "type": "many_to_one"}
            ]
        }
        
        # SaaS application template
        self.schema_templates["saas"] = {
            "tables": ["organizations", "users", "subscriptions", "features", "usage_logs", "billing"],
            "common_fields": {
                "organizations": ["id", "name", "slug", "plan", "settings"],
                "users": ["id", "email", "password_hash", "organization_id", "role", "permissions"],
                "subscriptions": ["id", "organization_id", "plan", "status", "trial_ends_at", "billing_cycle"]
            },
            "relationships": [
                {"source": "users", "target": "organizations", "type": "many_to_one"},
                {"source": "subscriptions", "target": "organizations", "type": "one_to_one"}
            ]
        }
        
        logger.info(f"Loaded {len(self.schema_templates)} schema templates")
    
    def _load_field_patterns(self):
        """Load field naming and type patterns"""
        
        self.field_patterns = {
            "id_fields": {
                "pattern": r".*_?id$",
                "type": FieldType.UUID,
                "nullable": False,
                "description": "Primary or foreign key identifier"
            },
            "email_fields": {
                "pattern": r".*email.*",
                "type": FieldType.STRING,
                "max_length": 255,
                "nullable": False,
                "constraints": ["UNIQUE", "CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')"]
            },
            "password_fields": {
                "pattern": r".*password.*",
                "type": FieldType.STRING,
                "max_length": 255,
                "nullable": False,
                "description": "Hashed password field"
            },
            "name_fields": {
                "pattern": r".*(name|title).*",
                "type": FieldType.STRING,
                "max_length": 255,
                "nullable": False
            },
            "description_fields": {
                "pattern": r".*(description|content|bio).*",
                "type": FieldType.TEXT,
                "nullable": True
            },
            "status_fields": {
                "pattern": r".*status.*",
                "type": FieldType.ENUM,
                "nullable": False,
                "default": "active"
            },
            "amount_fields": {
                "pattern": r".*(amount|price|cost).*",
                "type": FieldType.DECIMAL,
                "precision": 10,
                "scale": 2,
                "nullable": False
            },
            "date_fields": {
                "pattern": r".*(_at|_date)$",
                "type": FieldType.TIMESTAMP,
                "nullable": True
            },
            "boolean_fields": {
                "pattern": r"^(is_|has_|can_|should_).*",
                "type": FieldType.BOOLEAN,
                "nullable": False,
                "default": False
            }
        }
        
        logger.info(f"Loaded {len(self.field_patterns)} field patterns")
    
    def _load_relationship_patterns(self):
        """Load relationship inference patterns"""
        
        self.relationship_patterns = {
            "user_relationships": {
                "pattern": r".*user_id.*",
                "target_table": "users",
                "relationship_type": RelationshipType.MANY_TO_ONE,
                "cascade_delete": False
            },
            "category_relationships": {
                "pattern": r".*category_id.*",
                "target_table": "categories",
                "relationship_type": RelationshipType.MANY_TO_ONE,
                "cascade_delete": False
            },
            "parent_relationships": {
                "pattern": r".*parent_id.*",
                "target_table": "self",
                "relationship_type": RelationshipType.MANY_TO_ONE,
                "cascade_delete": False
            },
            "organization_relationships": {
                "pattern": r".*organization_id.*",
                "target_table": "organizations",
                "relationship_type": RelationshipType.MANY_TO_ONE,
                "cascade_delete": True
            }
        }
        
        logger.info(f"Loaded {len(self.relationship_patterns)} relationship patterns")
    
    def _load_optimization_rules(self):
        """Load database optimization rules"""
        
        self.optimization_rules = {
            "indexing": {
                "foreign_keys": "Always index foreign key fields",
                "search_fields": "Index fields commonly used in WHERE clauses",
                "unique_fields": "Create unique indexes for unique constraints",
                "composite_queries": "Create composite indexes for multi-field queries"
            },
            "normalization": {
                "avoid_redundancy": "Eliminate redundant data through normalization",
                "separate_concerns": "Separate different types of data into different tables",
                "optimize_queries": "Balance normalization with query performance"
            },
            "performance": {
                "partition_large_tables": "Consider partitioning for tables with millions of rows",
                "archive_old_data": "Implement archiving strategy for historical data",
                "optimize_joins": "Minimize complex joins through denormalization where appropriate"
            }
        }
        
        logger.info(f"Loaded {len(self.optimization_rules)} optimization rules")
    
    async def generate_schema(self, 
                            app_description: str, 
                            database_type: DatabaseType,
                            requirements: Dict[str, Any] = None) -> DatabaseSchema:
        """Generate database schema from application description"""
        
        schema_id = f"schema_{int(datetime.now().timestamp())}"
        logger.info(f"Generating database schema {schema_id} for {database_type.value}")
        
        try:
            # Analyze application requirements
            analysis = await self._analyze_application_requirements(app_description, requirements)
            
            # Generate tables based on analysis
            tables = await self._generate_tables(analysis, database_type)
            
            # Infer and create relationships
            relationships = self._infer_relationships(tables)
            
            # Optimize schema
            optimized_tables = self._optimize_schema(tables, relationships, database_type)
            
            # Generate global indexes
            global_indexes = self._generate_global_indexes(optimized_tables, database_type)
            
            # Generate constraints
            constraints = self._generate_constraints(optimized_tables, database_type)
            
            # Create schema
            schema = DatabaseSchema(
                schema_id=schema_id,
                name=analysis.get("app_name", "generated_app"),
                database_type=database_type,
                tables=optimized_tables,
                global_indexes=global_indexes,
                constraints=constraints,
                metadata={
                    "analysis": analysis,
                    "generation_time": datetime.now().isoformat(),
                    "optimization_applied": True,
                    "template_used": analysis.get("template", "custom")
                },
                created_at=datetime.now()
            )
            
            # Store generated schema
            self.generated_schemas[schema_id] = schema
            
            logger.info(f"Generated schema with {len(schema.tables)} tables")
            return schema
            
        except Exception as e:
            logger.error(f"Error generating schema: {e}")
            raise
    
    async def _analyze_application_requirements(self, description: str, requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze application description to extract database requirements"""
        
        analysis = {
            "app_name": self._extract_app_name(description),
            "entities": self._extract_entities(description),
            "relationships": self._extract_relationships_from_text(description),
            "features": self._extract_features(description),
            "template": self._determine_template(description),
            "scale": self._estimate_scale(description, requirements),
            "complexity": self._assess_complexity(description)
        }
        
        return analysis
    
    def _extract_app_name(self, description: str) -> str:
        """Extract application name from description"""
        # Simple extraction - in production, this would use NLP
        words = description.split()
        
        # Look for app/application keywords
        app_keywords = ["app", "application", "system", "platform", "service"]
        
        for i, word in enumerate(words):
            if word.lower() in app_keywords and i > 0:
                return words[i-1].lower().replace(" ", "_")
        
        return "generated_app"
    
    def _extract_entities(self, description: str) -> List[str]:
        """Extract main entities from description"""
        entities = []
        
        # Common entity patterns
        entity_patterns = [
            r"\b(user|customer|client|member)s?\b",
            r"\b(product|item|article)s?\b",
            r"\b(order|purchase|transaction)s?\b",
            r"\b(category|tag|label)s?\b",
            r"\b(post|article|blog)s?\b",
            r"\b(comment|review|rating)s?\b",
            r"\b(organization|company|team)s?\b",
            r"\b(subscription|plan|billing)s?\b",
            r"\b(notification|message|email)s?\b",
            r"\b(file|document|media)s?\b"
        ]
        
        for pattern in entity_patterns:
            matches = re.findall(pattern, description.lower())
            for match in matches:
                entity = match.rstrip('s')  # Remove plural
                if entity not in entities:
                    entities.append(entity)
        
        return entities
    
    def _extract_relationships_from_text(self, description: str) -> List[Dict[str, str]]:
        """Extract relationships from description text"""
        relationships = []
        
        # Simple relationship patterns
        relationship_patterns = [
            (r"(\w+) belongs to (\w+)", "many_to_one"),
            (r"(\w+) has many (\w+)", "one_to_many"),
            (r"(\w+) can have multiple (\w+)", "one_to_many"),
            (r"(\w+) is associated with (\w+)", "many_to_many")
        ]
        
        for pattern, rel_type in relationship_patterns:
            matches = re.findall(pattern, description.lower())
            for match in matches:
                relationships.append({
                    "source": match[0],
                    "target": match[1],
                    "type": rel_type
                })
        
        return relationships
    
    def _extract_features(self, description: str) -> List[str]:
        """Extract application features from description"""
        features = []
        
        feature_keywords = {
            "authentication": ["login", "register", "auth", "signin", "signup"],
            "search": ["search", "filter", "find", "query"],
            "notifications": ["notify", "alert", "email", "message"],
            "payments": ["payment", "billing", "subscription", "checkout"],
            "file_upload": ["upload", "file", "image", "document"],
            "comments": ["comment", "review", "feedback"],
            "ratings": ["rating", "star", "score", "vote"],
            "admin": ["admin", "dashboard", "manage", "control"],
            "api": ["api", "rest", "endpoint", "integration"],
            "real_time": ["real-time", "live", "instant", "websocket"]
        }
        
        description_lower = description.lower()
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                features.append(feature)
        
        return features
    
    def _determine_template(self, description: str) -> str:
        """Determine which schema template to use"""
        description_lower = description.lower()
        
        template_keywords = {
            "ecommerce": ["shop", "store", "ecommerce", "product", "cart", "order", "payment"],
            "blog": ["blog", "post", "article", "cms", "content", "publish"],
            "saas": ["saas", "subscription", "tenant", "organization", "plan", "billing"]
        }
        
        for template, keywords in template_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return template
        
        return "custom"
    
    def _estimate_scale(self, description: str, requirements: Dict[str, Any] = None) -> str:
        """Estimate application scale"""
        if requirements and "expected_users" in requirements:
            users = requirements["expected_users"]
            if users < 1000:
                return "small"
            elif users < 100000:
                return "medium"
            else:
                return "large"
        
        # Estimate from description
        scale_indicators = {
            "small": ["personal", "small", "startup", "prototype"],
            "medium": ["business", "company", "enterprise", "commercial"],
            "large": ["global", "massive", "millions", "scale", "distributed"]
        }
        
        description_lower = description.lower()
        
        for scale, indicators in scale_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                return scale
        
        return "medium"  # Default
    
    def _assess_complexity(self, description: str) -> str:
        """Assess application complexity"""
        complexity_indicators = {
            "simple": ["simple", "basic", "minimal", "straightforward"],
            "medium": ["moderate", "standard", "typical", "common"],
            "complex": ["complex", "advanced", "sophisticated", "enterprise", "multi-tenant"]
        }
        
        description_lower = description.lower()
        
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                return complexity
        
        return "medium"  # Default
    
    async def _generate_tables(self, analysis: Dict[str, Any], database_type: DatabaseType) -> List[DatabaseTable]:
        """Generate database tables based on analysis"""
        tables = []
        
        # Use template if available
        template = analysis.get("template")
        if template and template in self.schema_templates:
            tables.extend(self._generate_from_template(template, analysis, database_type))
        
        # Generate custom tables for extracted entities
        for entity in analysis.get("entities", []):
            if not any(table.name == entity for table in tables):
                table = self._generate_table_for_entity(entity, analysis, database_type)
                tables.append(table)
        
        # Add common tables based on features
        feature_tables = self._generate_feature_tables(analysis.get("features", []), database_type)
        tables.extend(feature_tables)
        
        return tables
    
    def _generate_from_template(self, template: str, analysis: Dict[str, Any], database_type: DatabaseType) -> List[DatabaseTable]:
        """Generate tables from template"""
        tables = []
        template_config = self.schema_templates[template]
        
        for table_name in template_config["tables"]:
            fields = []
            
            # Add ID field
            fields.append(DatabaseField(
                name="id",
                field_type=FieldType.UUID,
                nullable=False,
                description="Primary key"
            ))
            
            # Add template-specific fields
            if table_name in template_config["common_fields"]:
                for field_name in template_config["common_fields"][table_name]:
                    if field_name != "id":  # Skip ID as we already added it
                        field = self._generate_field(field_name, database_type)
                        fields.append(field)
            
            # Add timestamp fields
            if analysis.get("features", []):
                fields.extend(self._generate_timestamp_fields())
            
            # Generate indexes
            indexes = self._generate_table_indexes(table_name, fields, database_type)
            
            table = DatabaseTable(
                name=table_name,
                fields=fields,
                indexes=indexes,
                relationships=[],
                description=f"Generated {table_name} table from {template} template",
                timestamps=True
            )
            
            tables.append(table)
        
        return tables
    
    def _generate_table_for_entity(self, entity: str, analysis: Dict[str, Any], database_type: DatabaseType) -> DatabaseTable:
        """Generate table for a specific entity"""
        fields = []
        
        # Add ID field
        fields.append(DatabaseField(
            name="id",
            field_type=FieldType.UUID,
            nullable=False,
            description="Primary key"
        ))
        
        # Add common fields based on entity type
        common_fields = self._get_common_fields_for_entity(entity)
        for field_name in common_fields:
            field = self._generate_field(field_name, database_type)
            fields.append(field)
        
        # Add timestamp fields
        fields.extend(self._generate_timestamp_fields())
        
        # Generate indexes
        indexes = self._generate_table_indexes(entity, fields, database_type)
        
        return DatabaseTable(
            name=entity,
            fields=fields,
            indexes=indexes,
            relationships=[],
            description=f"Generated table for {entity} entity",
            timestamps=True
        )
    
    def _generate_field(self, field_name: str, database_type: DatabaseType) -> DatabaseField:
        """Generate field based on name and patterns"""
        
        # Check field patterns
        for pattern_name, pattern_config in self.field_patterns.items():
            if re.match(pattern_config["pattern"], field_name, re.IGNORECASE):
                return DatabaseField(
                    name=field_name,
                    field_type=pattern_config["type"],
                    nullable=pattern_config.get("nullable", True),
                    default=pattern_config.get("default"),
                    max_length=pattern_config.get("max_length"),
                    precision=pattern_config.get("precision"),
                    scale=pattern_config.get("scale"),
                    constraints=pattern_config.get("constraints", []),
                    description=pattern_config.get("description")
                )
        
        # Default field type
        return DatabaseField(
            name=field_name,
            field_type=FieldType.STRING,
            max_length=255,
            nullable=True
        )
    
    def _generate_timestamp_fields(self) -> List[DatabaseField]:
        """Generate standard timestamp fields"""
        return [
            DatabaseField(
                name="created_at",
                field_type=FieldType.TIMESTAMP,
                nullable=False,
                default="CURRENT_TIMESTAMP",
                description="Record creation timestamp"
            ),
            DatabaseField(
                name="updated_at",
                field_type=FieldType.TIMESTAMP,
                nullable=False,
                default="CURRENT_TIMESTAMP",
                description="Record last update timestamp"
            )
        ]
    
    def _get_common_fields_for_entity(self, entity: str) -> List[str]:
        """Get common fields for entity type"""
        entity_fields = {
            "user": ["email", "password_hash", "first_name", "last_name", "phone", "is_active"],
            "product": ["name", "description", "price", "sku", "stock_quantity", "is_active"],
            "order": ["total_amount", "status", "shipping_address", "billing_address"],
            "post": ["title", "slug", "content", "excerpt", "status", "published_at"],
            "comment": ["content", "is_approved", "parent_id"],
            "category": ["name", "slug", "description", "parent_id"],
            "organization": ["name", "slug", "description", "settings"],
            "subscription": ["plan", "status", "trial_ends_at", "billing_cycle"]
        }
        
        return entity_fields.get(entity, ["name", "description", "is_active"])
    
    def _generate_feature_tables(self, features: List[str], database_type: DatabaseType) -> List[DatabaseTable]:
        """Generate tables for specific features"""
        tables = []
        
        feature_table_map = {
            "notifications": "notifications",
            "file_upload": "media_files",
            "api": "api_keys",
            "ratings": "ratings"
        }
        
        for feature in features:
            if feature in feature_table_map:
                table_name = feature_table_map[feature]
                table = self._generate_table_for_entity(table_name, {}, database_type)
                tables.append(table)
        
        return tables
    
    def _generate_table_indexes(self, table_name: str, fields: List[DatabaseField], database_type: DatabaseType) -> List[DatabaseIndex]:
        """Generate indexes for a table"""
        indexes = []
        
        # Primary key index
        id_field = next((f for f in fields if f.name == "id"), None)
        if id_field:
            indexes.append(DatabaseIndex(
                name=f"{table_name}_pkey",
                index_type=IndexType.PRIMARY,
                fields=["id"],
                unique=True,
                description="Primary key index"
            ))
        
        # Unique indexes for unique fields
        for field in fields:
            if field.constraints and "UNIQUE" in field.constraints:
                indexes.append(DatabaseIndex(
                    name=f"{table_name}_{field.name}_unique",
                    index_type=IndexType.UNIQUE,
                    fields=[field.name],
                    unique=True,
                    description=f"Unique index for {field.name}"
                ))
        
        # Foreign key indexes
        for field in fields:
            if field.field_type == FieldType.FOREIGN_KEY or field.name.endswith("_id"):
                indexes.append(DatabaseIndex(
                    name=f"{table_name}_{field.name}_idx",
                    index_type=IndexType.INDEX,
                    fields=[field.name],
                    description=f"Foreign key index for {field.name}"
                ))
        
        return indexes
    
    def _infer_relationships(self, tables: List[DatabaseTable]) -> List[DatabaseRelationship]:
        """Infer relationships between tables"""
        relationships = []
        
        for table in tables:
            for field in table.fields:
                # Check for foreign key patterns
                for pattern_name, pattern_config in self.relationship_patterns.items():
                    if re.match(pattern_config["pattern"], field.name, re.IGNORECASE):
                        target_table = pattern_config["target_table"]
                        
                        # Handle self-referential relationships
                        if target_table == "self":
                            target_table = table.name
                        
                        # Check if target table exists
                        if any(t.name == target_table for t in tables):
                            relationship = DatabaseRelationship(
                                name=f"{table.name}_{target_table}",
                                relationship_type=pattern_config["relationship_type"],
                                source_table=table.name,
                                target_table=target_table,
                                source_field=field.name,
                                target_field="id",
                                cascade_delete=pattern_config.get("cascade_delete", False),
                                description=f"Relationship between {table.name} and {target_table}"
                            )
                            relationships.append(relationship)
        
        return relationships
    
    def _optimize_schema(self, tables: List[DatabaseTable], relationships: List[DatabaseRelationship], database_type: DatabaseType) -> List[DatabaseTable]:
        """Optimize schema for performance"""
        optimized_tables = []
        
        for table in tables:
            optimized_table = DatabaseTable(
                name=table.name,
                fields=table.fields.copy(),
                indexes=table.indexes.copy(),
                relationships=table.relationships.copy(),
                description=table.description,
                timestamps=table.timestamps,
                soft_deletes=table.soft_deletes
            )
            
            # Add relationships to table
            table_relationships = [r for r in relationships if r.source_table == table.name]
            optimized_table.relationships.extend(table_relationships)
            
            # Optimize indexes based on relationships
            for relationship in table_relationships:
                # Ensure foreign key fields are indexed
                fk_index = DatabaseIndex(
                    name=f"{table.name}_{relationship.source_field}_fk_idx",
                    index_type=IndexType.INDEX,
                    fields=[relationship.source_field],
                    description=f"Foreign key index for {relationship.name}"
                )
                
                # Check if index already exists
                if not any(idx.fields == fk_index.fields for idx in optimized_table.indexes):
                    optimized_table.indexes.append(fk_index)
            
            optimized_tables.append(optimized_table)
        
        return optimized_tables
    
    def _generate_global_indexes(self, tables: List[DatabaseTable], database_type: DatabaseType) -> List[DatabaseIndex]:
        """Generate global indexes for cross-table queries"""
        global_indexes = []
        
        # This would implement global index generation
        # For now, return empty list
        
        return global_indexes
    
    def _generate_constraints(self, tables: List[DatabaseTable], database_type: DatabaseType) -> List[str]:
        """Generate global constraints"""
        constraints = []
        
        # Generate foreign key constraints
        for table in tables:
            for relationship in table.relationships:
                constraint = f"ALTER TABLE {relationship.source_table} ADD CONSTRAINT fk_{relationship.name} FOREIGN KEY ({relationship.source_field}) REFERENCES {relationship.target_table}({relationship.target_field})"
                
                if relationship.cascade_delete:
                    constraint += " ON DELETE CASCADE"
                if relationship.cascade_update:
                    constraint += " ON UPDATE CASCADE"
                
                constraints.append(constraint)
        
        return constraints
    
    def generate_sql(self, schema: DatabaseSchema) -> str:
        """Generate SQL DDL for the schema"""
        sql_parts = []
        
        # Generate table creation statements
        for table in schema.tables:
            sql_parts.append(self._generate_table_sql(table, schema.database_type))
        
        # Generate index creation statements
        for table in schema.tables:
            for index in table.indexes:
                if index.index_type != IndexType.PRIMARY:  # Primary key is created with table
                    sql_parts.append(self._generate_index_sql(table.name, index, schema.database_type))
        
        # Generate constraint statements
        sql_parts.extend(schema.constraints)
        
        return "\n\n".join(sql_parts)
    
    def _generate_table_sql(self, table: DatabaseTable, database_type: DatabaseType) -> str:
        """Generate SQL for table creation"""
        field_definitions = []
        
        for field in table.fields:
            field_sql = self._generate_field_sql(field, database_type)
            field_definitions.append(field_sql)
        
        # Add primary key constraint
        primary_key_fields = [f.name for f in table.fields if f.name == "id"]
        if primary_key_fields:
            field_definitions.append(f"PRIMARY KEY ({', '.join(primary_key_fields)})")
        
        sql = f"CREATE TABLE {table.name} (\n  " + ",\n  ".join(field_definitions) + "\n);"
        
        return sql
    
    def _generate_field_sql(self, field: DatabaseField, database_type: DatabaseType) -> str:
        """Generate SQL for field definition"""
        type_mapping = {
            DatabaseType.POSTGRESQL: {
                FieldType.STRING: "VARCHAR",
                FieldType.TEXT: "TEXT",
                FieldType.INTEGER: "INTEGER",
                FieldType.BIGINT: "BIGINT",
                FieldType.FLOAT: "REAL",
                FieldType.DECIMAL: "DECIMAL",
                FieldType.BOOLEAN: "BOOLEAN",
                FieldType.DATE: "DATE",
                FieldType.DATETIME: "TIMESTAMP",
                FieldType.TIMESTAMP: "TIMESTAMP",
                FieldType.JSON: "JSONB",
                FieldType.UUID: "UUID"
            }
        }
        
        db_type_map = type_mapping.get(database_type, type_mapping[DatabaseType.POSTGRESQL])
        sql_type = db_type_map.get(field.field_type, "VARCHAR")
        
        # Add length/precision
        if field.max_length and field.field_type == FieldType.STRING:
            sql_type += f"({field.max_length})"
        elif field.precision and field.scale:
            sql_type += f"({field.precision},{field.scale})"
        
        sql = f"{field.name} {sql_type}"
        
        # Add nullable constraint
        if not field.nullable:
            sql += " NOT NULL"
        
        # Add default value
        if field.default is not None:
            if isinstance(field.default, str) and field.default.upper() in ["CURRENT_TIMESTAMP", "NOW()"]:
                sql += f" DEFAULT {field.default}"
            else:
                sql += f" DEFAULT '{field.default}'"
        
        return sql
    
    def _generate_index_sql(self, table_name: str, index: DatabaseIndex, database_type: DatabaseType) -> str:
        """Generate SQL for index creation"""
        index_type = ""
        if index.unique:
            index_type = "UNIQUE "
        
        sql = f"CREATE {index_type}INDEX {index.name} ON {table_name} ({', '.join(index.fields)})"
        
        if index.partial_condition:
            sql += f" WHERE {index.partial_condition}"
        
        sql += ";"
        
        return sql
    
    def get_generated_schemas(self) -> List[DatabaseSchema]:
        """Get all generated schemas"""
        return list(self.generated_schemas.values())
    
    def get_schema_by_id(self, schema_id: str) -> Optional[DatabaseSchema]:
        """Get schema by ID"""
        return self.generated_schemas.get(schema_id)

# Export main class
__all__ = ['PHALANXDatabaseGenerator', 'DatabaseSchema', 'DatabaseTable', 'DatabaseField', 'DatabaseType', 'FieldType']
