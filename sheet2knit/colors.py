def hex_to_rgb(hex_colour):
    return tuple(
        int(hex_colour[i:i+2], 16)
        for i in (1, 3, 5)
    )

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def adjust_colour(hex_colour, factor):
    rgb = hex_to_rgb(hex_colour)

    adjusted = tuple(
        min(int(channel * factor), 255)
        for channel in rgb
    )

    return rgb_to_hex(adjusted)