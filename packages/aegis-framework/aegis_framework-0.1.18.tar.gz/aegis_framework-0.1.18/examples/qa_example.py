#!/usr/bin/env python3
from aegis_framework import MasterAIAgent

def test_model(model_name: str, question: str):
    print(f"\n=== Testing {model_name} ===")
    agent = MasterAIAgent(model=model_name)
    print(f"Question: {question}")
    response = agent.answer_question(question)
    print(f"Response: {response}")
    print("=" * 80)

def main():
    # Test question
    question = "What are the key principles of software engineering?"
    
    # Test with different models
    models = [
        "llama2:13b",       # Large model
        "qwen2.5-coder",    # Coding-specific model
        "llama3.2",         # Latest llama
        "tinydolphin"       # Small model
    ]
    
    print("=== AI Model Comparison Demo ===")
    print("Testing software engineering question with different models...")
    
    for model in models:
        test_model(model, question)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting the program...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
