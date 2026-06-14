# Traffic Flow Data Analysis

A Python console and GUI application that analyses real traffic survey data from two road junctions, computes 16 statistical outcomes per dataset, and renders an interactive Tkinter histogram comparing vehicle frequency per hour at each junction. Multiple CSV datasets can be loaded and analysed in a single session.

Built as coursework for *Software Development 1 (COSC006C)* — Software Engineering Level 4, University of Westminster / Informatics Institute of Technology.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [CSV Data Format](#csv-data-format)
- [How to Run](#how-to-run)
- [Computed Outcomes](#computed-outcomes)
- [Histogram GUI](#histogram-gui)
- [Module Breakdown](#module-breakdown)
- [Sample Output](#sample-output)

---

## Overview

The program reads traffic survey CSV files named in the format `traffic_dataDD MM YYYY.csv` (e.g. `traffic_data15062024.csv`). The user enters a date via a validated console prompt, the matching file is loaded, 16 statistical outcomes are computed and displayed, results are appended to `results.txt`, and a Tkinter histogram window opens showing hourly vehicle counts for both junctions side by side.

---

## Features

- **Validated date input** — DD, MM, YYYY each validated separately with range checks, type checks, and calendar validity (e.g. rejects 31 February)
- **16 computed traffic outcomes** per dataset (see full list below)
- **Results saved** to `results.txt` with append mode — multiple runs accumulate in one file
- **Tkinter histogram** — side-by-side bars per hour for both junctions, proportionally scaled, with colour legend and date in heading
- **Multiple dataset support** — Y/N prompt after each file; choosing Y clears previous data and `results.txt`, then loops for a new date
- **FileNotFoundError handling** — re-prompts the user to enter a new date if the file doesn't exist
- **Modular architecture** — Tasks A/B/C in one file imported by Tasks D/E in another

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3 |
| **GUI framework** | Tkinter (`tk.Canvas`, `tk.Tk`) |
| **Data parsing** | `csv.DictReader` |
| **Date handling** | `datetime`, `date`, `strptime` |
| **File I/O** | Built-in `open()` with read/write/append modes |
| **Standard library** | `csv`, `datetime`, `tkinter` |
| **IDE** | Any Python IDE / terminal |
| **Version control** | Git, GitHub |

No third-party packages — runs on Python 3 standard library only.

---

## Project Structure

```
TRAFFIC-FLOW-DATA-ANALYSIS/
│
├── w2120028_ABC.py          # Tasks A, B, C — validation, data processing, file output
├── w2120028_DE.py           # Tasks D, E  — Tkinter histogram, multi-file processor
│
├── traffic_data15062024.csv # Survey data — 15 June 2024
├── traffic_data16062024.csv # Survey data — 16 June 2024
├── traffic_data21062024.csv # Survey data — 21 June 2024
│
├── results.txt              # Auto-generated output — excluded from version control
├── .gitignore
└── README.md
```

---

## CSV Data Format

Each CSV file has one row per vehicle recorded at a junction:

| Column | Type | Example |
|--------|------|---------|
| `JunctionName` | String | `Elm Avenue/Rabbit Road` |
| `Date` | String | `15/06/2024` |
| `timeOfDay` | Time | `08:34:12` |
| `travel_Direction_in` | String | `N` |
| `travel_Direction_out` | String | `N` |
| `Weather_Conditions` | String | `Heavy Rain` |
| `JunctionSpeedLimit` | Integer | `30` |
| `VehicleSpeed` | Integer | `34` |
| `VehicleType` | String | `Truck` |
| `elctricHybrid` | Boolean | `True` |

Two junctions are recorded: **Elm Avenue/Rabbit Road** and **Hanley Highway/Westway**.

---

## How to Run

**Requirements:** Python 3.8+ (no external packages needed)

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/traffic-flow-data-analysis.git
cd traffic-flow-data-analysis

# 2. Run the main program (Tasks A–E, includes histogram)
python w2120028_DE.py

# OR run Tasks A–C only (console output, no GUI)
python w2120028_ABC.py
```

When prompted:
```
Please enter the day of the survey in the format DD: 15
Please enter the month of the survey in the format MM: 06
Please enter the year of the survey in the format YYYY: 2024
```
This loads `traffic_data15062024.csv`, prints all 16 outcomes, saves to `results.txt`, and opens the histogram window.

---

## Computed Outcomes

For each loaded CSV file, the program computes and displays all of the following:

| # | Outcome |
|---|---------|
| 1 | Selected data file name |
| 2 | Total number of vehicles for the date |
| 3 | Total number of trucks |
| 4 | Total number of electric/hybrid vehicles |
| 5 | Total number of two-wheeled vehicles (bicycle, motorcycle, scooter) |
| 6 | Total number of buses leaving Elm Avenue/Rabbit Road heading North |
| 7 | Total vehicles passing through both junctions without turning (direction in == direction out) |
| 8 | Percentage of total vehicles that are trucks (rounded to nearest %) |
| 9 | Average number of bicycles per hour across 24 hours |
| 10 | Total vehicles recorded over the speed limit |
| 11 | Total vehicles through Elm Avenue/Rabbit Road |
| 12 | Total vehicles through Hanley Highway/Westway |
| 13 | Percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters |
| 14 | Highest number of vehicles in any single hour on Hanley Highway/Westway |
| 15 | The hour range when peak traffic occurred on Hanley Highway/Westway |
| 16 | Number of hours during which rain was recorded (heavy or light) |

---

## Histogram GUI

The Tkinter window (`HistogramApp`) displays:

- **Title:** `Histogram of Vehicle Frequency per Hour (DD/MM/YYYY)`
- **Two bars per hour** (hours 00–23 on x-axis):
  - **Purple** — Elm Avenue/Rabbit Road
  - **Sky blue** — Hanley Highway/Westway
- Vehicle count displayed above each bar
- Bars scaled proportionally to the maximum hourly count across both junctions
- **Colour legend** in the top-left corner
- **X-axis label:** `Hours 00:00 to 24:00`
- Canvas: 1000×600px, lavender background

---

## Module Breakdown

### `w2120028_ABC.py` — Tasks A, B, C

**Task A — Input Validation**

`validate_date_input()` — prompts for DD, MM, YYYY separately. Each field loops until valid:
- Type check: rejects non-integers with `"Integer required!!!"`
- Range check: day 1–31, month 1–12, year 2000–2024
- Calendar check: `date(year, month, day)` catches invalid combinations (e.g. 31 April)
- `process_file_name(day, month, year)` — zero-pads day/month and returns `traffic_dataDDMMYYYY.csv`
- `validate_continue_input()` — Y/N prompt using `match/case`, strips whitespace, case-insensitive

**Task B — Processing**

`process_csv_data(file_name)` — reads the CSV with `csv.DictReader`, iterates every row, and accumulates all 16 outcome values using global variables reset at the start of each call. Returns an `outcomes` list.

`display_outcomes(outcomes)` — formats and prints all 16 outcomes; returns the formatted string for saving.

**Task C — File Output**

`save_results_to_file(output_text)` — appends the formatted output to `results.txt` using `open("results.txt", "a")`.

---

### `w2120028_DE.py` — Tasks D, E

**Task D — `HistogramApp` class**

| Method | Description |
|--------|-------------|
| `__init__` | Stores `traffic_data` dict and `survey_date`, creates `tk.Tk()` instance |
| `setup_window()` | Sets 1000×600 geometry, creates lavender canvas |
| `add_legend()` | Draws heading with date, two colour legend boxes, x-axis label |
| `draw_histogram()` | Loops hours 0–23, calculates bar heights proportional to `max_value`, draws both bars per hour with value labels above and hour label below |
| `run()` | Calls setup, legend, histogram, then `mainloop()` |

**Task E — `MultiCSVProcessor` class**

| Method | Description |
|--------|-------------|
| `__init__` | Initialises two `hour_counts` arrays of 24 zeros (one per junction) |
| `handle_user_interaction()` | Full date validation loop (mirrors Task A, re-implemented for class use) |
| `load_csv_file(file_name)` | Reads CSV, populates `hour_counts` and `hour_counts2` by junction; returns `True`/`False` |
| `process_file_name()` | Returns formatted filename string using f-string zero-padding |
| `clear_previous_data()` | Resets hour count arrays, clears `results.txt`, prints confirmation |
| `process_files()` | Main loop: validates date → builds filename → loads CSV → calls ABC functions → builds `traffic_data` dict → launches `HistogramApp` → Y/N to continue |

---

## Sample Output

**Console (15/06/2024):**
```
Here is the requested traffic data.

*********************************
The selected data file: traffic_data15062024.csv
*********************************

The total number of vehicles for this date: 1037
The total number of trucks for this date: 109
The total number of electric vehicles for this date: 368
The total number of "two wheeled" vehicles for this date: 401
The total number of busses leaving Elm Avenue/Rabbit Road heading north: 15
The total number of vehicles passing through both junctions without turning: 363
The percentage of total vehicles recorded that are Trucks for this date: 11%
The average number Bicycles per hour for this date: 7
The total number of vehicles recorded as over the speed limit for this date: 205
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction: 494
The total number of vehicles recorded through Hanley Highway/Westway junction: 543
10% of vehicles recorded through Elm Avenue/Rabbit Road that are Scooters.
The highest number of vehicles in an hour on Hanley Highway/Westway: 39
The most vehicles through Hanley Highway/Westway were recorded between: 18:00 between 19:00
The number of hours of rain for this date: 0

*********************************
```
