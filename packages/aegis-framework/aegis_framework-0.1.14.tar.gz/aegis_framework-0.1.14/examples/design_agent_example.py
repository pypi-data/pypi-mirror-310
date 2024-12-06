"""
Example demonstrating the use of the DesignAgent.
"""

from aegis_framework import DesignAgent
from aegis_framework.public.design_agent import run_design_task

def main():
    """Run the design agent example."""
    print("\n=== Design Agent Demo ===")
    
    # Initialize design agent
    agent = DesignAgent(model="gemma2:9b")
    
    # Get suggested designs
    print("\nSuggested design patterns:")
    for design in agent.get_suggested_designs():
        print(f"- {design}")
    
    # Generate a new design
    print("\nGenerating new design...")
    design = agent.generate_new_design()
    print(f"Design: {design}")
    
    # Run specific design tasks
    tasks = [
        "design a data processing pipeline agent",
        "create an agent for natural language understanding",
        "design a multi-agent system for distributed computing"
    ]
    
    print("\nRunning design tasks:")
    for task in tasks:
        print(f"\nTask: {task}")
        result = run_design_task(task)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
