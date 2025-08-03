#!/usr/bin/env python3
"""
Test script for the refactored LLM Quiz Challenge library.

This demonstrates the new modular design and notebook-friendly interface.
"""

import os
import sys
from pathlib import Path

# Add the grading-toolkit to Python path
sys.path.insert(0, str(Path(__file__).parent))

from llm_quiz import LLMQuizChallenge

def test_basic_usage():
    """Test basic usage with the new interface."""
    print("🔧 Testing Basic Usage")
    print("="*50)
    
    # Get API key from environment
    api_key = os.getenv("CHAT_API", "dummy-key-for-testing")
    
    try:
        # Initialize with clean interface
        challenge = LLMQuizChallenge(api_key=api_key)
        print("✅ Successfully initialized LLMQuizChallenge")
        
        # Test connection (will likely fail with dummy key, but tests the interface)
        print("🔗 Testing connection...")
        connection_ok = challenge.test_connection()
        print(f"Connection test: {'✅ Success' if connection_ok else '❌ Failed (expected with dummy key)'}")
        
        return challenge
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        return None

def test_question_validation():
    """Test question validation without running full challenge."""
    print("\n📝 Testing Question Validation")
    print("="*50)
    
    # Get API key from environment  
    api_key = os.getenv("CHAT_API", "dummy-key-for-testing")
    
    try:
        challenge = LLMQuizChallenge(api_key=api_key)
        
        # Test questions
        test_questions = [
            {
                "question": "What is 2 + 2?",
                "answer": "4"
            },
            {
                "question": "Calculate the derivative of x^2 + 3x + 5 with respect to x using advanced calculus methods",
                "answer": "2x + 3"
            }
        ]
        
        print("🔍 Validating questions...")
        validation_summary = challenge.validate_questions_only(test_questions)
        
        print(f"Total Questions: {validation_summary['total_questions']}")
        print(f"Valid Questions: {validation_summary['valid_questions']}")
        print(f"Invalid Questions: {validation_summary['invalid_questions']}")
        print(f"Validation Rate: {validation_summary['validation_rate']:.1%}")
        
        if validation_summary['common_issues']:
            print("Common Issues:", validation_summary['common_issues'])
        
        if validation_summary['recommendations']:
            print("Recommendations:")
            for rec in validation_summary['recommendations']:
                print(f"  • {rec}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return False

def test_modular_components():
    """Test individual modular components."""
    print("\n🧩 Testing Modular Components")
    print("="*50)
    
    try:
        # Test ContentLoader
        from llm_quiz import ContentLoader
        
        content_loader = ContentLoader()
        print("✅ ContentLoader initialized")
        
        # Test with example URLs (will fail but tests interface)
        test_urls = [
            "https://raw.githubusercontent.com/example/repo/main/file1.md",
            "https://example.com/content.txt"
        ]
        
        print("🔗 Testing content loading...")
        summary = content_loader.get_load_summary(test_urls)
        print(f"Load summary: {summary['total_urls']} URLs, {summary['successful_loads']} successful")
        
        # Test LLMClient
        from llm_quiz import LLMClient
        
        client = LLMClient("https://api.openai.com/v1", "dummy-key")
        print("✅ LLMClient initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing modular components: {e}")
        return False

def test_notebook_interface():
    """Test notebook-friendly methods."""
    print("\n📓 Testing Notebook Interface")
    print("="*50)
    
    api_key = os.getenv("CHAT_API", "dummy-key-for-testing")
    
    try:
        # Quick setup method
        challenge = LLMQuizChallenge.quick_setup(api_key)
        print("✅ Quick setup successful")
        
        # Test with programmatic questions
        questions = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 5 + 3?", "answer": "8"}
        ]
        
        print("🏃 Testing quick run with programmatic questions...")
        
        # This would normally run the full challenge, but will fail with dummy key
        try:
            results = challenge.run_quiz_from_questions(questions, "Test Quiz")
            challenge.print_summary(results)
            
        except Exception as e:
            print(f"Expected failure with dummy key: {str(e)[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing notebook interface: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Refactored LLM Quiz Challenge Library")
    print("="*60)
    
    # Test basic usage
    challenge = test_basic_usage()
    
    # Test validation
    validation_ok = test_question_validation()
    
    # Test modular components
    modular_ok = test_modular_components()
    
    # Test notebook interface
    notebook_ok = test_notebook_interface()
    
    print("\n📊 Test Summary")
    print("="*30)
    print(f"Basic Usage: {'✅' if challenge else '❌'}")
    print(f"Validation: {'✅' if validation_ok else '❌'}")
    print(f"Modular Components: {'✅' if modular_ok else '❌'}")
    print(f"Notebook Interface: {'✅' if notebook_ok else '❌'}")
    
    all_tests_passed = all([challenge, validation_ok, modular_ok, notebook_ok])
    
    print(f"\n🎯 Overall Result: {'✅ All tests passed!' if all_tests_passed else '❌ Some tests failed'}")
    
    if challenge:
        print("\n💡 To test with a real API key, set the CHAT_API environment variable:")
        print("   export CHAT_API=your-api-key")
        print("   python test_refactored.py")

if __name__ == "__main__":
    main()