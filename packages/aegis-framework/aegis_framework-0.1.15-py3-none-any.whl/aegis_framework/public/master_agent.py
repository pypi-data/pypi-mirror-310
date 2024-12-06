"""
Public interface for the Master AI Agent.
Provides a simplified interface to the core agent functionality.
"""

from typing import Dict, Any, List
from ..core.master_agent import CoreMasterAgent

class MasterAIAgent:
    """Public interface for the Master AI Agent."""
    
    def __init__(self, model: str = "gemma2:9b"):
        """
        Initialize the Master AI Agent.
        
        Args:
            model: Name of the LLM model to use
        """
        self._core = CoreMasterAgent(model=model)
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question using the agent's capabilities.
        
        Args:
            question: The question to answer
            
        Returns:
            str: The agent's response
        """
        return self._core.answer_question(question)
    
    def perform_task(self, task: str) -> Dict[str, Any]:
        """
        Perform a specified task using the agent's capabilities.
        
        Args:
            task: The task to perform
            
        Returns:
            Dict[str, Any]: Task result
        """
        return self._core.perform_task(task)
    
    def get_task_list(self) -> List[str]:
        """
        Get a list of all available tasks.
        
        Returns:
            List[str]: List of available tasks
        """
        return self._core.get_task_list()
    
    def get_suggested_prompts(self) -> List[str]:
        """
        Get a list of suggested prompts.
        
        Returns:
            List[str]: List of suggested prompts
        """
        return self._core.generate_suggested_prompts()
