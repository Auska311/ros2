from ament_flake8.main import main


def test_flake8():
    """Test code style with flake8."""
    assert main() == 0
