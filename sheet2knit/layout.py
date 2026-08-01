def calculate_stitch_pitch(settings):
    return settings.stitch_width + settings.stitch_width * settings.stitch_gap_ratio


def calculate_canvas_size(width_stitches, height_stitches, settings):
    pitch = calculate_stitch_pitch(settings)

    width = width_stitches * pitch * settings.stitch_x_spacing + settings.margin * 2
    height = height_stitches * settings.stitch_height + settings.margin * 2

    return width, height


def calculate_stitch_position(col, row, settings):
    pitch = calculate_stitch_pitch(settings)

    x = settings.margin + col * pitch * settings.stitch_x_spacing
    y = settings.margin + row * settings.stitch_height * settings.stitch_y_spacing

    return x, y