"""
Advanced Az-Core Implementation with Plan Validation and Adaptive Replanning

This demonstrates:
1. Using CoordinatorNode for basic coordination
2. Using PlannerNode for task planning
3. Using PlanValidatorNode to check plan feasibility
4. Using AdaptiveReplannerNode for error recovery
5. Smart routing based on validation results

Flow:
User Request → Coordinator → Planner → Validator 
                                          ↓
                            ┌─────────────┴──────────────┐
                            ↓                            ↓
                     [Valid: Supervisor]    [Invalid: Replanner → Supervisor]
                            ↓
                        Teams → Response Generator

Author: Az-Core Framework
Date: 2025-10-27
"""

from azcore.config import load_config
from azcore.agents.team_builder import TeamBuilder
from azcore.agents.mcp_team_builder import MCPTeamBuilder
from azcore.core.orchestrator import GraphOrchestrator
from azcore.core.supervisor import MainSupervisor
from azcore.nodes import (
    CoordinatorNode,
    PlannerNode,
    ResponseGeneratorNode,
    AdvancedPlannerNode,
    PlanValidatorNode,
    AdaptiveReplannerNode,
    create_advanced_planner,
    create_plan_validator,
    create_adaptive_replanner,
    PlanComplexity,
)
from azcore.rl import RLManager, ToolUsageRewardCalculator
from langchain_core.tools import tool
from langgraph.types import Command
import logging
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# CAMERA TOOLS
# ============================================================================

