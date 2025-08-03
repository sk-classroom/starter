# LLM Quiz Challenge Library

A Python library and CLI tool for creating educational quiz challenges where students try to stump AI models. Students create challenging questions, and the system evaluates whether they can outsmart Large Language Models (LLMs).

## 🎯 Overview

The LLM Quiz Challenge system works by:
1. **Students create quiz questions** in TOML format with correct answers
2. **Question validation** ensures appropriateness for the subject area
3. **Quiz-taking LLM** attempts to answer questions (without seeing correct answers)
4. **Evaluator LLM** judges whether the quiz-taker's response is correct
5. **Students win** if they stump the AI on their questions (100% win rate required)
6. **Automatic grading** provides pass/fail results for GitHub Classroom integration

## 🚀 Quick Start

### Installation

#### Using uv (Recommended)
```bash
# Clone the repository
git clone <repository-url>

# Option 1: Run from parent directory
cd assignments/starter  # or wherever the repo is
uv run python -m grading-toolkit.llm_quiz --quiz-file quiz.toml --api-key sk-xxx

# Option 2: Run from grading-toolkit directory
cd grading-toolkit
uv run python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx

# Option 3: Create a virtual environment
cd grading-toolkit
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx
```

### Basic Usage

#### With uv
```bash
# From grading-toolkit directory
cd grading-toolkit
uv run python -m llm_quiz --quiz-file quiz.toml --api-key sk-your-key

# From parent directory (use full module path)
uv run python -m grading-toolkit.llm_quiz --quiz-file quiz.toml --api-key sk-your-key

# With context from URLs
uv run python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx --context-urls context_urls.txt

# Using the CLI wrapper (backward compatible)
uv run python grading-toolkit/llm_quiz_grading.py --quiz-file quiz.toml --api-key sk-your-key
```

#### With regular Python
```bash
# Using the library module
python -m llm_quiz --quiz-file quiz.toml --api-key sk-your-key

# Using the CLI wrapper (backward compatible)
python llm_quiz_grading.py --quiz-file quiz.toml --api-key sk-your-key

# With context from URLs
python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx --context-urls context_urls.txt
```

### Quiz File Format
Create a `quiz.toml` file with your questions:
```toml
[[questions]]
question = "What happens when you combine sodium and water?"
answer = "Sodium reacts violently with water, producing sodium hydroxide and hydrogen gas, with significant heat release."

[[questions]]
question = "In what scenario would this reaction be considered safe?"
answer = "The reaction is never truly safe due to its violent nature, but it can be demonstrated safely in controlled laboratory conditions with proper safety equipment and minimal amounts."
```

## 📚 Command Line Options

### Required Arguments
- `--quiz-file`: Path to TOML file containing questions
- `--api-key`: API key for your LLM provider

### Optional Arguments
- `--base-url`: API endpoint (default: OpenRouter)
- `--quiz-model`: Model for answering questions (default: "gpt-4o-mini")
- `--evaluator-model`: Model for evaluating answers (default: "gpt-4o")
- `--context-urls`: File containing URLs for context loading
- `--output`: JSON file for detailed results
- `--verbose`: Enable detailed logging
- `--exit-on-fail`: Exit with error code if student fails (default: True)

### Examples

#### With uv
```bash
# From grading-toolkit directory
cd grading-toolkit

# Basic usage with OpenRouter
uv run python -m llm_quiz --quiz-file quiz.toml --api-key sk-or-v1-xxx

# Quiz with context materials and custom models
uv run python -m llm_quiz \
  --quiz-file quiz.toml \
  --api-key sk-xxx \
  --context-urls "lecture_urls.txt" \
  --quiz-model "gpt-4o-mini" \
  --evaluator-model "gpt-4o"

# Local Ollama instance
uv run python -m llm_quiz \
  --quiz-file quiz.toml \
  --base-url http://localhost:11434/v1 \
  --api-key dummy

# Save detailed results
uv run python -m llm_quiz \
  --quiz-file quiz.toml \
  --api-key sk-xxx \
  --output results.json \
  --verbose
```

