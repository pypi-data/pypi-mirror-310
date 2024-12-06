"""
Basic usage examples of the Aegis Framework.
Demonstrates MasterAIAgent and DesignAgent functionality.
"""

from aegis_framework import MasterAIAgent, DesignAgent

def demonstrate_master_agent():
    """Example usage of MasterAIAgent."""
    print("\n=== MasterAIAgent Demo ===")
    
    # Initialize agent with Gemma model
    agent = MasterAIAgent(model="gemma2:9b")
    
    # Get suggested prompts
    prompts = agent.get_suggested_prompts()
    print("\nSuggested prompts:")
    for prompt in prompts[:5]:  # Show first 5 prompts
        print(f"- {prompt}")
    
    # Ask a question
    question = "What are the key principles of artificial intelligence?"
    print(f"\nAsking: {question}")
    response = agent.answer_question(question)
    print(f"Response: {response}")
    
    # Perform a task
    task = "create a new agent for data analysis"
    print(f"\nPerforming task: {task}")
    result = agent.perform_task(task)
    print(f"Result: {result}")

def demonstrate_design_agent():
    """Example usage of DesignAgent."""
    print("\n=== DesignAgent Demo ===")
    
    # Initialize design agent
    designer = DesignAgent()
    
    # Generate a new design
    print("\nGenerating new agent design...")
    design = designer.generate_new_design()
    print(f"Design: {design}")
    
    # Run a design task
    task = "design an agent for natural language processing"
    print(f"\nRunning design task: {task}")
    from aegis_framework.public.design_agent import run_design_task
    result = run_design_task(task)
    print(f"Result: {result}")

if __name__ == "__main__":
    demonstrate_master_agent()
    demonstrate_design_agent()
