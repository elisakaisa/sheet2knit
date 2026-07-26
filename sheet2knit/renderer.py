from sheet2knit import pattern
import svgwrite
import random

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

    gap = w * settings.stitch_gap_ratio
    thickness = w * settings.stitch_thickness_ratio

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

        points = left + right[::-1]

        return (
            f"M {points[0][0]} {points[0][1]} "
            + " ".join(
                f"L {x} {y}"
                for x, y in points[1:]
            )
            + " Z "
        )

    return (tapered_strand(0, 0, w / 2 - gap, h) + tapered_strand(w, 0, w / 2 + gap, h))

def calculate_yarn_thickness(settings):
    return settings.stitch_height * 0.4

def darken_colour(hex_colour, factor=0.6):
    """
    Make a hex colour darker.

    factor:
    1.0 = unchanged
    0.0 = black
    """
    r = int(hex_colour[1:3], 16)
    g = int(hex_colour[3:5], 16)
    b = int(hex_colour[5:7], 16)

    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)

    return f"#{r:02x}{g:02x}{b:02x}"

def lighten_colour(hex_colour, factor=1.35):
    """
    Make a hex colour lighter.
    """
    r = int(hex_colour[1:3], 16)
    g = int(hex_colour[3:5], 16)
    b = int(hex_colour[5:7], 16)

    r = min(int(r * factor), 255)
    g = min(int(g * factor), 255)
    b = min(int(b * factor), 255)

    return f"#{r:02x}{g:02x}{b:02x}"


def get_stitch_transform(x, y, settings):
    """
    Adds randomness to the stitch transform
    """
    if not settings.randomize:
        return f"translate({x},{y})"

    rotation = random.uniform(-settings.random_rotation, settings.random_rotation)
    scale = random.uniform(1 - settings.random_scale, 1 + settings.random_scale)

    return (
        f"translate({x},{y}) "
        f"rotate({rotation},{settings.stitch_width/2},{settings.stitch_height/2}) "
        f"scale({scale})"
    )

def add_offset_to_transform(transform, dx, dy):
    return f"{transform} translate({dx},{dy})"


def draw_stockinette_stitch(dwg, x, y, colour, settings):
    stich_path = create_stockinette_stitch_path(settings)
    yarn_width = calculate_yarn_thickness(settings)
    transform = get_stitch_transform(x, y, settings)

    # Shadow layer
    dwg.add(
        dwg.path(
            d=stich_path,
            fill="none",
            stroke=darken_colour(colour),
            stroke_width=yarn_width+4,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=add_offset_to_transform(transform, 2, 3)
        )
    )

    # Highlight layer
    dwg.add(
        dwg.path(
            d=stich_path,
            fill="none",
            stroke=lighten_colour(colour, 1.35),
            stroke_width=yarn_width+1,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=add_offset_to_transform(transform, -1, -1)
        )
    )

    # Main yarn layer
    dwg.add(
        dwg.path(
            d=stich_path,
            fill="none",
            stroke=colour,
            stroke_width=yarn_width,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=transform
        )
    )

def calculate_stitch_pitch(settings):
    yarn_width = calculate_yarn_thickness(settings)

    # Extra room so thick yarn does not collide
    return settings.stitch_width + yarn_width


def calculate_canvas_size(pattern, settings):
    pitch = calculate_stitch_pitch(settings)

    width = (
        pattern.width * pitch * settings.stitch_x_spacing
        + settings.margin * 2
    )

    height = (
        pattern.height * settings.stitch_height
        + settings.margin * 2
    )

    return width, height


def calculate_stitch_position(col, row, settings):
    pitch = calculate_stitch_pitch(settings)

    x = (settings.margin + col * pitch * settings.stitch_x_spacing)
    y = (settings.margin + row * settings.stitch_height)

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