"""Tests for a module in the main package."""

from {{name}}.{{name}} import main


class TestSuite:
    """Test suite for a module in the main package."""

    @staticmethod
    def test_main_returns_zero() -> None:
        """Test the main function returns zero."""
        assert main() == 0
