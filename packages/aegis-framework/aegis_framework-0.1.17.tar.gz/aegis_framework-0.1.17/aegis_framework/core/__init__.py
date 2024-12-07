"""Core components of the Aegis Framework."""

from .master_agent import CoreMasterAgent
from .ollama_model import OllamaLocalModel
from .design_agent import CoreDesignAgent

__all__ = ["CoreMasterAgent", "OllamaLocalModel", "CoreDesignAgent"]
