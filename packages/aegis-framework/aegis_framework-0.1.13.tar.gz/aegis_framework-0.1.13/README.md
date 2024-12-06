# Aegis Multi-Agent Framework

A powerful framework for creating multi-agent AI colonies, with support for local LLM integration through Ollama.

## Features

- 🤖 Multi-agent system architecture
- 🔄 Seamless Ollama LLM integration
- 🛠️ Easy-to-use API
- 📚 Comprehensive examples
- 🔌 Extensible design

## Installation

### Prerequisites

1. Python 3.8 or higher
2. [Ollama](https://ollama.ai) (optional, for LLM integration)

### Install from PyPI

```bash
pip install aegis-framework
```

### Install from Source

```bash
git clone https://github.com/metisos/aegis_framework.git
cd aegis_framework
pip install -e .
```

## Quick Start


### Basic Usage (With Ollama LLM)

```python
from aegis_framework import MasterAIAgent, OllamaLocalModel

# Initialize Ollama model
llm = OllamaLocalModel(model="llama2")  # or any other Ollama model

# Create an agent with LLM
agent = MasterAIAgent(name="LLM Agent", llm=llm)

# Ask questions
response = agent.answer_question("Explain quantum computing")
print(response)
```

## Coding Assistant Example

The framework includes a powerful coding assistant example that can help with various programming tasks:

```python
from aegis_framework import MasterAIAgent, OllamaLocalModel

def create_coding_agent():
    """Create an AI agent specialized for coding tasks"""
    llm = OllamaLocalModel(model="llama2")
    return MasterAIAgent(name="Code Assistant", llm=llm)

# Create the coding agent
agent = create_coding_agent()

# Example coding tasks
coding_questions = [
    "Write a Python function that implements binary search",
    "Create a Flask REST API endpoint",
    "Write unit tests for email validation"
]

# Get coding assistance
for question in coding_questions:
    print(f"\nQuestion: {question}")
    response = agent.answer_question(question)
    print(f"Response: {response}")
```

See `coding_agent_example.py` for a complete example with interactive mode.

## Sample Scripts

The package includes several example scripts:

1. `sample_usage.py`: Basic usage examples
2. `coding_agent_example.py`: Coding assistant implementation

## Configuration

### Supported Ollama Models

You can use any model available in Ollama. Some recommended models:

- llama2
- codellama
- mistral
- gemma

To use a specific model:
```python
llm = OllamaLocalModel(model="your_preferred_model")
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- Author: Metis Analytics
- Email: cjohnson@metisos.com
- GitHub: https://github.com/metisos/aegis_framework

## Acknowledgments

- Thanks to the Ollama team for their excellent LLM runtime
- All contributors and users of the framework