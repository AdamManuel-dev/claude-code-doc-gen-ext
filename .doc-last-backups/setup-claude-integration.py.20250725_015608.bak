#!/usr/bin/env python3
"""
Claude Code Integration Setup Script

Automatically configures the Claude Code Documentation Generation Extension
with your Claude Code CLI installation.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(message):
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.CYAN}ℹ {message}{Colors.ENDC}")

def run_command(command, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=capture_output, 
            text=True, 
            check=True
        )
        return result.stdout.strip() if capture_output else True
    except subprocess.CalledProcessError as e:
        if capture_output:
            return None
        return False

def check_prerequisites():
    """Check if all required tools are installed."""
    print_header("Checking Prerequisites")
    
    checks = {
        'Claude Code': 'claude --version',
        'Node.js': 'node --version', 
        'Python': 'python3 --version',
        'Git': 'git --version'
    }
    
    all_good = True
    
    for tool, command in checks.items():
        version = run_command(command)
        if version:
            print_success(f"{tool}: {version}")
        else:
            print_error(f"{tool}: Not found or not working")
            all_good = False
    
    return all_good

def find_claude_config_dir():
    """Find the Claude Code configuration directory."""
    print_info("Looking for Claude Code configuration directory...")
    
    # Common locations
    possible_paths = [
        Path.home() / '.claude',
        Path.home() / '.config' / 'claude',
        Path(os.environ.get('APPDATA', '')) / 'claude' if os.name == 'nt' else None,
        Path(os.environ.get('USERPROFILE', '')) / '.claude' if os.name == 'nt' else None,
    ]
    
    # Filter out None values
    possible_paths = [p for p in possible_paths if p is not None]
    
    for path in possible_paths:
        if path.exists():
            print_success(f"Found Claude config at: {path}")
            return path
    
    # Try to get from Claude CLI
    config_output = run_command('claude config show')
    if config_output:
        # Parse the output to find config directory
        for line in config_output.split('\n'):
            if 'config' in line.lower() and ('dir' in line.lower() or 'path' in line.lower()):
                # Extract path from the line
                parts = line.split()
                for part in parts:
                    if os.path.exists(part):
                        path = Path(part)
                        print_success(f"Found Claude config at: {path}")
                        return path
    
    print_warning("Could not automatically find Claude config directory")
    return None

def get_project_root():
    """Get the root directory of this project."""
    return Path(__file__).parent.absolute()

def setup_slash_commands(claude_config_dir, project_root):
    """Set up the slash commands for Claude Code."""
    print_header("Setting Up Slash Commands")
    
    # Create slash-commands directory
    slash_commands_dir = claude_config_dir / 'slash-commands'
    slash_commands_dir.mkdir(exist_ok=True)
    print_success(f"Created slash commands directory: {slash_commands_dir}")
    
    # Copy the Python script
    source_script = project_root / 'documentation-slash-command.py'
    target_script = slash_commands_dir / 'doc-commands.py'
    
    if source_script.exists():
        shutil.copy2(source_script, target_script)
        os.chmod(target_script, 0o755)  # Make executable
        print_success(f"Copied slash command script to: {target_script}")
    else:
        print_error(f"Source script not found: {source_script}")
        return False
    
    # Create configuration file
    config_data = {
        "commands": {
            "doc-last": {
                "description": "Document files from the most recent git commit",
                "script": "doc-commands.py",
                "args": ["--mode", "last"]
            },
            "doc-recent": {
                "description": "Document recently modified files (last 5 minutes)",
                "script": "doc-commands.py",
                "args": ["--mode", "recent"]
            },
            "doc-staged": {
                "description": "Document files currently staged in git",
                "script": "doc-commands.py",
                "args": ["--mode", "staged"]
            },
            "doc-all": {
                "description": "Document all supported files in the project (use with caution)",
                "script": "doc-commands.py",
                "args": ["--mode", "all"]
            },
            "doc-preview": {
                "description": "Preview documentation changes without modifying files",
                "script": "doc-commands.py",
                "args": ["--mode", "last", "--dry-run"]
            }
        },
        "config": {
            "doc_generator_path": str(project_root / 'doc-generator.js'),
            "auto_enhance": True,
            "backup_enabled": True,
            "verbose_default": False
        }
    }
    
    config_file = slash_commands_dir / 'doc-commands.json'
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    print_success(f"Created configuration file: {config_file}")
    
    # Update the Python script with correct paths
    script_content = target_script.read_text()
    updated_content = script_content.replace(
        'DOC_GENERATOR_PATH = None',
        f'DOC_GENERATOR_PATH = "{project_root / "doc-generator.js"}"'
    )
    target_script.write_text(updated_content)
    print_success("Updated script paths")
    
    return True

def install_project_dependencies(project_root):
    """Install Node.js dependencies for the project."""
    print_header("Installing Project Dependencies")
    
    package_json = project_root / 'package.json'
    if not package_json.exists():
        print_error("package.json not found")
        return False
    
    print_info("Installing Node.js dependencies...")
    if run_command(f'cd "{project_root}" && npm install', capture_output=False):
        print_success("Dependencies installed successfully")
        return True
    else:
        print_error("Failed to install dependencies")
        return False

def make_scripts_executable(project_root):
    """Make the main scripts executable."""
    print_header("Setting Script Permissions")
    
    scripts = [
        'doc-generator.js',
        'documentation-slash-command.py',
        'claude-code-documentation-hooks.py'
    ]
    
    for script in scripts:
        script_path = project_root / script
        if script_path.exists():
            os.chmod(script_path, 0o755)
            print_success(f"Made executable: {script}")
        else:
            print_warning(f"Script not found: {script}")

def test_installation(project_root):
    """Test the installation by running basic commands."""
    print_header("Testing Installation")
    
    # Test Node.js generator
    print_info("Testing Node.js documentation generator...")
    result = run_command(f'cd "{project_root}" && node doc-generator.js --help')
    if result:
        print_success("Node.js generator is working")
    else:
        print_error("Node.js generator test failed")
        return False
    
    # Test Python slash command handler
    print_info("Testing Python slash command handler...")
    result = run_command(f'cd "{project_root}" && python3 documentation-slash-command.py --help')
    if result:
        print_success("Python slash command handler is working")
    else:
        print_error("Python slash command handler test failed")
        return False
    
    return True

def create_environment_config(project_root):
    """Create environment configuration suggestions."""
    print_header("Environment Configuration")
    
    shell_config = f"""
