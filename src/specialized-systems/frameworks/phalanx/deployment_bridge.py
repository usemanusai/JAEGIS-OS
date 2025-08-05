"""
P.H.A.L.A.N.X. Deployment Bridge System
One-click deployment to Vercel, Netlify, AWS, and other cloud platforms
Part of the JAEGIS A.E.G.I.S. Protocol Suite
"""

import json
import logging
import asyncio
import subprocess
import tempfile
import shutil
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import os
import zipfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentPlatform(Enum):
    """Supported deployment platforms"""
    VERCEL = "vercel"
    NETLIFY = "netlify"
    AWS_AMPLIFY = "aws_amplify"
    AWS_S3 = "aws_s3"
    GITHUB_PAGES = "github_pages"
    DOCKER = "docker"
    KUBERNETES = "kubernetes"
    RAILWAY = "railway"
    RENDER = "render"

class DeploymentStatus(Enum):
    """Deployment status states"""
    PENDING = "pending"
    BUILDING = "building"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ApplicationType(Enum):
    """Types of applications for deployment"""
    STATIC_SITE = "static_site"
    SPA = "spa"
    FULLSTACK = "fullstack"
    API_ONLY = "api_only"
    SERVERLESS = "serverless"

@dataclass
class DeploymentConfig:
    """Deployment configuration"""
    platform: DeploymentPlatform
    app_type: ApplicationType
    build_command: str
    output_directory: str
    environment_variables: Dict[str, str]
    custom_domain: Optional[str] = None
    ssl_enabled: bool = True
    auto_deploy: bool = True
    branch: str = "main"

@dataclass
class DeploymentResult:
    """Result of a deployment operation"""
    deployment_id: str
    platform: DeploymentPlatform
    status: DeploymentStatus
    url: Optional[str]
    build_logs: List[str]
    error_message: Optional[str]
    deployment_time: datetime
    metadata: Dict[str, Any]

@dataclass
class DeploymentJob:
    """Represents a deployment job"""
    job_id: str
    app_id: str
    config: DeploymentConfig
    source_path: str
    status: DeploymentStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[DeploymentResult] = None

