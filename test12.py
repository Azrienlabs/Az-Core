"""
Test 12: SelfConsistencyAgent Pattern - Multiple Responses with Consensus

This test demonstrates the SelfConsistencyAgent pattern which generates multiple
independent responses and aggregates them for improved reliability and accuracy.
"""

import os
from langchain_openai import ChatOpenAI
from rise_framework.agents import SelfConsistencyAgent


def test_basic_consensus():
    """Test basic consensus building from multiple responses."""
    print("\n" + "="*80)
    print("TEST 12.1: Basic Consensus Building")
    print("="*80)
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create self-consistency agent
    sc_agent = SelfConsistencyAgent(
        name="consensus-builder",
        llm=llm,
        num_samples=3
    )
    
    # Question that benefits from consensus
    question = "What are the three most important principles of good software design?"
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print(f"\nQuestion: {question}")
    print(f"\nGenerating {sc_agent.num_samples} independent responses...")
    
    # Invoke self-consistency agent
    result = sc_agent.invoke(state)
    
    print("\nIndividual Responses:")
    if "responses" in result:
        for i, response in enumerate(result["responses"], 1):
            print(f"\n--- Response {i} ---")
            print(response[:200] + "..." if len(response) > 200 else response)
    
    print("\nAggregated Consensus:")
    consensus = result["messages"][-1]["content"]
    print(consensus)
    
    return result


def test_mathematical_consensus():
    """Test consensus on mathematical problems."""
    print("\n" + "="*80)
    print("TEST 12.2: Mathematical Problem Consensus")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    sc_agent = SelfConsistencyAgent(
        name="math-consensus",
        llm=llm,
        num_samples=5
    )
    
    # Math problem
    problem = """
    A store sells apples for $0.50 each. If you buy 10 or more, you get a 20% discount.
    How much would 15 apples cost?
    """
    
    state = {
        "messages": [
            {"role": "user", "content": problem}
        ]
    }
    
    print("\nMath Problem:")
    print(problem.strip())
    print(f"\nGenerating {sc_agent.num_samples} solutions for validation...")
    
    result = sc_agent.invoke(state)
    
    print("\nDifferent Approaches:")
    if "responses" in result:
        for i, response in enumerate(result["responses"], 1):
            print(f"\nApproach {i}:")
            # Extract just the key part
            lines = response.split('\n')
            for line in lines[:3]:
                if line.strip():
                    print(f"  {line.strip()}")
    
    print("\nConsensus Answer:")
    print(result["messages"][-1]["content"])
    
    return result


def test_answer_validation():
    """Test validating if specific answer appears in responses."""
    print("\n" + "="*80)
    print("TEST 12.3: Answer Validation")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    sc_agent = SelfConsistencyAgent(
        name="validator",
        llm=llm,
        num_samples=3
    )
    
    # Question with known answer
    question = "What is the capital of France?"
    expected_answer = "Paris"
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print(f"\nQuestion: {question}")
    print(f"Expected Answer: {expected_answer}")
    print("\nValidating answer across multiple responses...")
    
    result = sc_agent.invoke(state)
    
    # Check if expected answer is present
    has_answer = sc_agent.check_responses_for_answer(
        result.get("responses", []),
        expected_answer
    )
    
    print(f"\nAnswer '{expected_answer}' found in responses: {'✅ Yes' if has_answer else '❌ No'}")
    
    print("\nAll Responses:")
    if "responses" in result:
        for i, response in enumerate(result["responses"], 1):
            print(f"{i}. {response[:100]}...")
    
    return result


def test_opinion_aggregation():
    """Test aggregating diverse opinions."""
    print("\n" + "="*80)
    print("TEST 12.4: Opinion Aggregation")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.8,  # Higher temperature for diversity
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    sc_agent = SelfConsistencyAgent(
        name="opinion-aggregator",
        llm=llm,
        num_samples=4
    )
    
    # Opinion-based question
    question = """
    What are the pros and cons of remote work vs office work?
    Provide a balanced perspective.
    """
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print("\nQuestion:")
    print(question.strip())
    print(f"\nGenerating {sc_agent.num_samples} diverse perspectives...")
    
    result = sc_agent.invoke(state)
    
    print("\nDiverse Perspectives:")
    if "responses" in result:
        for i, response in enumerate(result["responses"], 1):
            print(f"\n--- Perspective {i} ---")
            # Show first few lines
            lines = response.split('\n')[:4]
            for line in lines:
                if line.strip():
                    print(line)
    
    print("\nBalanced Aggregation:")
    print(result["messages"][-1]["content"])
    
    return result


