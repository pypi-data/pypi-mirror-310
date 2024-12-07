"""
Public interface for OllamaLocalModel.
"""

from ..core.ollama_model import OllamaLocalModel as CoreOllamaModel

class OllamaLocalModel(CoreOllamaModel):
    """
    Public interface for local LLM models using Ollama.
    Requires Ollama to be installed locally: https://ollama.ai
    """
    
    def __init__(self, model: str = "llama2:13b"):
        """
        Initialize the Ollama model interface.
        
        Args:
            model: Name of the Ollama model to use (e.g., "llama2:13b", "mistral", "codellama")
        """
        super().__init__(model=model)
    
    def invoke(self, prompt: str) -> str:
        """
        Generate a response using the Ollama model.
        
        Args:
            prompt: Input text to process
            
        Returns:
            str: Generated response from the model
            
        Raises:
            subprocess.CalledProcessError: If Ollama command fails
        """
        return super().invoke(prompt)
