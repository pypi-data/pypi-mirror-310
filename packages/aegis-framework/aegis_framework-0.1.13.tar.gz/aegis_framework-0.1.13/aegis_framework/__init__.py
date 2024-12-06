"""
Aegis Framework - A framework for creating multi-agent colonies
"""

__version__ = "0.1.13"
__author__ = "Metis Analytics"
__email__ = "cjohnson@metisos.com"

from .core.master_agent import MasterAIAgent
from .core.ollama_model import OllamaLocalModel
from .core.design_agent import DesignAgent

__all__ = ["MasterAIAgent", "OllamaLocalModel", "DesignAgent"]
