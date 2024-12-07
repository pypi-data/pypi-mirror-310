"""
Design Agent: Specialized agent for creating and optimizing new agents within the framework.
This agent focuses on designing, generating, and improving other agents to enhance the overall system's capabilities.
"""

import os
import time
import logging
import subprocess
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
AGENT_DESIGNS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent_designs")
DESIGN_INTERVAL = 7200  # 2 hours in seconds

class CoreDesignAgent:
    """Core implementation of the Design Agent with proprietary features."""
    
    def __init__(self, model: str = "gemma2:9b"):
        """Initialize the Design Agent with advanced features."""
        from .ollama_model import OllamaLocalModel
        self.design_model = OllamaLocalModel(model=model)
        self.review_model = OllamaLocalModel(model=model)
        self.last_design_time = datetime.now() - timedelta(hours=2)
        self.design_thread = None
        self.running = False
        
        # Create designs directory if it doesn't exist
        os.makedirs(AGENT_DESIGNS_DIR, exist_ok=True)
        
    def start_periodic_design(self):
        """Start the periodic design generation thread."""
        if self.design_thread is None or not self.design_thread.is_alive():
            self.running = True
            self.design_thread = threading.Thread(target=self._design_loop)
            self.design_thread.daemon = True
            self.design_thread.start()
            logger.info("Started periodic design generation")
            return "Started periodic design generation"
    
    def stop_periodic_design(self):
        """Stop the periodic design generation."""
        self.running = False
        if self.design_thread:
            self.design_thread.join()
            logger.info("Stopped periodic design generation")
            return "Stopped periodic design generation"
    
    def _design_loop(self):
        """Main loop for periodic design generation."""
        while self.running:
            now = datetime.now()
            if (now - self.last_design_time).total_seconds() >= DESIGN_INTERVAL:
                try:
                    self.generate_new_design()
                    self.last_design_time = now
                except Exception as e:
                    logger.error(f"Error in design loop: {str(e)}")
            time.sleep(60)
    
    def generate_new_design(self, context: Optional[str] = None) -> Dict[str, Any]:
        """Generate a new agent design."""
        try:
            design_prompt = self._construct_design_prompt(context)
            design = self.design_model.generate(design_prompt)
            
            # Generate unique name based on context or default
            purpose = context if context else "agent"
            class_name = self._generate_unique_name(purpose)
            
            # Save the design
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            design_dir = os.path.join(AGENT_DESIGNS_DIR, f"{class_name}_{timestamp}")
            os.makedirs(design_dir, exist_ok=True)
            
            # Save README.md
            readme_path = os.path.join(design_dir, "README.md")
            with open(readme_path, "w") as f:
                f.write(f"""# {class_name}

{design}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
            
            logger.info(f"Generated new design: {class_name}")
            return {
                "status": "success",
                "design": design,
                "class_name": class_name,
                "path": readme_path
            }
            
        except Exception as e:
            logger.error(f"Error generating design: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _generate_unique_name(self, purpose: str) -> str:
        """Generate a unique, meaningful name for the agent."""
        # Clean and format the purpose string
        words = purpose.lower().replace("agent", "").replace("for", "").strip()
        words = ''.join(c for c in words if c.isalnum() or c.isspace())
        words = words.split()
        
        # Create camel case name
        name_parts = [word.capitalize() for word in words]
        base_name = ''.join(name_parts) + "Agent"
        
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime("%H%M%S")
        return f"{base_name}_{timestamp}"
    
    def _construct_design_prompt(self, context: Optional[str] = None) -> str:
        """Construct the design generation prompt."""
        if context:
            prompt = f"""Design an AI agent for: {context}

Please provide a detailed design including:
1. Purpose and capabilities
2. Key features and functionalities
3. Integration points
4. Required dependencies
5. Implementation considerations
"""
        else:
            prompt = """Design a new AI agent with innovative capabilities.

Please provide a detailed design including:
1. Purpose and capabilities
2. Key features and functionalities
3. Integration points
4. Required dependencies
5. Implementation considerations
"""
        return prompt
    
    def run_task(self, task_description: str) -> Dict[str, Any]:
        """Handle various design-related tasks."""
        try:
            return self.generate_new_design(context=task_description)
        except Exception as e:
            logger.error(f"Error running task: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
