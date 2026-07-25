import svgwrite
import random

STITCH_PATH = (
    "M 0 0 "
    "L 25 30 "
    "M 35 30 "
    "L 60 0"
)

STITCH_WIDTH = 70
STITCH_HEIGHT = 30

RANDOMIZE_STITCHES = True   # adds random rotation and scale to each stitch
RANDOM_ROTATION = 3      # degrees
RANDOM_SCALE = 0.07      # ±7%

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


def get_stitch_transform(x, y):
    if not RANDOMIZE_STITCHES:
        return f"translate({x},{y})"

    rotation = random.uniform(
        -RANDOM_ROTATION,
        RANDOM_ROTATION
    )

    scale = random.uniform(
        1 - RANDOM_SCALE,
        1 + RANDOM_SCALE
    )

    return (
        f"translate({x},{y}) "
        f"rotate({rotation},30,15) "
        f"scale({scale})"
    )

def add_offset_to_transform(transform, dx, dy):
    return f"{transform} translate({dx},{dy})"

def draw_stitch(dwg, x, y, colour):
    transform = get_stitch_transform(x, y)

    # Shadow layer
    dwg.add(
        dwg.path(
            d=STITCH_PATH,
            fill="none",
            stroke=darken_colour(colour),
            stroke_width=14,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=add_offset_to_transform(transform, 2, 3)
        )
    )

    # Highlight layer
    dwg.add(
        dwg.path(
            d=STITCH_PATH,
            fill="none",
            stroke=lighten_colour(colour, 1.35),
            stroke_width=11,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=add_offset_to_transform(transform, -1, -1)
        )
    )

    # Main yarn layer
    dwg.add(
        dwg.path(
            d=STITCH_PATH,
            fill="none",
            stroke=colour,
            stroke_width=10,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=transform
        )
    )


def draw_pattern(pattern, filename):
    margin = 10

    width = pattern.width * STITCH_WIDTH + 40
    height = pattern.height * STITCH_HEIGHT + 40

    dwg = svgwrite.Drawing(
        filename,
        size=(f"{width}px", f"{height}px")
    )

    for row in range(pattern.height):
        for col in range(pattern.width):
            colour = pattern[col, row]

            if colour is not None:
                x = margin + col * STITCH_WIDTH
                y = margin + row * STITCH_HEIGHT

                draw_stitch(
                    dwg,
                    x,
                    y,
                    colour
                )

    dwg.save()