#!/usr/bin/env python3

from aegis_framework import MasterAIAgent, DesignAgent
from examples.custom_agent_example import DataAnalysisAgent
from examples.design_agent_example import DesignManager

def test_custom_agent():
    print("\n=== Testing Custom Data Analysis Agent ===")
    # Initialize the data analysis agent
    agent = DataAnalysisAgent(model="llama2")
    
    # Test basic interaction
    prompt = "Can you help me analyze a dataset of customer feedback?"
    print(f"\nPrompt: {prompt}")
    response = agent.generate_response(prompt)
    print(f"Response: {response}")

def test_design_agent():
    print("\n=== Testing Design Agent ===")
    # Initialize the design manager
    manager = DesignManager(model="llama2")
    
    # Test design generation with constraints
    constraints = {
        "type": "web_application",
        "requirements": [
            "User authentication",
            "Dashboard interface",
            "Data visualization"
        ],
        "technology_stack": ["Python", "React", "PostgreSQL"]
    }
    
    print("\nGenerating design with constraints:", constraints)
    design = manager.generate_design_with_constraints(constraints)
    print("\nGenerated Design:")
    print(design)

def main():
    print("Starting Aegis Framework Test...")
    
    try:
        # Test custom agent
        test_custom_agent()
        
        # Test design agent
        test_design_agent()
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        print("\nValid models: ['gemma2:9b', 'codellama', 'llama2', 'mistral']")

if __name__ == "__main__":
    main()
