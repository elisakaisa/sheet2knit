class Pattern:
    def __init__(self, colours):
        self.colours = colours

    @property
    def width(self):
        return len(self.colours[0]) if self.colours else 0

    @property
    def height(self):
        return len(self.colours)

    def colour(self, row, col):
        return self.colours[row][col]

    def __getitem__(self, pos):
        x, y = pos
        return self.colours[y][x]

    def __str__(self):
        return "\n".join(
            " ".join(colour or "EMPTY" for colour in row)
            for row in self.colours
        )