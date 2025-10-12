"""
RL Test: Using TeamBuilder with built-in RL support

This demonstrates the NEW simplified API where TeamBuilder directly
supports RL without needing custom wrapper classes.

Author: Rise Framework
Date: 2025
"""

from rise_framework.config import load_config
from rise_framework.agents.team_builder import TeamBuilder
from rise_framework.core.orchestrator import GraphOrchestrator
from rise_framework.core.supervisor import MainSupervisor
from rise_framework.nodes import ResponseGeneratorNode, PlannerNode, CoordinatorNode
from rise_framework.rl import RLManager, HeuristicRewardCalculator
from rise_framework.agents import MCPTeamBuilder
from langchain_core.tools import tool
import logging
import asyncio
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


tool_data = []




cams = {
    "main entrance": "http://122.255.33.126:36589/view_nav/cam1",
    "office room": "http://122.255.33.126:36589/view_nav/cam2",
    "office room 2": "http://122.255.33.126:36589/view_nav/cam8",
    "kitchen": "http://122.255.33.126:36589/view_nav/cam3?q=high",
    "store room": "http://122.255.33.126:36589/view_nav/cam13",
    "parking lot": "http://122.255.33.126:36589/view_nav/cam5",
    "workshop": "http://122.255.33.126:36589/view_nav/cam4",
    "lobby" : "http://122.255.33.126:36589/view_nav/cam10",
    "workshop":"http://122.255.33.126:36589/view_nav/cam4"    
}

@tool
def get_all_cams() -> str:
    """Returns a string containing all the camera locations separated by commas.

    Returns:
        str: A string containing all the camera locations separated by commas.
    """
    return ", ".join(cams.keys())


@tool
def get_feed_from_cam(location: str) -> str:
    """Fetches a feed from a given camera location and returns the feed content.

    Args:
        location (str): The location of the camera (e.g. main entrance, office room)

    Returns:
        str: The feed content from the camera at the specified location.
    """
    tool_data.clear()

    requested_cam = cams.get(location)
    if not requested_cam:
        return f"No camera found at {location}"
    
    cam_feed = cams.get(location)
    
    if cam_feed:
        tool_data.append(cam_feed)
        return f"Fetched feed from {location}: {cam_feed}"
    else:
        return f"Could not fetch feed from {location}"





def main():
    """Run RL-enabled hierarchical graph with simplified API.
    """
    # Load configuration
    logger.info("\nLoading configuration...")
    config = load_config("config.yml")
    llm = config.get_llm()
    

    logger.info("\nSetting up RL managers...")



    cam_tools = [get_all_cams, get_feed_from_cam]
    cam_rl = RLManager(
        tool_names=[t.name for t in cam_tools],
        q_table_path="rl_data/cam_q_table.pkl",
        exploration_rate=0.2,
        use_embeddings=False
    )
    cam_reward = HeuristicRewardCalculator()
    

    
    logger.info("✓ RL managers created")
    

    logger.info("\nCreating RL-enabled teams with TeamBuilder...")

    security_cam_team = (TeamBuilder("security_cam_team")
        .with_llm(llm)
        .with_tools(cam_tools)
        .with_prompt("You are a security camera specialist. Use the appropriate camera tool.  do not provide any suggestions only perform the task that you assinged and provide the infroamtion ")
        .with_rl(cam_rl, cam_reward)  
        .with_description("Security camera management with RL-optimized tool selection")
    )

    wms_team = (MCPTeamBuilder("water_management_team")
        .with_llm(llm)
        .with_mcp_server(
            url="http://16.171.152.178:8000/sse",
            transport="sse",
            timeout=120,  # 2 minutes - SSE connections need longer timeouts
            sse_read_timeout=300  # 5 minutes for reading from SSE stream
        )
        .with_prompt(
            "You are a water management specialist. "
            "Use the available WMS tools to help with water management tasks. do not provide any suggestions only perform the task that you assinged and provide the infroamtion "
        )
        .with_description("Water Management Team")
    )
    logger.info("✓ Security camera team created with RL")
    
    # Get MCP tools directly from the builder - no need for manual client setup!
    logger.info("Fetching MCP tools from WMS server...")
    wms_tools = wms_team.get_mcp_tools()
    

    logger.info("\nBuilding hierarchical graph...")
    
    supervisor = MainSupervisor(
        llm=llm,
        members=["water_management_team", "security_cam_team"]
    )
    
    orchestrator = GraphOrchestrator()
    
    # Get tool names for planner prompt
    wms_tool_names = [t.name for t in wms_tools]
    cam_tool_names = [t.name for t in cam_tools]
    
    graph = orchestrator.build_hierarchical_graph(
        coordinator=CoordinatorNode(llm=llm),
        planner=PlannerNode(llm=llm, system_prompt=f"7. you've water_management_team and a security_cam_team only and these teams don't intercorrelate water system tools {wms_tool_names} security camera realted tools  {cam_tool_names}"),
        supervisor=supervisor,
        teams=[wms_team, security_cam_team],  # RL-enabled teams work seamlessly!
        generator=ResponseGeneratorNode(llm=llm)
    )
    
    logger.info("✓ Graph built successfully with RL-enabled teams")
    

    logger.info("\nRunning test queries...")
    logger.info("=" * 80)
    
    test_queries = [
        "Get me all the cam feeds please",
        "Get me all the water levels at the rise please "
    ]
    
    configure = {"configurable": {"thread_id": "rl_simple_test"}}
    
    for i, query in enumerate(test_queries, 1):
        logger.info(f"\nQuery {i}: {query}")
        logger.info("-" * 80)
        
        try:
            result = graph.invoke({"messages": [("user", query)]}, configure)
            
            if result and "messages" in result:
                response = result["messages"][-1].content
                logger.info(f"Response: {response}")
            
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
        
        logger.info("")
    

    logger.info("\n" + "=" * 80)
    logger.info("RL Statistics:")
    logger.info("=" * 80)
    
    logger.info("\nMath Team RL:")
    
    
    logger.info("\nSecurity Cam Team RL:")
    for key, value in cam_rl.get_statistics().items():
        logger.info(f"  {key}: {value}")
    


    # Export Q-tables
    logger.info("\nExporting Q-tables...")
    try:
       
        cam_rl.export_readable("rl_data/cam_q_table_readable.txt")
        logger.info("✓ Q-tables exported")
    except Exception as e:
        logger.error(f"Export failed: {e}")
    



if __name__ == "__main__":
    main()
