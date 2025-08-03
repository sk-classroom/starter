#!/usr/bin/env python3
"""
Example usage of the TOML quiz format
Demonstrates how to create and use different question types
"""

from quiz_parser import QuizParser
import json


def create_simple_quiz():
    """Create a simple quiz with different question types"""
    quiz_content = """
# Simple Quiz Example
title = "Network Science Basics"
description = "A simple quiz to test network science knowledge"
version = "1.0"
total_points = 50

# Multiple Choice Question
[[questions]]
id = "mc1"
type = "multiple_choice"
points = 10
difficulty = "easy"
topic = "basics"
question = "What is a node in a network?"
[questions.options]
A = "A connection between two points"
B = "A point or entity in the network"
C = "A path through the network"
D = "A measure of network density"
questions.correct_answer = "B"
questions.explanation = "A node represents an entity or point in the network."

# Free-form Question
[[questions]]
id = "ff1"
type = "free_form"
points = 15
difficulty = "medium"
topic = "concepts"
question = "Explain what the friendship paradox is and why it occurs."
[questions.validation]
min_words = 30
max_words = 100
required_keywords = ["friendship paradox", "sampling bias", "high-degree"]
case_sensitive = false
questions.sample_answer = "The friendship paradox occurs because people with many friends appear more frequently in others' friend lists, creating a sampling bias where your friends seem to have more friends than you do."

# Numerical Question
[[questions]]
id = "num1"
type = "numerical"
points = 10
difficulty = "medium"
topic = "calculations"
question = "In a network with 5 nodes where each node connects to 2 others, how many edges are there in total?"
[questions.validation]
min_value = 0
max_value = 20
tolerance = 0.1
unit = "edges"
questions.correct_answer = 5.0
questions.explanation = "With 5 nodes each having degree 2, the total degree sum is 10. Since each edge contributes to 2 degrees, there are 10/2 = 5 edges."

# True/False Question
[[questions]]
id = "tf1"
type = "true_false"
points = 5
difficulty = "easy"
topic = "theory"
question = "In an undirected network, the adjacency matrix is symmetric."
questions.correct_answer = true
questions.explanation = "In undirected networks, if node A connects to node B, then B also connects to A, making the adjacency matrix symmetric."

# Matching Question
[[questions]]
id = "match1"
type = "matching"
points = 10
difficulty = "medium"
topic = "definitions"
question = "Match each network concept with its definition:"
[questions.left_items]
A = "Degree"
B = "Clustering Coefficient"
C = "Betweenness Centrality"
D = "Eigenvector Centrality"
[questions.right_items]
1 = "Number of connections a node has"
2 = "Fraction of neighbors that are also connected"
3 = "Fraction of shortest paths passing through a node"
4 = "Importance based on neighbors' importance"
[questions.correct_matches]
A = "1"
B = "2"
C = "3"
D = "4"
questions.explanation = "Each centrality measure captures different aspects of node importance."
"""

    with open("simple_quiz.toml", "w") as f:
        f.write(quiz_content)

    print("Created simple_quiz.toml")


def demonstrate_usage():
    """Demonstrate how to use the quiz parser"""
    print("=== TOML Quiz Format Demonstration ===\n")

    # Create a simple quiz
    create_simple_quiz()

    # Load and parse the quiz
    parser = QuizParser("simple_quiz.toml")
    quiz = parser.load_quiz()

    # Show quiz summary
    summary = parser.get_quiz_summary()
    print("Quiz Summary:")
    print(f"  Title: {summary['title']}")
    print(f"  Total Points: {summary['total_points']}")
    print(f"  Questions: {summary['total_questions']}")
    print(f"  Question Types: {summary['question_types']}")
    print()

    # Demonstrate answer validation
    print("=== Answer Validation Examples ===\n")

    # Multiple choice validation
    print("1. Multiple Choice Question:")
    result = parser.validate_answer("mc1", "B")
    print(f"   Answer: B")
    print(f"   Result: {result['feedback']}")
    print(f"   Score: {result['score']}/10")
    print()

    # Free-form validation
    print("2. Free-form Question:")
    sample_answer = "The friendship paradox occurs because people with many friends appear more frequently in friend lists, creating sampling bias where your friends seem to have more friends than you do."
    result = parser.validate_answer("ff1", sample_answer)
    print(f"   Answer: {sample_answer[:50]}...")
    print(f"   Result: {result['feedback']}")
    print(f"   Score: {result['score']}/15")
    print()

    # Numerical validation
    print("3. Numerical Question:")
    result = parser.validate_answer("num1", 5.0)
    print(f"   Answer: 5.0")
    print(f"   Result: {result['feedback']}")
    print(f"   Score: {result['score']}/10")
    print()

    # True/False validation
    print("4. True/False Question:")
    result = parser.validate_answer("tf1", True)
    print(f"   Answer: True")
    print(f"   Result: {result['feedback']}")
    print(f"   Score: {result['score']}/5")
    print()

    # Matching validation
    print("5. Matching Question:")
    matching_answer = {"A": "1", "B": "2", "C": "3", "D": "4"}
    result = parser.validate_answer("match1", matching_answer)
    print(f"   Answer: {matching_answer}")
    print(f"   Result: {result['feedback']}")
    print(f"   Score: {result['score']}/10")
    print()


def show_question_types():
    """Show the different question types supported"""
    print("=== Supported Question Types ===\n")

    question_types = {
        "multiple_choice": {
            "description": "Questions with predefined answer options (A, B, C, D)",
            "validation": "Exact match with correct answer",
            "example": "What is a node in a network? A) Connection B) Point C) Path D) Measure"
        },
        "free_form": {
            "description": "Open-ended text responses",
            "validation": "Word count, required keywords, code detection",
            "example": "Explain the friendship paradox in your own words."
        },
        "numerical": {
            "description": "Questions requiring numerical answers",
            "validation": "Exact match with tolerance",
            "example": "Calculate the average degree of this network."
        },
        "true_false": {
            "description": "True or false statements",
            "validation": "Boolean comparison",
            "example": "The adjacency matrix of an undirected network is symmetric. (True/False)"
        },
        "matching": {
            "description": "Matching items from two lists",
            "validation": "Partial credit for correct matches",
            "example": "Match each centrality measure with its definition."
        }
    }

    for q_type, info in question_types.items():
        print(f"{q_type.upper()}:")
        print(f"  Description: {info['description']}")
        print(f"  Validation: {info['validation']}")
        print(f"  Example: {info['example']}")
        print()


if __name__ == "__main__":
    show_question_types()
    print("\n" + "="*50 + "\n")
    demonstrate_usage()