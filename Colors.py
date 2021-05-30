from dataclasses import dataclass


@dataclass
class Colors:
    """A class representing colors."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LIGHT_GRAY = (64, 64, 64)
    DARK_GRAY = (200, 200, 200)
    GRAY = (100, 100, 100)
    TEAL = (0, 255, 255)