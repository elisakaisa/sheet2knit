import svgwrite

STITCH_PATH = (
    "M 10 10 "
    "L 30 40 "
    "L 50 10"
)

STITCH_WIDTH = 60
STITCH_HEIGHT = 50


def draw_stitch(dwg, x, y, colour):
    dwg.add(
        dwg.path(
            d=STITCH_PATH,
            fill="none",
            stroke=colour,
            stroke_width=4,
            stroke_linecap="round",
            stroke_linejoin="round",
            transform=f"translate({x},{y})"
        )
    )


def draw_pattern(pattern, filename):
    width = pattern.width * STITCH_WIDTH
    height = pattern.height * STITCH_HEIGHT

    dwg = svgwrite.Drawing(
        filename,
        size=(f"{width}px", f"{height}px")
    )

    for row in range(pattern.height):
        for col in range(pattern.width):
            colour = pattern[col, row]

            if colour is not None:
                x = col * STITCH_WIDTH
                y = row * STITCH_HEIGHT

                draw_stitch(
                    dwg,
                    x,
                    y,
                    colour
                )

    dwg.save()