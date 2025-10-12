"""
Simple MCP Usage Example - Direct Comparison

This shows the simplest way to use MCPTeamBuilder,
compared directly with your original code pattern.
"""

from arc.config import load_config
from arc.agents.mcp_team_builder import MCPTeamBuilder
from arc.core.orchestrator import GraphOrchestrator
from arc.core.supervisor import MainSupervisor
from arc.nodes import ResponseGeneratorNode, PlannerNode, CoordinatorNode
from arc.utils.visualization import GraphVisualizer, visualize_orchestrator
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""
Simple example showing how to use MCPTeamBuilder with SSE transport.

This replaces your manual async setup with a clean fluent interface.
"""

# Load configuration
config = load_config("config.yml")
llm = config.get_llm()

# =========================================================================
# STEP 1: Create Water Management Team (replaces your get_wms_tools)
# =========================================================================
logger.info("Creating Water Management MCP Team...")

wms_team = MCPTeamBuilder("water_management_team")\
    .with_llm(llm)\
    .with_mcp_server(
        url="http://16.171.152.178:8000/sse",
        transport="sse",
        timeout=120,  # 2 minutes - SSE connections need longer timeouts
        sse_read_timeout=300  # 5 minutes for reading from SSE stream
    )\
    .with_prompt(
        "You are a water management specialist. "
        "Use the available WMS tools to help with water management tasks."
    )\
    .with_description("Water Management Team")


# =========================================================================
# STEP 2: Build the Graph (replaces your wms_builder setup)
# =========================================================================
logger.info("Building hierarchical graph...")

supervisor = MainSupervisor(
    llm=llm,
    members=["water_management_team"]
)

orchestrator = GraphOrchestrator()
graph = orchestrator.build_hierarchical_graph(
    coordinator=CoordinatorNode(llm=llm),
    planner=PlannerNode(llm=llm),
    supervisor=supervisor,
    teams=[wms_team],
    generator=ResponseGeneratorNode(llm=llm)
)

# =========================================================================
# STEP 3: Run Queries
# =========================================================================
logger.info("Running test query...")

query = "Check the water management system status"

try:
    result = graph.invoke(
        {"messages": [("user", query)]},
        {"configurable": {"thread_id": "wms_test_1"}}
    )
    
    if result and "messages" in result:
        response = result["messages"][-1].content
        logger.info(f"\n{'='*80}")
        logger.info(f"Query: {query}")
        logger.info(f"Response: {response}")
        logger.info(f"{'='*80}\n")

except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)



