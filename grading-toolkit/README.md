# LLM Quiz Challenge

This script implements a quiz challenge system where students create questions to try to stump an LLM.

## How it Works

1. **Students create quiz questions** in TOML format
2. **LLM attempts to answer** using `llama3.2:latest` model
3. **Evaluator judges correctness** using `gemma3:27b` model  
4. **Students win** if they can stump the LLM

## Usage

### Basic Usage (No Module Content)
```bash
export CHAT_API="your-api-key-here"
python llm_quiz_grading.py --quiz-file ../quiz/quiz.toml
```

### Enhanced Usage (With Module Content)
```bash
export CHAT_API="your-api-key-here"
python llm_quiz_grading.py --quiz-file ../quiz/quiz.toml --module m01-euler_tour
```

## Command Line Options

```bash
python llm_quiz_grading.py \
    --quiz-file ../quiz/quiz.toml \
    --output challenge_results.json \
    --base-url https://chat.binghamton.edu/api \
    --quiz-model llama3.2:latest \
    --evaluator-model gemma3:27b \
    --module m01-euler_tour
```

### Module Context System

The script looks for `llm_context.qmd` files in the dedicated llm-context directory to provide contextual information to the quiz-taking LLM. 

**Expected file locations:**
- `docs/lecture-note/llm-context/intro.qmd`
- `docs/lecture-note/llm-context/m01-euler_tour.qmd` 
- `docs/lecture-note/llm-context/m02-small-world.qmd`
- `docs/lecture-note/llm-context/m03-robustness.qmd`
- And so on...

**Available Module Options:**
- `intro` - Introduction to Network Science
- `m01-euler_tour` - Euler Tour and Graph Theory Basics
- `m02-small-world` - Small World Networks
- `m03-robustness` - Network Robustness
- `m04-friendship-paradox` - Friendship Paradox
- `m05-clustering` - Network Clustering
- `m06-centrality` - Centrality Measures
- `m07-random-walks` - Random Walks
- `m08-embedding` - Network Embeddings
- `m09-graph-neural-networks` - Graph Neural Networks

If an `llm_context.qmd` file doesn't exist for a module, the script will fall back to running without module context.

## Environment Variables

- `CHAT_API`: API key for the LLM endpoint (GitHub secret)

## Troubleshooting

If you see errors like "Authentication failed" or "Your session has expired", this means:
1. The API key is invalid or expired
2. You need to be connected to the Binghamton University campus network or VPN
3. Contact your instructor for a valid API key

## Quiz Format

Questions should be in TOML format:

```toml
title = "Network Science Quiz"
description = "A comprehensive quiz covering network science concepts"
version = "1.0"

[[questions]]
question = "Your challenging question here..."
answer = "The correct answer here..."

[[questions]]
question = "Another question..."
answer = "Another answer..."
```

## Output

The script generates a JSON file with detailed results:

```json
{
  "quiz_title": "Network Science Quiz",
  "quiz_model": "llama3.2:latest",
  "evaluator_model": "gemma3:27b",
  "total_questions": 3,
  "student_wins": 1,
  "llm_wins": 2,
  "student_success_rate": 0.33,
  "question_results": [...]
}
```

## Requirements

- Python 3.8+
- `requests`
- `tomli` (for Python < 3.11) or built-in `tomllib` (Python 3.11+)