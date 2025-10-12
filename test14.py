"""
Test 14: ReactAgent - Standard ReAct Pattern Agent

This test demonstrates the ReactAgent which implements the ReAct (Reasoning + Acting)
pattern for general-purpose agent tasks.
"""

import os
from langchain_openai import ChatOpenAI
from arc.agents.agent_factory import ReactAgent
from langchain_core.tools import tool


# Define some example tools
@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression. Input should be a valid Python expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def word_count(text: str) -> str:
    """Count the number of words in the given text."""
    words = text.split()
    return f"Word count: {len(words)}"


@tool
def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]


def test_basic_react():
    """Test basic ReactAgent without tools."""
    print("\n" + "="*80)
    print("TEST 14.1: Basic ReactAgent (No Tools)")
    print("="*80)
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create ReactAgent
    agent = ReactAgent(
        name="basic-agent",
        llm=llm,
        prompt="You are a helpful AI assistant."
    )
    
    question = "Explain the concept of recursion in programming."
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print(f"\nQuestion: {question}")
    print("\nExecuting ReactAgent...")
    
    result = agent.invoke(state)
    
    print("\nResponse:")
    print(result["messages"][-1]["content"])
    
    return result


def test_react_with_tools():
    """Test ReactAgent with tools."""
    print("\n" + "="*80)
    print("TEST 14.2: ReactAgent with Tools")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create ReactAgent with tools
    agent = ReactAgent(
        name="tool-agent",
        llm=llm,
        tools=[calculate, word_count, reverse_text],
        prompt="You are a helpful assistant with access to calculation and text manipulation tools."
    )
    
    task = "Calculate the result of 15 * 8 + 12, then reverse the result as text."
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print(f"\nTask: {task}")
    print(f"Available tools: {[t.name for t in agent.tools]}")
    print("\nExecuting with tools...")
    
    result = agent.invoke(state)
    
    print("\nResult:")
    print(result["messages"][-1]["content"])
    
    return result


def test_text_processing():
    """Test text processing with ReactAgent."""
    print("\n" + "="*80)
    print("TEST 14.3: Text Processing")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = ReactAgent(
        name="text-processor",
        llm=llm,
        tools=[word_count, reverse_text]
    )
    
    text = "The quick brown fox jumps over the lazy dog"
    task = f"Count the words in this text and then reverse it: '{text}'"
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print(f"\nOriginal text: {text}")
    print(f"Task: {task}")
    print("\nProcessing...")
    
    result = agent.invoke(state)
    
    print("\nResult:")
    print(result["messages"][-1]["content"])
    
    return result


def test_calculation_agent():
    """Test mathematical calculations."""
    print("\n" + "="*80)
    print("TEST 14.4: Mathematical Calculations")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = ReactAgent(
        name="calculator",
        llm=llm,
        tools=[calculate],
        prompt="You are a mathematical assistant. Use the calculate tool for complex calculations."
    )
    
    problems = [
        "What is 25% of 200?",
        "Calculate: (15 + 25) * 3 - 10",
        "What is 2 to the power of 10?"
    ]
    
    print(f"\nSolving {len(problems)} math problems...")
    
    results = []
    for i, problem in enumerate(problems, 1):
        print(f"\n--- Problem {i} ---")
        print(problem)
        
        state = {
            "messages": [
                {"role": "user", "content": problem}
            ]
        }
        
        result = agent.invoke(state)
        
        print("Answer:")
        print(result["messages"][-1]["content"])
        
        results.append(result)
    
    return results


