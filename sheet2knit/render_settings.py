from dataclasses import dataclass

@dataclass
class RenderSettings:
    stitch_width: int = 70
    stitch_height: int = 60

    stitch_x_spacing: float = 1.05    # <1 more compact, >1 more spaced out
    stitch_y_spacing: float = 0.86   # <1 more compact, >1 more spaced out
    margin: int = 30                 # margin around the pattern in the output image

    randomize: bool = True
    random_rotation: float = 2
    random_scale: float = 0.05

    # Stockinette stitch appearance
    stitch_gap_ratio: float = 0.07  # gap between the two halves of the stitch, as a fraction of stitch width
    stitch_thickness_ratio: float = 0.55 # thickness of the middle part of the stictch
    