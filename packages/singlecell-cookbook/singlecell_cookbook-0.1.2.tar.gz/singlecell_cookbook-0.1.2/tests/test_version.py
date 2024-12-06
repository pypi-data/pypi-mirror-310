"""Test version information."""

from singlecell_cookbook import __version__


def test_version() -> None:
    """Test version is a string."""
    assert isinstance(__version__, str)
