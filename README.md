# TMDB Renamer

Some movie and episode management applications, such as Infuse, Plex, can automatically match episode metadata from TMDB, but require episodes to have canonical names. This tool will rename episodes to match the [canonical names](https://support.firecore.com/hc/en-us/articles/215090947-Metadata-101#heading-3).

TMDB Renamer can be used directly after installation without additional configuration.

## Installation

Clone the repository and install the dependencies, Supposing you have Python 3.8+ installed:

```bash
git clone https://github.com/huhuhang/tmdb-renamer
cd tmdb-renamer
pip install --editable .
```

Show help message:

```bash
$ tmdb tv -h
Usage: tmdb tv [OPTIONS]

Options:
  -u, --url <website_url>  TMDB TV Series Website URL.  [required]
  -d, --dir <folder_path>  Local TV Series Folder Path.
  -h, --help               Show this message and exit.
```

## Usage

Step 1: Find and copy the TMDB TV Series Website URL from [TMDB website](https://www.themoviedb.org/), for example, the URL of [Star Wars: Andor (2022)](https://www.themoviedb.org/tv/83867-star-wars-andor):

```text
https://www.themoviedb.org/tv/83867-star-wars-andor
```

Step 2: Using the `tree` command to list the files in a demo directory:

```bash
$ tree test_folder/
test_folder/
├── 01.mp4
├── 02.mp4
├── 03.mp4
├── 04.mp4
├── 05.mp4
├── 06.mp4
└── 07.mp4

0 directories, 7 files
```

Step 3: Run the `tmdb-renamer` command:

```bash
$ tmdb tv --url https://www.themoviedb.org/tv/83867-star-wars-andor --dir test_folder/
               Star Wars: Andor
┏━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Index ┃ Season Name ┃  Air Date  ┃ Episodes ┃
┡━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│   0   │  Specials   │ 2022-09-17 │        1 │
│   1   │  Season 1   │ 2022-09-21 │       12 │
└───────┴─────────────┴────────────┴──────────┘
→ Please Select a Season Index: [0/1] (1):
✓ Season Selected: Star Wars: Andor.S01
✕ Mismatch between the number of local files and the Episodes
→ Please Enter the Start Episode Number: [1/2/3/4/5/6] (1):
→ Please Check the Files to be Renamed:
01.mp4 → Star Wars Andor.S01.E01.mp4
02.mp4 → Star Wars Andor.S01.E02.mp4
03.mp4 → Star Wars Andor.S01.E03.mp4
04.mp4 → Star Wars Andor.S01.E04.mp4
05.mp4 → Star Wars Andor.S01.E05.mp4
06.mp4 → Star Wars Andor.S01.E06.mp4
07.mp4 → Star Wars Andor.S01.E07.mp4
→ Do you want to rename the files? [Y/n]:
✓ 7 Files Renamed.
→ Do you want to rename the folder? [Y/n]:
✓ Folder Renamed: test_folder/ → Star Wars Andor.S01
```

Step 4: Checking the files are renamed:

```bash
$ tree Star\ Wars\ Andor.S01/
Star Wars Andor.S01/
├── Star Wars Andor.S01.E01.mp4
├── Star Wars Andor.S01.E02.mp4
├── Star Wars Andor.S01.E03.mp4
├── Star Wars Andor.S01.E04.mp4
├── Star Wars Andor.S01.E05.mp4
├── Star Wars Andor.S01.E06.mp4
└── Star Wars Andor.S01.E07.mp4

0 directories, 7 files
```
