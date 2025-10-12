"""
Test 10: ReasoningDuoAgent Pattern - Two-Stage Reasoning

This test demonstrates the ReasoningDuoAgent pattern which uses two agents:
one for explicit reasoning and one for generating the final answer.
"""

import os
from langchain_openai import ChatOpenAI
from arc.agents import ReasoningDuoAgent


def test_basic_reasoning():
    """Test basic two-stage reasoning."""
    print("\n" + "="*80)
    print("TEST 10.1: Basic Two-Stage Reasoning")
    print("="*80)
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create reasoning duo agent
    duo = ReasoningDuoAgent(
        name="math-reasoner",
        llm=llm,
        max_loops=1
    )
    
    # Math problem
    problem = "If a train travels at 60 mph for 2.5 hours, how far does it travel?"
    
    state = {
        "messages": [
            {"role": "user", "content": problem}
        ]
    }
    
    print(f"\nProblem: {problem}")
    print("\nProcessing with two-stage reasoning...")
    
    # Invoke duo agent
    result = duo.invoke(state)
    
    print("\nReasoning Process:")
    if "conversation" in result:
        for entry in result["conversation"]:
            role = entry["role"].upper()
            content = entry["content"]
            print(f"\n{role}:")
            print(content)
    
    print("\nFinal Answer:")
    final_answer = result["messages"][-1]["content"]
    print(final_answer)
    
    return result


def test_complex_problem():
    """Test with complex problem solving."""
    print("\n" + "="*80)
    print("TEST 10.2: Complex Problem Solving")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    duo = ReasoningDuoAgent(
        name="problem-solver",
        llm=llm,
        max_loops=1
    )
    
    # Complex problem
    problem = """
    A company has 120 employees. 60% work in development, 25% in sales, and the rest in support.
    If they hire 20 more developers and 10 more sales people, what percentage of the total
    workforce will be in support?
    """
    
    state = {
        "messages": [
            {"role": "user", "content": problem}
        ]
    }
    
    print("\nComplex Problem:")
    print(problem.strip())
    print("\nReasoning through the solution...")
    
    result = duo.invoke(state)
    
    print("\nReasoning Steps:")
    if "conversation" in result:
        for i, entry in enumerate(result["conversation"], 1):
            print(f"\nStep {i} ({entry['role']}):")
            print(entry["content"])
    
    return result


def test_logical_reasoning():
    """Test logical reasoning capabilities."""
    print("\n" + "="*80)
    print("TEST 10.3: Logical Reasoning")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    duo = ReasoningDuoAgent(
        name="logic-reasoner",
        llm=llm,
        max_loops=1
    )
    
    # Logical puzzle
    puzzle = """
    If all roses are flowers, and some flowers fade quickly, can we conclude that
    some roses fade quickly? Explain your reasoning step by step.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": puzzle}
        ]
    }
    
    print("\nLogical Puzzle:")
    print(puzzle.strip())
    print("\nAnalyzing with explicit reasoning...")
    
    result = duo.invoke(state)
    
    print("\nLogical Analysis:")
    if "conversation" in result:
        for entry in result["conversation"]:
            print(f"\n{entry['role'].upper()}:")
            print(entry["content"])
    
    return result


def test_technical_explanation():
    """Test technical concept explanation."""
    print("\n" + "="*80)
    print("TEST 10.4: Technical Concept Explanation")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    duo = ReasoningDuoAgent(
        name="tech-explainer",
        llm=llm,
        max_loops=1
    )
    
    # Technical question
    question = """
    Explain the difference between synchronous and asynchronous programming.
    Include examples of when to use each approach.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print("\nTechnical Question:")
    print(question.strip())
    print("\nGenerating explanation with reasoning...")
    
    result = duo.invoke(state)
    
    print("\nReasoning and Explanation:")
    if "conversation" in result:
        for entry in result["conversation"]:
            role = "REASONING AGENT" if entry["role"] == "reasoning" else "MAIN AGENT"
            print(f"\n{role}:")
            print(entry["content"][:300] + "..." if len(entry["content"]) > 300 else entry["content"])
    
    return result


def test_decision_making():
    """Test decision-making with reasoning."""
    print("\n" + "="*80)
    print("TEST 10.5: Decision Making with Reasoning")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    duo = ReasoningDuoAgent(
        name="decision-maker",
        llm=llm,
        max_loops=1
    )
    
    # Decision problem
    scenario = """
    A startup has $100,000 to invest and three options:
    A) Hire 2 senior developers ($80,000/year)
    B) Hire 4 junior developers ($40,000/year) and 1 mentor ($60,000/year)
    C) Outsource development ($70,000) and use remainder for marketing
    
    Which option would you recommend for a 6-month MVP development cycle and why?
    """
    
    state = {
        "messages": [
            {"role": "user", "content": scenario}
        ]
    }
    
    print("\nDecision Scenario:")
    print(scenario.strip())
    print("\nAnalyzing options with explicit reasoning...")
    
    result = duo.invoke(state)
    
    print("\nDecision Analysis:")
    if "conversation" in result:
        for entry in result["conversation"]:
            print(f"\n{entry['role'].upper()}:")
            print(entry["content"])
    
    print("\nRecommendation:")
    print(result["messages"][-1]["content"])
    
    return result


def test_multiple_problems():
    """Test solving multiple problems in sequence."""
    print("\n" + "="*80)
    print("TEST 10.6: Multiple Problem Solving")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    duo = ReasoningDuoAgent(
        name="multi-solver",
        llm=llm,
        max_loops=1
    )
    
    problems = [
        "What is 15% of 240?",
        "If x + 5 = 12, what is x?",
        "How many minutes are in 2.5 hours?"
    ]
    
    print(f"\nSolving {len(problems)} problems sequentially...")
    
    results = []
    for i, problem in enumerate(problems, 1):
        print(f"\n--- Problem {i} ---")
        print(problem)
        
        state = {
            "messages": [
                {"role": "user", "content": problem}
            ]
        }
        
        result = duo.invoke(state)
        
        print("\nReasoning:")
        if "conversation" in result and len(result["conversation"]) > 0:
            reasoning = result["conversation"][0]["content"]
            print(reasoning[:150] + "..." if len(reasoning) > 150 else reasoning)
        
        print("\nAnswer:")
        answer = result["messages"][-1]["content"]
        print(answer)
        
        results.append(result)
    
    print(f"\nCompleted solving {len(results)} problems")
    
    return results


def main():
    """Run all ReasoningDuoAgent tests."""
    print("\n" + "="*80)
    print("REASONING DUO AGENT PATTERN - COMPREHENSIVE TESTS")
    print("="*80)
    
    try:
        # Run all tests
        test_basic_reasoning()
        test_complex_problem()
        test_logical_reasoning()
        test_technical_explanation()
        test_decision_making()
        test_multiple_problems()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nReasoningDuoAgent Capabilities Demonstrated:")
        print("✅ Basic mathematical reasoning")
        print("✅ Complex problem solving")
        print("✅ Logical analysis")
        print("✅ Technical explanations")
        print("✅ Decision making")
        print("✅ Sequential problem solving")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
