"""
Public interfaces for the Aegis Framework.
"""

from .master_agent import MasterAIAgent
from .ollama_model import OllamaLocalModel
from .design_agent import DesignAgent

__all__ = [
    "MasterAIAgent",
    "OllamaLocalModel",
    "DesignAgent"
]
