"""Initialize new Az-Core project."""

import os
import click
from pathlib import Path
from typing import Optional

from azcore.cli.templates import (
    get_basic_agent_template,
    get_team_agent_template,
    get_rl_agent_template,
    get_workflow_template,
    get_config_template,
    get_gitignore_template,
    get_readme_template,
)

# Import version from main package
try:
    from azcore import __version__ as AZCORE_VERSION
except ImportError:
    AZCORE_VERSION = "0.0.5"


def print_banner():
    """Print Az-Core ASCII banner."""
    banner = """
    
   ###    ########      ######   #######  ########  ######## 
  ## ##        ##      ##    ## ##     ## ##     ## ##       
 ##   ##      ##       ##       ##     ## ##     ## ##       
##     ##    ##   #### ##       ##     ## ########  ######   
#########   ##         ##       ##     ## ##   ##   ##       
##     ##  ##          ##    ## ##     ## ##    ##  ##       
##     ## ########      ######   #######  ##     ## ######## 
    
"""
    
    # Print banner in cyan
    click.secho(banner, fg="cyan", bold=True)
    
    # Print attribution and version
    click.secho("                           by Azrienlabs", fg="bright_black")
    click.secho(f"                           version {AZCORE_VERSION}", fg="green")
    click.echo()


TEMPLATES = {
    "basic-agent": {
        "name": "Basic Agent",
        "description": "Single agent setup with ReAct reasoning",
        "details": "Perfect for simple tasks, Q&A, or getting started with Az-Core",
        "use_cases": ["Question answering", "Simple automation", "Getting started"]
    },
    "team-agent": {
        "name": "Team Agent",
        "description": "Multi-agent collaboration system",
        "details": "Multiple specialized agents working together on complex tasks",
        "use_cases": ["Complex workflows", "Role-based tasks", "Research & analysis"]
    },
    "rl-agent": {
        "name": "RL-Optimized Agent",
        "description": "Agent with reinforcement learning for tool selection",
        "details": "Self-improving agent that learns optimal tool usage patterns",
        "use_cases": ["Tool optimization", "Adaptive systems", "Long-term learning"]
    },
    "workflow": {
        "name": "Custom Workflow",
        "description": "Flexible workflow orchestration system",
        "details": "Build custom agent workflows with sequential, parallel, or graph execution",
        "use_cases": ["Custom pipelines", "Complex orchestration", "Advanced patterns"]
    }
}


@click.command()
@click.option(
    "--template",
    "-t",
    type=click.Choice(list(TEMPLATES.keys())),
    default=None,
    help="Project template to use (skip interactive mode)",
)
@click.option(
    "--name",
    "-n",
    default=None,
    help="Project name (skip interactive mode)",
)
@click.option(
    "--path",
    "-p",
    type=click.Path(),
    default=".",
    help="Directory to create project in",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Override existing files",
)
def init(template: Optional[str], name: Optional[str], path: str, force: bool):
    """Initialize a new Az-Core project.
    
    Interactive mode (no options):
        azcore init
        
    Direct mode (with options):
        azcore init --template basic-agent --name my-agent
        azcore init -t rl-agent -n rl-optimizer
    """
    # Interactive mode if no template or name provided
    if template is None or name is None:
        # Print the banner
        print_banner()
        click.secho(">>> Welcome to Az-Core Project Setup! <<<\n", fg="cyan", bold=True)
        
        # Get project name
        if name is None:
            name = click.prompt(
                click.style("Enter project name", fg="yellow"),
                default="my-azcore-project",
                type=str
            )
        
        # Get template with interactive selection
        if template is None:
            template = _interactive_template_selection()
    
    # Show banner in direct mode too
    else:
        print_banner()
    
    # Validate template
    if template not in TEMPLATES:
        click.secho(f"Error: Invalid template '{template}'", fg="red")
        return
    project_path = Path(path) / name
    
    # Check if directory exists
    if project_path.exists() and not force:
        if any(project_path.iterdir()):
            click.secho(
                f"Error: Directory '{project_path}' already exists and is not empty.",
                fg="red"
            )
            click.echo("Use --force to override existing files.")
            return
    
    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    
    click.echo("=" * 70)
    click.secho(f"Creating Az-Core project: {name}", fg="cyan", bold=True)
    click.echo(f"Template: {TEMPLATES[template]['name']}")
    click.echo(f"Location: {project_path.absolute()}")
    click.echo("=" * 70 + "\n")
    
    # Create project structure
    _create_project_structure(project_path, template, name)
    
    click.echo()
    click.secho("[SUCCESS] Project created successfully!", fg="green", bold=True)
    click.echo("\n" + "=" * 70)
    click.secho("Next Steps:", fg="cyan", bold=True)
    click.echo("=" * 70)
    click.echo(f"  1. cd {name}")
    click.echo("  2. pip install -r requirements.txt")
    click.echo("  3. Copy .env.example to .env and add your API keys")
    click.echo("  4. azcore run main.py")
    click.echo("\n" + "=" * 70)
    click.secho(f"Project Type: {TEMPLATES[template]['name']}", fg="blue")
    click.echo(f"   {TEMPLATES[template]['details']}")
    click.echo("=" * 70 + "\n")


