# Aegis Framework

A comprehensive, extensible AI agent framework with local LLM integration.

## Version 0.1.14

### Features

- Modular agent architecture
- Local LLM integration with Ollama
- Simplified public interfaces
- Extensible design patterns
- Real-time task monitoring
- Database insights tracking
- Flexible model selection

## Installation

```bash
pip install aegis-framework
```

For web interface support:
```bash
pip install aegis-framework[web]
```

## Quick Start

```python
from aegis_framework import MasterAIAgent, DesignAgent

# Create a basic agent
agent = MasterAIAgent(model="gemma2:9b")

# Ask questions
response = agent.answer_question("What are the key principles of AI?")
print(response)

# Generate designs
designer = DesignAgent()
design = designer.generate_new_design()
print(design)
```

## Creating Custom Agents

```python
from aegis_framework import MasterAIAgent

class DataAnalysisAgent(MasterAIAgent):
    def __init__(self, model: str = "codellama"):
        super().__init__(model=model)
        self.agent_task_map.update({
            "data_analysis": [
                "analyze data",
                "run analysis",
                "statistical test"
            ]
        })
    
    def analyze_data(self, data: str) -> str:
        return self.generate_response(f"Analyze this data: {data}")

# Use custom agent
analyst = DataAnalysisAgent()
result = analyst.analyze_data("Your data here")
```

## Requirements

- Python 3.7+
- Ollama (for local LLM support)

## Optional Dependencies

- Flask & Flask-SocketIO (for web interface)
- fuzzywuzzy (for enhanced text matching)
- sqlite3-api (for database insights)

## Documentation

For detailed documentation and examples, visit our [GitHub repository](https://github.com/metisos/aegis-framework).

## License

MIT License. See LICENSE file for details.

## Contact

- Author: Metis Analytics
- Email: cjohnson@metisos.com