#### With regular Python
```bash
# Basic usage with OpenRouter
python -m llm_quiz --quiz-file quiz.toml --api-key sk-or-v1-xxx

# Quiz with context materials and custom models
python -m llm_quiz \
  --quiz-file quiz.toml \
  --api-key sk-xxx \
  --context-urls "lecture_urls.txt" \
  --quiz-model "gpt-4o-mini" \
  --evaluator-model "gpt-4o"

# Local Ollama instance
python -m llm_quiz \
  --quiz-file quiz.toml \
  --base-url http://localhost:11434/v1 \
  --api-key dummy

# Save detailed results
python -m llm_quiz \
  --quiz-file quiz.toml \
  --api-key sk-xxx \
  --output results.json \
  --verbose
```

## 💻 Python Library Usage

```python
from llm_quiz import LLMQuizChallenge

# Basic initialization
challenge = LLMQuizChallenge(
    base_url="https://openrouter.ai/api/v1",
    quiz_model="gpt-4o-mini",
    evaluator_model="gpt-4o",
    api_key="sk-or-v1-your-key"
)

# With context from URLs
challenge = LLMQuizChallenge(
    base_url="https://openrouter.ai/api/v1",
    quiz_model="gpt-4o-mini",
    evaluator_model="gpt-4o",
    api_key="sk-or-v1-your-key",
    context_urls_file="context_urls.txt"
)

# Load and run quiz
quiz_data = challenge.load_quiz("chemistry_quiz.toml")
results = challenge.run_sequential_challenge(quiz_data)

# Generate feedback
feedback = challenge.generate_student_feedback(results)
print(feedback)

# Save results
challenge.save_results(results, "results.json")
```

## 📚 Context Loading from URLs

The library can automatically fetch content from any URLs to provide context to the quiz-taking LLM.

### URL File Format

Create a text file containing URLs (one per line). Comments starting with `#` are ignored:

```txt
# Context URLs for Biology Course
https://raw.githubusercontent.com/professor/bio-course/main/lecture-01.md
https://raw.githubusercontent.com/professor/bio-course/main/exercises-01.py
https://docs.example.com/api/course-materials/chapter1.txt
https://university.edu/courses/bio101/notes.md

# Additional materials
https://raw.githubusercontent.com/professor/bio-course/main/reading-list.md
```

### Examples

#### Basic Context Loading
```bash
# Load context from URLs file
uv run python -m llm_quiz \
  --quiz-file quiz.toml \
  --api-key sk-xxx \
  --context-urls "context_urls.txt"
```

#### Different Content Sources
```bash
# Mix GitHub, documentation sites, and other sources
# context_urls.txt contains:
# https://raw.githubusercontent.com/user/course/main/lecture.md
# https://docs.university.edu/course/chapter1.html
# https://api.example.com/materials/exercises.json

uv run python -m llm_quiz \
  --quiz-file quiz.toml \
  --api-key sk-xxx \
  --context-urls "mixed_sources.txt"
```

### Supported URL Types

The library can fetch content from any publicly accessible URL:

- **GitHub Raw Files**: `https://raw.githubusercontent.com/user/repo/branch/file.md`
- **Documentation Sites**: `https://docs.example.com/content.html`
- **API Endpoints**: `https://api.example.com/materials/text`
- **University Portals**: `https://university.edu/courses/content.txt`
- **Any Public URL**: Any URL returning text content

## 📚 Context Materials

The library works with any type of course materials provided via URLs. The context helps the quiz-taking LLM understand the specific content being tested.

### Content Types Supported
- **Lecture Notes**: Markdown, HTML, or plain text files
- **Code Examples**: Python, JavaScript, or any programming language
- **Documentation**: API docs, course websites, reference materials
- **Academic Papers**: Text content from research papers
- **Exercise Files**: Problem sets, solutions, practice materials

## 🔧 API Provider Configuration

### OpenRouter (Default)
```bash
python -m llm_quiz \
  --base-url "https://openrouter.ai/api/v1" \
  --api-key "sk-or-v1-your-key"
```

### Ollama (Local)
```bash
python -m llm_quiz \
  --base-url "http://localhost:11434/v1" \
  --api-key "dummy"
```

### OpenAI
```bash
python -m llm_quiz \
  --base-url "https://api.openai.com/v1" \
  --api-key "sk-your-openai-key"
```

### Custom Provider
```bash
python -m llm_quiz \
  --base-url "https://your-api.com/v1" \
  --api-key "your-key"
```


## 🎯 Creating Effective Questions

### Question Types That Stump LLMs
- **Edge cases**: Boundary conditions, exceptions, unusual scenarios
- **Subtle distinctions**: Fine differences between similar concepts
- **Multi-constraint problems**: Questions combining multiple factors
- **Counterintuitive examples**: Results that seem wrong but are correct
- **Failure modes**: When do methods/theories break down?
- **Context-specific details**: Questions requiring knowledge of provided materials