# Claude Code Documentation Generator Configuration
# Add these lines to your ~/.bashrc, ~/.zshrc, or ~/.profile

export CLAUDE_DOC_GENERATOR="{project_root / 'doc-generator.js'}"
export CLAUDE_DOC_OPTIONS="--verbose"
export CLAUDE_DOC_DEBUG=0

# Optional: Add project to PATH for global access
export PATH="{project_root}:$PATH"
"""
    
    config_file = project_root / 'environment-config.sh'
    with open(config_file, 'w') as f:
        f.write(shell_config)
    
    print_success(f"Created environment configuration: {config_file}")
    print_info("To apply the configuration, run:")
    print(f"  source {config_file}")
    print("Or manually add the exports to your shell configuration file")

def setup_git_hooks_template(project_root):
    """Create a template for git hooks setup."""
    print_header("Git Hooks Template")
    
    hook_setup_script = f"""#!/bin/bash
# Git Hooks Setup Script for Claude Code Documentation Generator
# Run this script in any git repository where you want automatic documentation

PROJECT_ROOT="{project_root}"
HOOK_SCRIPT="$PROJECT_ROOT/claude-code-documentation-hooks.py"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

echo "Setting up documentation hooks in $(pwd)"

# Copy pre-commit hook
cp "$HOOK_SCRIPT" .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Update the hook with correct paths
sed -i.bak "s|DOC_GENERATOR_PATH = None|DOC_GENERATOR_PATH = \\\"$PROJECT_ROOT/doc-generator.js\\\"|" .git/hooks/pre-commit

echo "✓ Pre-commit hook installed"
echo "✓ Documentation will be generated automatically on git commit"
echo ""
echo "To disable hooks for a specific commit, use:"
echo "  git commit --no-verify"
"""
    
    hook_setup_file = project_root / 'setup-git-hooks.sh'
    with open(hook_setup_file, 'w') as f:
        f.write(hook_setup_script)
    os.chmod(hook_setup_file, 0o755)
    
    print_success(f"Created git hooks setup script: {hook_setup_file}")
    print_info("To set up git hooks in a project, run:")
    print(f"  cd /path/to/your/project && {hook_setup_file}")

def main():
    """Main setup function."""
    print_header("Claude Code Documentation Generator Setup")
    print("This script will configure the documentation generator with your Claude Code installation.\n")
    
    # Get project root
    project_root = get_project_root()
    print_info(f"Project root: {project_root}")
    
    # Check prerequisites
    if not check_prerequisites():
        print_error("Prerequisites check failed. Please install missing tools and try again.")
        sys.exit(1)
    
    # Find Claude config directory
    claude_config_dir = find_claude_config_dir()
    if not claude_config_dir:
        manual_path = input(f"\n{Colors.WARNING}Please enter the Claude config directory path: {Colors.ENDC}")
        claude_config_dir = Path(manual_path.strip())
        if not claude_config_dir.exists():
            print_error("Directory does not exist")
            sys.exit(1)
    
    # Install project dependencies
    if not install_project_dependencies(project_root):
        print_error("Failed to install dependencies")
        sys.exit(1)
    
    # Make scripts executable
    make_scripts_executable(project_root)
    
    # Set up slash commands
    if not setup_slash_commands(claude_config_dir, project_root):
        print_error("Failed to set up slash commands")
        sys.exit(1)
    
    # Test installation
    if not test_installation(project_root):
        print_error("Installation tests failed")
        sys.exit(1)
    
    # Create additional configuration
    create_environment_config(project_root)
    setup_git_hooks_template(project_root)
    
    # Final success message
    print_header("Setup Complete!")
    print_success("Claude Code Documentation Generator has been successfully configured!")
    print("\nNext steps:")
    print("1. Restart your Claude Code CLI")
    print("2. Test the slash commands:")
    print("   - /doc-last --dry-run")
    print("   - /doc-recent --help")
    print("3. Set up git hooks in your projects using setup-git-hooks.sh")
    print("4. Read the documentation: docs/guides/GETTING_STARTED.md")
    print(f"\n{Colors.CYAN}Happy documenting! 📝{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Setup failed with error: {e}{Colors.ENDC}")
        sys.exit(1)