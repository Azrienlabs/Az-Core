"""Agent templates for project initialization."""


def get_basic_agent_template(project_name: str) -> str:
    """Get basic agent template."""
    return f'''"""
{project_name} - Basic Agent
Created with Az-Core CLI
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from azcore.agents.react_agent import ReactAgent
from azcore.core.state import State

# Load environment variables
load_dotenv()


def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"{project_name}")
    print("=" * 60 + "\\n")
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create agent
    agent = ReactAgent(
        name="basic_agent",
        llm=llm,
        tools=[],  # Add your tools here
        prompt="You are a helpful AI assistant."
    )
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("Enter your query: ")
    
    # Initialize state
    state = State(messages=[{{"role": "user", "content": query}}])
    
    # Run agent
    print("\\nProcessing...\\n")
    result = agent.invoke(state)
    
    # Display result
    print("\\nResult:")
    print("-" * 60)
    if result.get("messages"):
        last_message = result["messages"][-1]
        print(last_message.content if hasattr(last_message, 'content') else str(last_message))
    print("-" * 60)


if __name__ == "__main__":
    main()
'''


def get_team_agent_template(project_name: str) -> str:
    """Get team agent template."""
    return f'''"""
{project_name} - Team Agent Collaboration
Created with Az-Core CLI
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from azcore.agents.team_builder import TeamBuilder
from azcore.workflows.sequential_workflow import SequentialWorkflow
from azcore.core.state import State

# Load environment variables
load_dotenv()


def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"{project_name}")
    print("=" * 60 + "\\n")
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Define team members
    team_config = {{
        "researcher": {{
            "role": "researcher",
            "goal": "Research and gather information",
            "backstory": "Expert at finding and analyzing information"
        }},
        "analyst": {{
            "role": "analyst",
            "goal": "Analyze data and provide insights",
            "backstory": "Skilled at critical thinking and analysis"
        }},
        "writer": {{
            "role": "writer",
            "goal": "Create well-written content",
            "backstory": "Expert at clear and concise communication"
        }}
    }}
    
    # Build team
    team_builder = TeamBuilder(llm=llm)
    agents = team_builder.build_team(team_config)
    
    # Create workflow
    workflow = SequentialWorkflow(agents=list(agents.values()))
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("Enter your query: ")
    
    # Initialize state
    state = State(messages=[{{"role": "user", "content": query}}])
    
    # Run workflow
    print("\\nProcessing through team...\\n")
    result = workflow.run(state)
    
    # Display result
    print("\\nFinal Result:")
    print("-" * 60)
    if result.get("messages"):
        last_message = result["messages"][-1]
        print(last_message.content if hasattr(last_message, 'content') else str(last_message))
    print("-" * 60)


if __name__ == "__main__":
    main()
'''


def get_rl_agent_template(project_name: str) -> str:
    """Get RL agent template."""
    return f'''"""
{project_name} - RL-Optimized Agent
Created with Az-Core CLI
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from azcore.agents.react_agent import ReactAgent
from azcore.rl.rl_manager import RLManager
from azcore.core.state import State

# Load environment variables
load_dotenv()


def calculator_tool(query: str) -> str:
    """Simple calculator tool."""
    try:
        result = eval(query)
        return f"Result: {{result}}"
    except Exception as e:
        return f"Error: {{str(e)}}"


def search_tool(query: str) -> str:
    """Simulated search tool."""
    return f"Search results for: {{query}}"


def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"{project_name}")
    print("=" * 60 + "\\n")
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Define tools
    tools = [
        Tool(
            name="calculator",
            func=calculator_tool,
            description="Useful for mathematical calculations"
        ),
        Tool(
            name="search",
            func=search_tool,
            description="Useful for searching information"
        )
    ]
    
    # Initialize RL Manager
    rl_manager = RLManager(
        tools=tools,
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_strategy="epsilon_greedy",
        epsilon=0.2,
        q_table_path="./rl_data/q_table.pkl"
    )
    
    # Create RL-optimized agent
    agent = ReactAgent(
        name="rl_agent",
        llm=llm,
        tools=tools,
        prompt="You are an AI assistant with RL-optimized tool selection."
    )
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("Enter your query: ")
    
    # Use RL Manager to select optimal tools
    print("\\nSelecting optimal tools with RL...\\n")
    selected_tools = rl_manager.select_tools(query, top_n=2)
    print(f"Selected tools: {{[t.name for t in selected_tools]}}\\n")
    
    # Initialize state
    state = State(messages=[{{"role": "user", "content": query}}])
    
    # Run agent
    print("Processing...\\n")
    result = agent.invoke(state)
    
    # Update RL with reward (placeholder - implement your reward logic)
    reward = 1.0 if result.get("messages") else 0.0
    rl_manager.update(query, selected_tools, reward)
    
    # Save Q-table
    rl_manager.save_q_table()
    
    # Display result
    print("\\nResult:")
    print("-" * 60)
    if result.get("messages"):
        last_message = result["messages"][-1]
        print(last_message.content if hasattr(last_message, 'content') else str(last_message))
    print("-" * 60)
    print(f"\\nRL Stats: {{rl_manager.get_stats()}}")


if __name__ == "__main__":
    main()
'''
