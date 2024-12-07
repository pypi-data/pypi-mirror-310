from aegis_framework import MasterAIAgent, DesignAgent

# Initialize a master agent
agent = MasterAIAgent(model="gemma2:9b")

# Generate responses
response = agent.answer_question(
    "What are the key principles of multi-agent systems?"
)
print(response)

# Create a specialized design agent
designer = DesignAgent(model="gemma2:9b")
design = designer.generate_new_design(
    context="""Design an AI agent for:
    - Type: Microservices architecture
    - Requirements:
        * Scalability
        * Fault-tolerance
    Please provide a detailed design including:
    1. Architecture overview
    2. Key components
    3. Integration points
    4. Implementation considerations"""
)
print(design)
