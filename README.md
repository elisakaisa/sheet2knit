# sheet2knit

Convert coloured spreadsheet patterns into SVG knitting charts.

`sheet2knit` reads an Excel spreadsheet where each cell's background colour represents a stitch colour, then renders the pattern as a simple stockinette-style SVG visualization.

The current renderer uses V-shaped stitches as the basic building block. The stitch appearance will evolve over time.

Some randomness in rotation and scale is applied, as well as some shading on the stich for a more realistic look.

## Features

* Reads `.xlsx` knitting patterns
* Converts cell background colours into stitch colours
* Outputs scalable SVG files
* Keeps the pattern representation separate from the renderer

## Quick start (Docker)

Docker is the recommended way to run `sheet2knit`, as it requires no Python installation or dependency management.

Clone the repository:
```bash
git clone https://github.com/elisakaisa/sheet2knit.git
cd sheet2knit
```

Build the container:
```bash
docker compose build
```

Place one or more Excel pattern files in the sample directory:

```text
sheet2knit/
├── sample/
│   ├── mittens.xlsx
│   └── socks.xlsx
├── compose.yaml
└── ...
```

Run:
```bash
docker compose run --rm sheet2knit
```

An SVG file will be generated next to each input spreadsheet:

```text
sample/
├── mittens.xlsx
├── mittens.svg
├── socks.xlsx
└── socks.svg
```

Open the generated SVG in a web browser, VS Code, or any SVG-compatible viewer.

## Running locally with Python

If you prefer not to use Docker:
Clone the repository:
```bash
git clone https://github.com/elisakaisa/sheet2knit.git
cd sheet2knit
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python3 -m sheet2knit
```

The program searches the `sample` directory for `.xlsx` files and generates matching `.svg` files in the same location.


## Input format

The input spreadsheet should use cell background colours as the pattern.

Example:

|    |    |    |
| -- | -- | -- |
| 🟥 | 🟥 | 🟦 |
| 🟩 | 🟥 | 🟥 |

Cell values are ignored. Only the background colours are used.

## Project structure

```text
sheet2knit/
│
├── sample/
├── sheet2knit/
│   ├── cli.py              # Command-line entry point
│   ├── reader.py           # Excel reader
│   ├── pattern.py          # Pattern data model
│   ├── render_settings.py  # Rendering settings
│   └── renderer.py         # SVG renderer
│
├── compose.yaml 
├── Dockerfile 
├── requirements.txt
└── README.md
```

## AI usage note

AI assistance was used through a browser-based chatbot as a conversational development aid for brainstorming, debugging, and reviewing implementation ideas.

No autonomous coding agents or AI-assisted development workflows were used. All code was manually written, adapted, reviewed, and tested by the author.

Documentation was AI-generated, and reviewed by the author.

## Development notes

Future improvements:

* More realistic stockinette stitch rendering
* Better yarn texture and shading -> shading partly done
* Adjustable stitch size -> partly done, not fully tested
* Support for more spreadsheet formats
* Command-line options for output filename and rendering style
