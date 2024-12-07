"""
Advanced Custom Agent Example for the Aegis Framework.

This script demonstrates how to create and use custom agents with specialized
capabilities, focusing on data analysis as an example use case.

Features demo/home/ubuntu/aegis_framework/examplesnstrated:
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
        model: str = "llama2",
        custom_tasks: Optional[Dict[str, List[str]]] = None
    ):
        super().__init__(model=model)
        self.model = model  # Store the model name
        
        # Add specialized tasks
        self.tasks = {
            "data_analysis": [
                "Analyze datasets and provide insights",
                "Generate statistical summaries",
                "Create data visualizations",
                "Identify trends and patterns"
            ],
            "reporting": [
                "Generate analysis reports",
                "Create executive summaries",
                "Prepare data presentations"
            ]
        }
        
        if custom_tasks:
            self.tasks.update(custom_tasks)
    
    def interact_with_model(self, prompt: str) -> str:
        """Interact with the AI model."""
        try:
            # This is a simulated response. In a real implementation,
            # you would use the actual model interaction from the parent class
            return f"[Local {self.model}] Response to: {prompt}\n\nThis is a simulated response from the local LLM. In a real implementation, this would use local inference."
        except Exception as e:
            return f"Error interacting with model: {str(e)}"
            
    def generate_response(self, prompt: str) -> str:
        """Generate a response using the AI model."""
        try:
            # Add context about capabilities
            context = "As a data analysis specialist, I can help with: "
            for task_type, task_list in self.tasks.items():
                context += f"\n- {task_type.replace('_', ' ').title()}: " + ", ".join(task_list)
            
            # Combine context and prompt
            full_prompt = f"{context}\n\nUser Query: {prompt}\n\nResponse:"
            
            # Use the parent class's method to interact with the model
            response = self.interact_with_model(full_prompt)
            return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _construct_analysis_prompt(
        self,
        data: str,
        analysis_type: str,
        confidence_level: float = 0.95
    ) -> str:
        """
        Construct a prompt for data analysis.
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis to perform
            confidence_level: Statistical confidence level
            
        Returns:
            str: Constructed prompt
        """
        return f"""
        Perform a {analysis_type} analysis of this data with {confidence_level} confidence level:
        
        {data}
        
        Please include:
        1. Key trends and patterns
        2. Statistical summary (mean, median, variance)
        3. Confidence intervals where applicable
        4. Recommendations based on the analysis
        """
    
    def analyze_data(
        self,
        data: str,
        analysis_type: str = "comprehensive",
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Analyze data using LLM capabilities.
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis to perform
            confidence_level: Statistical confidence level
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        prompt = self._construct_analysis_prompt(
            data=data,
            analysis_type=analysis_type,
            confidence_level=confidence_level
        )
        return self.generate_structured_response(prompt)

def demonstrate_custom_agent(model: str = "gemma2:9b"):
    """Show how to use a custom agent."""
    print("\n=== Custom Agent Demo ===")
    print(f"Using model: {model}")
    
    try:
        # Create custom agent
        analyst = DataAnalysisAgent(model=model)
        
        # Show available tasks
        print("\nAvailable tasks:")
        for category, tasks in analyst.tasks.items():
            print(f"\n{category.upper()}:")
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
        result = analyst.analyze_data(
            data=data,
            analysis_type="statistical",
            confidence_level=0.95
        )
        
        if result["status"] == "success":
            print("\nAnalysis Results:")
            print(result["response"])
        else:
            print("\nError during analysis:", result["message"])
            
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        print("Please check that you're using a supported model and have set up the framework correctly.")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Custom Agent Example")
    parser.add_argument(
        "--model",
        default="gemma2:9b",
        help="Name of the Ollama model to use"
    )
    args = parser.parse_args()
    
    demonstrate_custom_agent(model=args.model)

if __name__ == "__main__":
    main()
