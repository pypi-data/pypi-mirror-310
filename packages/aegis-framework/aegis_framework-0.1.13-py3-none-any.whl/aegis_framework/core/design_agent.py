"""
Design Agent: Specialized agent for creating and optimizing new agents within the framework.

This agent focuses on designing, generating, and improving other agents to enhance the overall system's capabilities.
"""

import os
import time
import logging
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from .ollama_model import OllamaLocalModel

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
AGENT_DESIGNS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent_designs")
DESIGN_INTERVAL = 7200  # 2 hours in seconds

class DesignAgent:
    """
    A specialized agent for creating and optimizing new agents within the framework.
    
    This agent can:
    1. Generate new agent designs periodically
    2. Create unique, meaningful names for agents
    3. Save and manage agent designs
    4. Run in continuous or one-off mode
    """
    
    def __init__(self, 
                 design_model: Optional[OllamaLocalModel] = None,
                 review_model: Optional[OllamaLocalModel] = None,
                 design_interval: int = DESIGN_INTERVAL):
        """
        Initialize the DesignAgent.
        
        Args:
            design_model: OllamaLocalModel for generating designs
            review_model: OllamaLocalModel for reviewing designs
            design_interval: Time between automatic designs in seconds
        """
        self.design_model = design_model or OllamaLocalModel(model="llama2:13b")
        self.review_model = review_model or OllamaLocalModel(model="llama2:13b")
        self.design_interval = design_interval
        self.last_design_time = datetime.now() - timedelta(hours=2)  # Start immediately
        self.design_thread = None
        self.running = False
        
        # Ensure designs directory exists
        os.makedirs(AGENT_DESIGNS_DIR, exist_ok=True)
        
    def start_periodic_design(self) -> str:
        """Start the periodic design generation thread."""
        if self.design_thread is None or not self.design_thread.is_alive():
            self.running = True
            self.design_thread = threading.Thread(target=self._design_loop)
            self.design_thread.daemon = True
            self.design_thread.start()
            logger.info("Started periodic design generation")
            return "Periodic design generation started"
        return "Periodic design generation already running"
    
    def stop_periodic_design(self) -> str:
        """Stop the periodic design generation."""
        self.running = False
        if self.design_thread:
            self.design_thread.join()
            logger.info("Stopped periodic design generation")
            return "Periodic design generation stopped"
        return "No periodic design generation running"
    
    def _design_loop(self):
        """Main loop for periodic design generation."""
        while self.running:
            now = datetime.now()
            if (now - self.last_design_time).total_seconds() >= self.design_interval:
                try:
                    self.generate_new_design()
                    self.last_design_time = now
                except Exception as e:
                    logger.error(f"Error in design loop: {str(e)}")
            time.sleep(60)  # Check every minute
    
    def generate_new_design(self) -> str:
        """Generate a new agent design."""
        try:
            design_prompt = """
            Generate a new agent design for the Aegis Framework.
            The agent should:
            1. Have a clear, focused purpose
            2. Solve a specific problem
            3. Be useful in a multi-agent system
            4. Be implementable with current LLM technology
            
            Return a design in this format:
            {
                "class_name": "AgentName",
                "purpose": "Clear purpose statement",
                "requirements": ["req1", "req2", ...],
                "capabilities": ["cap1", "cap2", ...],
                "interactions": ["interaction1", "interaction2", ...]
            }
            """
            
            design = self.design_model.invoke(design_prompt)
            
            # Generate unique name based on purpose
            class_name = self._generate_unique_name(design.get("purpose", ""))
            
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
            return f"Created new design at {readme_path}"
            
        except Exception as e:
            logger.error(f"Error generating design: {str(e)}")
            return f"Error: {str(e)}"

    def _generate_unique_name(self, purpose: str) -> str:
        """Generate a unique, meaningful name for the agent."""
        prompt = f"""
        Create a unique, meaningful name for an AI agent with the following purpose: {purpose}
        Requirements:
        - Name should be descriptive but concise
        - End with 'Agent'
        - No spaces (use camel case)
        - Should reflect the agent's primary function
        
        Return ONLY the name, nothing else.
        """
        name = self.design_model.invoke(prompt).strip()
        # Clean up the name
        name = ''.join(c for c in name if c.isalnum() or c == '_')
        if not name.endswith('Agent'):
            name += 'Agent'
        return name

    def run_task(self, task_description: str) -> str:
        """
        Main task handler for the design agent.
        
        Args:
            task_description: Description of the task to perform
            
        Returns:
            str: Result of the task execution
        """
        try:
            logger.info(f"Design agent received task: {task_description}")
            
            # Handle different types of design tasks
            if "start" in task_description.lower() and "periodic" in task_description.lower():
                return self.start_periodic_design()
                
            elif "stop" in task_description.lower() and "periodic" in task_description.lower():
                return self.stop_periodic_design()
                
            elif "generate" in task_description.lower() or "new design" in task_description.lower():
                return self.generate_new_design()
                
            elif "improve" in task_description.lower() or "optimize" in task_description.lower():
                return "Design improvement functionality coming soon"
                
            else:
                return "Unknown task. Try 'start periodic', 'stop periodic', or 'generate new design'"
                
        except Exception as e:
            logger.error(f"Error in run_task: {str(e)}")
            return f"Error: {str(e)}"
