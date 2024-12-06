"""
Example showing how to create and use custom agents with the Aegis Framework.
"""

from aegis_framework import MasterAIAgent, DesignAgent
from aegis_framework.public.design_agent import run_design_task

class DataAnalysisAgent(MasterAIAgent):
    """Custom agent specialized for data analysis tasks."""
    
    def __init__(self, model: str = "codellama"):
        super().__init__(model=model)
        
        # Add data analysis specific tasks
        self.agent_task_map.update({
            "data_analysis": [
                "analyze data",
                "run analysis",
                "data visualization",
                "statistical test",
                "data insights"
            ]
        })
    
    def analyze_data(self, data_description: str) -> str:
        """
        Analyze data using LLM capabilities.
        
        Args:
            data_description: Description of data and analysis needed
            
        Returns:
            str: Analysis results
        """
        return self.perform_task(f"Analyze this data: {data_description}")

def demonstrate_custom_agent():
    """Show how to use a custom agent."""
    print("\n=== Custom Agent Demo ===")
    
    # Create custom agent
    analyst = DataAnalysisAgent()
    
    # Show available tasks
    print("\nAvailable analysis tasks:")
    for task in analyst.agent_task_map["data_analysis"]:
        print(f"- {task}")
    
    # Run analysis
    data = """
    Monthly sales data for 2023:
    Jan: $10,000
    Feb: $12,000
    Mar: $15,000
    Apr: $11,000
    May: $13,000
    """
    
    print("\nAnalyzing sales data...")
    result = analyst.analyze_data(data)
    print(f"Analysis result: {result}")
    
    # Use design agent to create a new analysis agent
    print("\nGenerating new analysis agent design...")
    design_prompt = "design an agent for advanced time series analysis"
    design = run_design_task(design_prompt)
    print(f"New agent design: {design}")

if __name__ == "__main__":
    demonstrate_custom_agent()
