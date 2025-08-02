#!/usr/bin/env python3
"""
JAEGIS Unified Command Line Interface
Comprehensive CLI for all JAEGIS framework components

Provides unified access to JAEGIS, M.A.S.T.R., A.T.L.A.S., S.C.R.I.P.T., 
P.I.T.C.E.S., and other framework components through natural language commands.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from core.intelligence.command_adjudicator import CommandAdjudicator
    COMMAND_ADJUDICATOR_AVAILABLE = True
except ImportError:
    COMMAND_ADJUDICATOR_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JAEGISUnifiedCLI:
    """JAEGIS Unified Command Line Interface"""
    
    def __init__(self):
        """Initialize JAEGIS CLI"""
        self.adjudicator = None
        if COMMAND_ADJUDICATOR_AVAILABLE:
            try:
                self.adjudicator = CommandAdjudicator()
            except Exception as e:
                logger.warning(f"Failed to initialize Command Adjudicator: {e}")
    
    def _print_banner(self):
        """Print JAEGIS banner"""
        print("🧠 JAEGIS - Just Another Extremely Great Intelligence System")
        print("   Unified Command Line Interface")
        print("=" * 60)
    
    def _print_success(self, message: str):
        """Print success message"""
        print(f"✅ {message}")
    
    def _print_error(self, message: str):
        """Print error message"""
        print(f"❌ {message}")
    
    def _print_info(self, message: str):
        """Print info message"""
        print(f"ℹ️  {message}")
    
    def cmd_do(self, args) -> int:
        """Execute natural language command using Command Adjudicator"""
        if not args.command:
            self._print_error("Command text is required")
            return 1
        
        command_text = ' '.join(args.command)
        
        print(f"🧠 Processing: '{command_text}'")
        print("=" * 50)
        
        if not self.adjudicator:
            self._print_error("Command Adjudicator not available")
            self._print_info("Falling back to direct framework routing...")
            return self._route_command_directly(command_text)
        
        try:
            result = self.adjudicator.adjudicate(command_text)
            
            if result.get('success', False):
                self._print_success(f"Command executed successfully")
                
                # Display result based on intent
                intent = result.get('intent', 'unknown')
                
                if intent.startswith('mastr_'):
                    self._display_mastr_result(result)
                elif intent in ['set_setting', 'get_setting']:
                    self._display_setting_result(result)
                elif intent == 'status':
                    self._display_status_result(result)
                else:
                    self._display_generic_result(result)
                
                return 0
            else:
                self._print_error(f"Command failed: {result.get('error', 'Unknown error')}")
                
                # Show suggestions if available
                suggestions = result.get('suggestions', [])
                if suggestions:
                    print("\n💡 Suggestions:")
                    for suggestion in suggestions:
                        print(f"   • {suggestion}")
                
                return 1
                
        except Exception as e:
            self._print_error(f"Command processing failed: {e}")
            return 1
    
    def _route_command_directly(self, command_text: str) -> int:
        """Route command directly to appropriate framework"""
        command_lower = command_text.lower()
        
        # M.A.S.T.R. commands
        if any(keyword in command_lower for keyword in ['find tools', 'search tools', 'forge toolset', 'armory']):
            return self._route_to_mastr(command_text)
        
        # A.T.L.A.S. commands
        elif any(keyword in command_lower for keyword in ['sync profile', 'list profiles']):
            return self._route_to_atlas(command_text)
        
        # S.C.R.I.P.T. commands
        elif any(keyword in command_lower for keyword in ['set', 'get', 'setting']):
            return self._route_to_script(command_text)
        
        else:
            self._print_error("Could not determine target framework")
            self._print_info("Try: 'jaegis help' for available commands")
            return 1
    
    def _route_to_mastr(self, command_text: str) -> int:
        """Route command to M.A.S.T.R. CLI"""
        try:
            mastr_cli_path = project_root / "integrations" / "cli" / "mastr_cli.py"
            
            if command_text.lower().startswith('find tools'):
                query = command_text[10:].strip()
                cmd = [sys.executable, str(mastr_cli_path), 'search', query]
            elif command_text.lower().startswith('forge toolset'):
                description = command_text[13:].strip()
                cmd = [sys.executable, str(mastr_cli_path), 'forge', description]
            elif 'armory status' in command_text.lower():
                cmd = [sys.executable, str(mastr_cli_path), 'status']
            else:
                cmd = [sys.executable, str(mastr_cli_path), 'health']
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return result.returncode
            
        except Exception as e:
            self._print_error(f"Failed to route to M.A.S.T.R.: {e}")
            return 1
    
    def _route_to_atlas(self, command_text: str) -> int:
        """Route command to A.T.L.A.S. CLI"""
        self._print_info("A.T.L.A.S. CLI routing not implemented yet")
        return 1
    
    def _route_to_script(self, command_text: str) -> int:
        """Route command to S.C.R.I.P.T. CLI"""
        self._print_info("S.C.R.I.P.T. CLI routing not implemented yet")
        return 1
    
    def _display_mastr_result(self, result: Dict[str, Any]):
        """Display M.A.S.T.R. command result"""
        intent = result.get('intent', '')
        
        if intent == 'mastr_search_tools':
            tools_found = result.get('tools_found', 0)
            tools = result.get('tools', [])
            
            print(f"\n🔍 Found {tools_found} tools:")
            for i, tool in enumerate(tools[:5], 1):  # Show top 5
                print(f"   {i}. {tool.get('name', 'Unknown')}")
                print(f"      Type: {tool.get('type', 'unknown')}")
                print(f"      Score: {tool.get('similarity_score', 0.0):.3f}")
        
        elif intent == 'mastr_forge_toolset':
            forge_id = result.get('forge_id')
            status = result.get('status')
            print(f"\n🔥 Forge Process: {forge_id}")
            print(f"   Status: {status}")
            print(f"   Use 'jaegis do \"check forge {forge_id}\"' to monitor progress")
        
        elif intent == 'mastr_armory_status':
            stats = result.get('armory_stats', {})
            print(f"\n🧰 Armory Statistics:")
            print(f"   Total Tools: {stats.get('total_tools', 0)}")
            print(f"   Success Rate: {stats.get('success_rate', 0.0):.2%}")
    
    def _display_setting_result(self, result: Dict[str, Any]):
        """Display setting command result"""
        intent = result.get('intent', '')
        
        if intent == 'set_setting':
            key = result.get('key')
            print(f"\n⚙️  Setting '{key}' updated successfully")
        
        elif intent == 'get_setting':
            key = result.get('key')
            value = result.get('value', 'Not set')
            print(f"\n⚙️  {key}: {value}")
    
    def _display_status_result(self, result: Dict[str, Any]):
        """Display status command result"""
        print(f"\n📊 JAEGIS System Status:")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Timestamp: {result.get('timestamp', 'unknown')}")
    
    def _display_generic_result(self, result: Dict[str, Any]):
        """Display generic command result"""
        intent = result.get('intent', 'unknown')
        print(f"\n📋 Command Result ({intent}):")
        
        # Show key result fields
        for key, value in result.items():
            if key not in ['intent', 'success', 'timestamp', 'method']:
                if isinstance(value, (str, int, float, bool)):
                    print(f"   {key}: {value}")
    
    def cmd_mastr(self, args) -> int:
        """Direct M.A.S.T.R. command access"""
        try:
            mastr_cli_path = project_root / "integrations" / "cli" / "mastr_cli.py"
            cmd = [sys.executable, str(mastr_cli_path)] + args.mastr_args
            
            result = subprocess.run(cmd)
            return result.returncode
            
        except Exception as e:
            self._print_error(f"M.A.S.T.R. command failed: {e}")
            return 1
    
    def cmd_status(self, args) -> int:
        """Show JAEGIS system status"""
        self._print_banner()
        
        print("📊 Framework Status:")
        
        # Check Command Adjudicator
        if self.adjudicator:
            self._print_success("Command Adjudicator: Available")
        else:
            self._print_error("Command Adjudicator: Not available")
        
        # Check M.A.S.T.R.
        try:
            mastr_cli_path = project_root / "integrations" / "cli" / "mastr_cli.py"
            result = subprocess.run([sys.executable, str(mastr_cli_path), 'health'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self._print_success("M.A.S.T.R. Framework: Healthy")
            else:
                self._print_error("M.A.S.T.R. Framework: Unhealthy")
        except Exception:
            self._print_error("M.A.S.T.R. Framework: Not available")
        
        # Check other frameworks (placeholder)
        self._print_info("A.T.L.A.S. Framework: Status check not implemented")
        self._print_info("S.C.R.I.P.T. Framework: Status check not implemented")
        self._print_info("P.I.T.C.E.S. Framework: Status check not implemented")
        
        return 0
    
    def cmd_version(self, args) -> int:
        """Show version information"""
        print("JAEGIS Unified CLI v2.2.0")
        print("Just Another Extremely Great Intelligence System")
        print()
        print("Integrated Frameworks:")
        print("  • M.A.S.T.R. - Multi-Agent System for Tool Retrieval")
        print("  • A.T.L.A.S. - Advanced Technology & Library Acquisition System")
        print("  • S.C.R.I.P.T. - Systematic Configuration & Resource Integration Platform Tool")
        print("  • P.I.T.C.E.S. - Parallel Integrated Task Contexting Engine System")
        print("  • Command Adjudicator - Natural Language Processing")
        
        return 0
    
    def cmd_help(self, args) -> int:
        """Show help information"""
        self._print_banner()
        
        print("Available Commands:")
        print("  jaegis do \"<natural language command>\"  - Execute natural language command")
        print("  jaegis mastr <mastr-command>              - Direct M.A.S.T.R. access")
        print("  jaegis status                             - Show system status")
        print("  jaegis help                               - Show this help")
        print()
        print("Natural Language Examples:")
        print("  jaegis do \"find tools for web development\"")
        print("  jaegis do \"create toolset for API development\"")
        print("  jaegis do \"register tool FastAPI web framework\"")
        print("  jaegis do \"armory status\"")
        print("  jaegis do \"set github.token my-token\"")
        print("  jaegis do \"get openrouter.api_key\"")
        print()
        print("Direct M.A.S.T.R. Examples:")
        print("  jaegis mastr search \"database management\"")
        print("  jaegis mastr forge \"REST API with authentication\"")
        print("  jaegis mastr register \"PostgreSQL\" --type database")
        print("  jaegis mastr status")
        print()
        print("For more information: https://github.com/usemanusai/JAEGIS")
        
        return 0

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        prog='jaegis',
        description='JAEGIS - Just Another Extremely Great Intelligence System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jaegis do "find tools for web development"
  jaegis do "create toolset for machine learning"
  jaegis do "armory status"
  jaegis mastr search "database management"
  jaegis status
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Do command (natural language)
    do_parser = subparsers.add_parser('do', help='Execute natural language command')
    do_parser.add_argument('command', nargs='+', help='Natural language command')

    # M.A.S.T.R. direct access
    mastr_parser = subparsers.add_parser('mastr', help='Direct M.A.S.T.R. framework access')
    mastr_parser.add_argument('mastr_args', nargs='*', help='M.A.S.T.R. command arguments')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show JAEGIS system status')

    # Help command
    help_parser = subparsers.add_parser('help', help='Show help information')

    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')

    return parser

def main() -> int:
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize CLI
    cli = JAEGISUnifiedCLI()

    # Route to appropriate command
    command_map = {
        'do': cli.cmd_do,
        'mastr': cli.cmd_mastr,
        'status': cli.cmd_status,
        'help': cli.cmd_help,
        'version': cli.cmd_version
    }

    if args.command in command_map:
        try:
            return command_map[args.command](args)
        except KeyboardInterrupt:
            print("\n⚠️  Operation cancelled by user")
            return 130
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            logger.error(f"CLI error: {e}", exc_info=True)
            return 1
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1

if __name__ == '__main__':
    exit(main())