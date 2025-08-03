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

from .challenge import LLMQuizChallenge

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

  # Run with custom Ollama instance
  python -m llm_quiz.cli --quiz-file quiz.toml --base-url http://localhost:11434/v1 --api-key dummy

  # Run with custom models
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --quiz-model gpt-4o-mini --evaluator-model gpt-4o

  # Load context from URLs file
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --context-urls context_urls.txt

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
        default="gpt-4o-mini",
        help="Model for taking the quiz (default: gpt-4o-mini)"
    )
    
    parser.add_argument(
        "--evaluator-model", 
        default="gpt-4o",
        help="Model for evaluating answers (default: gpt-4o)"
    )
    
    # Context configuration
    parser.add_argument(
        "--context-urls",
        help="File containing URLs to fetch for context (one URL per line)"
    )
    
    parser.add_argument(
        "--context-window-size",
        type=int,
        default=32768,
        help="Context window size for LLM models (default: 32768)"
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
        logger.info(f"Context Window Size: {args.context_window_size}")
        if args.context_urls:
            logger.info(f"Context URLs file: {args.context_urls}")
        
        challenge = LLMQuizChallenge(
            api_key=args.api_key,
            base_url=args.base_url,
            quiz_model=args.quiz_model,
            evaluator_model=args.evaluator_model,
            context_window_size=args.context_window_size
        )
        
        # Load context if provided
        if args.context_urls:
            context_loaded = challenge.load_context_from_urls_file(args.context_urls)
            if not context_loaded:
                logger.warning("Failed to load context from URLs file")
        
        # Run the challenge
        logger.info("Starting quiz challenge...")
        results = challenge.run_quiz_from_file(args.quiz_file)
        
        # Generate and display feedback
        feedback = challenge.get_student_feedback(results)
        print(feedback)
        
        # Save results if requested
        if args.output:
            challenge.save_results(args.output, results)
            logger.info(f"Detailed results saved to {args.output}")
        
        # Exit with appropriate code for GitHub Classroom
        if args.exit_on_fail and not results.student_passes:
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