"""
P.H.A.L.A.N.X. Application Generator Core
Procedural Hyper-Accessible Adaptive Nexus - Full-Stack Application Generation

This module implements complete application generation including frontend, backend,
and database components using the JAEGIS A.E.G.I.S. Protocol Suite.
"""

import json
import logging
import asyncio
import uuid
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum

# J.O.L.T. Observability Stack Integration
from core.utils.telemetry_init import get_tracer, get_meter, trace_method
from core.utils.metrics import (
    PHALANX_APPS_GENERATED_TOTAL,
    PHALANX_GENERATION_DURATION,
    PHALANX_ACTIVE_GENERATIONS,
    PHALANX_COMPONENT_GENERATION_DURATION,
    PHALANX_GENERATED_COMPONENTS_TOTAL
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# P.H.A.L.A.N.X. Application Generator Metrics are now imported from centralized registry

class StackType(Enum):
    """Supported full-stack configurations"""
    REACT_NODE = "react_node"
    VUE_EXPRESS = "vue_express"
    NEXT_FULLSTACK = "next_fullstack"
    SVELTE_FASTAPI = "svelte_fastapi"
    ANGULAR_NESTJS = "angular_nestjs"

class DatabaseType(Enum):
    """Supported database types"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    SQLITE = "sqlite"
    SUPABASE = "supabase"
    FIREBASE = "firebase"

class DeploymentTarget(Enum):
    """Supported deployment targets"""
    VERCEL = "vercel"
    NETLIFY = "netlify"
    AWS = "aws"
    DOCKER = "docker"
    KUBERNETES = "kubernetes"

@dataclass
class ApplicationSpec:
    """Application specification for generation"""
    app_id: str
    name: str
    description: str
    stack_type: StackType
    database_type: DatabaseType
    features: List[str]
    pages: List[Dict[str, Any]]
    api_endpoints: List[Dict[str, Any]]
    database_schema: Dict[str, Any]
    styling: Dict[str, Any]
    deployment_target: DeploymentTarget
    requirements: Dict[str, Any]
    timestamp: datetime

@dataclass
class GeneratedApplication:
    """Generated application result"""
    app_id: str
    name: str
    stack_type: StackType
    frontend_code: Dict[str, str]
    backend_code: Dict[str, str]
    database_schema: Dict[str, Any]
    configuration: Dict[str, Any]
    deployment_config: Dict[str, Any]
    dependencies: Dict[str, List[str]]
    documentation: str
    metadata: Dict[str, Any]
    timestamp: datetime

class PHALANXAppGenerator:
    """
    P.H.A.L.A.N.X. Application Generator
    
    Generates complete full-stack applications from high-level specifications
    using the A.E.G.I.S. Protocol Suite components.
    """
    
    def __init__(self, config_path: str = "config/phalanx/app_generator_config.json"):
        self.config_path = Path(config_path)
        
        # Stack templates and configurations
        self.stack_templates = {}
        self.database_templates = {}
        self.deployment_templates = {}
        
        # Generated applications storage
        self.generated_apps: Dict[str, GeneratedApplication] = {}
        
        # Integration with other A.E.G.I.S. components
        self.aura_integration = True  # A.U.R.A. for frontend generation
        self.acid_integration = True  # A.C.I.D. for orchestration
        self.odin_integration = True  # O.D.I.N. for development environment
        
        # Load templates and configurations
        self._load_stack_templates()
        self._load_database_templates()
        self._load_deployment_templates()
        
        logger.info("P.H.A.L.A.N.X. Application Generator initialized")
    
    def _load_stack_templates(self):
        """Load stack-specific templates"""
        
        # React + Node.js template
        self.stack_templates[StackType.REACT_NODE] = {
            "frontend": {
                "framework": "react",
                "build_tool": "vite",
                "styling": "tailwindcss",
                "state_management": "zustand",
                "routing": "react-router-dom"
            },
            "backend": {
                "framework": "express",
                "language": "javascript",
                "orm": "prisma",
                "auth": "jwt",
                "validation": "joi"
            },
            "structure": {
                "frontend_dir": "client",
                "backend_dir": "server",
                "shared_dir": "shared"
            }
        }
        
        # Next.js Full-Stack template
        self.stack_templates[StackType.NEXT_FULLSTACK] = {
            "frontend": {
                "framework": "nextjs",
                "build_tool": "next",
                "styling": "tailwindcss",
                "state_management": "swr",
                "routing": "next-router"
            },
            "backend": {
                "framework": "nextjs-api",
                "language": "typescript",
                "orm": "prisma",
                "auth": "next-auth",
                "validation": "zod"
            },
            "structure": {
                "app_dir": "app",
                "api_dir": "app/api",
                "components_dir": "components"
            }
        }
        
        # Vue + Express template
        self.stack_templates[StackType.VUE_EXPRESS] = {
            "frontend": {
                "framework": "vue",
                "build_tool": "vite",
                "styling": "tailwindcss",
                "state_management": "pinia",
                "routing": "vue-router"
            },
            "backend": {
                "framework": "express",
                "language": "typescript",
                "orm": "typeorm",
                "auth": "passport",
                "validation": "class-validator"
            },
            "structure": {
                "frontend_dir": "frontend",
                "backend_dir": "backend",
                "shared_dir": "shared"
            }
        }
        
        logger.info(f"Loaded {len(self.stack_templates)} stack templates")
    
    def _load_database_templates(self):
        """Load database-specific templates"""
        
        self.database_templates[DatabaseType.POSTGRESQL] = {
            "driver": "pg",
            "orm_config": {
                "dialect": "postgresql",
                "port": 5432,
                "ssl": True
            },
            "schema_syntax": "sql",
            "features": ["transactions", "json", "full_text_search", "arrays"]
        }
        
        self.database_templates[DatabaseType.MONGODB] = {
            "driver": "mongodb",
            "orm_config": {
                "dialect": "mongodb",
                "port": 27017
            },
            "schema_syntax": "mongoose",
            "features": ["document_store", "aggregation", "indexing", "sharding"]
        }
        
        self.database_templates[DatabaseType.SUPABASE] = {
            "driver": "supabase",
            "orm_config": {
                "dialect": "postgresql",
                "realtime": True,
                "auth": True,
                "storage": True
            },
            "schema_syntax": "sql",
            "features": ["realtime", "auth", "storage", "edge_functions"]
        }
        
        logger.info(f"Loaded {len(self.database_templates)} database templates")
    
    def _load_deployment_templates(self):
        """Load deployment-specific templates"""
        
        self.deployment_templates[DeploymentTarget.VERCEL] = {
            "config_file": "vercel.json",
            "build_command": "npm run build",
            "output_directory": "dist",
            "environment": "serverless",
            "features": ["edge_functions", "analytics", "domains"]
        }
        
        self.deployment_templates[DeploymentTarget.NETLIFY] = {
            "config_file": "netlify.toml",
            "build_command": "npm run build",
            "output_directory": "dist",
            "environment": "jamstack",
            "features": ["forms", "functions", "identity"]
        }
        
        self.deployment_templates[DeploymentTarget.AWS] = {
            "config_file": "aws-config.yml",
            "build_command": "npm run build",
            "output_directory": "build",
            "environment": "cloud",
            "features": ["lambda", "s3", "cloudfront", "rds"]
        }
        
        logger.info(f"Loaded {len(self.deployment_templates)} deployment templates")
    
    @trace_method("phalanx.application.generation")
    async def generate_application(self, spec: ApplicationSpec) -> GeneratedApplication:
        """Generate a complete full-stack application"""
        tracer = get_tracer("phalanx.app_generator")

        with tracer.start_as_current_span("phalanx.application.complete_generation") as span:
            span.set_attribute("app_name", spec.name)
            span.set_attribute("stack_type", spec.stack_type.value)
            span.set_attribute("pages_count", len(spec.pages))
            span.set_attribute("api_endpoints_count", len(spec.api_endpoints))
            span.set_attribute("database_type", spec.database_type.value)

            logger.info(f"Generating application: {spec.name} ({spec.stack_type.value})")

            # Update active generations metric
            PHALANX_ACTIVE_GENERATIONS.inc()

            # Determine complexity based on features and components
            complexity = "simple" if len(spec.pages) <= 3 and len(spec.api_endpoints) <= 5 else "complex"

            with PHALANX_GENERATION_DURATION.labels(
                stack_type=spec.stack_type.value,
                complexity=complexity
            ).time():
                try:
            # Get stack template
            stack_template = self.stack_templates[spec.stack_type]
            
            # Generate frontend code
            frontend_code = await self._generate_frontend_code(spec, stack_template)
            
            # Generate backend code
            backend_code = await self._generate_backend_code(spec, stack_template)
            
            # Generate database schema
            database_schema = self._generate_database_schema(spec)
            
            # Generate configuration files
            configuration = self._generate_configuration(spec, stack_template)
            
            # Generate deployment configuration
            deployment_config = self._generate_deployment_config(spec)
            
            # Determine dependencies
            dependencies = self._determine_dependencies(spec, stack_template)
            
            # Generate documentation
            documentation = self._generate_documentation(spec)
            
            # Create generated application
            app = GeneratedApplication(
                app_id=spec.app_id,
                name=spec.name,
                stack_type=spec.stack_type,
                frontend_code=frontend_code,
                backend_code=backend_code,
                database_schema=database_schema,
                configuration=configuration,
                deployment_config=deployment_config,
                dependencies=dependencies,
                documentation=documentation,
                metadata={
                    "generation_time": datetime.now().isoformat(),
                    "stack_template": stack_template,
                    "features": spec.features,
                    "pages_count": len(spec.pages),
                    "api_endpoints_count": len(spec.api_endpoints)
                },
                timestamp=datetime.now()
            )
            
                    # Store generated application
                    self.generated_apps[app.app_id] = app

                    # Update success metrics
                    PHALANX_APPS_GENERATED_TOTAL.labels(
                        stack_type=spec.stack_type.value,
                        status="success"
                    ).inc()
                    span.set_attribute("generation_status", "success")
                    span.set_attribute("app_id", app.app_id)
                    span.set_attribute("components_generated", len(app.frontend_code) + len(app.backend_code))

                    logger.info(f"Generated application {app.name} successfully")
                    return app

                except Exception as e:
                    span.set_attribute("generation_status", "failed")
                    span.set_attribute("error_message", str(e))
                    logger.error(f"Error generating application: {e}")
                    raise
                finally:
                    # Decrement active generations
                    PHALANX_ACTIVE_GENERATIONS.dec()
    
    @trace_method("phalanx.frontend.generation")
    async def _generate_frontend_code(self, spec: ApplicationSpec, stack_template: Dict) -> Dict[str, str]:
        """Generate frontend code using A.U.R.A. integration"""
        with PHALANX_COMPONENT_GENERATION_DURATION.labels(component_type="frontend").time():
            frontend_code = {}

            framework = stack_template["frontend"]["framework"]
        
        # Generate main app component
        frontend_code["App.tsx"] = self._generate_app_component(spec, framework)
        
        # Generate page components
        for page in spec.pages:
            page_name = page["name"]
            frontend_code[f"pages/{page_name}.tsx"] = self._generate_page_component(page, framework)
        
        # Generate shared components
        frontend_code["components/Layout.tsx"] = self._generate_layout_component(spec, framework)
        frontend_code["components/Navigation.tsx"] = self._generate_navigation_component(spec, framework)
        
        # Generate API client
        frontend_code["lib/api.ts"] = self._generate_api_client(spec)
        
        # Generate configuration files
        frontend_code["package.json"] = self._generate_frontend_package_json(spec, stack_template)
        frontend_code["tailwind.config.js"] = self._generate_tailwind_config(spec)
        frontend_code["vite.config.ts"] = self._generate_vite_config(spec)
        
            return frontend_code
    
    @trace_method("phalanx.backend.generation")
    async def _generate_backend_code(self, spec: ApplicationSpec, stack_template: Dict) -> Dict[str, str]:
        """Generate backend code"""
        with PHALANX_COMPONENT_GENERATION_DURATION.labels(component_type="backend").time():
            backend_code = {}

            framework = stack_template["backend"]["framework"]
        
        # Generate main server file
        backend_code["server.ts"] = self._generate_server_file(spec, framework)
        
        # Generate API routes
        for endpoint in spec.api_endpoints:
            route_name = endpoint["path"].replace("/", "_").strip("_")
            backend_code[f"routes/{route_name}.ts"] = self._generate_api_route(endpoint, framework)
        
        # Generate database models
        for model_name, model_schema in spec.database_schema.items():
            backend_code[f"models/{model_name}.ts"] = self._generate_model_file(model_name, model_schema, spec.database_type)
        
        # Generate middleware
        backend_code["middleware/auth.ts"] = self._generate_auth_middleware(spec)
        backend_code["middleware/cors.ts"] = self._generate_cors_middleware(spec)
        
        # Generate configuration files
        backend_code["package.json"] = self._generate_backend_package_json(spec, stack_template)
        backend_code["tsconfig.json"] = self._generate_tsconfig(spec)
        
            return backend_code
    
    def _generate_app_component(self, spec: ApplicationSpec, framework: str) -> str:
        """Generate main app component"""
        if framework == "react":
            return f"""
import React from 'react';
import {{ BrowserRouter as Router, Routes, Route }} from 'react-router-dom';
import Layout from './components/Layout';
{chr(10).join([f"import {page['name']} from './pages/{page['name']}';" for page in spec.pages])}

function App() {{
  return (
    <Router>
      <Layout>
        <Routes>
          {chr(10).join([f"<Route path=\"{page.get('path', '/' + page['name'].lower())}\" element={{<{page['name']} />}} />" for page in spec.pages])}
        </Routes>
      </Layout>
    </Router>
  );
}}

export default App;
""".strip()
        
        elif framework == "vue":
            return f"""
<template>
  <router-view />
</template>

<script setup lang="ts">
import {{ onMounted }} from 'vue';

onMounted(() => {{
  console.log('{spec.name} app mounted');
}});
</script>

<style>
/* Global styles */
</style>
""".strip()
        
        return f"// {framework} app component for {spec.name}"
    
    def _generate_page_component(self, page: Dict, framework: str) -> str:
        """Generate page component"""
        page_name = page["name"]
        
        if framework == "react":
            return f"""
import React from 'react';

const {page_name}: React.FC = () => {{
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">{page_name}</h1>
      <div>
        {{/* Page content */}}
        <p>Welcome to the {page_name} page.</p>
      </div>
    </div>
  );
}};

