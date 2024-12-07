"""
MasterAIAgent: Core agent class for the Aegis Framework.
Contains proprietary implementation of the master agent functionality.
"""

import json
from typing import Optional, Dict, Any, List
from .ollama_model import OllamaLocalModel

class CoreMasterAgent:
    """
    Core agent class for managing AI agents and tasks.
    Contains proprietary implementation.
    """
    
    def __init__(self, model: str = "gemma2:9b"):
        """
        Initialize the MasterAIAgent.
        
        Args:
            model: Name of the Ollama model to use
        """
        self.llm = OllamaLocalModel(model=model)
        self.agent_task_map = {
            "general": ["answer questions", "analyze text", "generate content"],
            "data_analysis": ["analyze data", "statistical analysis", "data visualization"],
            "design": ["design agent", "create new agent", "agent architecture"]
        }
        self.suggested_prompts = self.generate_suggested_prompts()

    def generate_suggested_prompts(self) -> List[str]:
        """Generate a list of suggested prompts."""
        return [
            "How do I implement a neural network?",
            "What are the best practices for code review?",
            "Explain the concept of recursion"
        ]

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using the LLM.
        
        Args:
            prompt: Input prompt for the model
            
        Returns:
            str: Generated response
        """
        try:
            response = self.llm.generate(prompt)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_structured_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a structured response using the LLM.
        
        Args:
            prompt: Input prompt for the model
            
        Returns:
            Dict[str, Any]: Structured response
        """
        try:
            response = self.generate_response(prompt)
            return {
                "status": "success",
                "response": response,
                "model": self.llm.model
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": self.llm.model
            }

    def answer_question(self, question: str) -> str:
        """
        Answer a question using the agent's capabilities.
        
        Args:
            question: The question to answer
            
        Returns:
            str: The agent's response
        """
        prompt = f"Please answer this question: {question}"
        return self.generate_response(prompt)

    def perform_task(self, task: str) -> Dict[str, Any]:
        """
        Perform a specified task using the agent's capabilities.
        
        Args:
            task: The task to perform
            
        Returns:
            Dict[str, Any]: Task result
        """
        return self.generate_structured_response(task)

    def get_task_list(self) -> List[str]:
        """Get a list of all available tasks."""
        tasks = []
        for task_group in self.agent_task_map.values():
            tasks.extend(task_group)
        return tasks
