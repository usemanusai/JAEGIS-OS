#!/usr/bin/env python3
"""
A.E.G.I.S. Directory Structure Creator
Creates the complete directory structure for the A.E.G.I.S. Protocol Suite
"""

import os
from pathlib import Path

def create_aegis_structure():
    """Create the complete A.E.G.I.S. directory structure"""
    
    # Define the A.E.G.I.S. directory structure
    aegis_dirs = [
        # A.C.I.D. - Autonomous Cognitive Intelligence Directorate
        "core/acid",
        "core/acid/formation",
        "core/acid/swarm", 
        "core/acid/consensus",
        "core/acid/persistence",
        "core/acid/scaling",
        
        # A.U.R.A. - Artistic & UI Responsive Assistant
        "integrations/vscode/aura",
        "integrations/vscode/aura/generators",
        "integrations/vscode/aura/preview",
        "integrations/vscode/aura/styles",
        "integrations/vscode/aura/assets",
        
        # P.H.A.L.A.N.X. - Procedural Hyper-Accessible Adaptive Nexus
        "frameworks/phalanx",
        "frameworks/phalanx/generators",
        "frameworks/phalanx/editor",
        "frameworks/phalanx/export",
        "frameworks/phalanx/deployment",
        "frameworks/phalanx/database",
        
        # O.D.I.N. - Open Development & Integration Network
        "integrations/vscode/odin",
        "integrations/vscode/continue_dev_config",
        "integrations/cli/odin",
        "integrations/cli/odin/commands",
        "integrations/cli/odin/config",
        
        # Additional supporting directories
        "docs/aegis",
        "docs/aegis/acid",
        "docs/aegis/aura", 
        "docs/aegis/phalanx",
        "docs/aegis/odin",
        "examples/aegis",
        "tests/aegis"
    ]
    
    print("🏗️ Creating A.E.G.I.S. Protocol Suite directory structure...")
    
    created_count = 0
    for directory in aegis_dirs:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"  📁 Created: {directory}")
            created_count += 1
        except Exception as e:
            print(f"  ❌ Failed to create {directory}: {e}")
    
    print(f"✅ A.E.G.I.S. directory structure created: {created_count}/{len(aegis_dirs)} directories")
    
    # Create .gitkeep files for empty directories
    for directory in aegis_dirs:
        gitkeep_path = Path(directory) / ".gitkeep"
        try:
            gitkeep_path.touch()
        except Exception:
            pass
    
    print("📄 Added .gitkeep files to maintain directory structure")
    
    return True

if __name__ == "__main__":
    create_aegis_structure()
