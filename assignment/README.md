# Quiz Assignment: Challenge the AI

## 🎯 Objective

Your goal is to create challenging quiz questions that can **stump an AI** (Large Language Model). You need to demonstrate deep understanding of course concepts by crafting questions that test edge cases, subtle distinctions, and require multi-step reasoning.

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
question = "What specific conditions must be met for this fundamental theorem to apply in disconnected structures?"
answer = "A disconnected structure cannot satisfy the theorem. The theorem requires connectivity as a fundamental prerequisite, regardless of other properties."

[[questions]]
question = "In this type of system with parameter γ=2.1, what happens to stability when you remove the top 1% highest-ranked elements versus removing 10% random elements?"
answer = "Removing the top 1% highest-ranked elements causes catastrophic failure due to the power-law distribution, while removing 10% random elements has minimal impact since most elements have very low rank."
```

## 🎯 Creating Challenging Questions

### ✅ Question Types That Stump LLMs:
- **Edge cases and exceptions** (disconnected structures, empty sets, boundary conditions)
- **Subtle distinctions** between similar concepts (related terms, measurement methods)
- **Multi-constraint scenarios** (combine multiple course properties)
- **Counterintuitive examples** (paradoxes and edge cases)
- **Failure modes** (when do algorithms or theories break down?)
- **Parameter-specific behavior** (what happens at specific values?)

### ❌ Question Types LLMs Handle Easily:
- Basic definitions ("What is this concept?")
- Standard textbook examples
- General conceptual explanations
- Simple algorithmic steps
- Obvious keyword-based questions

### 💡 Pro Tips:
1. **Be specific** - Ask about specific parameter ranges, edge cases, or conditions
2. **Test understanding** - Don't just ask for definitions
3. **Use constraints** - Combine multiple course properties in one question
4. **Think critically** - What would confuse even a smart student?
5. **Validate locally** - Test your questions with the grading tool first

## 🔧 Testing Your Questions

Before submitting, you can test your questions using the grading tool:
- Run the quiz challenge locally with your questions
- See how the AI performs on each question
- Check validation feedback and adjust accordingly
- Refine based on evaluation results

## ⚠️ Validation Rules

Your questions will be automatically validated for:
- ✅ **Relevance** to course subject area
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
- Explore parameter sensitivity in course models
- Challenge assumptions about course properties
- Test knowledge of when methods fail or don't apply

Remember: Your goal is to demonstrate mastery by creating questions that challenge even an advanced AI system!

## 🆘 Need Help?

- **Technical Issues**: Check the grading tool documentation and error messages
- **Content Questions**: Review course materials and lecture notes
- **Format Problems**: Follow the TOML examples exactly as shown above

Good luck creating questions that stump the AI! 🤖⚔️