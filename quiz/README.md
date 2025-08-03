# TOML Quiz Format

This directory contains a flexible quiz system using TOML files to define questions that can be multiple choice or free-form. The system supports various question types with automatic validation and scoring.

## Features

- **Multiple Question Types**: Multiple choice, free-form text, numerical, true/false, and matching questions
- **Flexible Validation**: Word count limits, required keywords, code detection, numerical tolerance
- **Automatic Scoring**: Built-in scoring algorithms for each question type
- **Rich Metadata**: Difficulty levels, topics, explanations, and sample answers
- **Easy to Extend**: Simple TOML format that's human-readable and easy to modify

## Question Types

### 1. Multiple Choice (`multiple_choice`)

Standard multiple choice questions with predefined options.

```toml
[[questions]]
id = "q1"
type = "multiple_choice"
points = 10
difficulty = "medium"
topic = "euler_tour"
question = "What is the friendship paradox?"
[questions.options]
A = "People have fewer friends than they think"
B = "Your friends have more friends than you do"
C = "Everyone has the same number of friends"
D = "Friendship is an illusion"
questions.correct_answer = "B"
questions.explanation = "The friendship paradox occurs due to sampling bias."
```

### 2. Free-form Text (`free_form`)

Open-ended questions with customizable validation rules.

```toml
[[questions]]
id = "q2"
type = "free_form"
points = 20
difficulty = "medium"
topic = "small_world"
question = "Explain the small-world phenomenon in network science."
[questions.validation]
min_words = 50
max_words = 200
required_keywords = ["six degrees", "Milgram", "shortest path"]
case_sensitive = false
questions.sample_answer = "The small-world phenomenon describes..."
```

### 3. Numerical (`numerical`)

Questions requiring numerical answers with tolerance.

```toml
[[questions]]
id = "q3"
type = "numerical"
points = 10
difficulty = "medium"
topic = "calculations"
question = "Calculate the average degree of this network."
[questions.validation]
min_value = 0.0
max_value = 10.0
tolerance = 0.01
unit = "degree"
questions.correct_answer = 2.5
questions.explanation = "Sum all degrees and divide by number of nodes."
```

### 4. True/False (`true_false`)

Simple true or false statements.

```toml
[[questions]]
id = "q4"
type = "true_false"
points = 5
difficulty = "easy"
topic = "theory"
question = "In an undirected network, the adjacency matrix is symmetric."
questions.correct_answer = true
questions.explanation = "Undirected networks have symmetric adjacency matrices."
```

### 5. Matching (`matching`)

Match items from two lists.

```toml
[[questions]]
id = "q5"
type = "matching"
points = 15
difficulty = "medium"
topic = "definitions"
question = "Match each centrality measure with its definition:"
[questions.left_items]
A = "Degree Centrality"
B = "Betweenness Centrality"
[questions.right_items]
1 = "Number of connections"
2 = "Fraction of shortest paths"
[questions.correct_matches]
A = "1"
B = "2"
questions.explanation = "Each centrality measure captures different aspects."
```

## Validation Options

### For Free-form Questions

- `min_words`: Minimum word count required
- `max_words`: Maximum word count allowed
- `required_keywords`: List of keywords that must be present
- `case_sensitive`: Whether keyword matching is case-sensitive
- `code_required`: Whether code structure is expected
- `language`: Programming language if code is required
- `required_functions`: List of functions that should be used
- `max_lines`: Maximum number of lines allowed

### For Numerical Questions

- `min_value`: Minimum acceptable value
- `max_value`: Maximum acceptable value
- `tolerance`: Acceptable deviation from correct answer
- `unit`: Unit of measurement (for display)

## Usage

### Basic Usage

```python
from quiz_parser import QuizParser

# Load a quiz
parser = QuizParser("quiz.toml")
quiz = parser.load_quiz()

# Validate an answer
result = parser.validate_answer("q1", "B")
print(f"Score: {result['score']}")
print(f"Feedback: {result['feedback']}")
```

### Running Examples

```bash
# Run the example usage
python example_usage.py

# Run the main parser
python quiz_parser.py
```

## File Structure

```
quiz/
├── quiz.toml              # Main quiz file with all question types
├── quiz_parser.py         # Parser and validation logic
├── example_usage.py       # Example usage and demonstrations
├── simple_quiz.toml       # Simple example quiz
└── README.md             # This file
```

## Quiz Metadata

Each quiz file should start with metadata:

```toml
title = "Quiz Title"
description = "Quiz description"
version = "1.0"
total_points = 100
```

## Question Metadata

Each question can include:

- `id`: Unique identifier for the question
- `type`: Question type (multiple_choice, free_form, numerical, true_false, matching)
- `points`: Point value for the question
- `difficulty`: Difficulty level (easy, medium, hard)
- `topic`: Topic category for organization
- `question`: The question text
- `correct_answer`: The correct answer
- `explanation`: Explanation of the correct answer
- `sample_answer`: Example answer (for free-form questions)
- `image`: Reference to an image file (optional)

## Scoring

- **Multiple Choice**: Full points for correct answer, 0 for incorrect
- **Free-form**: Partial credit based on word count (30%), keywords (40%), and code structure (30%)
- **Numerical**: Full points if within tolerance, 0 otherwise
- **True/False**: Full points for correct answer, 0 for incorrect
- **Matching**: Partial credit proportional to correct matches

## Extending the System

To add new question types:

1. Add the new type to the `QuestionType` enum in `quiz_parser.py`
2. Add validation logic in the `QuizParser` class
3. Update the TOML structure to support the new type
4. Add example usage

## Tips for Writing Questions

1. **Be Specific**: Clear, unambiguous questions work best
2. **Use Validation**: Set appropriate word limits and required keywords for free-form questions
3. **Provide Explanations**: Always include explanations to help students learn
4. **Test Your Questions**: Use the parser to test your questions before deployment
5. **Organize by Topic**: Use the topic field to organize questions by subject area
6. **Vary Difficulty**: Mix easy, medium, and hard questions appropriately

## Example Quiz Structure

See `quiz.toml` for a complete example with all question types, or `simple_quiz.toml` for a basic example.