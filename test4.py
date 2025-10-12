"""
MCP Integration Test: Using MCPTeamBuilder with MainSupervisor

This demonstrates how to integrate Model Context Protocol (MCP) servers
with the Arc Framework using the new MCPTeamBuilder class.

Features Demonstrated:
- Connecting to MCP servers
- Automatic tool discovery and conversion
- Integration with MainSupervisor
- Optional RL for MCP tool selection
- Hierarchical graph with MCP-enabled teams

Author: Arc Framework
Date: 2025
"""

from arc.config import load_config
from arc.agents.mcp_team_builder import MCPTeamBuilder
from arc.agents.team_builder import TeamBuilder
from arc.core.orchestrator import GraphOrchestrator
from arc.core.supervisor import MainSupervisor
from arc.nodes import ResponseGeneratorNode, PlannerNode, CoordinatorNode
from arc.rl import RLManager, HeuristicRewardCalculator
from langchain_core.tools import tool
import logging
from dotenv import load_dotenv

load_dotenv()  # This is correct - calling the function
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# SECTION 1: Define Regular (Non-MCP) Tools
# =============================================================================

@tool
def calculate_sum(numbers: str) -> str:
    """Calculate the sum of comma-separated numbers."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        return f"The sum is {sum(nums)}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def format_as_report(title_and_content: str) -> str:
    """Format content as a report. Format: 'title|content'."""
    try:
        parts = title_and_content.split('|', 1)
        if len(parts) != 2:
            return "Error: Use format 'title|content'"
        title, content = parts
        return f"\n=== {title.upper()} ===\n\n{content}\n\n" + "="*50
    except Exception as e:
        return f"Error: {str(e)}"


# =============================================================================
# SECTION 2: Setup MCP Team (Example Configurations)
# =============================================================================

def create_mcp_team_basic(llm):
    """
    Create a basic MCP team without RL.
    
    This example shows how to connect to a single MCP server.
    Replace the server path with your actual MCP server.
    
    Args:
        llm: Language model for the team
        
    Returns:
        MCPTeamBuilder instance
    """
    logger.info("\n" + "=" * 80)
    logger.info("Creating Basic MCP Team...")
    logger.info("=" * 80)
    
    # Example: Connect to a Python-based MCP server
    # Replace "path/to/your/mcp_server.py" with actual server path
    mcp_team = (MCPTeamBuilder("mcp_research_team")
        .with_llm(llm)
        .with_mcp_server(
            command="python",
            args=["path/to/your/mcp_server.py"]
        )
        .with_prompt(
            "You are a research assistant with access to MCP tools. "
            "Use the appropriate MCP tools to gather information and complete tasks."
        )
        .with_description("Research team with MCP server capabilities")
    )
    
    logger.info("✓ Basic MCP team configured (not yet built)")
    return mcp_team


def create_mcp_team_with_rl(llm):
    """
    Create an MCP team with RL-enabled tool selection.
    
    This example shows how to add RL to optimize MCP tool selection.
    
    Args:
        llm: Language model for the team
        
    Returns:
        MCPTeamBuilder instance
    """
    logger.info("\n" + "=" * 80)
    logger.info("Creating RL-Enabled MCP Team...")
    logger.info("=" * 80)
    
    # Setup RL for MCP tools
    # Note: Tool names will be auto-discovered from MCP server
    # You can configure RL with expected tool names or update after discovery
    mcp_rl = RLManager(
        tool_names=[],  # Will be populated after MCP connection
        q_table_path="rl_data/mcp_q_table.pkl",
        exploration_rate=0.2,
        use_embeddings=False
    )
    mcp_reward = HeuristicRewardCalculator()
    
    mcp_team = (MCPTeamBuilder("mcp_research_team")
        .with_llm(llm)
        .with_mcp_server(
            command="python",
            args=["path/to/your/mcp_server.py"]
        )
        .with_rl(mcp_rl, mcp_reward)
        .with_prompt(
            "You are a research assistant with access to MCP tools. "
            "Use RL-optimized tool selection to efficiently complete tasks."
        )
        .with_description("RL-optimized research team with MCP capabilities")
    )
    
    logger.info("✓ RL-enabled MCP team configured")
    return mcp_team


def create_multi_mcp_team(llm):
    """
    Create a team that connects to multiple MCP servers.
    
    This example shows how to aggregate tools from multiple MCP sources.
    
    Args:
        llm: Language model for the team
        
    Returns:
        MCPTeamBuilder instance
    """
    logger.info("\n" + "=" * 80)
    logger.info("Creating Multi-MCP Team...")
    logger.info("=" * 80)
    
    mcp_team = (MCPTeamBuilder("multi_mcp_team")
        .with_llm(llm)
        # Connect to first MCP server
        .with_mcp_server(
            command="python",
            args=["path/to/mcp_server1.py"]
        )
        # Connect to second MCP server (e.g., NPX-based)
        .with_mcp_server(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
        )
        # Connect to third MCP server with environment variables
        .with_mcp_server(
            command="python",
            args=["path/to/mcp_server2.py"],
            env={"API_KEY": "your_api_key_here"}
        )
        .with_prompt(
            "You are an advanced assistant with tools from multiple MCP servers. "
            "Choose the most appropriate tool for each task."
        )
        .with_description("Multi-source MCP team with aggregated capabilities")
    )
    
    logger.info("✓ Multi-MCP team configured")
    return mcp_team


def create_hybrid_mcp_team(llm):
    """
    Create a team with both MCP tools and regular LangChain tools.
    
    This example shows how to combine MCP and non-MCP tools in one team.
    
    Args:
        llm: Language model for the team
        
    Returns:
        MCPTeamBuilder instance
    """
    logger.info("\n" + "=" * 80)
    logger.info("Creating Hybrid MCP Team...")
    logger.info("=" * 80)
    
    # Define regular tools
    regular_tools = [calculate_sum, format_as_report]
    
    mcp_team = (MCPTeamBuilder("hybrid_team")
        .with_llm(llm)
        # Add regular LangChain tools
        .with_tools(regular_tools)
        # Add MCP server
        .with_mcp_server(
            command="python",
            args=["path/to/your/mcp_server.py"]
        )
        .with_prompt(
            "You are a versatile assistant with both standard and MCP tools. "
            "Use standard tools for basic operations and MCP tools for specialized tasks."
        )
        .with_description("Hybrid team combining standard and MCP tools")
    )
    
    logger.info("✓ Hybrid MCP team configured")
    return mcp_team


# =============================================================================
# SECTION 3: Build Hierarchical Graph with MCP Teams
# =============================================================================

def build_mcp_hierarchical_graph(llm, mcp_team, regular_team=None):
    """
    Build a hierarchical graph that includes MCP-enabled teams.
    
    Args:
        llm: Language model
        mcp_team: MCPTeamBuilder instance
        regular_team: Optional regular TeamBuilder instance
        
    Returns:
        Compiled graph
    """
    logger.info("\n" + "=" * 80)
    logger.info("Building Hierarchical Graph with MCP Team...")
    logger.info("=" * 80)
    
    # Prepare team list
    teams = [mcp_team]
    member_names = [mcp_team.name]
    
    if regular_team:
        teams.append(regular_team)
        member_names.append(regular_team.name)
    
    # Create supervisor
    supervisor = MainSupervisor(
        llm=llm,
        members=member_names
    )
    
    # Build graph
    orchestrator = GraphOrchestrator()
    graph = orchestrator.build_hierarchical_graph(
        coordinator=CoordinatorNode(llm=llm),
        planner=PlannerNode(llm=llm),
        supervisor=supervisor,
        teams=teams,
        generator=ResponseGeneratorNode(llm=llm)
    )
    
    logger.info("✓ Hierarchical graph built successfully with MCP team")
    return graph


# =============================================================================
# SECTION 4: Example Main Functions
# =============================================================================

def main_basic_mcp():
    """
    Run basic MCP team example.
    
    This is a simple example showing MCP integration without RL.
    """
    logger.info("\n" + "=" * 80)
    logger.info("BASIC MCP TEAM EXAMPLE")
    logger.info("=" * 80)
    
    # Load configuration
    config = load_config("config.yml")
    llm = config.get_llm()
    
    # Create MCP team
    # NOTE: Replace with your actual MCP server path
    # For now, this will fail if no MCP server is available
    try:
        mcp_team = create_mcp_team_basic(llm)
        
        # Build the graph
        graph = build_mcp_hierarchical_graph(llm, mcp_team)
        
        # Test query
        logger.info("\n" + "=" * 80)
        logger.info("Running Test Query...")
        logger.info("=" * 80)
        
        query = "Use MCP tools to help me research AI frameworks"
        logger.info(f"Query: {query}")
        
        result = graph.invoke(
            {"messages": [("user", query)]},
            {"configurable": {"thread_id": "mcp_basic_test"}}
        )
        
        if result and "messages" in result:
            response = result["messages"][-1].content
            logger.info(f"\nResponse: {response}")
        
    except ImportError as e:
        logger.error(f"MCP not available: {e}")
        logger.info("Install with: pip install langchain-mcp-adapters")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


def main_mcp_with_rl():
    """
    Run MCP team with RL example.
    
    This example shows how to use RL for optimizing MCP tool selection.
    """
    logger.info("\n" + "=" * 80)
    logger.info("MCP TEAM WITH RL EXAMPLE")
    logger.info("=" * 80)
    
    # Load configuration
    config = load_config("config.yml")
    llm = config.get_llm()
    
    try:
        # Create RL-enabled MCP team
        mcp_team = create_mcp_team_with_rl(llm)
        
        # Build the graph
        graph = build_mcp_hierarchical_graph(llm, mcp_team)
        
        # Run test queries
        test_queries = [
            "Research the latest developments in quantum computing",
            "Find information about renewable energy trends",
            "Analyze data science best practices"
        ]
        
        logger.info("\n" + "=" * 80)
        logger.info("Running Test Queries...")
        logger.info("=" * 80)
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"\nQuery {i}: {query}")
            
            try:
                result = graph.invoke(
                    {"messages": [("user", query)]},
                    {"configurable": {"thread_id": f"mcp_rl_test_{i}"}}
                )
                
                if result and "messages" in result:
                    response = result["messages"][-1].content
                    logger.info(f"Response: {response}")
            except Exception as e:
                logger.error(f"Query failed: {e}")
        
        # Display RL statistics
        logger.info("\n" + "=" * 80)
        logger.info("RL Statistics:")
        logger.info("=" * 80)
        # Note: Access RL manager from team if needed
        # mcp_rl.get_statistics()
        
    except ImportError as e:
        logger.error(f"MCP or RL not available: {e}")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


def main_hybrid_example():
    """
    Run hybrid team example (MCP + regular tools).
    
    This example shows how to combine MCP and non-MCP teams.
    """
    logger.info("\n" + "=" * 80)
    logger.info("HYBRID MCP + REGULAR TEAM EXAMPLE")
    logger.info("=" * 80)
    
    # Load configuration
    config = load_config("config.yml")
    llm = config.get_llm()
    
    try:
        # Create MCP team
        mcp_team = create_hybrid_mcp_team(llm)
        
        # Create regular team
        math_team = (TeamBuilder("math_team")
            .with_llm(llm)
            .with_tools([calculate_sum])
            .with_prompt("You are a math specialist. Use calculation tools.")
            .with_description("Handles mathematical operations")
        )
        
        # Build graph with both teams
        teams = [mcp_team, math_team]
        supervisor = MainSupervisor(
            llm=llm,
            members=[t.name for t in teams]
        )
        
        orchestrator = GraphOrchestrator()
        graph = orchestrator.build_hierarchical_graph(
            coordinator=CoordinatorNode(llm=llm),
            planner=PlannerNode(llm=llm),
            supervisor=supervisor,
            teams=teams,
            generator=ResponseGeneratorNode(llm=llm)
        )
        
        # Test queries
        test_queries = [
            "Calculate the sum of 10, 20, 30",  # Should use math_team
            "Research AI frameworks using MCP tools",  # Should use mcp_team
        ]
        
        logger.info("\n" + "=" * 80)
        logger.info("Running Test Queries...")
        logger.info("=" * 80)
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"\nQuery {i}: {query}")
            
            try:
                result = graph.invoke(
                    {"messages": [("user", query)]},
                    {"configurable": {"thread_id": f"hybrid_test_{i}"}}
                )
                
                if result and "messages" in result:
                    response = result["messages"][-1].content
                    logger.info(f"Response: {response}")
            except Exception as e:
                logger.error(f"Query failed: {e}")
        
    except ImportError as e:
        logger.error(f"MCP not available: {e}")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


# =============================================================================
# SECTION 5: Information and Setup Guide
# =============================================================================

def print_mcp_setup_guide():
    """Print a guide for setting up MCP servers."""
    guide = """
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                     MCP TEAM BUILDER SETUP GUIDE                       ║
    ╚════════════════════════════════════════════════════════════════════════╝
    
    📦 INSTALLATION:
    ---------------
    pip install langchain-mcp-adapters
    
    
    🔧 CREATING AN MCP SERVER:
    -------------------------
    1. Create a Python file (e.g., my_mcp_server.py)
    2. Implement MCP server protocol
    3. Define tools/resources your server provides
    
    Example server structure:
        from mcp.server import Server
        from mcp.types import Tool
        
        server = Server("my-server")
        
        @server.tool()
        def my_tool(param: str) -> str:
            return f"Processed: {param}"
    
    
    🚀 USING MCP WITH Arc Framework:
    ---------------------------------
    
    # Basic MCP Team
    mcp_team = (MCPTeamBuilder("mcp_team")
        .with_llm(llm)
        .with_mcp_server("python", ["path/to/server.py"])
        .build())
    
    # MCP Team with RL
    mcp_team = (MCPTeamBuilder("mcp_team")
        .with_llm(llm)
        .with_mcp_server("python", ["server.py"])
        .with_rl(rl_manager, reward_calc)
        .build())
    
    # Multiple MCP Servers
    mcp_team = (MCPTeamBuilder("mcp_team")
        .with_llm(llm)
        .with_mcp_server("python", ["server1.py"])
        .with_mcp_server("npx", ["-y", "@modelcontextprotocol/server-filesystem"])
        .build())
    
    
    🔗 INTEGRATION WITH MAINSUPERVISOR:
    -----------------------------------
    supervisor = MainSupervisor(llm=llm, members=["mcp_team"])
    
    orchestrator = GraphOrchestrator()
    graph = orchestrator.build_hierarchical_graph(
        coordinator=CoordinatorNode(llm=llm),
        planner=PlannerNode(llm=llm),
        supervisor=supervisor,
        teams=[mcp_team],
        generator=ResponseGeneratorNode(llm=llm)
    )
    
    
    📚 AVAILABLE MCP SERVERS:
    ------------------------
    - @modelcontextprotocol/server-filesystem
    - @modelcontextprotocol/server-github
    - @modelcontextprotocol/server-postgres
    - Custom Python MCP servers
    
    
    💡 TIPS:
    -------
    - Test MCP servers independently before integration
    - Use RL for teams with many MCP tools
    - Combine MCP and regular tools in hybrid teams
    - Monitor MCP server logs for debugging
    
    ╚════════════════════════════════════════════════════════════════════════╝
    """
    print(guide)


if __name__ == "__main__":
    import sys
    
    # Print setup guide
    print_mcp_setup_guide()
    
    logger.info("\n" + "=" * 80)
    logger.info("SELECT EXAMPLE TO RUN:")
    logger.info("=" * 80)
    logger.info("1. Basic MCP Team (main_basic_mcp)")
    logger.info("2. MCP Team with RL (main_mcp_with_rl)")
    logger.info("3. Hybrid MCP + Regular Team (main_hybrid_example)")
    logger.info("=" * 80)
    
    # Run examples
    # Uncomment the example you want to run:
    
    # main_basic_mcp()
    # main_mcp_with_rl()
    # main_hybrid_example()
    
    logger.info("\n⚠️  NOTE: Uncomment the example function you want to run")
    logger.info("⚠️  Make sure to replace 'path/to/your/mcp_server.py' with actual MCP server path")
    logger.info("⚠️  Install MCP support: pip install langchain-mcp-adapters\n")
