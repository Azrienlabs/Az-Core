"""Miscellaneous templates."""


def get_gitignore_template() -> str:
    """Get .gitignore template."""
    return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Logs
logs/
*.log

# Data
data/
rl_data/
models/
*.pkl
*.pt
*.pth

# Cache
.cache/
*.cache

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/
"""


def get_readme_template(project_name: str, template_type: str) -> str:
    """Get README template."""
    template_desc = {
        "basic-agent": "single agent setup",
        "team-agent": "multi-agent team collaboration",
        "rl-agent": "RL-optimized agent with training capabilities",
        "workflow": "custom workflow orchestration",
    }
    
    desc = template_desc.get(template_type, "Az-Core project")
    
    return f"""# {project_name}

An Az-Core project with {desc}.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Usage

Run the main application:
```bash
azcore run main.py
```

Or run with a custom input:
```bash
azcore run main.py --input "Your query here"
```

With a config file:
```bash
azcore run main.py --config configs/config.yml
```

## Configuration

Edit `configs/config.yml` to customize:
- LLM settings (model, temperature, etc.)
- Agent behavior
- Workflow parameters
- RL training settings (if applicable)

## Project Structure

```
{project_name}/
├── main.py              # Main application entry point
├── configs/             # Configuration files
│   └── config.yml
├── data/               # Data directory
├── logs/               # Log files
{"├── rl_data/           # RL training data" if template_type == "rl-agent" else ""}
{"├── models/            # Trained models" if template_type == "rl-agent" else ""}
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Commands

### Run
```bash
azcore run main.py
```

### Validate Configuration
```bash
azcore validate configs/config.yml
```

{"### Train RL Agent" if template_type == "rl-agent" else ""}
{"```bash" if template_type == "rl-agent" else ""}
{"azcore train rl-agent --config configs/config.yml --episodes 1000" if template_type == "rl-agent" else ""}
{"```" if template_type == "rl-agent" else ""}

{"### View Statistics" if template_type == "rl-agent" else ""}
{"```bash" if template_type == "rl-agent" else ""}
{"azcore stats --show-rl-metrics" if template_type == "rl-agent" else ""}
{"```" if template_type == "rl-agent" else ""}

## Documentation

- [Az-Core Documentation](https://github.com/Azrienlabs/Az-Core)
- [Examples](https://github.com/Azrienlabs/Az-Core/tree/main/examples)

## License

[Your License Here]
"""
