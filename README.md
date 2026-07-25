# sheet2knit

Convert coloured spreadsheet patterns into SVG knitting charts.

`sheet2knit` reads an Excel spreadsheet where each cell's background colour represents a stitch colour, then renders the pattern as a simple stockinette-style SVG visualization.

The current renderer uses \/-shaped stitches as the basic building block. The stitch appearance will evolve over time.

Some randomness in rotation and scale is applied, as well as some shading on the stich for a more realsitic look

## Features

* Reads `.xlsx` knitting patterns
* Converts cell background colours into stitch colours
* Outputs scalable SVG files
* Keeps the pattern representation separate from the renderer

## Setup

Clone the repository and enter the project folder:

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

## Usage

Place your Excel pattern file in the project folder, replacing any existing ones. Name does matter, the program will pick the first one it can find

Example:

```text
sheet2knit/
├── sample/
|    └── <excelname>.xlsx
├── requirements.txt
└── sheet2knit/
```

Run:

```bash
python -m sheet2knit
```

The program will generate in the same sample folder:

```text
<excelname>.svg
```

Open the SVG file in a browser / VS code / somewhere to view the pattern in a stockinette stich mock up.

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
├── sheet2knit/
│   ├── cli.py        # Command-line entry point
│   ├── reader.py     # Excel reader
│   ├── pattern.py    # Pattern data model
│   └── renderer.py   # SVG renderer
│
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
* Make it a Docker container