export default {page_name};
""".strip()
        
        return f"// {framework} page component for {page_name}"
    
    def _generate_layout_component(self, spec: ApplicationSpec, framework: str) -> str:
        """Generate layout component"""
        if framework == "react":
            return f"""
import React from 'react';
import Navigation from './Navigation';

interface LayoutProps {{
  children: React.ReactNode;
}}

const Layout: React.FC<LayoutProps> = ({{ children }}) => {{
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        {{children}}
      </main>
      <footer className="bg-gray-800 text-white py-8 mt-auto">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 {spec.name}. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}};

export default Layout;
""".strip()
        
        return f"// {framework} layout component"
    
    def _generate_navigation_component(self, spec: ApplicationSpec, framework: str) -> str:
        """Generate navigation component"""
        if framework == "react":
            nav_links = "\n".join([
                f'          <Link to="{page.get("path", "/" + page["name"].lower())}" className="text-gray-600 hover:text-gray-900">{page["name"]}</Link>'
                for page in spec.pages
            ])
            
            return f"""
import React from 'react';
import {{ Link }} from 'react-router-dom';

const Navigation: React.FC = () => {{
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-xl font-bold text-gray-900">
            {spec.name}
          </Link>
          <div className="flex space-x-6">
{nav_links}
          </div>
        </div>
      </div>
    </nav>
  );
}};

