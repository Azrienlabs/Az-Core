"""
Test 9: AgentJudge Pattern - Quality Evaluation Agent

This test demonstrates the AgentJudge pattern for evaluating and providing
feedback on agent outputs. Perfect for quality control and validation.
"""

import os
from langchain_openai import ChatOpenAI
from rise_framework.agents import AgentJudge


def test_basic_evaluation():
    """Test basic output evaluation."""
    print("\n" + "="*80)
    print("TEST 9.1: Basic Output Evaluation")
    print("="*80)
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create judge agent
    judge = AgentJudge(
        name="quality-judge",
        llm=llm,
        evaluation_criteria={
            "accuracy": 0.4,
            "completeness": 0.3,
            "clarity": 0.3
        },
        max_loops=1
    )
    
    # Content to evaluate
    content = """
    Python is a high-level programming language. It was created by Guido van Rossum
    and first released in 1991. Python is known for its simple syntax and readability.
    It supports multiple programming paradigms including procedural, object-oriented,
    and functional programming.
    """
    
    # Create state
    state = {
        "messages": [
            {"role": "user", "content": content}
        ]
    }
    
    print("\nContent to evaluate:")
    print(content.strip())
    print("\nEvaluating...")
    
    # Invoke judge
    result = judge.invoke(state)
    
    print("\nEvaluation Result:")
    evaluation = result["messages"][-1]["content"]
    print(evaluation)
    
    return result


def test_custom_criteria():
    """Test judge with custom evaluation criteria."""
    print("\n" + "="*80)
    print("TEST 9.2: Custom Evaluation Criteria")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create judge with custom criteria
    judge = AgentJudge(
        name="tech-reviewer",
        llm=llm,
        evaluation_criteria={
            "technical_accuracy": 0.35,
            "code_quality": 0.25,
            "best_practices": 0.20,
            "documentation": 0.20
        },
        max_loops=1
    )
    
    # Code to evaluate
    code_sample = """
    def calculate_sum(numbers):
        total = 0
        for num in numbers:
            total += num
        return total
    
    result = calculate_sum([1, 2, 3, 4, 5])
    print(result)
    """
    
    state = {
        "messages": [
            {"role": "user", "content": f"Evaluate this Python code:\n\n{code_sample}"}
        ]
    }
    
    print("\nCode to evaluate:")
    print(code_sample)
    print("\nEvaluating with custom criteria...")
    
    result = judge.invoke(state)
    
    print("\nTechnical Review:")
    evaluation = result["messages"][-1]["content"]
    print(evaluation)
    
    return result


def test_comparative_evaluation():
    """Test comparing multiple outputs."""
    print("\n" + "="*80)
    print("TEST 9.3: Comparative Evaluation")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    judge = AgentJudge(
        name="comparator",
        llm=llm,
        evaluation_criteria={
            "effectiveness": 0.5,
            "efficiency": 0.3,
            "readability": 0.2
        }
    )
    
    # Two solutions to compare
    comparison_content = """
    Compare these two sorting implementations:
    
    Solution A (Bubble Sort):
    def sort_list(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    
    Solution B (Built-in Sort):
    def sort_list(arr):
        return sorted(arr)
    
    Which solution is better and why?
    """
    
    state = {
        "messages": [
            {"role": "user", "content": comparison_content}
        ]
    }
    
    print("\nComparing two solutions...")
    print(comparison_content)
    
    result = judge.invoke(state)
    
    print("\nComparative Analysis:")
    evaluation = result["messages"][-1]["content"]
    print(evaluation)
    
    return result


def test_batch_evaluation():
    """Test evaluating multiple items."""
    print("\n" + "="*80)
    print("TEST 9.4: Batch Evaluation")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    judge = AgentJudge(
        name="batch-evaluator",
        llm=llm,
        evaluation_criteria={
            "quality": 0.6,
            "relevance": 0.4
        }
    )
    
    # Multiple responses to evaluate
    responses = [
        "Python is a programming language.",
        "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "Python, created by Guido van Rossum in 1991, is a versatile programming language with dynamic typing and automatic memory management."
    ]
    
    print(f"\nEvaluating {len(responses)} responses...")
    
    results = []
    for i, response in enumerate(responses, 1):
        print(f"\n--- Response {i} ---")
        print(response)
        
        state = {
            "messages": [
                {"role": "user", "content": f"Evaluate this response about Python:\n\n{response}"}
            ]
        }
        
        result = judge.invoke(state)
        evaluation = result["messages"][-1]["content"]
        
        print("\nEvaluation:")
        print(evaluation[:200] + "..." if len(evaluation) > 200 else evaluation)
        
        results.append(result)
    
    print(f"\nCompleted evaluating {len(results)} responses")
    
    return results


def test_feedback_generation():
    """Test generating constructive feedback."""
    print("\n" + "="*80)
    print("TEST 9.5: Constructive Feedback Generation")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    judge = AgentJudge(
        name="feedback-generator",
        llm=llm,
        evaluation_criteria={
            "strengths": 0.3,
            "weaknesses": 0.3,
            "improvements": 0.4
        }
    )
    
    # Essay to evaluate
    essay = """
    Climate change is a big problem. The Earth is getting warmer because of pollution.
    We should do something about it. People need to use less energy and recycle more.
    If we don't act now, it will be too late.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": f"Provide detailed feedback on this essay about climate change:\n\n{essay}"}
        ]
    }
    
    print("\nEssay to review:")
    print(essay.strip())
    print("\nGenerating feedback...")
    
    result = judge.invoke(state)
    
    print("\nConstructive Feedback:")
    feedback = result["messages"][-1]["content"]
    print(feedback)
    
    return result


def main():
    """Run all AgentJudge tests."""
    print("\n" + "="*80)
    print("AGENT JUDGE PATTERN - COMPREHENSIVE TESTS")
    print("="*80)
    
    try:
        # Run all tests
        test_basic_evaluation()
        test_custom_criteria()
        test_comparative_evaluation()
        test_batch_evaluation()
        test_feedback_generation()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nAgentJudge Capabilities Demonstrated:")
        print("✅ Basic output evaluation")
        print("✅ Custom evaluation criteria")
        print("✅ Comparative analysis")
        print("✅ Batch processing")
        print("✅ Constructive feedback generation")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
