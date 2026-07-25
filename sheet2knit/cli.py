from sheet2knit.render_settings import RenderSettings

from .reader import read_pattern
from .renderer import draw_pattern
from pathlib import Path

def find_input_file():
    sample_folder = Path("sample")

    files = list(sample_folder.glob("*.xlsx"))

    if not files:
        raise FileNotFoundError("No .xlsx files found")

    return files[0]

def main():
    input_file = find_input_file()

    pattern = read_pattern(input_file)

    settings = RenderSettings(
        stitch_width=70,
        stitch_height=30,
        randomize=True
    )

    output_file = input_file.with_suffix(".svg")

    draw_pattern(
        pattern,
        output_file,
        settings
    )

    print(f"Created {output_file}")


if __name__ == "__main__":
    main()