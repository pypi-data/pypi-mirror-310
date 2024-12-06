"""
Advanced Design Agent Example for the Aegis Framework.

This script demonstrates the advanced capabilities of the DesignAgent,
focusing on agent design generation, optimization, and management.

Features demonstrated:
- Context-based design generation
- Design constraints handling
- Periodic design generation
- Design storage and retrieval
- Design task execution

Example usage:
    $ python design_agent_example.py
    $ python design_agent_example.py --model gemma2:9b
    $ python design_agent_example.py --task "design a trading bot"
    $ python design_agent_example.py --periodic --interval 3600
"""

import os
import time
import argparse
from typing import Dict, Any, List
from aegis_framework import DesignAgent

class DesignManager:
    """Helper class to manage and demonstrate design agent capabilities."""
    
    def __init__(self, model: str = "gemma2:9b"):
        """Initialize the design manager."""
        self.agent = DesignAgent(model=model)
        self.designs: List[Dict[str, Any]] = []
    
    def generate_design_with_constraints(
        self,
        context: str,
        constraints: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a design with specific constraints.
        
        Args:
            context: The design context or purpose
            constraints: List of design constraints
            
        Returns:
            Dict[str, Any]: Generated design
        """
        constraints = constraints or []
        context_with_constraints = f"{context}\nConstraints:\n"
        for i, constraint in enumerate(constraints, 1):
            context_with_constraints += f"{i}. {constraint}\n"
        
        design = self.agent.generate_new_design(context=context_with_constraints)
        if design.get("status") == "success":
            self.designs.append(design)
        return design
    
    def run_periodic_generation(
        self,
        interval: int = 3600,
        max_designs: int = 3
    ) -> None:
        """
        Run periodic design generation.
        
        Args:
            interval: Time between designs in seconds
            max_designs: Maximum number of designs to generate
        """
        print(f"\nStarting periodic design generation (every {interval} seconds)")
        self.agent.start_periodic_design()
        
        try:
            designs_generated = 0
            while designs_generated < max_designs:
                time.sleep(interval)
                designs_generated += 1
                print(f"\nGenerated design {designs_generated}/{max_designs}")
        
        finally:
            self.agent.stop_periodic_design()
            print("\nStopped periodic design generation")
    
    def demonstrate_capabilities(self) -> None:
        """Demonstrate various design agent capabilities."""
        # 1. Basic Design Generation
        print("\n=== Basic Design Generation ===")
        basic_design = self.generate_design_with_constraints(
            "Create an AI agent for automated code review"
        )
        print(f"Basic Design Result: {basic_design}")
        
        # 2. Constrained Design Generation
        print("\n=== Constrained Design Generation ===")
        constraints = [
            "Must be lightweight and fast",
            "Should work offline",
            "Must handle multiple programming languages",
            "Should integrate with git workflows"
        ]
        constrained_design = self.generate_design_with_constraints(
            "Create a code analysis agent",
            constraints=constraints
        )
        print(f"Constrained Design Result: {constrained_design}")
        
        # 3. Domain-Specific Designs
        print("\n=== Domain-Specific Designs ===")
        domains = [
            "financial analysis",
            "healthcare diagnostics",
            "cybersecurity monitoring"
        ]
        
        for domain in domains:
            print(f"\nGenerating design for {domain}...")
            design = self.generate_design_with_constraints(
                f"Create an AI agent for {domain}"
            )
            print(f"Design Result: {design}")
    
    def print_design_summary(self) -> None:
        """Print a summary of all generated designs."""
        print("\n=== Design Generation Summary ===")
        print(f"Total designs generated: {len(self.designs)}")
        
        for i, design in enumerate(self.designs, 1):
            print(f"\nDesign {i}:")
            print(f"Status: {design.get('status', 'unknown')}")
            print(f"Class Name: {design.get('class_name', 'unnamed')}")
            if design.get('path'):
                print(f"Saved to: {design['path']}")

def main():
    """Run the design agent demonstration."""
    parser = argparse.ArgumentParser(
        description="Demonstrate advanced DesignAgent capabilities"
    )
    parser.add_argument(
        "--model",
        default="gemma2:9b",
        help="Name of the LLM model to use"
    )
    parser.add_argument(
        "--task",
        help="Specific design task to run"
    )
    parser.add_argument(
        "--periodic",
        action="store_true",
        help="Run periodic design generation"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=3600,
        help="Interval between periodic designs in seconds"
    )
    args = parser.parse_args()
    
    try:
        manager = DesignManager(model=args.model)
        
        if args.task:
            # Run single design task
            print(f"\nGenerating design for: {args.task}")
            design = manager.generate_design_with_constraints(args.task)
            print(f"Design Result: {design}")
        
        elif args.periodic:
            # Run periodic generation
            manager.run_periodic_generation(
                interval=args.interval,
                max_designs=3
            )
        
        else:
            # Run full demonstration
            manager.demonstrate_capabilities()
        
        # Print summary
        manager.print_design_summary()
        
        print("\nDesign generation complete!")
        print("View the generated designs in their respective directories.")
        print("For more examples and documentation, visit: https://github.com/metisos/aegis-framework")
    
    except KeyboardInterrupt:
        print("\nDesign generation interrupted by user.")
    except Exception as e:
        print(f"\nError during design generation: {str(e)}")
        print("Please check that you're using a supported model and have set up the framework correctly.")

if __name__ == "__main__":
    main()
