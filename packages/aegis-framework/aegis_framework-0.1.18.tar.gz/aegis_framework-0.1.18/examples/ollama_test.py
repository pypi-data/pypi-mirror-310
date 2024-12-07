#!/usr/bin/env python3
import requests
import json

def test_model(model_name: str, question: str):
    print(f"\n=== Testing {model_name} ===")
    print(f"Question: {question}")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": f"Please answer this question: {question}",
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result['response']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    print("=" * 80)

def main():
    # Get list of installed models
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [tag["name"] for tag in response.json()["models"]]
            print(f"Found {len(models)} installed models: {', '.join(models)}")
        else:
            print(f"Error getting models: {response.text}")
            return
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        return
    
    # Test question
    question = "What are the key principles of software engineering?"
    print("\nTesting models with software engineering question...")
    
    # Test each model
    for model in models:
        test_model(model, question)

if __name__ == "__main__":
    main()
