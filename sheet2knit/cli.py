from .reader import read_pattern
from .renderer import draw_pattern


def main():
    input_file = "test-pattern.xlsx"

    pattern = read_pattern(input_file)

    draw_pattern(
        pattern,
        "fabric.svg"
    )

    print("Created fabric.svg")


if __name__ == "__main__":
    main()