def test_conversational_agent():
    """Test multi-turn conversation."""
    print("\n" + "="*80)
    print("TEST 14.5: Multi-Turn Conversation")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = ReactAgent(
        name="conversational-agent",
        llm=llm,
        prompt="You are a helpful programming tutor."
    )
    
    # Simulate multi-turn conversation
    conversation = [
        "What is a function in Python?",
        "Can you show me an example?",
        "How do I call this function?"
    ]
    
    print("\nMulti-turn conversation:")
    
    state = {"messages": []}
    
    for i, message in enumerate(conversation, 1):
        print(f"\n--- Turn {i} ---")
        print(f"User: {message}")
        
        # Add user message to state
        state["messages"].append({"role": "user", "content": message})
        
        # Invoke agent
        state = agent.invoke(state)
        
        # Get assistant response
        assistant_msg = state["messages"][-1]["content"]
        print(f"Assistant: {assistant_msg[:200]}...")
    
    print(f"\nConversation completed with {len(state['messages'])} messages")
    
    return state


def test_custom_prompt():
    """Test ReactAgent with custom system prompt."""
    print("\n" + "="*80)
    print("TEST 14.6: Custom System Prompt")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Custom prompt for a specific personality
    custom_prompt = """
    You are a Shakespearean scholar who explains technical concepts in
    the style of William Shakespeare. Use flowery language and dramatic expressions.
    """
    
    agent = ReactAgent(
        name="shakespeare-agent",
        llm=llm,
        prompt=custom_prompt
    )
    
    question = "Explain what a database is."
    
    state = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    print("\nCustom Prompt: Shakespearean scholar")
    print(f"Question: {question}")
    print("\nExecuting...")
    
    result = agent.invoke(state)
    
    print("\nShakespearean Response:")
    print(result["messages"][-1]["content"])
    
    return result


def test_async_invocation():
    """Test asynchronous agent invocation."""
    print("\n" + "="*80)
    print("TEST 14.7: Async Invocation")
    print("="*80)
    
    import asyncio
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = ReactAgent(
        name="async-agent",
        llm=llm
    )
    
    async def run_async():
        state = {
            "messages": [
                {"role": "user", "content": "What is machine learning?"}
            ]
        }
        
        print("\nExecuting asynchronously...")
        result = await agent.ainvoke(state)
        
        print("\nAsync Response:")
        print(result["messages"][-1]["content"][:250] + "...")
        
        return result
    
    # Run async function
    result = asyncio.run(run_async())
    
    return result


def test_tool_addition():
    """Test dynamically adding tools to agent."""
    print("\n" + "="*80)
    print("TEST 14.8: Dynamic Tool Addition")
    print("="*80)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create agent without tools
    agent = ReactAgent(
        name="dynamic-agent",
        llm=llm
    )
    
    print(f"\nInitial tools: {len(agent.tools)}")
    
    # Add tools dynamically
    agent.add_tool(calculate)
    agent.add_tool(word_count)
    
    print(f"After adding tools: {len(agent.tools)}")
    print(f"Available tools: {[t.name for t in agent.tools]}")
    
    task = "Calculate 50 * 3 and count the words in 'Hello World Example'"
    
    state = {
        "messages": [
            {"role": "user", "content": task}
        ]
    }
    
    print(f"\nTask: {task}")
    print("\nExecuting with dynamically added tools...")
    
    result = agent.invoke(state)
    
    print("\nResult:")
    print(result["messages"][-1]["content"])
    
    return result


def main():
    """Run all ReactAgent tests."""
    print("\n" + "="*80)
    print("REACT AGENT PATTERN - COMPREHENSIVE TESTS")
    print("="*80)
    
    try:
        # Run all tests
        test_basic_react()
        test_react_with_tools()
        test_text_processing()
        test_calculation_agent()
        test_conversational_agent()
        test_custom_prompt()
        test_async_invocation()
        test_tool_addition()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nReactAgent Capabilities Demonstrated:")
        print("✅ Basic question answering")
        print("✅ Tool usage and integration")
        print("✅ Text processing operations")
        print("✅ Mathematical calculations")
        print("✅ Multi-turn conversations")
        print("✅ Custom system prompts")
        print("✅ Asynchronous invocation")
        print("✅ Dynamic tool addition")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