export default Navigation;
""".strip()
        
        return f"// {framework} navigation component"
    
    def _generate_api_client(self, spec: ApplicationSpec) -> str:
        """Generate API client"""
        endpoints = "\n".join([
            f"  {endpoint['method'].lower()}{endpoint['path'].replace('/', '_').replace('-', '_').title().replace('_', '')}: (data?: any) => api('{endpoint['path']}', {{ method: '{endpoint['method']}', body: data }}),"
            for endpoint in spec.api_endpoints
        ])
        
        return f"""
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

class ApiClient {{
  private async request(endpoint: string, options: RequestInit = {{}}) {{
    const url = `${{API_BASE_URL}}${{endpoint}}`;
    const config = {{
      headers: {{
        'Content-Type': 'application/json',
        ...options.headers,
      }},
      ...options,
    }};

    if (config.body && typeof config.body === 'object') {{
      config.body = JSON.stringify(config.body);
    }}

    const response = await fetch(url, config);
    
    if (!response.ok) {{
      throw new Error(`API Error: ${{response.status}} ${{response.statusText}}`);
    }}

    return response.json();
  }}

  // API methods
{endpoints}
}}

export const api = new ApiClient();
export default api;
""".strip()
    
    def _generate_server_file(self, spec: ApplicationSpec, framework: str) -> str:
        """Generate main server file"""
        if framework == "express":
            route_imports = "\n".join([
                f"import {endpoint['path'].replace('/', '').replace('-', '_')}Routes from './routes{endpoint['path']}';"
                for endpoint in spec.api_endpoints
            ])
            
            route_uses = "\n".join([
                f"app.use('/api{endpoint['path']}', {endpoint['path'].replace('/', '').replace('-', '_')}Routes);"
                for endpoint in spec.api_endpoints
            ])
            
            return f"""
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
{route_imports}

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({{ extended: true }}));

