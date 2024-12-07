#!/usr/bin/env python3
from aegis_framework import MasterAIAgent

def main():
    # Initialize the agent
    agent = MasterAIAgent(model="gemma2:9b")
    
    # List of questions to test
    questions = [
        "What is artificial intelligence?",
        "How do neural networks work?",
        "What are the differences between supervised and unsupervised learning?",
        "Explain the concept of reinforcement learning."
    ]
    
    print("=== AI Question-Answering Demo ===\n")
    
    # Ask each question and show response
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        response = agent.answer_question(question)
        print(f"Response: {response}\n")
        print("-" * 80)

if __name__ == "__main__":
    main()
