"""
OllamaLocalModel: Core implementation of local LLM using Ollama.
"""

import os
import json
import requests
from typing import Optional, Dict, Any, List

class OllamaLocalModel:
    """
    Core implementation of local LLM using Ollama.
    """
    
    def __init__(self, model: str = "gemma2:9b"):
        """
        Initialize the Ollama model for local inference.
        
        Args:
            model: Name of the model to use
        """
        self.model = model
        self.api_base = "http://localhost:11434/api"
        self.simulation_mode = False
        self._validate_model()
        
    def _get_installed_models(self) -> List[str]:
        """Get list of installed Ollama models."""
        try:
            response = requests.get(f"{self.api_base}/tags")
            if response.status_code == 200:
                return [tag["name"] for tag in response.json()["models"]]
        except requests.exceptions.RequestException:
            pass
        return []
        
    def _validate_model(self) -> None:
        """Validate that the model exists locally."""
        installed_models = self._get_installed_models()
        
        if not installed_models:
            print("Warning: Could not get installed models. Running in simulation mode.")
            self.simulation_mode = True
            return
            
        if self.model not in installed_models:
            print(f"Warning: Model {self.model} not found. Available models: {installed_models}")
            print("Running in simulation mode.")
            self.simulation_mode = True
            return
            
    def _pull_model(self) -> None:
        """Pull the model from Ollama."""
        try:
            response = requests.post(f"{self.api_base}/pull", json={"name": self.model})
            if response.status_code != 200:
                print(f"Warning: Failed to pull model {self.model}. Running in simulation mode.")
                self.simulation_mode = True
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to pull model: {str(e)}. Running in simulation mode.")
            self.simulation_mode = True
            
    def generate(self, prompt: str) -> str:
        """
        Generate a response using local inference.
        
        Args:
            prompt: Input prompt for the model
            
        Returns:
            str: Generated response
        """
        if self.simulation_mode:
            return self._simulate_response(prompt)
            
        try:
            response = requests.post(
                f"{self.api_base}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                print(f"Warning: Failed to generate response: {response.text}. Falling back to simulation mode.")
                self.simulation_mode = True
                return self._simulate_response(prompt)
                
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to generate response: {str(e)}. Falling back to simulation mode.")
            self.simulation_mode = True
            return self._simulate_response(prompt)
    
    def _simulate_response(self, prompt: str) -> str:
        """Generate a simulated response when Ollama is not available."""
        return f"[Local {self.model}] Response to: {prompt}\n" + \
               "This is a simulated response as Ollama is not available. " + \
               "To get real responses, please install and run Ollama: https://ollama.ai"
               
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            "name": self.model,
            "api_base": self.api_base,
            "simulation_mode": self.simulation_mode,
            "installed_models": self._get_installed_models()
        }
