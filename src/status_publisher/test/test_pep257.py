from ament_pep257.main import main


def test_pep257():
    """Test Python docstrings."""
    assert main() == 0
