import os
import click
import mimetypes
from rich import print
from rich.table import Table
from rich.prompt import Prompt
from .src.tmdb_api import TMDB

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Rename Episodes Using the TMDB Database."""
    pass


@click.command(short_help="Rename TV Series.")
@click.option(
    "--url",
    "-u",
    type=str,
    required=True,
    help="TMDB TV Series Website URL.",
    metavar="<website_url>",
)
@click.option(
    "--dir",
    "-d",
    type=str,
    required=False,
    help="Local TV Series Folder Path.",
    metavar="<folder_path>",
)
def tv(url, dir):
    try:
        tv = TMDB().get_tv(tv_url=url)
        # TMDB Data Processing
        tv_name = tv["name"]
        tv_seasons = tv["seasons"]
        if len(tv_seasons) > 1:
            # Multiple Seasons
            table = Table(title=tv_name, show_header=True, header_style="bold")
            table.add_column("Index", justify="center", style="magenta", no_wrap=True)
            table.add_column(
                "Season Name", justify="center", style="cyan", no_wrap=True
            )
            table.add_column("Air Date", justify="center", style="cyan")
            table.add_column("Episodes", justify="right", style="cyan")
            season_index = 0
            for s in tv_seasons:
                table.add_row(
                    *[
                        str(season_index),
                        s["name"],
                        s["air_date"],
                        str(s["episode_count"]),
                    ]
                )
                season_index += 1
            print(table)
            season_numbers = [str(n) for n in range(len(tv_seasons))]
            season_index = Prompt.ask(
                "[green]→[/green] Please Select a Season Index:",
                choices=season_numbers,
                default=season_numbers[-1],
            )
            # Select Season by User Input
            season_selected = tv_seasons[int(season_index)]
        else:
            # Select Season by Default
            season_selected = tv_seasons[0]
        season_number = season_selected["season_number"]
        season_episode_count = season_selected["episode_count"]
        season_name = f"{tv_name}.S{season_number:02d}"
        print(f"[green bold]✓ Season Selected: {season_name}[/green bold]")
        # Local Data Processing
        # Get Local Files
        for root, dirs, files in os.walk(dir):
            file_names = []
            # Get File Names
            for file_name in sorted(files):
                # Guess Video File Type
                file_type = mimetypes.guess_type(file_name)[0]
                # Check if File is Video
                if file_type is not None and file_type.startswith("video"):
                    file_names.append(file_name)
        # Check if File Count Matches
        if len(file_names) != season_episode_count:
            # File Count Mismatch
            print(
                f"[yellow bold]✕ Mismatch between the number of local files and the Episodes[/yellow bold]"
            )
            episode_start = Prompt.ask(
                "[green]→[/green] Please Enter the Start Episode Number:",
                choices=[
                    str(n) for n in range(1, season_episode_count - len(file_names) + 2)
                ],
                default="1",
            )
            episode_numbers = [
                n
                for n in range(int(episode_start), int(episode_start) + len(file_names))
            ]
        else:
            # File Count Match
            episode_numbers = [n for n in range(1, season_episode_count + 1)]
        # Rename Files Correctly
        print(f"[green]→[/green] Please Check the Files to be Renamed:")
        new_file_names = []
        for episode_number, file_name in zip(episode_numbers, file_names):
            # Add Season Number to Episode Name
            file_ext = os.path.splitext(file_name)[1]
            episode_name = f"{season_name}.E{episode_number:02d}{file_ext}"
            # Clean Episode Name
            badchars = '\\/:*?"<>|'
            for char in badchars:
                episode_name = episode_name.replace(char, "")
            new_file_names.append(episode_name)
            print(f"{file_name} → {episode_name}")
        # Rename Files
        if click.confirm(f"→ Do you want to rename the files?", default=True):
            renamed_counts = 0
            for file_name, new_file_name in zip(file_names, new_file_names):
                # Check if File Exists
                if new_file_name not in file_names:
                    # Rename File
                    os.rename(
                        os.path.join(dir, file_name), os.path.join(dir, new_file_name)
                    )
                    renamed_counts += 1
            print(f"[green bold]✓ {renamed_counts} Files Renamed.[/green bold]")
        # Rename Folders
        if click.confirm(f"→ Do you want to rename the folder?", default=True):
            # Clean Season Name
            badchars = '\\/:*?"<>|'
            for char in badchars:
                season_name = season_name.replace(char, "")
            # Rename Folder
            os.rename(dir, season_name)
            print(f"[green bold]✓ Folder Renamed:[/green bold] {dir} → {season_name}")
    except Exception as e:
        print(f"[red]✕[/] {str(e)}")
        print(
            f"[green]→ You can report this issue here: https://github.com/huhuhang/tmdb-renamer/issues[/green]"
        )


cli.add_command(tv)

if __name__ == "__main__":
    cli()

