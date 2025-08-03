"""
Command Line Interface for LLM Quiz Challenge.

This module provides the CLI for running quiz challenges where students
try to stump AI models.
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from .core import LLMQuizChallenge

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def validate_arguments(args) -> bool:
    """Validate command line arguments."""
    # Check quiz file exists
    if not args.quiz_file.exists():
        print(f"Error: Quiz file not found: {args.quiz_file}")
        return False
    
    # Check API key is provided
    if not args.api_key or not args.api_key.strip():
        print("Error: API key is required (use --api-key or environment variable)")
        return False
    
    # Check base URL is provided
    if not args.base_url:
        print("Error: Base URL is required (use --base-url)")
        return False
        
    return True


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="LLM Quiz Challenge - Test if students can stump AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default OpenRouter settings
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-or-v1-xxx

  # Run with custom subject area
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --subject-area "biology"

  # Run with custom Ollama instance
  python -m llm_quiz.cli --quiz-file quiz.toml --base-url http://localhost:11434/v1 --api-key dummy

  # Run with custom models
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --quiz-model phi4:latest --evaluator-model gemma3:27b

  # Save results and show verbose output
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --output results.json --verbose

GitHub Classroom Integration:
  - Exit code 0: Student passes (100% win rate on valid questions)
  - Exit code 1: Student fails (less than 100% win rate or no valid questions)
  - Results include STUDENTS_QUIZ_KEIKO_WIN/LOSE markers for automated grading
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--quiz-file",
        type=Path,
        required=True,
        help="Path to TOML quiz file containing questions and answers"
    )
    
    parser.add_argument(
        "--api-key",
        required=True,
        help="API key for LLM endpoint (or set via environment variable)"
    )
    
    # API configuration
    parser.add_argument(
        "--base-url",
        default="https://openrouter.ai/api/v1",
        help="Base URL for LLM API endpoint (default: OpenRouter)"
    )
    
    # Model configuration
    parser.add_argument(
        "--quiz-model",
        default="phi4:latest",
        help="Model for taking the quiz (default: phi4:latest)"
    )
    
    parser.add_argument(
        "--evaluator-model", 
        default="gemma3:27b",
        help="Model for evaluating answers (default: gemma3:27b)"
    )
    
    # Module configuration
    parser.add_argument(
        "--module",
        help="Module name for context loading (e.g., m01-euler_tour)"
    )
    
    parser.add_argument(
        "--subject-area",
        default="course materials",
        help="Subject area for validation (e.g., 'network science', 'biology', 'history')"
    )
    
    # Output configuration
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON file for detailed results"
    )
    
    # Behavior options
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging output"
    )
    
    parser.add_argument(
        "--exit-on-fail",
        action="store_true",
        default=True,
        help="Exit with error code if students don't pass (default: True)"
    )
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    # Validate arguments
    if not validate_arguments(args):
        sys.exit(1)
    
    try:
        # Initialize the challenge system
        logger.info("Initializing LLM Quiz Challenge...")
        logger.info(f"Base URL: {args.base_url}")
        logger.info(f"Quiz Model: {args.quiz_model}")
        logger.info(f"Evaluator Model: {args.evaluator_model}")
        logger.info(f"Subject Area: {args.subject_area}")
        if args.module:
            logger.info(f"Module: {args.module}")
        
        challenge = LLMQuizChallenge(
            base_url=args.base_url,
            quiz_model=args.quiz_model,
            evaluator_model=args.evaluator_model,
            api_key=args.api_key,
            module_name=args.module,
            subject_area=args.subject_area
        )
        
        # Load quiz from file
        logger.info(f"Loading quiz from {args.quiz_file}")
        quiz_data = challenge.load_quiz(args.quiz_file)
        
        # Run the challenge
        logger.info("Starting quiz challenge...")
        results = challenge.run_sequential_challenge(quiz_data)
        
        # Generate and display feedback
        feedback = challenge.generate_student_feedback(results)
        print(feedback)
        
        # Save results if requested
        if args.output:
            challenge.save_results(results, args.output)
            logger.info(f"Detailed results saved to {args.output}")
        
        # Exit with appropriate code for GitHub Classroom
        if args.exit_on_fail and not results["student_passes"]:
            logger.info("Student did not pass grading criteria")
            sys.exit(1)
        else:
            logger.info("Quiz challenge completed successfully")
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("Quiz challenge interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()