from ast import pattern

import svgwrite

STITCH_PATH = (
    "M 0 0 "
    "L 25 30 "
    "M 35 30 "
    "L 60 0"
)

STITCH_WIDTH = 70
STITCH_HEIGHT = 30


def draw_stitch(dwg, x, y, colour):
    dwg.add(
        dwg.path(
            d=STITCH_PATH,
            fill="none",
            stroke=colour,
            stroke_width=12,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=f"translate({x},{y})"
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