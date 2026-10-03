"""Automated tests using fictional passwords only."""

import unittest

from password_analyzer import AnalysisResult, analyze_password


class PasswordAnalyzerTests(unittest.TestCase):
    def test_common_password_is_weak(self):
        result = analyze_password("password")
        self.assertEqual(result.rating, "Weak")
        self.assertFalse(result.checks["Not a common password"])

    def test_missing_character_types_produce_suggestions(self):
        result = analyze_password("fictionalphrase")
        combined = " ".join(result.suggestions)
        self.assertIn("uppercase", combined)
        self.assertIn("number", combined)
        self.assertIn("special", combined)

    def test_repeated_characters_are_detected(self):
        result = analyze_password("Fictional!!!Pass9")
        self.assertFalse(result.checks["No character repeated three times"])

    def test_number_sequence_is_detected(self):
        result = analyze_password("Example123!Phrase")
        self.assertFalse(result.checks["No predictable sequence"])

    def test_keyboard_pattern_is_detected(self):
        result = analyze_password("ExampleQwerty!9")
        self.assertFalse(result.checks["No predictable sequence"])

    def test_long_complex_fictional_password_scores_high(self):
        result = analyze_password("Mango-River7!Cloud")
        self.assertIn(result.rating, {"Strong", "Very Strong"})
        self.assertGreaterEqual(result.score, 65)

    def test_result_does_not_store_password(self):
        fictional_password = "DoNotStore-Me9!"
        result = analyze_password(fictional_password)
        self.assertIsInstance(result, AnalysisResult)
        self.assertNotIn(fictional_password, repr(result))
        self.assertFalse(hasattr(result, "password"))


if __name__ == "__main__":
    unittest.main()