### Question Types LLMs Handle Easily
- Basic definitions and explanations
- Standard textbook examples
- General conceptual overviews
- Simple step-by-step procedures
- Obvious keyword-based questions

### Examples by Content Type

#### Biology
```toml
[[questions]]
question = "In extreme drought conditions, what happens to CAM plant stomatal behavior during the day versus C4 plants?"
answer = "CAM plants keep stomata closed during day to conserve water, while C4 plants may partially open stomata since their CO2 concentration mechanism is less water-efficient than CAM."
```

#### History
```toml
[[questions]]
question = "What was the primary economic factor that made the Mali Empire's control of salt mines more strategically important than gold mines?"
answer = "Salt was essential for food preservation and had consistent daily demand, while gold was luxury trade dependent on external markets and political stability."
```

#### Chemistry
```toml
[[questions]]
question = "Why does increasing pressure favor the formation of diamond over graphite, despite graphite being more thermodynamically stable at standard conditions?"
answer = "Diamond has higher density than graphite, so increased pressure shifts equilibrium toward the more compact diamond structure according to Le Chatelier's principle, overcoming the kinetic barrier."
```

## ✅ Question Validation System

Questions are automatically validated for:
- ❌ **Heavy math** (no complex derivations)
- ❌ **Prompt injection** (no AI manipulation attempts)
- ✅ **Answer quality** (accurate and complete)
- ✅ **Context relevance** (when context materials are provided)

## 🎓 GitHub Classroom Integration

### Automatic Grading
- **Exit Code 0**: Student passes (100% win rate on valid questions)
- **Exit Code 1**: Student fails (less than 100% win rate or validation issues)

### Grade Markers
The system outputs markers for automated grading:
- `STUDENTS_QUIZ_KEIKO_WIN`: Student passed
- `STUDENTS_QUIZ_KEIKO_LOSE`: Student failed

## 🔍 Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Check your API key format
--api-key "sk-or-v1-..." # OpenRouter
--api-key "sk-..." # OpenAI
--api-key "dummy" # Ollama
```

#### Model Not Found
```bash
# Use the exact model names supported by your API provider
--quiz-model "gpt-4o-mini" # OpenAI/OpenRouter
--quiz-model "llama3.2:latest" # Ollama
--quiz-model "microsoft/phi-4" # OpenRouter specific path
```

#### Validation Failures
- Avoid complex mathematical derivations
- Don't include prompt injection attempts
- Provide clear, accurate answers
- When using context materials, ensure questions relate to the provided content

### Debugging

#### With uv
```bash
# From grading-toolkit directory
cd grading-toolkit

# Enable verbose logging
uv run python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx --verbose

# Save detailed results for analysis
uv run python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx --output debug.json
```

#### With regular Python
```bash
# Enable verbose logging
python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx --verbose

# Save detailed results for analysis
python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx --output debug.json
```

## 📈 Results and Feedback

### Console Output
- **Validation Summary**: Shows how many questions passed/failed validation
- **Detailed Question Analysis**: Each question, expected answer, LLM's answer, and verdict
- **Validation Issues**: Clear explanation of why questions were rejected
- **Improvement Feedback**: Specific suggestions based on success rate
- **General Tips**: Question types that work vs. those LLMs handle easily

### JSON Output Format
```json
{
  "quiz_title": "Biology Quiz",
  "quiz_model": "microsoft/phi-4",
  "evaluator_model": "google/gemma-3-27b-it:free",
  "total_questions": 3,
  "valid_questions": 2,
  "invalid_questions": 1,
  "system_errors": 0,
  "student_wins": 1,
  "llm_wins": 1,
  "student_success_rate": 0.5,
  "github_classroom_result": "STUDENTS_QUIZ_KEIKO_LOSE",
  "student_passes": false,
  "question_results": [...]
}
```

## 📋 Requirements

- Python 3.7+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- No external dependencies (uses standard library only)
- API access to an OpenAI-compatible LLM provider

### Installing uv
```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv
```

## 🆘 Support

- **Technical Issues**: Check error messages and logs with `--verbose`
- **Content Questions**: Review your course materials
- **API Problems**: Verify your provider's documentation
- **Format Issues**: Follow TOML examples exactly

---

**Happy Quiz Creation!** 🎯🤖