def _create_project_structure(project_path: Path, template: str, name: str):
    """Create the project structure based on template."""
    
    # Create directories
    (project_path / "configs").mkdir(exist_ok=True)
    (project_path / "data").mkdir(exist_ok=True)
    (project_path / "logs").mkdir(exist_ok=True)
    
    if template == "rl-agent":
        (project_path / "rl_data").mkdir(exist_ok=True)
        (project_path / "models").mkdir(exist_ok=True)
    
    # Create main application file
    main_content = _get_template_content(template, name)
    _write_file(project_path / "main.py", main_content)
    click.echo("  Created main.py")
    
    # Create config file
    config_content = get_config_template(template)
    _write_file(project_path / "configs" / "config.yml", config_content)
    click.echo("  Created configs/config.yml")
    
    # Create requirements.txt
    requirements = _get_requirements(template)
    _write_file(project_path / "requirements.txt", requirements)
    click.echo("  Created requirements.txt")
    
    # Create .gitignore
    gitignore = get_gitignore_template()
    _write_file(project_path / ".gitignore", gitignore)
    click.echo("  Created .gitignore")
    
    # Create README.md
    readme = get_readme_template(name, template)
    _write_file(project_path / "README.md", readme)
    click.echo("  Created README.md")
    
    # Create .env.example
    env_example = _get_env_example()
    _write_file(project_path / ".env.example", env_example)
    click.echo("  Created .env.example")


def _get_template_content(template: str, name: str) -> str:
    """Get the main application content for the template."""
    if template == "basic-agent":
        return get_basic_agent_template(name)
    elif template == "team-agent":
        return get_team_agent_template(name)
    elif template == "rl-agent":
        return get_rl_agent_template(name)
    elif template == "workflow":
        return get_workflow_template(name)
    else:
        return get_basic_agent_template(name)


def _get_requirements(template: str) -> str:
    """Get requirements.txt content based on template."""
    base_requirements = """# Az-Core Framework
azcore>=0.0.5

# LangChain
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-anthropic>=0.1.0

# Utilities
python-dotenv>=1.0.0
pyyaml>=6.0
"""
    
    if template == "rl-agent":
        base_requirements += """
# RL-specific dependencies
sentence-transformers>=2.2.0
torch>=2.0.0
numpy>=1.24.0
"""
    
    return base_requirements


def _get_env_example() -> str:
    """Get .env.example content."""
    return """# OpenAI API Key
OPENAI_API_KEY=your-api-key-here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your-api-key-here

# LangSmith (optional)
LANGCHAIN_API_KEY=your-api-key-here
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=azcore-project
"""


def _write_file(path: Path, content: str):
    """Write content to file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _interactive_template_selection() -> str:
    """Interactive template selection with descriptions."""
    click.echo("\n" + "=" * 70)
    click.secho("Available Project Templates", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    # Display all templates with details
    template_keys = list(TEMPLATES.keys())
    for idx, key in enumerate(template_keys, 1):
        template_info = TEMPLATES[key]
        
        # Template header
        click.secho(f"{idx}. {template_info['name']}", fg="green", bold=True)
        click.echo(f"   {template_info['description']}")
        
        # Details
        click.secho(f"   > Details: ", fg="blue", nl=False)
        click.echo(template_info['details'])
        
        # Use cases
        click.secho(f"   > Use Cases: ", fg="blue", nl=False)
        click.echo(", ".join(template_info['use_cases']))
        click.echo()
    
    # Get user selection
    click.echo("-" * 70)
    while True:
        choice = click.prompt(
            click.style("\nSelect a template", fg="yellow"),
            type=click.IntRange(1, len(template_keys)),
            default=1
        )
        
        selected_key = template_keys[choice - 1]
        selected_template = TEMPLATES[selected_key]
        
        # Confirm selection
        click.echo()
        click.secho(f"[*] Selected: {selected_template['name']}", fg="green")
        click.echo(f"    {selected_template['description']}")
        
        if click.confirm("\nProceed with this template?", default=True):
            return selected_key
        
        click.echo("\nLet's choose again...\n")
