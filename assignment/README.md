# Quiz Assignment: Challenge the AI

## 🎯 Objective

Your goal is to create challenging quiz questions that can **stump an AI** (Large Language Model). You need to demonstrate deep understanding of network science concepts by crafting questions that test edge cases, subtle distinctions, and require multi-step reasoning.

## 📋 Requirements

### ✅ To Pass This Assignment:
1. **Submit at least 1 valid question** (passes validation)
2. **Achieve 100% win rate** - stump the LLM on ALL your valid questions

### 📝 Question Format (REQUIRED):
Use **TOML format** for all questions:

```toml
[[questions]]
question = "Your challenging question here?"
answer = "Complete and accurate answer here."

[[questions]]
question = "Another question if you want multiple?"
answer = "Another complete answer."
```

## 📁 Files to Submit

### `quiz.toml` (Required)
This is your main submission file containing your challenging questions. Replace the example questions with your own.

**Example Structure:**
```toml
[[questions]]
question = "According to Euler's Path Theorem, what specific conditions must be met for a disconnected graph to have an Euler path?"
answer = "A disconnected graph cannot have an Euler path. Euler's Path Theorem requires the graph to be connected as a fundamental prerequisite, regardless of vertex degrees."

[[questions]]
question = "In a scale-free network with γ=2.1, what happens to the network's robustness when you remove the top 1% highest-degree nodes versus removing 10% random nodes?"
answer = "Removing the top 1% highest-degree nodes causes catastrophic failure due to the power-law distribution, while removing 10% random nodes has minimal impact since most nodes have very low degree."
```

## 🎯 Creating Challenging Questions

### ✅ Question Types That Stump LLMs:
- **Edge cases and exceptions** (disconnected graphs, empty sets, boundary conditions)
- **Subtle distinctions** between similar concepts (path vs circuit, centrality measures)
- **Multi-constraint scenarios** (combine multiple network properties)
- **Counterintuitive examples** (friendship paradox edge cases)
- **Failure modes** (when do algorithms break down?)
- **Parameter-specific behavior** (what happens at specific values?)

### ❌ Question Types LLMs Handle Easily:
- Basic definitions ("What is degree centrality?")
- Standard textbook examples
- General conceptual explanations
- Simple algorithmic steps
- Obvious keyword-based questions

### 💡 Pro Tips:
1. **Be specific** - Ask about specific parameter ranges, edge cases, or conditions
2. **Test understanding** - Don't just ask for definitions
3. **Use constraints** - Combine multiple network properties in one question
4. **Think critically** - What would confuse even a smart student?
5. **Validate locally** - Test your questions with the [Quiz Creator Dojo](../../docs/lecture-note/dojo/quiz-creator.qmd) first

## 🔧 Testing Your Questions

Before submitting, you can test your questions using the Quiz Creator tool:
- Visit the [Quiz Creator Dojo](../../docs/lecture-note/dojo/quiz-creator.qmd)
- Paste your TOML questions
- See how the AI performs
- Refine based on feedback

## ⚠️ Validation Rules

Your questions will be automatically validated for:
- ✅ **Relevance** to network science/graph theory
- ❌ **Heavy math** (no complex derivations or extensive calculations)
- ❌ **Off-topic content** (must relate to course materials)
- ❌ **Prompt injection** (no attempts to manipulate the AI system)
- ✅ **Answer quality** (your answers must be accurate and complete)

## 📊 Grading

### Automatic Grading Process:
1. **Validation** - Questions checked for appropriateness
2. **AI Challenge** - LLM attempts to answer your questions
3. **Evaluation** - Expert LLM judges correctness
4. **Pass/Fail** - Based on 100% win rate requirement

### Grade Markers:
- **PASS**: `STUDENTS_QUIZ_KEIKO_WIN`
- **FAIL**: `STUDENTS_QUIZ_KEIKO_LOSE`

### Common Failure Reasons:
- Questions too easy for the LLM
- Invalid questions (off-topic, heavy math, etc.)
- Incorrect or incomplete answers
- Wrong file format (not using TOML)

## 🚀 Getting Started

1. **Study the modules** - Review course materials for concepts to challenge
2. **Edit `quiz.toml`** - Replace example questions with your challenging ones
3. **Test locally** - Use the Quiz Creator Dojo to refine your questions
4. **Submit** - Push your `quiz.toml` file
5. **Check results** - GitHub Classroom will show PASS/FAIL status

## 💯 Success Strategy

Focus on creating questions that require **deep understanding** rather than memorization:
- Find edge cases in algorithms or theorems
- Explore parameter sensitivity in network models
- Challenge assumptions about network properties
- Test knowledge of when methods fail or don't apply

Remember: Your goal is to demonstrate mastery by creating questions that challenge even an advanced AI system!

## 🆘 Need Help?

- **Technical Issues**: Check the [Quiz Creator Dojo troubleshooting](../../docs/lecture-note/dojo/quiz-creator.qmd)
- **Content Questions**: Review course materials and lecture notes
- **Format Problems**: Follow the TOML examples exactly as shown above

Good luck creating questions that stump the AI! 🤖⚔️