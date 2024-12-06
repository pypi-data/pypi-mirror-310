"""
Basic usage examples of the Aegis Framework.

This script demonstrates the core functionality of the Aegis Framework,
including the MasterAIAgent for general AI tasks and the DesignAgent
for creating new agent designs.

Example usage:
    $ python basic_usage.py
    $ python basic_usage.py --model gemma2:9b
    $ python basic_usage.py --task "design a chatbot"
"""

import argparse
from typing import Dict, Any
from aegis_framework import MasterAIAgent, DesignAgent

def demonstrate_master_agent(model: str = "gemma2:9b") -> None:
    """
    Demonstrate the capabilities of MasterAIAgent.
    
    The MasterAIAgent is a versatile AI agent that can:
    - Answer questions on various topics
    - Perform complex tasks
    - Generate content
    - Analyze text and data
    
    Args:
        model: Name of the LLM model to use
    """
    print("\n=== MasterAIAgent Demo ===")
    print(f"Using model: {model}")
    
    # Initialize agent
    agent = MasterAIAgent(model=model)
    
    # 1. Task List
    print("\nAvailable Tasks:")
    tasks = agent.get_task_list()
    for task in tasks:
        print(f"- {task}")
    
    # 2. Question Answering
    questions = [
        "What are the key principles of machine learning?",
        "How does natural language processing work?",
        "What is the difference between supervised and unsupervised learning?"
    ]
    
    print("\nQuestion Answering Demo:")
    for question in questions:
        print(f"\nQ: {question}")
        response = agent.answer_question(question)
        print(f"A: {response}")
    
    # 3. Task Performance
    tasks = [
        "analyze the sentiment of: 'This framework is amazing and easy to use!'",
        "create a python function to calculate fibonacci numbers",
        "suggest three ways to optimize a slow database query"
    ]
    
    print("\nTask Performance Demo:")
    for task in tasks:
        print(f"\nTask: {task}")
        result = agent.perform_task(task)
        print(f"Result: {result}")

def demonstrate_design_agent(model: str = "gemma2:9b", task: str = None) -> Dict[str, Any]:
    """
    Demonstrate the capabilities of DesignAgent.
    
    The DesignAgent specializes in:
    - Creating new agent designs
    - Generating agent architectures
    - Periodic design generation
    - Design optimization
    
    Args:
        model: Name of the LLM model to use
        task: Optional specific design task
        
    Returns:
        Dict[str, Any]: The generated design
    """
    print("\n=== DesignAgent Demo ===")
    print(f"Using model: {model}")
    
    # Initialize design agent
    designer = DesignAgent(model=model)
    
    # Generate a design based on task or default
    context = task if task else "Create an AI agent for automated code review"
    print(f"\nGenerating design for: {context}")
    design = designer.generate_new_design(context=context)
    
    # Start periodic design generation if no specific task
    if not task:
        print("\nStarting periodic design generation...")
        designer.start_periodic_design()
        
        # Generate additional designs
        additional_tasks = [
            "design an agent for real-time data processing",
            "create an agent for automated testing",
            "design a multi-agent system coordinator"
        ]
        
        print("\nGenerating additional designs:")
        for task in additional_tasks:
            print(f"\nTask: {task}")
            result = designer.generate_new_design(context=task)
            print(f"Result: {result}")
        
        # Stop periodic generation
        print("\nStopping periodic design generation...")
        designer.stop_periodic_design()
    
    return design

def main():
    """Run the Aegis Framework demonstration."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Demonstrate Aegis Framework capabilities")
    parser.add_argument("--model", default="gemma2:9b", help="Name of the LLM model to use")
    parser.add_argument("--task", help="Specific design task to run")
    args = parser.parse_args()
    
    try:
        # Run demonstrations
        demonstrate_master_agent(model=args.model)
        design = demonstrate_design_agent(model=args.model, task=args.task)
        
        # Show where to find the design
        if design.get("path"):
            print(f"\nDesign saved to: {design['path']}")
            print("View the README.md file in that directory for the complete design.")
    
    except KeyboardInterrupt:
        print("\nDemonstration interrupted by user.")
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        print("Please check that you're using a supported model and have set up the framework correctly.")
    
    print("\nFor more examples and documentation, visit: https://github.com/metisos/aegis-framework")

if __name__ == "__main__":
    main()