// Routes
{route_uses}

// Health check
app.get('/health', (req, res) => {{
  res.json({{ status: 'OK', timestamp: new Date().toISOString() }});
}});

// Error handling
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {{
  console.error(err.stack);
  res.status(500).json({{ error: 'Something went wrong!' }});
}});

app.listen(PORT, () => {{
  console.log(`{spec.name} server running on port ${{PORT}}`);
}});

export default app;
""".strip()
        
        return f"// {framework} server file"
    
    def _generate_database_schema(self, spec: ApplicationSpec) -> Dict[str, Any]:
        """Generate database schema"""
        return spec.database_schema
    
    def _generate_configuration(self, spec: ApplicationSpec, stack_template: Dict) -> Dict[str, Any]:
        """Generate application configuration"""
        return {
            "app_name": spec.name,
            "stack_type": spec.stack_type.value,
            "database_type": spec.database_type.value,
            "deployment_target": spec.deployment_target.value,
            "features": spec.features,
            "stack_template": stack_template
        }
    
    def _generate_deployment_config(self, spec: ApplicationSpec) -> Dict[str, Any]:
        """Generate deployment configuration"""
        template = self.deployment_templates[spec.deployment_target]
        
        return {
            "target": spec.deployment_target.value,
            "config_file": template["config_file"],
            "build_command": template["build_command"],
            "output_directory": template["output_directory"],
            "environment_variables": {
                "NODE_ENV": "production",
                "DATABASE_URL": "${DATABASE_URL}",
                "API_URL": "${API_URL}"
            }
        }
    
    def _determine_dependencies(self, spec: ApplicationSpec, stack_template: Dict) -> Dict[str, List[str]]:
        """Determine required dependencies"""
        frontend_deps = ["react", "react-dom", "react-router-dom", "tailwindcss"]
        backend_deps = ["express", "cors", "helmet", "morgan", "dotenv"]
        
        if spec.database_type == DatabaseType.POSTGRESQL:
            backend_deps.extend(["pg", "prisma"])
        elif spec.database_type == DatabaseType.MONGODB:
            backend_deps.extend(["mongodb", "mongoose"])
        
        return {
            "frontend": frontend_deps,
            "backend": backend_deps,
            "dev": ["typescript", "@types/node", "nodemon", "concurrently"]
        }
    
    def _generate_documentation(self, spec: ApplicationSpec) -> str:
        """Generate application documentation"""
        return f"""
