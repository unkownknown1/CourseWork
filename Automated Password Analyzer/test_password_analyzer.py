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

    def test_common_password_variation_is_weak(self):
        result = analyze_password("Password123!")
        self.assertEqual(result.rating, "Weak")
        self.assertLessEqual(result.score, 20)
        self.assertFalse(result.checks["Not a common password"])

    def test_short_complex_password_remains_weak(self):
        result = analyze_password("R7!mK2@")
        self.assertEqual(result.rating, "Weak")
        self.assertLessEqual(result.score, 39)

    def test_password_under_twelve_characters_is_not_strong(self):
        result = analyze_password("R7!mK2@q")
        self.assertEqual(result.rating, "Moderate")
        self.assertLessEqual(result.score, 64)

    def test_fewer_than_three_character_types_limits_rating(self):
        result = analyze_password("fictionalphraseonly")
        self.assertEqual(result.rating, "Moderate")
        self.assertLessEqual(result.score, 64)

if __name__ == "__main__":
    unittest.main()
