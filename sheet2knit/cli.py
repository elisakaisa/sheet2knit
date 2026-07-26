from sheet2knit.render_settings import RenderSettings

from .reader import read_pattern
from .renderer import draw_pattern
from pathlib import Path

def find_input_files():
    sample_folder = Path("sample")
    files = sorted(sample_folder.glob("*.xlsx"))

    if not files:
        raise FileNotFoundError("No .xlsx files found in the sample directory.")

    return files

def main():
    settings = RenderSettings()

    for input_file in find_input_files():
        pattern = read_pattern(input_file)

        output_file = input_file.with_suffix(".svg")

        draw_pattern(pattern, output_file, settings)

        print(f"Created {output_file}")


if __name__ == "__main__":
    main()