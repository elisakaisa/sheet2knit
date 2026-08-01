import svgwrite

from .colors import adjust_colour
from .layout import calculate_canvas_size, calculate_stitch_position
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

def render_single_stitch(dwg, col, row, colour, settings):
    x, y = calculate_stitch_position(col, row, settings)
    draw_stockinette_stitch(dwg, x, y, colour, settings)

def create_svg(filename, width, height):
    return svgwrite.Drawing(filename, size=(f"{width}px", f"{height}px"))

def render_pattern(pattern, filename, settings, repeat_x=1, repeat_y=1):
    width, height = calculate_canvas_size(
        pattern.width * repeat_x,
        pattern.height * repeat_y,
        settings
    )
    
    dwg = create_svg(filename, width, height)

    for ry in range(repeat_y):
        for rx in range(repeat_x):

            x_offset = rx * pattern.width
            y_offset = ry * pattern.height

            for row in range(pattern.height):
                for col in range(pattern.width):

                    colour = pattern[col, row]
                    if colour is None:
                        continue

                    render_single_stitch(dwg, col + x_offset, row + y_offset, colour, settings)
    dwg.save()

def render_jog_pattern(pattern, filename, settings, jog_column):
    width, height = calculate_canvas_size(pattern.width * 3, pattern.height + 1, settings)

    dwg = create_svg(filename, width, height)

    absolute_jog_column = pattern.width + jog_column

    for row in range(-1, pattern.height):
        for col in range(pattern.width * 3):

            pattern_col = col % pattern.width

            if col >= absolute_jog_column:
                pattern_row = row + 1
            else:
                pattern_row = row

            if pattern_row < 0 or pattern_row >= pattern.height:
                continue

            colour = pattern[pattern_col, pattern_row]

            if colour is None:
                continue

            render_single_stitch(dwg, col, row + 1, colour, settings)

    dwg.save()