class PHALANXDeploymentBridge:
    """
    P.H.A.L.A.N.X. Deployment Bridge
    
    Provides one-click deployment capabilities to multiple cloud platforms
    with automated build processes and environment configuration.
    """
    
    def __init__(self, config_path: str = "config/phalanx/deployment_config.json"):
        self.config_path = Path(config_path)
        
        # Platform configurations
        self.platform_configs = {}
        self.deployment_jobs: Dict[str, DeploymentJob] = {}
        self.deployment_history: List[DeploymentResult] = []
        
        # Platform-specific clients
        self.platform_clients = {}
        
        # Load configurations
        self._load_platform_configs()
        self._initialize_platform_clients()
        
        logger.info("P.H.A.L.A.N.X. Deployment Bridge initialized")
    
    def _load_platform_configs(self):
        """Load platform-specific configurations"""
        
        # Vercel configuration
        self.platform_configs[DeploymentPlatform.VERCEL] = {
            "cli_command": "vercel",
            "build_timeout": 600,  # 10 minutes
            "supported_frameworks": ["nextjs", "react", "vue", "svelte", "angular"],
            "environment_prefix": "VERCEL_",
            "config_file": "vercel.json"
        }
        
        # Netlify configuration
        self.platform_configs[DeploymentPlatform.NETLIFY] = {
            "cli_command": "netlify",
            "build_timeout": 900,  # 15 minutes
            "supported_frameworks": ["react", "vue", "svelte", "angular", "gatsby"],
            "environment_prefix": "NETLIFY_",
            "config_file": "netlify.toml"
        }
        
        # AWS Amplify configuration
        self.platform_configs[DeploymentPlatform.AWS_AMPLIFY] = {
            "cli_command": "amplify",
            "build_timeout": 1200,  # 20 minutes
            "supported_frameworks": ["react", "vue", "angular", "nextjs"],
            "environment_prefix": "AWS_",
            "config_file": "amplify.yml"
        }
        
        # Docker configuration
        self.platform_configs[DeploymentPlatform.DOCKER] = {
            "cli_command": "docker",
            "build_timeout": 1800,  # 30 minutes
            "supported_frameworks": ["any"],
            "environment_prefix": "DOCKER_",
            "config_file": "Dockerfile"
        }
        
        # Railway configuration
        self.platform_configs[DeploymentPlatform.RAILWAY] = {
            "cli_command": "railway",
            "build_timeout": 600,
            "supported_frameworks": ["nextjs", "react", "vue", "express", "fastapi"],
            "environment_prefix": "RAILWAY_",
            "config_file": "railway.json"
        }
        
        logger.info(f"Loaded {len(self.platform_configs)} platform configurations")
    
    def _initialize_platform_clients(self):
        """Initialize platform-specific clients"""
        # This would initialize actual API clients for each platform
        # For now, we'll use CLI-based deployment
        
        for platform in DeploymentPlatform:
            self.platform_clients[platform] = {
                "authenticated": False,
                "api_key": os.getenv(f"{platform.value.upper()}_API_KEY"),
                "cli_available": self._check_cli_availability(platform)
            }
    
    def _check_cli_availability(self, platform: DeploymentPlatform) -> bool:
        """Check if platform CLI is available"""
        config = self.platform_configs.get(platform)
        if not config:
            return False
        
        try:
            result = subprocess.run(
                [config["cli_command"], "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    async def deploy_application(self, app_id: str, source_path: str, config: DeploymentConfig) -> DeploymentJob:
        """Deploy application to specified platform"""
        job_id = f"deploy_{app_id}_{int(datetime.now().timestamp())}"
        
        job = DeploymentJob(
            job_id=job_id,
            app_id=app_id,
            config=config,
            source_path=source_path,
            status=DeploymentStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.deployment_jobs[job_id] = job
        
        logger.info(f"Starting deployment job {job_id} to {config.platform.value}")
        
        # Start deployment in background
        asyncio.create_task(self._execute_deployment(job))
        
        return job
    
    async def _execute_deployment(self, job: DeploymentJob):
        """Execute the deployment process"""
        try:
            job.status = DeploymentStatus.BUILDING
            job.started_at = datetime.now()
            
            # Prepare deployment package
            deployment_package = await self._prepare_deployment_package(job)
            
            # Execute platform-specific deployment
            if job.config.platform == DeploymentPlatform.VERCEL:
                result = await self._deploy_to_vercel(job, deployment_package)
            elif job.config.platform == DeploymentPlatform.NETLIFY:
                result = await self._deploy_to_netlify(job, deployment_package)
            elif job.config.platform == DeploymentPlatform.AWS_AMPLIFY:
                result = await self._deploy_to_aws_amplify(job, deployment_package)
            elif job.config.platform == DeploymentPlatform.DOCKER:
                result = await self._deploy_to_docker(job, deployment_package)
            elif job.config.platform == DeploymentPlatform.RAILWAY:
                result = await self._deploy_to_railway(job, deployment_package)
            else:
                raise ValueError(f"Unsupported platform: {job.config.platform}")
            
            job.status = result.status
            job.result = result
            job.completed_at = datetime.now()
            
            # Add to history
            self.deployment_history.append(result)
            
            logger.info(f"Deployment job {job.job_id} completed with status: {result.status.value}")
            
        except Exception as e:
            job.status = DeploymentStatus.FAILED
            job.completed_at = datetime.now()
            job.result = DeploymentResult(
                deployment_id=job.job_id,
                platform=job.config.platform,
                status=DeploymentStatus.FAILED,
                url=None,
                build_logs=[],
                error_message=str(e),
                deployment_time=datetime.now(),
                metadata={}
            )
            
            logger.error(f"Deployment job {job.job_id} failed: {e}")
    
    async def _prepare_deployment_package(self, job: DeploymentJob) -> str:
        """Prepare deployment package"""
        logger.info(f"Preparing deployment package for {job.job_id}")
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix=f"phalanx_deploy_{job.job_id}_")
        
        # Copy source files
        shutil.copytree(job.source_path, temp_dir, dirs_exist_ok=True)
        
        # Generate platform-specific configuration
        await self._generate_platform_config(job, temp_dir)
        
        # Install dependencies if needed
        if job.config.app_type != ApplicationType.STATIC_SITE:
            await self._install_dependencies(temp_dir)
        
        # Build application if needed
        if job.config.build_command:
            await self._build_application(job, temp_dir)
        
        return temp_dir
    
    async def _generate_platform_config(self, job: DeploymentJob, temp_dir: str):
        """Generate platform-specific configuration files"""
        platform_config = self.platform_configs[job.config.platform]
        config_file = platform_config["config_file"]
        
        if job.config.platform == DeploymentPlatform.VERCEL:
            vercel_config = {
                "version": 2,
                "builds": [
                    {
                        "src": "package.json",
                        "use": "@vercel/node" if job.config.app_type == ApplicationType.FULLSTACK else "@vercel/static-build"
                    }
                ],
                "env": job.config.environment_variables,
                "regions": ["iad1"]
            }
            
            with open(Path(temp_dir) / config_file, 'w') as f:
                json.dump(vercel_config, f, indent=2)
        
        elif job.config.platform == DeploymentPlatform.NETLIFY:
            netlify_config = f"""
[build]
  command = "{job.config.build_command}"
  publish = "{job.config.output_directory}"

[build.environment]
{chr(10).join([f'  {key} = "{value}"' for key, value in job.config.environment_variables.items()])}

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
            
            with open(Path(temp_dir) / config_file, 'w') as f:
                f.write(netlify_config)
        
        elif job.config.platform == DeploymentPlatform.DOCKER:
            dockerfile_content = f"""
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

RUN {job.config.build_command}

EXPOSE 3000

CMD ["npm", "start"]
"""
            
            with open(Path(temp_dir) / config_file, 'w') as f:
                f.write(dockerfile_content)
    
    async def _install_dependencies(self, temp_dir: str):
        """Install application dependencies"""
        logger.info("Installing dependencies")
        
        package_json_path = Path(temp_dir) / "package.json"
        if package_json_path.exists():
            result = await self._run_command(["npm", "ci"], cwd=temp_dir)
            if result.returncode != 0:
                raise Exception(f"Failed to install dependencies: {result.stderr}")
    
    async def _build_application(self, job: DeploymentJob, temp_dir: str):
        """Build the application"""
        logger.info(f"Building application with command: {job.config.build_command}")
        
        build_commands = job.config.build_command.split(" ")
        result = await self._run_command(build_commands, cwd=temp_dir)
        
        if result.returncode != 0:
            raise Exception(f"Build failed: {result.stderr}")
    
    async def _deploy_to_vercel(self, job: DeploymentJob, package_path: str) -> DeploymentResult:
        """Deploy to Vercel"""
        logger.info("Deploying to Vercel")
        
        # Prepare Vercel deployment command
        cmd = ["vercel", "--prod", "--yes"]
        
        # Add environment variables
        for key, value in job.config.environment_variables.items():
            cmd.extend(["-e", f"{key}={value}"])
        
        result = await self._run_command(cmd, cwd=package_path)
        
        if result.returncode == 0:
            # Extract deployment URL from output
            deployment_url = self._extract_deployment_url(result.stdout, "vercel")
            
            return DeploymentResult(
                deployment_id=job.job_id,
                platform=DeploymentPlatform.VERCEL,
                status=DeploymentStatus.SUCCESS,
                url=deployment_url,
                build_logs=result.stdout.split('\n'),
                error_message=None,
                deployment_time=datetime.now(),
                metadata={"platform": "vercel", "region": "iad1"}
            )
        else:
            return DeploymentResult(
                deployment_id=job.job_id,
                platform=DeploymentPlatform.VERCEL,
                status=DeploymentStatus.FAILED,
                url=None,
                build_logs=result.stdout.split('\n'),
                error_message=result.stderr,
                deployment_time=datetime.now(),
                metadata={}
            )
    
    async def _deploy_to_netlify(self, job: DeploymentJob, package_path: str) -> DeploymentResult:
        """Deploy to Netlify"""
        logger.info("Deploying to Netlify")
        
        # Build the site first
        build_dir = Path(package_path) / job.config.output_directory
        
        cmd = ["netlify", "deploy", "--prod", "--dir", str(build_dir)]
        
        result = await self._run_command(cmd, cwd=package_path)
        
        if result.returncode == 0:
            deployment_url = self._extract_deployment_url(result.stdout, "netlify")
            
            return DeploymentResult(
                deployment_id=job.job_id,
                platform=DeploymentPlatform.NETLIFY,
                status=DeploymentStatus.SUCCESS,
                url=deployment_url,
                build_logs=result.stdout.split('\n'),
                error_message=None,
                deployment_time=datetime.now(),
                metadata={"platform": "netlify"}
            )
        else:
            return DeploymentResult(
                deployment_id=job.job_id,
                platform=DeploymentPlatform.NETLIFY,
                status=DeploymentStatus.FAILED,
                url=None,
                build_logs=result.stdout.split('\n'),
                error_message=result.stderr,
                deployment_time=datetime.now(),
                metadata={}
            )
    
    async def _deploy_to_aws_amplify(self, job: DeploymentJob, package_path: str) -> DeploymentResult:
        """Deploy to AWS Amplify"""
        logger.info("Deploying to AWS Amplify")
        
        # This would use AWS Amplify CLI
        cmd = ["amplify", "publish", "--yes"]
        
        result = await self._run_command(cmd, cwd=package_path)
        
        return DeploymentResult(
            deployment_id=job.job_id,
            platform=DeploymentPlatform.AWS_AMPLIFY,
            status=DeploymentStatus.SUCCESS if result.returncode == 0 else DeploymentStatus.FAILED,
            url=self._extract_deployment_url(result.stdout, "amplify") if result.returncode == 0 else None,
            build_logs=result.stdout.split('\n'),
            error_message=result.stderr if result.returncode != 0 else None,
            deployment_time=datetime.now(),
            metadata={"platform": "aws_amplify"}
        )
    
    async def _deploy_to_docker(self, job: DeploymentJob, package_path: str) -> DeploymentResult:
        """Deploy to Docker"""
        logger.info("Building Docker image")
        
        image_name = f"{job.app_id}:latest"
        
        # Build Docker image
        build_cmd = ["docker", "build", "-t", image_name, "."]
        result = await self._run_command(build_cmd, cwd=package_path)
        
        if result.returncode == 0:
            # Run container (for local deployment)
            run_cmd = ["docker", "run", "-d", "-p", "3000:3000", image_name]
            run_result = await self._run_command(run_cmd)
            
            return DeploymentResult(
                deployment_id=job.job_id,
                platform=DeploymentPlatform.DOCKER,
                status=DeploymentStatus.SUCCESS,
                url="http://localhost:3000",
                build_logs=result.stdout.split('\n'),
                error_message=None,
                deployment_time=datetime.now(),
                metadata={"platform": "docker", "image": image_name}
            )
        else:
            return DeploymentResult(
                deployment_id=job.job_id,
                platform=DeploymentPlatform.DOCKER,
                status=DeploymentStatus.FAILED,
                url=None,
                build_logs=result.stdout.split('\n'),
                error_message=result.stderr,
                deployment_time=datetime.now(),
                metadata={}
            )
    
    async def _deploy_to_railway(self, job: DeploymentJob, package_path: str) -> DeploymentResult:
        """Deploy to Railway"""
        logger.info("Deploying to Railway")
        
        cmd = ["railway", "up"]
        
        result = await self._run_command(cmd, cwd=package_path)
        
        return DeploymentResult(
            deployment_id=job.job_id,
            platform=DeploymentPlatform.RAILWAY,
            status=DeploymentStatus.SUCCESS if result.returncode == 0 else DeploymentStatus.FAILED,
            url=self._extract_deployment_url(result.stdout, "railway") if result.returncode == 0 else None,
            build_logs=result.stdout.split('\n'),
            error_message=result.stderr if result.returncode != 0 else None,
            deployment_time=datetime.now(),
            metadata={"platform": "railway"}
        )
    
    async def _run_command(self, cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        """Run a command asynchronously"""
        logger.debug(f"Running command: {' '.join(cmd)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=process.returncode,
            stdout=stdout.decode(),
            stderr=stderr.decode()
        )
    
    def _extract_deployment_url(self, output: str, platform: str) -> Optional[str]:
        """Extract deployment URL from command output"""
        # This would parse platform-specific output to extract URLs
        # For now, return a placeholder
        return f"https://{platform}-deployment-url.com"
    
    def get_deployment_job(self, job_id: str) -> Optional[DeploymentJob]:
        """Get deployment job by ID"""
        return self.deployment_jobs.get(job_id)
    
    def get_deployment_history(self, app_id: Optional[str] = None) -> List[DeploymentResult]:
        """Get deployment history, optionally filtered by app"""
        if app_id:
            return [result for result in self.deployment_history 
                   if any(job.app_id == app_id for job in self.deployment_jobs.values() 
                         if job.result and job.result.deployment_id == result.deployment_id)]
        return self.deployment_history.copy()
    
    def get_active_deployments(self) -> List[DeploymentJob]:
        """Get currently active deployment jobs"""
        return [job for job in self.deployment_jobs.values() 
                if job.status in [DeploymentStatus.PENDING, DeploymentStatus.BUILDING, DeploymentStatus.DEPLOYING]]
    
    async def cancel_deployment(self, job_id: str) -> bool:
        """Cancel a deployment job"""
        job = self.deployment_jobs.get(job_id)
        if job and job.status in [DeploymentStatus.PENDING, DeploymentStatus.BUILDING]:
            job.status = DeploymentStatus.CANCELLED
            job.completed_at = datetime.now()
            logger.info(f"Cancelled deployment job {job_id}")
            return True
        return False

# Export main class
__all__ = ['PHALANXDeploymentBridge', 'DeploymentConfig', 'DeploymentJob', 'DeploymentResult', 'DeploymentPlatform', 'ApplicationType']