# {spec.name}

{spec.description}

## Stack
- Frontend: {spec.stack_type.value.split('_')[0].title()}
- Backend: {spec.stack_type.value.split('_')[1].title()}
- Database: {spec.database_type.value.title()}

## Features
{chr(10).join([f"- {feature}" for feature in spec.features])}

## Pages
{chr(10).join([f"- {page['name']}" for page in spec.pages])}

## API Endpoints
{chr(10).join([f"- {endpoint['method']} {endpoint['path']}" for endpoint in spec.api_endpoints])}

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

3. Run development server:
   ```bash
   npm run dev
   ```

## Deployment

Deploy to {spec.deployment_target.value.title()}:
```bash
npm run deploy
```

Generated by P.H.A.L.A.N.X. Application Generator
""".strip()
    
    # Placeholder methods for package.json generation
    def _generate_frontend_package_json(self, spec: ApplicationSpec, stack_template: Dict) -> str:
        """Generate frontend package.json"""
        return json.dumps({
            "name": f"{spec.name.lower().replace(' ', '-')}-frontend",
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.8.0",
                "tailwindcss": "^3.2.0"
            },
            "devDependencies": {
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0",
                "typescript": "^4.9.0",
                "vite": "^4.0.0"
            }
        }, indent=2)
    
    def _generate_backend_package_json(self, spec: ApplicationSpec, stack_template: Dict) -> str:
        """Generate backend package.json"""
        return json.dumps({
            "name": f"{spec.name.lower().replace(' ', '-')}-backend",
            "version": "1.0.0",
            "scripts": {
                "dev": "nodemon src/server.ts",
                "build": "tsc",
                "start": "node dist/server.js"
            },
            "dependencies": {
                "express": "^4.18.0",
                "cors": "^2.8.5",
                "helmet": "^6.0.0",
                "morgan": "^1.10.0",
                "dotenv": "^16.0.0"
            },
            "devDependencies": {
                "@types/express": "^4.17.0",
                "@types/cors": "^2.8.0",
                "@types/morgan": "^1.9.0",
                "typescript": "^4.9.0",
                "nodemon": "^2.0.0",
                "ts-node": "^10.9.0"
            }
        }, indent=2)
    
    # Additional placeholder methods
    def _generate_api_route(self, endpoint: Dict, framework: str) -> str:
        """Generate API route file"""
        return f"// {framework} route for {endpoint['path']}"
    
    def _generate_model_file(self, model_name: str, model_schema: Dict, db_type: DatabaseType) -> str:
        """Generate database model file"""
        return f"// {db_type.value} model for {model_name}"
    
    def _generate_auth_middleware(self, spec: ApplicationSpec) -> str:
        """Generate authentication middleware"""
        return "// Authentication middleware"
    
    def _generate_cors_middleware(self, spec: ApplicationSpec) -> str:
        """Generate CORS middleware"""
        return "// CORS middleware"
    
    def _generate_tailwind_config(self, spec: ApplicationSpec) -> str:
        """Generate Tailwind config"""
        return "// Tailwind CSS configuration"
    
    def _generate_vite_config(self, spec: ApplicationSpec) -> str:
        """Generate Vite config"""
        return "// Vite configuration"
    
    def _generate_tsconfig(self, spec: ApplicationSpec) -> str:
        """Generate TypeScript config"""
        return "// TypeScript configuration"
    
    def get_generated_applications(self) -> List[GeneratedApplication]:
        """Get all generated applications"""
        return list(self.generated_apps.values())
    
    def get_application_by_id(self, app_id: str) -> Optional[GeneratedApplication]:
        """Get a specific application by ID"""
        return self.generated_apps.get(app_id)

# Export main class
__all__ = ['PHALANXAppGenerator', 'ApplicationSpec', 'GeneratedApplication', 'StackType', 'DatabaseType', 'DeploymentTarget']
