from openpyxl import load_workbook
from .pattern import Pattern


def excel_rgb_to_hex(rgb):
    """Convert an Excel ARGB colour (e.g. 'FFFF0000') to '#ff0000'."""
    if rgb is None:
        return None

    return "#" + rgb[-6:].lower()

wb = load_workbook("test-pattern.xlsx")
ws = wb.active

def read_pattern(filename):
    wb = load_workbook(filename)
    ws = wb.active

    rows = []

    for row in ws.iter_rows():
        current_row = []

        for cell in row:
            fill = cell.fill

            if fill.fill_type is None:
                current_row.append(None)
            else:
                current_row.append(excel_rgb_to_hex(fill.fgColor.rgb))

        rows.append(current_row)

    return Pattern(rows)