from dataclasses import dataclass

@dataclass
class RenderSettings:
    stitch_width: int = 70
    stitch_height: int = 30

    stitch_x_spacing: float = 1.1   # <1 more compact, >1 more spaced out
    margin: int = 30                # margin around the pattern in the output image

    randomize: bool = True
    random_rotation: float = 3
    random_scale: float = 0.07