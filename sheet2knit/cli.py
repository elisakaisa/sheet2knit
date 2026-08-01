from sheet2knit.render_settings import RenderSettings

from .reader import read_pattern
from .renderer import render_jog_pattern, render_pattern
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

        if settings.jog_simulation_enabled:
            jog_folder = output_file.with_name(f"{output_file.stem}-jogsimulations")
            jog_folder.mkdir(exist_ok=True)

            for jog_column in range(pattern.width):
                jog_file = ( jog_folder / f"{output_file.stem}-jog{jog_column + 1}.svg")

                render_jog_pattern(pattern, jog_file, settings, jog_column)

            print(f"Created {pattern.width} jog simulation files in {jog_folder}")


if __name__ == "__main__":
    main()