"""
Aegis Framework: A lightweight framework for creating and managing AI agents with local LLM integration.
"""

__version__ = "0.1.16"

from .public.master_agent import MasterAIAgent
from .public.ollama_model import OllamaLocalModel
from .public.design_agent import DesignAgent

__all__ = [
    "MasterAIAgent",
    "OllamaLocalModel",
    "DesignAgent"
]
