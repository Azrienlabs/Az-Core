"""
Test 13: AgentPatternRouter - Dynamic Pattern Selection

This test demonstrates the AgentPatternRouter which provides a unified interface
for selecting and using different agent patterns dynamically.
"""

import os
from langchain_openai import ChatOpenAI
from rise_framework.agents.agent_pattern_router import AgentPatternRouter, create_agent


def test_self_consistency_pattern():
    """Test using self-consistency pattern through router."""
    print("\n" + "="*80)
    print("TEST 13.1: Self-Consistency Pattern via Router")
    print("="*80)
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create router with self-consistency pattern
    router = AgentPatternRouter(
        pattern="self-consistency",
        name="consensus-router",
        llm=llm,
        num_samples=3
    )
    
    question = "What are the key benefits of containerization in software development?"
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print(f"\nPattern: self-consistency")
    print(f"Question: {question}")
    print("\nExecuting through pattern router...")
    
    # Invoke router
    result = router.invoke(state)
    
    print(f"\nSamples generated: {len(result.get('responses', []))}")
    print("\nConsensus result:")
    print(result["messages"][-1]["content"][:300] + "...")
    
    return result


def test_reflexion_pattern():
    """Test using reflexion pattern through router."""
    print("\n" + "="*80)
    print("TEST 13.2: Reflexion Pattern via Router")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create router with reflexion pattern
    router = AgentPatternRouter(
        pattern="reflexion",
        name="reflexion-router",
        llm=llm,
        max_loops=2
    )
    
    task = "Write a Python function to calculate the Fibonacci sequence up to n terms."
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print(f"\nPattern: reflexion")
    print(f"Task: {task}")
    print("\nExecuting with iterative improvement...")
    
    result = router.invoke(state)
    
    print(f"\nIterations completed: {len(result.get('iterations', []))}")
    print(f"Best score: {result.get('best_score', 'N/A'):.2f}")
    print("\nFinal result:")
    print(result["messages"][-1]["content"][:300] + "...")
    
    return result


def test_reasoning_duo_pattern():
    """Test using reasoning-duo pattern through router."""
    print("\n" + "="*80)
    print("TEST 13.3: Reasoning-Duo Pattern via Router")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create router with reasoning-duo pattern
    router = AgentPatternRouter(
        pattern="reasoning-duo",
        name="reasoning-router",
        llm=llm,
        max_loops=1
    )
    
    problem = """
    A rectangular garden is 12 meters long and 8 meters wide.
    If you want to put a fence around it, how many meters of fence do you need?
    """
    
    state = {
        "messages": [
            {"role": "user", "content": problem}
        ]
    }
    
    print(f"\nPattern: reasoning-duo")
    print(f"Problem: {problem.strip()}")
    print("\nExecuting two-stage reasoning...")
    
    result = router.invoke(state)
    
    print("\nReasoning process:")
    if "conversation" in result:
        for entry in result["conversation"]:
            print(f"\n{entry['role'].upper()}:")
            print(entry["content"][:200] + "..." if len(entry["content"]) > 200 else entry["content"])
    
    return result


