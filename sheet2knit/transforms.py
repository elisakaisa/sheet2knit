import random


def get_stitch_transform(x, y, settings):
    """
    Adds randomness to the stitch transform
    """
    if not settings.randomize:
        return f"translate({x},{y})"

    rotation = random.uniform(-settings.random_rotation, settings.random_rotation)
    scale_factor = random.uniform(1 - settings.random_scale, 1 + settings.random_scale)

    return make_transform(
        translate(x, y),
        rotate(
            rotation,
            settings.stitch_width / 2,
            settings.stitch_height / 2
        ),
        scale(scale_factor)
    )

def make_transform(*parts):
    return " ".join(parts)


def translate(x, y):
    return f"translate({x},{y})"


def rotate(angle, cx, cy):
    return f"rotate({angle},{cx},{cy})"


def scale(value):
    return f"scale({value})"

def add_offset_to_transform(transform, dx, dy):
    return f"{transform} {translate(dx, dy)}"