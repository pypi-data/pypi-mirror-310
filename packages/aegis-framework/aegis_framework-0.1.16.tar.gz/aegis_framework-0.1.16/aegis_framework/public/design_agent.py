"""
Public interface for the Design Agent.
Provides a simplified interface to the core design agent functionality.
"""

from typing import Optional, Dict, Any, List
from ..core.design_agent import CoreDesignAgent

class DesignAgent:
    """Public interface for the Design Agent."""
    
    def __init__(self, model: str = "llama2:13b"):
        """
        Initialize the Design Agent.
        
        Args:
            model: Name of the LLM model to use
        """
        self._core = CoreDesignAgent(model=model)
    
    def generate_new_design(self, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a new agent design.
        
        Args:
            context: Design context or requirements
            
        Returns:
            Dict containing the design specification
        """
        return self._core.generate_new_design(context)
    
    def start_periodic_design(self) -> str:
        """
        Start periodic design generation.
        
        Returns:
            str: Status message
        """
        return self._core.start_periodic_design()
    
    def stop_periodic_design(self) -> str:
        """
        Stop periodic design generation.
        
        Returns:
            str: Status message
        """
        return self._core.stop_periodic_design()

def run_design_task(task: str) -> Dict[str, Any]:
    """
    Run a design-related task.
    
    Args:
        task: Description of the design task
        
    Returns:
        Dict containing the task result
    """
    agent = DesignAgent()
    return agent.run_task(task)
