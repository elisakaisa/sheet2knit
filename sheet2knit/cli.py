from sheet2knit.render_settings import RenderSettings

from .reader import read_pattern
from .renderer import render_pattern
from pathlib import Path

def find_input_files():
    sample_folder = Path("sample")
    files = sorted(sample_folder.rglob("*.xlsx"))

    if not files:
        raise FileNotFoundError("No .xlsx files found in the sample directory.")

    return files

def main():
    settings = RenderSettings()

    for input_file in find_input_files():
        pattern = read_pattern(input_file)

        output_file = input_file.with_suffix(".svg")
        output_file_repeat = output_file.with_name(f"{output_file.stem}-repeat{output_file.suffix}")

        render_pattern(pattern, output_file, settings)
        render_pattern(pattern, output_file_repeat, settings, repeat_x=3, repeat_y=3)

        print(f"Created {output_file}")
        print(f"Created {output_file_repeat}")


if __name__ == "__main__":
    main()