def test_agent_judge_pattern():
    """Test using agent-judge pattern through router."""
    print("\n" + "="*80)
    print("TEST 13.4: Agent-Judge Pattern via Router")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create router with agent-judge pattern
    router = AgentPatternRouter(
        pattern="agent-judge",
        name="judge-router",
        llm=llm,
        evaluation_criteria={
            "quality": 0.5,
            "completeness": 0.5
        }
    )
    
    content = """
    Microservices architecture breaks down applications into small, independent services.
    Each service handles a specific business function. This approach offers better scalability.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": f"Evaluate this explanation:\n\n{content}"}
        ]
    }
    
    print(f"\nPattern: agent-judge")
    print(f"Content to evaluate:")
    print(content.strip())
    print("\nEvaluating...")
    
    result = router.invoke(state)
    
    print("\nEvaluation:")
    print(result["messages"][-1]["content"])
    
    return result


def test_react_pattern():
    """Test using default react pattern through router."""
    print("\n" + "="*80)
    print("TEST 13.5: ReAct Pattern via Router")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create router with react pattern (default)
    router = AgentPatternRouter(
        pattern="react",
        name="react-router",
        llm=llm
    )
    
    question = "What is the difference between a list and a tuple in Python?"
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print(f"\nPattern: react (default)")
    print(f"Question: {question}")
    print("\nExecuting...")
    
    result = router.invoke(state)
    
    print("\nResponse:")
    print(result["messages"][-1]["content"][:300] + "...")
    
    return result


def test_convenience_function():
    """Test using the convenience create_agent function."""
    print("\n" + "="*80)
    print("TEST 13.6: Convenience Function - create_agent()")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create agent directly using convenience function
    agent = create_agent(
        pattern="self-consistency",
        llm=llm,
        num_samples=4
    )
    
    question = "What are the main advantages of using TypeScript over JavaScript?"
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print(f"\nCreated agent with pattern: self-consistency")
    print(f"Question: {question}")
    print("\nExecuting...")
    
    result = agent.invoke(state)
    
    print(f"\nSamples: {len(result.get('responses', []))}")
    print("Result:")
    print(result["messages"][-1]["content"][:250] + "...")
    
    return result


def test_pattern_switching():
    """Test switching between different patterns dynamically."""
    print("\n" + "="*80)
    print("TEST 13.7: Dynamic Pattern Switching")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    patterns_to_test = [
        ("self-consistency", "What is 25% of 80?", {"num_samples": 3}),
        ("reasoning-duo", "If x + 7 = 15, what is x?", {"max_loops": 1}),
        ("reflexion", "Write 'Hello World' in Python", {"max_loops": 1}),
    ]
    
    print(f"\nTesting {len(patterns_to_test)} different patterns...")
    
    results = []
    for pattern_name, question, kwargs in patterns_to_test:
        print(f"\n--- Pattern: {pattern_name} ---")
        print(f"Question: {question}")
        
        # Create router with specific pattern
        router = AgentPatternRouter(
            pattern=pattern_name,
            llm=llm,
            **kwargs
        )
        
        state = {
            "messages": [
                {"role": "user", "content": question}
            ]
        }
        
        result = router.invoke(state)
        
        print("Result:")
        answer = result["messages"][-1]["content"]
        print(answer[:150] + "..." if len(answer) > 150 else answer)
        
        results.append(result)
    
    print(f"\nSuccessfully executed {len(results)} different patterns")
    
    return results


def test_pattern_info():
    """Test getting pattern configuration information."""
    print("\n" + "="*80)
    print("TEST 13.8: Pattern Configuration Info")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create routers with different patterns
    patterns = [
        AgentPatternRouter(pattern="self-consistency", llm=llm, num_samples=5),
        AgentPatternRouter(pattern="reflexion", llm=llm, max_loops=3),
        AgentPatternRouter(pattern="reasoning-duo", llm=llm),
        AgentPatternRouter(pattern="agent-judge", llm=llm),
    ]
    
    print("\nPattern Configuration Details:")
    
    for router in patterns:
        info = router.get_pattern_info()
        print(f"\n--- {info['pattern']} ---")
        print(f"Name: {info['name']}")
        print(f"LLM: {info['llm']}")
        print(f"Config: {info['config']}")
    
    return patterns


def main():
    """Run all AgentPatternRouter tests."""
    print("\n" + "="*80)
    print("AGENT PATTERN ROUTER - COMPREHENSIVE TESTS")
    print("="*80)
    
    try:
        # Run all tests
        test_self_consistency_pattern()
        test_reflexion_pattern()
        test_reasoning_duo_pattern()
        test_agent_judge_pattern()
        test_react_pattern()
        test_convenience_function()
        test_pattern_switching()
        test_pattern_info()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nAgentPatternRouter Capabilities Demonstrated:")
        print("✅ Self-consistency pattern routing")
        print("✅ Reflexion pattern routing")
        print("✅ Reasoning-duo pattern routing")
        print("✅ Agent-judge pattern routing")
        print("✅ ReAct pattern routing")
        print("✅ Convenience function usage")
        print("✅ Dynamic pattern switching")
        print("✅ Pattern configuration inspection")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
