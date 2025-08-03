#!/usr/bin/env python3
"""
Quiz Parser for TOML-based quiz files
Supports multiple choice, free-form, numerical, true/false, and matching questions
"""

import tomllib
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FREE_FORM = "free_form"
    NUMERICAL = "numerical"
    TRUE_FALSE = "true_false"
    MATCHING = "matching"


@dataclass
class ValidationRules:
    min_words: Optional[int] = None
    max_words: Optional[int] = None
    required_keywords: Optional[List[str]] = None
    case_sensitive: bool = False
    code_required: bool = False
    language: Optional[str] = None
    required_functions: Optional[List[str]] = None
    max_lines: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    tolerance: Optional[float] = None
    unit: Optional[str] = None


@dataclass
class Question:
    id: str
    type: QuestionType
    points: int
    difficulty: str
    topic: str
    question: str
    correct_answer: Any
    explanation: str
    options: Optional[Dict[str, str]] = None
    validation: Optional[ValidationRules] = None
    sample_answer: Optional[str] = None
    image: Optional[str] = None
    left_items: Optional[Dict[str, str]] = None
    right_items: Optional[Dict[str, str]] = None
    correct_matches: Optional[Dict[str, str]] = None


@dataclass
class Quiz:
    title: str
    description: str
    version: str
    total_points: int
    questions: List[Question]


class QuizParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.quiz_data = None
        self.quiz = None

    def load_quiz(self) -> Quiz:
        """Load and parse the TOML quiz file"""
        with open(self.file_path, 'rb') as f:
            self.quiz_data = tomllib.load(f)

        return self._parse_quiz()

    def _parse_quiz(self) -> Quiz:
        """Parse the quiz data into a structured Quiz object"""
        # Parse quiz metadata
        quiz = Quiz(
            title=self.quiz_data.get('title', 'Untitled Quiz'),
            description=self.quiz_data.get('description', ''),
            version=self.quiz_data.get('version', '1.0'),
            total_points=self.quiz_data.get('total_points', 0),
            questions=[]
        )

        # Parse questions
        for q_data in self.quiz_data.get('questions', []):
            question = self._parse_question(q_data)
            quiz.questions.append(question)

        self.quiz = quiz
        return quiz

    def _parse_question(self, q_data: Dict[str, Any]) -> Question:
        """Parse a single question from the TOML data"""
        # Parse validation rules if present
        validation = None
        if 'validation' in q_data:
            v_data = q_data['validation']
            validation = ValidationRules(
                min_words=v_data.get('min_words'),
                max_words=v_data.get('max_words'),
                required_keywords=v_data.get('required_keywords'),
                case_sensitive=v_data.get('case_sensitive', False),
                code_required=v_data.get('code_required', False),
                language=v_data.get('language'),
                required_functions=v_data.get('required_functions'),
                max_lines=v_data.get('max_lines'),
                min_value=v_data.get('min_value'),
                max_value=v_data.get('max_value'),
                tolerance=v_data.get('tolerance'),
                unit=v_data.get('unit')
            )

        return Question(
            id=q_data['id'],
            type=QuestionType(q_data['type']),
            points=q_data['points'],
            difficulty=q_data['difficulty'],
            topic=q_data['topic'],
            question=q_data['question'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            options=q_data.get('options'),
            validation=validation,
            sample_answer=q_data.get('sample_answer'),
            image=q_data.get('image'),
            left_items=q_data.get('left_items'),
            right_items=q_data.get('right_items'),
            correct_matches=q_data.get('correct_matches')
        )

    def validate_answer(self, question_id: str, answer: Any) -> Dict[str, Any]:
        """Validate a student's answer against the correct answer"""
        question = self._get_question_by_id(question_id)
        if not question:
            return {"valid": False, "error": "Question not found"}

        result = {
            "valid": False,
            "score": 0,
            "feedback": "",
            "explanation": question.explanation
        }

        if question.type == QuestionType.MULTIPLE_CHOICE:
            result = self._validate_multiple_choice(question, answer)
        elif question.type == QuestionType.FREE_FORM:
            result = self._validate_free_form(question, answer)
        elif question.type == QuestionType.NUMERICAL:
            result = self._validate_numerical(question, answer)
        elif question.type == QuestionType.TRUE_FALSE:
            result = self._validate_true_false(question, answer)
        elif question.type == QuestionType.MATCHING:
            result = self._validate_matching(question, answer)

        return result

    def _get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Get a question by its ID"""
        for question in self.quiz.questions:
            if question.id == question_id:
                return question
        return None

    def _validate_multiple_choice(self, question: Question, answer: str) -> Dict[str, Any]:
        """Validate a multiple choice answer"""
        is_correct = answer.upper() == question.correct_answer.upper()
        return {
            "valid": True,
            "score": question.points if is_correct else 0,
            "feedback": "Correct!" if is_correct else f"Incorrect. The correct answer is {question.correct_answer}.",
            "explanation": question.explanation
        }

    def _validate_free_form(self, question: Question, answer: str) -> Dict[str, Any]:
        """Validate a free-form answer"""
        if not question.validation:
            return {"valid": False, "error": "No validation rules defined"}

        validation = question.validation
        feedback = []
        score = 0

        # Check word count
        word_count = len(answer.split())
        if validation.min_words and word_count < validation.min_words:
            feedback.append(f"Answer too short. Minimum {validation.min_words} words required.")
        elif validation.max_words and word_count > validation.max_words:
            feedback.append(f"Answer too long. Maximum {validation.max_words} words allowed.")
        else:
            score += question.points * 0.3  # 30% for length

        # Check required keywords
        if validation.required_keywords:
            found_keywords = 0
            answer_lower = answer.lower() if not validation.case_sensitive else answer
            for keyword in validation.required_keywords:
                keyword_lower = keyword.lower() if not validation.case_sensitive else keyword
                if keyword_lower in answer_lower:
                    found_keywords += 1

            keyword_score = found_keywords / len(validation.required_keywords)
            score += question.points * 0.4 * keyword_score  # 40% for keywords
            feedback.append(f"Found {found_keywords}/{len(validation.required_keywords)} required keywords.")

        # Check for code if required
        if validation.code_required:
            if validation.language == "python":
                if "def " in answer or "import " in answer or "=" in answer:
                    score += question.points * 0.3  # 30% for code structure
                    feedback.append("Code structure detected.")
                else:
                    feedback.append("Code structure not detected.")

        return {
            "valid": True,
            "score": min(score, question.points),
            "feedback": " ".join(feedback),
            "explanation": question.explanation
        }

    def _validate_numerical(self, question: Question, answer: float) -> Dict[str, Any]:
        """Validate a numerical answer"""
        if not question.validation:
            return {"valid": False, "error": "No validation rules defined"}

        validation = question.validation
        tolerance = validation.tolerance or 0.01

        is_correct = abs(answer - question.correct_answer) <= tolerance

        return {
            "valid": True,
            "score": question.points if is_correct else 0,
            "feedback": f"Correct! ({answer} ± {tolerance})" if is_correct else f"Incorrect. Expected {question.correct_answer} ± {tolerance}.",
            "explanation": question.explanation
        }

    def _validate_true_false(self, question: Question, answer: bool) -> Dict[str, Any]:
        """Validate a true/false answer"""
        is_correct = answer == question.correct_answer
        return {
            "valid": True,
            "score": question.points if is_correct else 0,
            "feedback": "Correct!" if is_correct else "Incorrect.",
            "explanation": question.explanation
        }

    def _validate_matching(self, question: Question, answer: Dict[str, str]) -> Dict[str, Any]:
        """Validate a matching answer"""
        if not question.correct_matches:
            return {"valid": False, "error": "No correct matches defined"}

        correct_count = 0
        total_matches = len(question.correct_matches)

        for left_item, right_item in answer.items():
            if question.correct_matches.get(left_item) == right_item:
                correct_count += 1

        score = (correct_count / total_matches) * question.points

        return {
            "valid": True,
            "score": score,
            "feedback": f"Matched {correct_count}/{total_matches} correctly.",
            "explanation": question.explanation
        }

    def get_quiz_summary(self) -> Dict[str, Any]:
        """Get a summary of the quiz"""
        if not self.quiz:
            return {"error": "Quiz not loaded"}

        question_types = {}
        topics = {}

        for question in self.quiz.questions:
            # Count question types
            q_type = question.type.value
            question_types[q_type] = question_types.get(q_type, 0) + 1

            # Count topics
            topics[question.topic] = topics.get(question.topic, 0) + 1

        return {
            "title": self.quiz.title,
            "description": self.quiz.description,
            "version": self.quiz.version,
            "total_points": self.quiz.total_points,
            "total_questions": len(self.quiz.questions),
            "question_types": question_types,
            "topics": topics
        }


def main():
    """Example usage of the quiz parser"""
    parser = QuizParser("quiz.toml")

    try:
        quiz = parser.load_quiz()
        summary = parser.get_quiz_summary()

        print("=== Quiz Summary ===")
        print(f"Title: {summary['title']}")
        print(f"Description: {summary['description']}")
        print(f"Total Points: {summary['total_points']}")
        print(f"Total Questions: {summary['total_questions']}")
        print(f"Question Types: {summary['question_types']}")
        print(f"Topics: {summary['topics']}")

        # Example validation
        print("\n=== Example Validations ===")

        # Multiple choice
        result = parser.validate_answer("q1", "B")
        print(f"Q1 (Multiple Choice): {result}")

        # Free form
        sample_answer = "The small-world phenomenon describes how most nodes in a network can be reached by a small number of steps. Stanley Milgram's experiment showed six degrees of separation."
        result = parser.validate_answer("q3", sample_answer)
        print(f"Q3 (Free Form): {result}")

        # Numerical
        result = parser.validate_answer("q7", 1.33)
        print(f"Q7 (Numerical): {result}")

    except Exception as e:
        print(f"Error loading quiz: {e}")


if __name__ == "__main__":
    main()