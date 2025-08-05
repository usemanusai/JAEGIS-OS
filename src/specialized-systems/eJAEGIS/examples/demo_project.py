#!/usr/bin/env python3
"""
e.J.A.E.G.I.S. Demo Project
Demonstrates e.J.A.E.G.I.S. agent capabilities with a sample project structure
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
import json
import time

# Import e.J.A.E.G.I.S. components
import sys
sys.path.append(str(Path(__file__).parent.parent))
from core.eJaegis_agent import E-JAEGISAgent

class E-JAEGISDemo:
    """Demonstrates e.J.A.E.G.I.S. capabilities with a sample project"""
    
    def __init__(self):
        self.demo_dir = None
        self.eJaegis_agent = None
    
    async def setup_demo_project(self):
        """Create a sample project structure for demonstration"""
        
        # Create temporary directory for demo
        self.demo_dir = Path(tempfile.mkdtemp(prefix="eJaegis_demo_"))
        print(f"tool_7661": {
                "core": {
                    "models.py": '''"""Core data models for the application"""

class User:
    """User model with basic attributes"""
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }

class Product:
    """Product model for e-commerce"""
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price
    
    def calculate_tax(self, tax_rate: float = 0.08):
        """Calculate tax for the product"""
        return self.price * tax_rate
''',
                    "utils.py": '''"""Utility functions for the application"""

from .models import User, Product

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:.2f}"

def create_user_from_dict(data: dict) -> User:
    """Create User instance from dictionary"""
    return User(
        user_id=data["user_id"],
        name=data["name"],
        email=data["emailapi": {
                    "user_routes.py": '''"""API routes for user management"""

from ..core.models import User
from ..core.utils import validate_email, create_user_from_dict

class UserAPI:
    """User API endpoints"""
    
    def __init__(self):
        self.users = {}
    
    def create_user(self, user_data: dict):
        """Create a new user"""
        if not validate_email(user_data.get("email", "")):
            raise ValueError("Invalid email format")
        
        user = create_user_from_dict(user_data)
        self.users[user.user_id] = user
        return user.to_dict()
    
    def get_user(self, user_id: str):
        """Get user by ID"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user.to_dict()
    
    def update_user(self, user_id: str, updates: dict):
        """Update user information"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        if "email" in updates and not validate_email(updates["email"]):
            raise ValueError("Invalid email format")
        
        # Update user attributes
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return user.to_dict()
''',
                    "product_routes.py": '''"""API routes for product management"""

from ..core.models import Product
from ..core.utils import format_currency

class ProductAPI:
    """Product API endpoints"""
    
    def __init__(self):
        self.products = {}
    
    def create_product(self, product_data: dict):
        """Create a new product"""
        product = Product(
            product_id=product_data["product_id"],
            name=product_data["name"],
            price=float(product_data["price"])
        )
        self.products[product.product_id] = product
        return self._product_to_dict(product)
    
    def get_product(self, product_id: str):
        """Get product by ID"""
        product = self.products.get(product_id)
        if not product:
            raise ValueError("Product not found")
        return self._product_to_dict(product)
    
    def _product_to_dict(self, product: Product):
        """Convert product to dictionary with formatted price"""
        return {
            "product_id": product.product_id,
            "name": product.name,
            "price": product.price,
            "formatted_price": format_currency(product.price),
            "taxproduct_calculate_tax_services": {
                    "user_service.py": '''"""Business logic for user operations"""

from ..api.user_routes import UserAPI
from ..core.models import User

class UserService:
    """Service layer for user operations"""
    
    def __init__(self):
        self.user_api = UserAPI()
    
    def register_user(self, name: str, email: str):
        """Register a new user with validation"""
        import uuid
        
        user_data = {
            "user_id": str(uuid.uuid4()),
            "name": name.strip(),
            "email": email.lower().strip()
        }
        
        return self.user_api.create_user(user_data)
    
    def get_user_profile(self, user_id: str):
        """Get complete user profile"""
        user_data = self.user_api.get_user(user_id)
        
        # Add additional profile information
        user_data["profile_complete"] = all([
            user_data.get("name"),
            user_data.get("emailreturn_user_data_tests": {
                "test_models.py": '''"""Tests for core models"""

import unittest
from src.core.models import User, Product

class TestUser(unittest.TestCase):
    """Test User model"""
    
    def test_user_creation(self):
        """Test user creation"""
        user = User("123", "John Doe", "john@example.com")
        self.assertEqual(user.user_id, "123")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
    
    def test_user_to_dict(self):
        """Test user to dictionary conversion"""
        user = User("123", "John Doe", "john@example.com")
        user_dict = user.to_dict()
        
        expected = {
            "user_id": "123",
            "name": "John_Doe",
            "email": "john@example.com"
        }
        self.assertEqual(user_dict, expected)

class TestProduct(unittest.TestCase):
    """Test Product model"""
    
    def test_product_creation(self):
        """Test product creation"""
        product = Product("p123", "Test Product", 99.99)
        self.assertEqual(product.product_id, "p123")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 99.99)
    
    def test_calculate_tax(self):
        """Test tax calculation"""
        product = Product("p123", "Test Product", 100.0)
        tax = product.calculate_tax(0.1)
        self.assertEqual(tax, 10.0)
'''
            },
            "README.md": '''# Demo Project

This is a sample project to demonstrate e.J.A.E.G.I.S. capabilities.

## Structure

- `src/core/` - Core models and utilities
- `src/api/` - API endpoints
- `src/services/` - Business logic
- `tests/` - Test suites

## Dependencies

The project demonstrates various dependency relationships:

- API routes depend on core models and utilities
- Services depend on API routes and models
- Tests depend on all components
''',
            "requirements.txt": '''# Demo project dependencies
pytest>=7.0.0
requests>=2.28.0
'''
        }
        
        # Create files and directories
        self._create_structure(self.demo_dir, project_structure)
        
        print("✅ Demo project structure created")
        return self.demo_dir
    
    def _create_structure(self, base_path: Path, structure: dict):
        """Recursively create project structure"""
        for name, content in structure.items():
            path = base_path / name
            
            if isinstance(content, dict):
                # Create directory and recurse
                path.mkdir(exist_ok=True)
                self._create_structure(path, content)
            else:
                # Create file with content
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    async def initialize_eJaegis(self):
        """Initialize e.J.A.E.G.I.S. for the demo project"""
        print("🚀 Initializing e.J.A.E.G.I.S. for demo project...")
        
        self.eJaegis_agent = E-JAEGISAgent(self.demo_dir)
        await self.eJaegis_agent.initialize()
        
        print(f"✅ e.J.A.E.G.I.S. initialized with {len(self.eJaegis_agent.knowledge_graph.components)} components")
        
        # Show some statistics
        file_types = {}
        for comp in self.eJaegis_agent.knowledge_graph.components.values():
            ext = Path(comp.file_path).suffix
            file_types[ext] = file_types.get(ext, 0) + 1
        
        print("📊 Component analysis:")
        for ext, count in sorted(file_types.items()):
            print(f"  {ext}: {count} components")
    
    async def demonstrate_change_detection(self):
        """Demonstrate e.J.A.E.G.I.S.'s change detection capabilities"""
        print("\n🔄 Demonstrating change detection...")
        
        # Modify the User model to show impact analysis
        models_file = self.demo_dir / "src" / "core" / "models.py"
        
        print(f"📝 Modifying {models_file.relative_to(self.demo_dir)}")
        
        # Read current content
        with open(models_file, 'r') as f:
            content = f.read()
        
        # Add a new method to User class
        new_method = '''
    
    def get_display_name(self):
        """Get formatted display name"""
        return f"{self.name} <{self.email}>"'''
        
        # Insert the new method before the Product class
        modified_content = content.replace(
            'class Product:',
            new_method + '\n\nclass Product:'
        )
        
        # Write modified content
        with open(models_file, 'w') as f:
            f.write(modified_content)
        
        print("✅ File modified - e.J.A.E.G.I.S. should detect this change")
        
        # Give e.J.A.E.G.I.S. a moment to process the change
        await asyncio.sleep(2)
        
        # Manually trigger impact analysis for demonstration
        print("🔍 Analyzing impact of changes...")
        impact_tasks = await self.eJaegis_agent.impact_engine.analyze_impact(
            str(models_file.relative_to(self.demo_dir))
        )
        
        if impact_tasks:
            print(f"📊 Found {len(impact_tasks)} potential impacts:")
            for task in impact_tasks:
                print(f"  • {task.affected_component}")
                print(f"    Impact Level: {task.impact_level}")
                print(f"    Owner: {task.owner.owner_id} ({task.owner.owner_type})")
                print(f"    Suggested Actions:")
                for action in task.suggested_actions[:2]:
                    print(f"      - {action}")
                print()
        else:
            print("ℹ️  No immediate impacts detected (this is normal for new methods)")
    
    async def demonstrate_dependency_analysis(self):
        """Demonstrate dependency analysis capabilities"""
        print("\n🔍 Demonstrating dependency analysis...")
        
        # Analyze dependencies for a specific file
        user_routes_file = "src/api/user_routes.py"
        
        print(f"📊 Analyzing dependencies for {user_routes_file}")
        
        # Find components in the file
        file_components = [
            comp_id for comp_id, comp in self.eJaegis_agent.knowledge_graph.components.items()
            if comp.file_path == user_routes_file
        ]
        
        print(f"Found {len(file_components)} components in {user_routes_file}")
        
        # For each component, show its dependencies and dependents
        for comp_id in file_components[:3]:  # Show first 3 components
            component = self.eJaegis_agent.knowledge_graph.components[comp_id]
            dependents = await self.eJaegis_agent.knowledge_graph.find_dependents(comp_id)
            
            print(f"\n📦 Component: {component.name} ({component.component_type})")
            print(f"   File: {component.file_path}")
            print(f"   Dependencies: {component.dependencies[:5]}")  # Show first 5
            print(f"   Dependents: {len(dependents)} components depend on this")
    
    async def show_ownership_ledger(self):
        """Show the ownership ledger configuration"""
        print("\n👥 Ownership Ledger Configuration:")
        
        ledger_file = self.demo_dir / "OWNERSHIP_LEDGER.json"
        if ledger_file.exists():
            with open(ledger_file, 'r') as f:
                ledger = json.load(f)
            
            entries = ledger.get('ownership_entries', [])
            print(f"Found {len(entries)} ownership entries:")
            
            for entry in entries[:5]:  # Show first 5 entries
                print(f"  • Pattern: {entry.get('pattern', '')}")
                print(f"    Owner: {entry.get('owner_id', '')} ({entry.get('owner_type', '')})")
                print(f"    Contact: {entry.get('contact_method', '')}")
                print(f"    Priority: {entry.get('priority', '')}")
                print()
        else:
            print("❌ Ownership ledger not found")
    
    async def cleanup(self):
        """Clean up demo resources"""
        if self.eJaegis_agent:
            await self.eJaegis_agent.shutdown()
        
        if self.demo_dir and self.demo_dir.exists():
            shutil.rmtree(self.demo_dir)
            print(f"🧹 Cleaned up demo directory: {self.demo_dir}")

async def main():
    """Run the e.J.A.E.G.I.S. demonstration"""
    demo = E-JAEGISDemo()
    
    try:
        print("🎯 e.J.A.E.G.I.S. Agent Demonstration")
        print("=" * 50)
        
        # Setup demo project
        await demo.setup_demo_project()
        
        # Initialize e.J.A.E.G.I.S.
        await demo.initialize_eJaegis()
        
        # Show ownership configuration
        await demo.show_ownership_ledger()
        
        # Demonstrate dependency analysis
        await demo.demonstrate_dependency_analysis()
        
        # Demonstrate change detection
        await demo.demonstrate_change_detection()
        
        print("\n✅ e.J.A.E.G.I.S. demonstration completed successfully!")
        print("\nKey capabilities demonstrated:")
        print("  • Automatic codebase analysis and knowledge graph building")
        print("  • Dependency relationship mapping")
        print("  • Change detection and impact analysis")
        print("  • Ownership-based task routing")
        print("  • Multi-language code parsing")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await demo.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
