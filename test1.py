from rise_framework.config import load_config
from rise_framework.agents.team_builder import TeamBuilder
from rise_framework.core.orchestrator import GraphOrchestrator
from rise_framework.core.supervisor import MainSupervisor
from rise_framework.nodes import ResponseGeneratorNode, PlannerNode, CoordinatorNode
from langchain_core.tools import tool
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple math tool
@tool
def calculate_sum(numbers: str) -> str:
    """Calculate the sum of comma-separated numbers."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        return f"The sum is {sum(nums)}"
    except:
        return "Error: Invalid numbers"

# Simple report tool
@tool
def format_as_report(title: str, content: str) -> str:
    """Format content as a simple report."""
    return f"\n=== {title.upper()} ===\n\n{content}\n\n" + "="*50

# Create agent
logger.info("Loading configuration...")
config = load_config("config.yml")
llm = config.get_llm()

logger.info("Creating teams...")
# Math team
math_team = TeamBuilder("math_team")
math_team.with_llm(llm)
math_team.with_tools([calculate_sum])
math_team.with_prompt("You are a math specialist. Use calculate_sum tool for addition.")
math_team.with_description("Handles math calculations")

# Report team
report_team = TeamBuilder("report_writer_team")
report_team.with_llm(llm)
report_team.with_tools([format_as_report])
report_team.with_prompt("You are a report writer. Use format_as_report to create reports.")
report_team.with_description("Handles report formatting")

# Create supervisor and orchestrator
logger.info("Building graph...")
supervisor = MainSupervisor(llm=llm, members=["math_team", "report_writer_team"])



coordinator = CoordinatorNode(llm=llm)

planner = PlannerNode(llm=llm)

generator = ResponseGeneratorNode(llm=llm)

orchestrator = GraphOrchestrator()


orchestrator.build_hierarchical_graph(
    coordinator=coordinator,
    planner=planner,
    supervisor=supervisor,
    teams=[math_team],
    generator=generator
)

graph = orchestrator.compile()



logger.info("Graph built successfully.")


configure = {
        "configurable": {
            "thread_id": "test_thread_1",
        }
    }


for chunk in graph.stream(
        {"messages": ("user", "2 + 897 - 9")}, configure, stream_mode="values"
    ):
        if chunk["messages"]:
            print(chunk["messages"][-1].content) 

