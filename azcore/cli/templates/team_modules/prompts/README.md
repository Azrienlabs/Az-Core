# Team Prompts

This directory contains system prompts for each team in markdown format.

## Structure

Each team has its own prompt file:
- `research_team.md` - Research and web search specialist
- `data_team.md` - Data analysis and processing specialist
- `communication_team.md` - Communication and notification specialist
- `file_team.md` - File management specialist

## Usage

Prompts are automatically loaded by the `utils.load_prompt()` function in each team module.

```python
from .utils import load_prompt

team_config = {
    "name": "research_team",
    "prompt": load_prompt("research_team"),  # Loads from prompts/research_team.md
    ...
}
```

## Customization

To customize a team's behavior:

1. Edit the corresponding `.md` file in this directory
2. Modify the prompt structure, guidelines, or instructions
3. The changes will be automatically picked up when the team is initialized

## Prompt Structure

Each prompt file typically includes:

### Header
Team name and role description

### Responsibilities
List of primary duties and tasks

### Guidelines
Best practices and operational rules

### Response Format
How the team should structure its responses

### Important Notes
Critical considerations and warnings

## Best Practices

1. **Be Specific**: Clearly define the team's role and scope
2. **Provide Examples**: Include examples of good responses
3. **Set Boundaries**: Clearly state what the team should NOT do
4. **Use Clear Language**: Avoid ambiguity in instructions
5. **Include Context**: Provide necessary background information

## Adding New Teams

To add a new team prompt:

1. Create a new `.md` file: `prompts/new_team.md`
2. Follow the structure of existing prompts
3. Reference it in your team configuration: `load_prompt("new_team")`

## Versioning

Consider versioning prompts if you need to track changes:
- Use git to track prompt modifications
- Document significant changes in commit messages
- Test prompt changes before deploying to production
