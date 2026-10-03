"""Offline password strength and security analyzer.

The application evaluates a password in memory. It does not save, log, or
display the password.
"""

from __future__ import annotations

import getpass
import re
from dataclasses import dataclass


COMMON_PASSWORDS = {
    "123456", "12345678", "123456789", "abc123", "admin", "iloveyou",
    "letmein", "password", "password1", "qwerty", "welcome",
}

SEQUENCES = (
    "0123456789",
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
)


@dataclass(frozen=True)
class AnalysisResult:
    """A password assessment that contains no copy of the password."""

    score: int
    rating: str
    checks: dict[str, bool]
    suggestions: tuple[str, ...]


def _contains_sequence(password: str, minimum_length: int = 3) -> bool:
    """Return True when the password contains a predictable sequence."""
    lowered = password.lower()
    for source in SEQUENCES:
        for candidate_source in (source, source[::-1]):
            for start in range(len(candidate_source) - minimum_length + 1):
                candidate = candidate_source[start : start + minimum_length]
                if candidate in lowered:
                    return True
    return False


def analyze_password(password: str) -> AnalysisResult:
    """Evaluate a password without saving or returning the original value."""
    checks = {
        "At least 12 characters": len(password) >= 12,
        "At least 16 characters": len(password) >= 16,
        "Contains an uppercase letter": bool(re.search(r"[A-Z]", password)),
        "Contains a lowercase letter": bool(re.search(r"[a-z]", password)),
        "Contains a number": bool(re.search(r"\d", password)),
        "Contains a special character": bool(re.search(r"[^A-Za-z0-9]", password)),
        "Not a common password": password.lower() not in COMMON_PASSWORDS,
        "No character repeated three times": not bool(re.search(r"(.)\1{2,}", password)),
        "No predictable sequence": not _contains_sequence(password),
    }

    score = 0
    score += 25 if checks["At least 12 characters"] else min(len(password) * 2, 20)
    score += 10 if checks["At least 16 characters"] else 0
    score += 10 if checks["Contains an uppercase letter"] else 0
    score += 10 if checks["Contains a lowercase letter"] else 0
    score += 10 if checks["Contains a number"] else 0
    score += 10 if checks["Contains a special character"] else 0
    score += 10 if checks["Not a common password"] else -35
    score += 8 if checks["No character repeated three times"] else -10
    score += 7 if checks["No predictable sequence"] else -15
    score = max(0, min(100, score))

    if score < 40:
        rating = "Weak"
    elif score < 65:
        rating = "Moderate"
    elif score < 85:
        rating = "Strong"
    else:
        rating = "Very Strong"

    suggestions: list[str] = []
    if not checks["At least 12 characters"]:
        suggestions.append("Use at least 12 characters; 16 or more is better.")
    elif not checks["At least 16 characters"]:
        suggestions.append("Consider using 16 or more characters for added strength.")
    if not checks["Contains an uppercase letter"]:
        suggestions.append("Add at least one uppercase letter.")
    if not checks["Contains a lowercase letter"]:
        suggestions.append("Add at least one lowercase letter.")
    if not checks["Contains a number"]:
        suggestions.append("Add at least one number.")
    if not checks["Contains a special character"]:
        suggestions.append("Add at least one special character.")
    if not checks["Not a common password"]:
        suggestions.append("Avoid common passwords and choose a unique passphrase.")
    if not checks["No character repeated three times"]:
        suggestions.append("Avoid repeating the same character three or more times.")
    if not checks["No predictable sequence"]:
        suggestions.append("Avoid sequences such as 123, abc, qwerty, or keyboard patterns.")
    if not suggestions:
        suggestions.append("No basic weaknesses were detected. Keep the password unique for each account.")

    return AnalysisResult(score, rating, checks, tuple(suggestions))


def main() -> None:
    """Run the command-line interface using hidden password input."""
    print("Automated Password Strength and Security Analyzer")
    print("Your password is evaluated locally and is not saved or displayed.\n")
    password = getpass.getpass("Enter a password to analyze: ")

    if not password:
        print("No password was entered. Analysis canceled.")
        return

    result = analyze_password(password)
    del password

    print(f"\nScore: {result.score}/100")
    print(f"Rating: {result.rating}")
    print("\nSecurity checks:")
    for description, passed in result.checks.items():
        print(f"  {'PASS' if passed else 'NEEDS IMPROVEMENT'} - {description}")

    print("\nSuggestions:")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")

    print("\nThis result is educational and does not guarantee that a password is secure.")


if __name__ == "__main__":
    main()
