import svgwrite
import random

from .colors import adjust_colour
from .transforms import add_offset_to_transform, get_stitch_transform

def create_stockinette_stitch_path(settings):
    """
    Create a filled stockinette stitch.
    Keeps the original diagonal geometry:
    two separate inclined strands.

    Each strand:
    - starts as a point
    - gets thicker in the middle
    - ends as a point
    """

    w = settings.stitch_width
    h = settings.stitch_height

    gap = settings.stitch_gap_ratio * min(w, h)
    thickness = min(w, h) * settings.stitch_thickness_ratio

    def tapered_strand(x1, y1, x2, y2):
        # Direction vector
        dx = x2 - x1
        dy = y2 - y1

        length = (dx ** 2 + dy ** 2) ** 0.5

        # Perpendicular vector
        nx = -dy / length
        ny = dx / length

        # Points along the ORIGINAL diagonal
        center_points = [
            (x1, y1, 0),
            (x1 + dx * 0.5, y1 + dy * 0.5, thickness),
            (x2, y2, 0),
        ]

        left = []
        right = []

        for x, y, width in center_points:
            left.append((x + nx * width, y + ny * width))
            right.append((x - nx * width, y - ny * width))

        # Use quadratic curves
        return (
            f"M {left[0][0]} {left[0][1]} "
            f"Q {left[1][0]} {left[1][1]} "
            f"{left[2][0]} {left[2][1]} "
            f"L {right[2][0]} {right[2][1]} "
            f"Q {right[1][0]} {right[1][1]} "
            f"{right[0][0]} {right[0][1]} "
            "Z"
        )

    left_strand = tapered_strand(0, 0, w / 2 - gap, h)
    right_strand = tapered_strand(w, 0, w / 2 + gap, h)

    return left_strand + right_strand


def draw_stockinette_stitch(dwg, x, y, colour, settings):
    stich_path = create_stockinette_stitch_path(settings)
    transform = get_stitch_transform(x, y, settings)

    def draw_stitch_layer(fill_colour, offset_x=0, offset_y=0):
        dwg.add(
            dwg.path(
                d=stich_path,
                fill=fill_colour,
                stroke="none",
                transform=add_offset_to_transform(transform, offset_x, offset_y)
            )
        )

    layers = [
        (adjust_colour(colour, 0.6), 1, 1),     # shadow layer
        (adjust_colour(colour, 1.35), -1, -1),  # highlight layer
        (colour, 0, 0),
    ]

    for fill, dx, dy in layers:
        draw_stitch_layer(fill, dx, dy)

def calculate_stitch_pitch(settings):
    return settings.stitch_width + settings.stitch_width * settings.stitch_gap_ratio


def calculate_canvas_size(pattern, settings):
    pitch = calculate_stitch_pitch(settings)

    width = pattern.width * pitch * settings.stitch_x_spacing + settings.margin * 2
    height = pattern.height * settings.stitch_height + settings.margin * 2

    return width, height


def calculate_stitch_position(col, row, settings):
    pitch = calculate_stitch_pitch(settings)

    x = settings.margin + col * pitch * settings.stitch_x_spacing
    y = settings.margin + row * settings.stitch_height * settings.stitch_y_spacing

    return x, y

def draw_pattern(pattern, filename, settings):
    width, height = calculate_canvas_size(pattern, settings)

    dwg = svgwrite.Drawing(filename, size=(f"{width}px", f"{height}px"))

    for row in range(pattern.height):
        for col in range(pattern.width):
            colour = pattern[col, row]

            if colour is not None:
                x, y = calculate_stitch_position(col, row, settings)
                draw_stockinette_stitch(dwg, x, y, colour, settings)

    dwg.save()