def test_technical_decision():
    """Test technical decision making with consensus."""
    print("\n" + "="*80)
    print("TEST 12.5: Technical Decision Consensus")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    sc_agent = SelfConsistencyAgent(
        name="tech-decision",
        llm=llm,
        num_samples=5
    )
    
    # Technical decision
    scenario = """
    Your team needs to choose a database for a new e-commerce application.
    The app expects 10,000 users initially, with potential to scale to 1 million.
    Should you use PostgreSQL, MongoDB, or MySQL? Why?
    """
    
    state = {
        "messages": [
            {"role": "user", "content": scenario}
        ]
    }
    
    print("\nTechnical Scenario:")
    print(scenario.strip())
    print(f"\nAnalyzing with {sc_agent.num_samples} independent evaluations...")
    
    result = sc_agent.invoke(state)
    
    print("\nIndependent Evaluations:")
    if "responses" in result:
        # Count recommendations
        db_mentions = {"PostgreSQL": 0, "MongoDB": 0, "MySQL": 0}
        for response in result["responses"]:
            for db in db_mentions.keys():
                if db in response:
                    db_mentions[db] += 1
        
        print("\nDatabase Mentions:")
        for db, count in db_mentions.items():
            print(f"  {db}: {count}/{len(result['responses'])}")
    
    print("\nConsensus Recommendation:")
    print(result["messages"][-1]["content"][:300] + "...")
    
    return result


def test_multiple_questions():
    """Test processing multiple questions with consensus."""
    print("\n" + "="*80)
    print("TEST 12.6: Multiple Questions with Consensus")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    sc_agent = SelfConsistencyAgent(
        name="multi-question",
        llm=llm,
        num_samples=3
    )
    
    # Multiple questions
    questions = [
        "What is the time complexity of binary search?",
        "What is the space complexity of merge sort?",
        "What is better for searching: hash table or binary search tree?"
    ]
    
    print(f"\nProcessing {len(questions)} questions with consensus...")
    
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\n--- Question {i} ---")
        print(question)
        
        state = {
            "messages": [
                {"role": "user", "content": question}
            ]
        }
        
        result = sc_agent.invoke(state)
        
        print(f"\nSamples generated: {len(result.get('responses', []))}")
        print("Consensus:")
        consensus = result["messages"][-1]["content"]
        print(consensus[:150] + "..." if len(consensus) > 150 else consensus)
        
        results.append(result)
    
    print(f"\nCompleted consensus building for {len(results)} questions")
    
    return results


def test_high_sample_count():
    """Test with higher number of samples for critical decisions."""
    print("\n" + "="*80)
    print("TEST 12.7: High Sample Count for Critical Decisions")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    sc_agent = SelfConsistencyAgent(
        name="high-confidence",
        llm=llm,
        num_samples=7  # More samples for higher confidence
    )
    
    # Critical question
    question = """
    What are the most important security considerations when building a
    web application that handles sensitive user data?
    """
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print("\nCritical Security Question:")
    print(question.strip())
    print(f"\nGenerating {sc_agent.num_samples} responses for high confidence...")
    
    result = sc_agent.invoke(state)
    
    print(f"\nTotal responses generated: {len(result.get('responses', []))}")
    
    print("\nConsensus Security Recommendations:")
    consensus = result["messages"][-1]["content"]
    print(consensus)
    
    return result


def main():
    """Run all SelfConsistencyAgent tests."""
    print("\n" + "="*80)
    print("SELF-CONSISTENCY AGENT PATTERN - COMPREHENSIVE TESTS")
    print("="*80)
    
    try:
        # Run all tests
        test_basic_consensus()
        test_mathematical_consensus()
        test_answer_validation()
        test_opinion_aggregation()
        test_technical_decision()
        test_multiple_questions()
        test_high_sample_count()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nSelfConsistencyAgent Capabilities Demonstrated:")
        print("✅ Basic consensus building")
        print("✅ Mathematical problem validation")
        print("✅ Answer presence verification")
        print("✅ Opinion aggregation")
        print("✅ Technical decision making")
        print("✅ Multiple question handling")
        print("✅ High-confidence responses (many samples)")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
