#!/bin/bash

# Quiz Test Runner Script
# Handles intelligent quiz grading with file timestamp checking and result caching
# Usage: ./run_quiz_test.sh --config config.toml --quiz-file quiz.toml --api-key API_KEY [--output results.json]

set -e  # Exit on any error

# Parse command line arguments
CONFIG=""
QUIZ_FILE=""
API_KEY=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --quiz-file)
            QUIZ_FILE="$2"
            shift 2
            ;;
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$CONFIG" || -z "$QUIZ_FILE" || -z "$API_KEY" ]]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 --config CONFIG --quiz-file QUIZ_FILE --api-key API_KEY [--output OUTPUT]"
    exit 1
fi

# Set default output if not provided
if [[ -z "$OUTPUT" ]]; then
    OUTPUT="./assignment/quiz_results.json"
fi

echo "🎯 Quiz Test Runner Starting..."
echo "📋 Config: $CONFIG"
echo "📝 Quiz file: $QUIZ_FILE"
echo "💾 Output: $OUTPUT"

# Check if results file exists and determine what to do
if [[ ! -f "$OUTPUT" ]]; then
    echo "📂 No results file found - running LLM quiz for first time"
elif [[ "$QUIZ_FILE" -nt "$OUTPUT" ]]; then
    echo "🔄 Quiz file is newer than results - re-running grading"
    echo "🗑️ Removing old results file"
    rm -f "$OUTPUT"
else
    echo "📁 Results file found and quiz file is not newer - checking if student passed"

    # Check if student stumped all LLMs using jq
    if jq -e '.student_passes == true' "$OUTPUT" > /dev/null 2>&1; then
        echo "🎉 STUDENT PASSED: Stumped LLMs in all questions!"
        echo "✅ Skipping grading and awarding full points"
        exit 0
    else
        echo "❌ STUDENT FAILED: Did not stump LLMs in all questions"
        echo "🗑️ Removing old results file"
        exit 1
    fi
fi


# Run the quiz grading
echo "🚀 Starting LLM quiz grading..."
uv run python -m grading.llm_quiz \
    --config "$CONFIG" \
    --quiz-file "$QUIZ_FILE" \
    --api-key "$API_KEY" \
    --output "$OUTPUT"

# Check the result
if [[ -f "$OUTPUT" ]]; then
    echo "✅ Quiz grading completed successfully"
    echo "💾 Results saved to: $OUTPUT"

    # Show final result
    if jq -e '.student_passes == true' "$OUTPUT" > /dev/null 2>&1; then
        echo "🎉 FINAL RESULT: Student PASSED!"
    else
        echo "📊 FINAL RESULT: Student did not pass this attempt"
    fi
else
    echo "❌ Error: Quiz grading failed - no results file generated"
    exit 1
fi

echo "🏁 Quiz test runner completed"