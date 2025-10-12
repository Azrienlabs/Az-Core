"""
Test 11: ReflexionAgent Pattern - Self-Reflection and Iterative Improvement

This test demonstrates the ReflexionAgent pattern which iteratively improves
responses through self-reflection, evaluation, and refinement.
"""

import os
from langchain_openai import ChatOpenAI
from rise_framework.agents import ReflexionAgent


def test_basic_reflexion():
    """Test basic reflexion with iterative improvement."""
    print("\n" + "="*80)
    print("TEST 11.1: Basic Reflexion and Improvement")
    print("="*80)
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create reflexion agent
    reflexion = ReflexionAgent(
        name="writer",
        llm=llm,
        max_loops=3
    )
    
    # Writing task
    task = "Write a concise explanation of machine learning in 3-4 sentences."
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print(f"\nTask: {task}")
    print(f"\nExecuting reflexion with up to 3 iterations...")
    
    # Invoke reflexion agent
    result = reflexion.invoke(state)
    
    print("\nReflexion Iterations:")
    if "iterations" in result:
        for i, iteration in enumerate(result["iterations"], 1):
            print(f"\n--- Iteration {i} ---")
            print(f"Score: {iteration['score']:.2f}")
            print(f"\nResponse:")
            print(iteration["response"][:200] + "..." if len(iteration["response"]) > 200 else iteration["response"])
            print(f"\nReflection:")
            print(iteration["reflection"][:200] + "..." if len(iteration["reflection"]) > 200 else iteration["reflection"])
    
    print(f"\nBest Score: {result.get('best_score', 'N/A'):.2f}")
    print(f"\nFinal Response:")
    print(result["messages"][-1]["content"])
    
    return result


def test_code_improvement():
    """Test improving code quality through reflexion."""
    print("\n" + "="*80)
    print("TEST 11.2: Code Quality Improvement")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    reflexion = ReflexionAgent(
        name="code-improver",
        llm=llm,
        max_loops=2
    )
    
    # Code improvement task
    task = """
    Write a Python function to check if a string is a palindrome.
    Make it efficient, readable, and well-documented.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print("\nTask:")
    print(task.strip())
    print("\nImproving through reflexion...")
    
    result = reflexion.invoke(state)
    
    print("\nImprovement Process:")
    if "iterations" in result:
        for i, iteration in enumerate(result["iterations"], 1):
            print(f"\n--- Version {i} (Score: {iteration['score']:.2f}) ---")
            print(iteration["response"][:300] + "..." if len(iteration["response"]) > 300 else iteration["response"])
    
    print(f"\nFinal Score: {result.get('best_score', 'N/A'):.2f}")
    
    return result


def test_creative_writing():
    """Test creative writing improvement."""
    print("\n" + "="*80)
    print("TEST 11.3: Creative Writing Enhancement")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.8,  # Higher temperature for creativity
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    reflexion = ReflexionAgent(
        name="creative-writer",
        llm=llm,
        max_loops=3
    )
    
    # Creative writing task
    task = """
    Write an engaging opening paragraph for a science fiction story about
    artificial intelligence gaining consciousness.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print("\nCreative Task:")
    print(task.strip())
    print("\nRefining through multiple iterations...")
    
    result = reflexion.invoke(state)
    
    print("\nCreative Evolution:")
    if "iterations" in result:
        for i, iteration in enumerate(result["iterations"], 1):
            print(f"\n--- Draft {i} (Quality: {iteration['score']:.2f}) ---")
            print(iteration["response"])
            if i < len(result["iterations"]):
                print(f"\nSelf-Critique:")
                print(iteration["reflection"][:200] + "...")
    
    return result


def test_technical_documentation():
    """Test improving technical documentation."""
    print("\n" + "="*80)
    print("TEST 11.4: Technical Documentation Refinement")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    reflexion = ReflexionAgent(
        name="doc-writer",
        llm=llm,
        max_loops=2
    )
    
    # Documentation task
    task = """
    Write clear documentation for a REST API endpoint that creates a new user.
    Include: endpoint URL, HTTP method, request body, response format, and error codes.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print("\nDocumentation Task:")
    print(task.strip())
    print("\nRefining documentation quality...")
    
    result = reflexion.invoke(state)
    
    print("\nDocumentation Versions:")
    if "iterations" in result:
        for i, iteration in enumerate(result["iterations"], 1):
            print(f"\n--- Version {i} ---")
            print(f"Quality Score: {iteration['score']:.2f}")
            print("\nDocumentation:")
            print(iteration["response"][:400] + "..." if len(iteration["response"]) > 400 else iteration["response"])
    
    return result


def test_explanation_clarity():
    """Test improving explanation clarity."""
    print("\n" + "="*80)
    print("TEST 11.5: Explanation Clarity Enhancement")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    reflexion = ReflexionAgent(
        name="explainer",
        llm=llm,
        max_loops=3
    )
    
    # Explanation task
    task = """
    Explain the concept of 'Big O notation' in computer science to someone
    with basic programming knowledge. Use simple examples.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print("\nExplanation Task:")
    print(task.strip())
    print("\nIteratively improving clarity...")
    
    result = reflexion.invoke(state)
    
    print("\nClarity Progression:")
    if "iterations" in result:
        for i, iteration in enumerate(result["iterations"], 1):
            print(f"\n--- Attempt {i} (Clarity: {iteration['score']:.2f}) ---")
            print(iteration["response"])
            
            if i < len(result["iterations"]):
                print("\nWhat to improve:")
                reflection = iteration["reflection"]
                # Extract key improvement points
                lines = reflection.split('\n')[:3]
                for line in lines:
                    if line.strip():
                        print(f"  • {line.strip()}")
    
    return result


def test_memory_utilization():
    """Test memory system and learning from past reflections."""
    print("\n" + "="*80)
    print("TEST 11.6: Memory Utilization and Learning")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    reflexion = ReflexionAgent(
        name="learning-agent",
        llm=llm,
        max_loops=2,
        memory_capacity=50
    )
    
    # Series of related tasks
    tasks = [
        "Explain what a REST API is.",
        "Explain what GraphQL is.",
        "Compare REST API and GraphQL."
    ]
    
    print(f"\nProcessing {len(tasks)} related tasks to test memory...")
    
    results = []
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i} ---")
        print(task)
        
        state = {
            "messages": [
                {"role": "user", "content": task}
            ]
        }
        
        result = reflexion.invoke(state)
        
        print(f"\nIterations: {len(result.get('iterations', []))}")
        print(f"Best Score: {result.get('best_score', 0):.2f}")
        print(f"\nMemory Stats:")
        print(f"  Short-term: {len(reflexion.memory.short_term_memory)} entries")
        print(f"  Long-term: {len(reflexion.memory.long_term_memory)} entries")
        
        results.append(result)
    
    print(f"\nCompleted {len(results)} tasks with memory persistence")
    
    return results


def main():
    """Run all ReflexionAgent tests."""
    print("\n" + "="*80)
    print("REFLEXION AGENT PATTERN - COMPREHENSIVE TESTS")
    print("="*80)
    
    try:
        # Run all tests
        test_basic_reflexion()
        test_code_improvement()
        test_creative_writing()
        test_technical_documentation()
        test_explanation_clarity()
        test_memory_utilization()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nReflexionAgent Capabilities Demonstrated:")
        print("✅ Iterative improvement through self-reflection")
        print("✅ Code quality enhancement")
        print("✅ Creative writing refinement")
        print("✅ Technical documentation improvement")
        print("✅ Explanation clarity enhancement")
        print("✅ Memory-based learning")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
