"""
Advanced Custom Agent Example for the Aegis Framework.

This script demonstrates how to create and use custom agents with specialized
capabilities, focusing on data analysis as an example use case.

Features demonstrated:
- Custom agent creation
- Task specialization
- Data analysis capabilities
- Question answering

Example usage:
    $ python custom_agent_example.py
    $ python custom_agent_example.py --model gemma2:9b
"""

import argparse
from typing import Dict, Any, List, Optional

from aegis_framework import MasterAIAgent

class DataAnalysisAgent(MasterAIAgent):
    """Custom agent specialized for data analysis tasks."""
    
    def __init__(
        self,
        model: str = "gemma2:9b",
        custom_tasks: Optional[Dict[str, List[str]]] = None
    ):
        super().__init__(model=model)
        
        # Add specialized tasks
        self.agent_task_map.update({
            "data_analysis": [
                "analyze data",
                "statistical analysis",
                "trend analysis",
                "data visualization",
                "hypothesis testing"
            ]
        })
        
        # Add any custom tasks
        if custom_tasks:
            self.agent_task_map.update(custom_tasks)
    
    def analyze_data(
        self,
        data: str,
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Analyze data using LLM capabilities.
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis to perform
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        prompt = f"""
        Perform a {analysis_type} analysis of this data:
        
        {data}
        
        Please include:
        1. Key trends
        2. Statistical summary
        3. Notable patterns
        4. Recommendations
        """
        return self.perform_task(prompt)

def demonstrate_custom_agent(model: str = "gemma2:9b"):
    """Show how to use a custom agent."""
    print("\n=== Custom Agent Demo ===")
    print(f"Using model: {model}")
    
    # Create custom agent
    analyst = DataAnalysisAgent(model=model)
    
    # Show available tasks
    print("\nAvailable tasks:")
    tasks = analyst.get_task_list()
    for task in tasks:
        print(f"- {task}")
    
    # Run analysis
    data = """
    Monthly sales data for 2023:
    Jan: $50,000
    Feb: $55,000
    Mar: $48,000
    Apr: $62,000
    May: $58,000
    Jun: $65,000
    """
    
    print("\nAnalyzing sales data...")
    for analysis_type in ["comprehensive", "trend", "statistical"]:
        print(f"\nPerforming {analysis_type} analysis:")
        result = analyst.analyze_data(data, analysis_type=analysis_type)
        print(f"Results: {result}")
    
    # Ask specific questions
    questions = [
        "What is the overall trend in sales?",
        "Which month had the highest sales?",
        "What is the average monthly sales?",
        "What recommendations would you make based on this data?"
    ]
    
    print("\nAsking specific questions:")
    for question in questions:
        print(f"\nQ: {question}")
        answer = analyst.answer_question(question)
        print(f"A: {answer}")

def main():
    """Run the custom agent demonstration."""
    parser = argparse.ArgumentParser(
        description="Demonstrate custom agent capabilities"
    )
    parser.add_argument(
        "--model",
        default="gemma2:9b",
        help="Name of the LLM model to use"
    )
    args = parser.parse_args()
    
    try:
        demonstrate_custom_agent(model=args.model)
        print("\nDemonstration complete!")
        print("For more examples and documentation, visit: https://github.com/metisos/aegis-framework")
    
    except KeyboardInterrupt:
        print("\nDemonstration interrupted by user.")
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        print("Please check that you're using a supported model and have set up the framework correctly.")

if __name__ == "__main__":
    main()