cams = {
    "main entrance": "http://122.255.33.126:36589/view_nav/cam1",
    "office room": "http://122.255.33.126:36589/view_nav/cam2",
    "office room 2": "http://122.255.33.126:36589/view_nav/cam8",
    "kitchen": "http://122.255.33.126:36589/view_nav/cam3?q=high",
    "store room": "http://122.255.33.126:36589/view_nav/cam13",
    "parking lot": "http://122.255.33.126:36589/view_nav/cam5",
    "workshop": "http://122.255.33.126:36589/view_nav/cam4",
    "lobby": "http://122.255.33.126:36589/view_nav/cam10",
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
    requested_cam = cams.get(location)
    if not requested_cam:
        return f"No camera found at {location}"
    
    cam_feed = cams.get(location)
    if cam_feed:
        return f"Fetched feed from {location}: {cam_feed}"
    else:
        return f"Could not fetch feed from {location}"


# ============================================================================
# DOCUMENT MANAGEMENT TOOLS (Simplified for demonstration)
# ============================================================================

documents_store = {}  # In-memory store for demo


@tool
def add_document(file_path: str, category: str) -> Dict[str, Any]:
    """Add a document to the system with a category.
    
    Args:
        file_path: Path to the document file
        category: Category to classify the document under
        
    Returns:
        Dict with status and document info
    """
    try:
        doc_id = f"doc_{len(documents_store) + 1}"
        documents_store[doc_id] = {
            "filename": file_path,
            "category": category,
            "content": f"Sample content from {file_path}"
        }
        return {
            "status": "success",
            "document_id": doc_id,
            "filename": file_path,
            "category": category
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def get_uploaded_file_list() -> Dict[str, Any]:
    """Get a list of all uploaded documents.
    
    Returns:
        Dict containing status and list of files
    """
    try:
        files = [
            {"id": doc_id, "filename": doc["filename"], "category": doc["category"]}
            for doc_id, doc in documents_store.items()
        ]
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def get_uploaded_file_content(file_name: str) -> Dict[str, Any]:
    """Retrieve the content of an uploaded file.
    
    Args:
        file_name: Name of the file to retrieve
        
    Returns:
        Dict containing status and file content
    """
    try:
        for doc_id, doc in documents_store.items():
            if doc["filename"] == file_name:
                return {"status": "success", "content": doc["content"]}
        return {"status": "error", "message": "File not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def delete_document(file_name: str) -> Dict[str, Any]:
    """Delete a document from the system.
    
    Args:
        file_name: Name of the file to delete
        
    Returns:
        Dict with status message
    """
    try:
        for doc_id, doc in list(documents_store.items()):
            if doc["filename"] == file_name:
                del documents_store[doc_id]
                return {"status": "success", "message": "File deleted"}
        return {"status": "error", "message": "File not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def get_list_of_categories() -> Dict[str, Any]:
    """Get a list of unique document categories.
    
    Returns:
        Dict containing status and list of categories
    """
    try:
        categories = list(set(doc["category"] for doc in documents_store.values()))
        return {"status": "success", "categories": categories}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def get_files_by_category(category: str) -> Dict[str, Any]:
    """Get all files in a specific category.
    
    Args:
        category: Category to filter by
        
    Returns:
        Dict containing status and list of files
    """
    try:
        files = [
            {"id": doc_id, "filename": doc["filename"]}
            for doc_id, doc in documents_store.items()
            if doc["category"] == category
        ]
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# WATER MANAGEMENT TOOLS (Simplified for demonstration)
# ============================================================================

water_systems = {
    "tank_1": {"level": 75, "capacity": 1000, "location": "North Wing"},
    "tank_2": {"level": 45, "capacity": 800, "location": "South Wing"},
    "pump_1": {"status": "active", "flow_rate": 50},
    "pump_2": {"status": "inactive", "flow_rate": 0},
}


@tool
def get_water_tank_status(tank_id: str) -> Dict[str, Any]:
    """Get the status of a water tank.
    
    Args:
        tank_id: ID of the tank (e.g., tank_1, tank_2)
        
    Returns:
        Dict with tank status information
    """
    try:
        if tank_id in water_systems:
            return {"status": "success", "tank_data": water_systems[tank_id]}
        return {"status": "error", "message": "Tank not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def control_pump(pump_id: str, action: str) -> Dict[str, Any]:
    """Control a water pump (start/stop).
    
    Args:
        pump_id: ID of the pump (e.g., pump_1, pump_2)
        action: Action to perform ('start' or 'stop')
        
    Returns:
        Dict with operation status
    """
    try:
        if pump_id not in water_systems:
            return {"status": "error", "message": "Pump not found"}
        
        if action == "start":
            water_systems[pump_id]["status"] = "active"
            water_systems[pump_id]["flow_rate"] = 50
            return {"status": "success", "message": f"{pump_id} started"}
        elif action == "stop":
            water_systems[pump_id]["status"] = "inactive"
            water_systems[pump_id]["flow_rate"] = 0
            return {"status": "success", "message": f"{pump_id} stopped"}
        else:
            return {"status": "error", "message": "Invalid action"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def get_all_water_systems() -> Dict[str, Any]:
    """Get status of all water management systems.
    
    Returns:
        Dict with all system statuses
    """
    try:
        return {"status": "success", "systems": water_systems}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# INTELLIGENT COORDINATOR WITH COMPLEXITY DETECTION
# ============================================================================

# SmartCoordinatorNode removed - using simple CoordinatorNode instead


# ============================================================================
# BUILD GRAPH WITH ADVANCED PLANNING
# ============================================================================

def build_advanced_graph() -> Dict[str, Any]:
    """Build graph with intelligent planning strategy selection."""
    
    logger.info("\n" + "=" * 80)
    logger.info("🚀 INITIALIZING ADVANCED AZ-CORE SYSTEM")
    logger.info("=" * 80)
    
    # Load configuration
    logger.info("\n📋 Loading configuration...")
    config = load_config("config.yml")
    llm = config.get_llm()
    response_generator_llm = config.get_llm("response_generator_llm")
    logger.info("✓ Configuration loaded")
    
    # ========================================================================
    # SETUP RL MANAGERS
    # ========================================================================
    
    logger.info("\n🧠 Setting up RL managers...")
    
    cam_tools = [get_all_cams, get_feed_from_cam]
    cam_rl = RLManager(
        tool_names=[t.name for t in cam_tools],
        q_table_path="rl_data/cam_q_table.pkl",
        exploration_rate=0.2,
        use_embeddings=False
    )
    cam_reward = ToolUsageRewardCalculator(
        correct_tool_reward=1.0,
        wrong_tool_penalty=-0.8,
        partial_match_reward=0.3,
        no_tool_penalty=-0.5
    )
    
    document_tools = [
        add_document, get_uploaded_file_list, get_uploaded_file_content,
        delete_document, get_list_of_categories, get_files_by_category
    ]
    document_rl = RLManager(
        tool_names=[t.name for t in document_tools],
        q_table_path="rl_data/document_q_table.pkl",
        exploration_rate=0.2,
        use_embeddings=False
    )
    document_reward = ToolUsageRewardCalculator(
        correct_tool_reward=1.0,
        wrong_tool_penalty=-0.8,
        partial_match_reward=0.3,
        no_tool_penalty=-0.5
    )
    
    water_tools = [get_water_tank_status, control_pump, get_all_water_systems]
    water_rl = RLManager(
        tool_names=[t.name for t in water_tools],
        q_table_path="rl_data/water_q_table.pkl",
        exploration_rate=0.2,
        use_embeddings=False
    )
    water_reward = ToolUsageRewardCalculator(
        correct_tool_reward=1.0,
        wrong_tool_penalty=-0.8,
        partial_match_reward=0.3,
        no_tool_penalty=-0.5
    )
    
    logger.info("✓ RL managers created for all teams")
    
    # ========================================================================
    # CREATE RL-ENABLED TEAMS
    # ========================================================================
    
    logger.info("\n👥 Creating specialized teams...")
    
    security_cam_team = (TeamBuilder("security_cam_team")
        .with_llm(llm)
        .with_tools(cam_tools)
        .with_prompt(
            "You are a security camera specialist. Use the appropriate camera tool. "
            "When providing the footages, if no footage is found in the specific place, "
            "say you don't have the footage. Do not provide suggestions, only perform "
            "the assigned task and provide the information."
        )
        .with_rl(cam_rl, cam_reward)
        .with_description("Security camera management with RL-optimized tool selection")
    )
    logger.info("  ✓ Security camera team (with RL)")
    
    document_team = (TeamBuilder("document_and_data_management_team")
        .with_llm(llm)
        .with_tools(document_tools)
        .with_prompt(
            "You are a document management specialist. You're responsible for uploading "
            "documents, keeping records of processed documents and their categories. "
            "Always call a tool when needed. Do not provide suggestions, only perform "
            "the assigned task and provide information. When displaying info about docs, "
            "make sure to display them by categories if the category is available."
        )
        .with_rl(document_rl, document_reward)
        .with_description("Document loading and management with RL")
    )
    logger.info("  ✓ Document management team (with RL)")
    
    water_management_team = (TeamBuilder("water_management_team")
        .with_llm(llm)
        .with_tools(water_tools)
        .with_prompt(
            "You are a water management specialist. Use the available tools to help "
            "with water management tasks. Monitor tank levels, control pumps, and "
            "provide system status. Do not provide suggestions, only perform the "
            "assigned task and provide information."
        )
        .with_rl(water_rl, water_reward)
        .with_description("Water management with RL-optimized operations")
    )
    logger.info("  ✓ Water management team (with RL)")
    
    # ========================================================================
    # CREATE PLANNING NODES
    # ========================================================================
    
    logger.info("\n🧩 Creating planning nodes...")
    
    # Simple coordinator
    coordinator = CoordinatorNode(llm=llm)
    logger.info("  ✓ Coordinator")
    
    # Create a custom planner that routes to validator
    class ValidatedPlannerNode(PlannerNode):
        """Planner that routes to validator instead of directly to supervisor."""
        
        def execute(self, state: Dict[str, Any]):
            """Execute planning and route to validator."""
            result = super().execute(state)
            # Change routing to go to validator first
            if hasattr(result, 'goto') and result.goto == "supervisor":
                return Command(update=result.update, goto="plan_validator")
            return result
    
    # Simple planner that routes to validator
    simple_planner = ValidatedPlannerNode(
        llm=llm,
        system_prompt=f"""You are a task planner for a facility management system.

Available Teams:
- water_management_team: Handles water tanks, pumps, and water systems
- security_cam_team: Manages security cameras and footage
- document_and_data_management_team: Manages documents and file operations

Tools by Team:
- Water Management: {[t.name for t in water_tools]}
- Security Cameras: {[t.name for t in cam_tools]}
- Document Management: {[t.name for t in document_tools]}

Create a simple, direct plan for the task. Keep it concise."""
    )
    logger.info("  ✓ Planner (with validator routing)")
    
    # Advanced planner for complex multi-step tasks (not used in simple flow but available)
    advanced_planner = create_advanced_planner(
        llm=llm,
        validate_plans=False,  # We'll use separate validator
        max_complexity=PlanComplexity.VERY_COMPLEX,
        name="advanced_planner"
    )
    logger.info("  ✓ Advanced Planner (available for future use)")
    
    # Create custom validator that routes to replanner on failure
    class SmartValidatorNode(PlanValidatorNode):
        """Validator that routes to replanner on validation failure."""
        
        def execute(self, state: Dict[str, Any]):
            """Execute validation and route based on result."""
            result = super().execute(state)
            
            # Check if validation failed
            if hasattr(result, 'update') and result.update:
                validation_report = result.update.get("validation_report")
                if validation_report and not validation_report.is_valid:
                    # Route to replanner on validation failure
                    logger.info("🔄 Plan validation failed, routing to adaptive replanner")
                    return Command(update=result.update, goto="adaptive_replanner")
                else:
                    # Route to supervisor on success
                    logger.info("✅ Plan validation passed, routing to supervisor")
                    return Command(update=result.update, goto="supervisor")
            
            return result
    
    # Plan validator to check feasibility
    plan_validator = SmartValidatorNode(
        llm=llm,
        strict_mode=False,  # Allow warnings
        auto_fix=True,      # Attempt to fix issues
        name="plan_validator"
    )
    logger.info("  ✓ Plan Validator (with smart routing)")
    
    # Create custom replanner that routes back to supervisor after replanning
    class SupervisorReplannerNode(AdaptiveReplannerNode):
        """Replanner that routes to supervisor after creating new plan."""
        
        def execute(self, state: Dict[str, Any]):
            """Execute replanning and route to supervisor."""
            result = super().execute(state)
            
            # Always route to supervisor after replanning
            if hasattr(result, 'update'):
                logger.info("🔄 Replanning complete, routing to supervisor for execution")
                return Command(update=result.update, goto="supervisor")
            
            return result
    
    # Adaptive replanner for error recovery
    adaptive_replanner = SupervisorReplannerNode(
        llm=llm,
        name="adaptive_replanner"
    )
    logger.info("  ✓ Adaptive Replanner (with supervisor routing)")
    
    # Response generator
    response_generator = ResponseGeneratorNode(llm=response_generator_llm)
    logger.info("  ✓ Response Generator")
    
    # ========================================================================
    # CREATE SUPERVISOR
    # ========================================================================
    
    logger.info("\n🎯 Creating supervisor...")
    supervisor = MainSupervisor(
        llm=llm,
        members=[
            "water_management_team",
            "security_cam_team",
            "document_and_data_management_team"
        ],
    )
    logger.info("✓ Supervisor configured with 3 teams")
    
    # ========================================================================
    # BUILD GRAPH WITH VALIDATOR AND REPLANNER
    # ========================================================================
    
    logger.info("\n🔧 Building hierarchical graph with validation and replanning...")
    
    orchestrator = GraphOrchestrator()
    
    # Add all nodes
    orchestrator.add_node("coordinator", coordinator)
    orchestrator.add_node("planner", simple_planner)
    orchestrator.add_node("plan_validator", plan_validator)
    orchestrator.add_node("adaptive_replanner", adaptive_replanner)
    orchestrator.add_node("response_generator", response_generator)
    
    # Add supervisor and teams
    orchestrator.set_supervisor(supervisor)
    for team in [water_management_team, security_cam_team, document_team]:
        orchestrator.add_team(team)
    
    # Set entry point
    orchestrator.set_entry_point("coordinator")
    
    logger.info("  ✓ Graph with validator and replanner created")
    logger.info("  ✓ Plan validation enabled")
    logger.info("  ✓ Adaptive replanning enabled")
    
    # Compile the graph
    graph = orchestrator.compile()
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ ADVANCED AZ-CORE SYSTEM READY")
    logger.info("=" * 80)
    
    return {
        "graph": graph,
        "advanced_planner": advanced_planner,
        "plan_validator": plan_validator,
        "adaptive_replanner": adaptive_replanner,
        "teams": [water_management_team, security_cam_team, document_team]
    }


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demonstrate_simple_task():
    """Demonstrate simple task with basic planner."""
    logger.info("\n" + "=" * 80)
    logger.info("DEMO 1: SIMPLE TASK (Basic Planner)")
    logger.info("=" * 80)
    logger.info("\nTask: Get the status of water tank 1")
    logger.info("Expected: Routes to simple planner → direct execution")


def demonstrate_complex_task():
    """Demonstrate complex task with advanced planner."""
    logger.info("\n" + "=" * 80)
    logger.info("DEMO 2: COMPLEX TASK (Advanced Planner)")
    logger.info("=" * 80)
    logger.info("\nTask: Setup complete monitoring system for all tanks and cameras")
    logger.info("Expected: Routes to advanced planner → multi-step plan → validation")


def demonstrate_adaptive_replanning():
    """Demonstrate error recovery with adaptive replanner."""
    logger.info("\n" + "=" * 80)
    logger.info("DEMO 3: ERROR RECOVERY (Adaptive Replanner)")
    logger.info("=" * 80)
    logger.info("\nTask: Migration with simulated failure")
    logger.info("Expected: Detects failure → triggers replanning → recovery")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    try:
        logger.info("\n🎬 STARTING ADVANCED AZ-CORE DEMONSTRATION\n")
        
        # Build the advanced system
        system = build_advanced_graph()
        
        logger.info("\n📚 SYSTEM CAPABILITIES:")
        logger.info("  • Intelligent complexity detection")
        logger.info("  • Automatic planner selection (simple vs advanced)")
        logger.info("  • Multi-step plan validation")
        logger.info("  • Error detection and adaptive replanning")
        logger.info("  • RL-optimized tool selection")
        logger.info("  • Hierarchical team coordination")
        
        # Show demonstrations
        logger.info("\n" + "=" * 80)
        logger.info("DEMONSTRATION SCENARIOS")
        logger.info("=" * 80)
        
        demonstrate_simple_task()
        demonstrate_complex_task()
        demonstrate_adaptive_replanning()
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ SYSTEM INITIALIZATION COMPLETE")
        logger.info("=" * 80)
        logger.info("\n💡 To use this system:")
        logger.info("   1. Simple tasks (get, show, check) → Automatic basic planning")
        logger.info("   2. Complex tasks (setup, migrate, configure) → Advanced planning")
        logger.info("   3. All plans validated for feasibility")
        logger.info("   4. Automatic error recovery with replanning")
        logger.info("   5. RL learns optimal tool usage over time")
        
        return system
        
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    system = main()
    logger.info("\n🎉 System ready for use!")
