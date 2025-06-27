#!/usr/bin/env python3
"""
YouTube Music Downloader using yt-dlp
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.prompt import Confirm, Prompt
from rich.table import Table


class YouTubeDownloader:
    def __init__(self):
        self.console = Console()
        self.setup_logging()
        self.config = self.load_config()
        self.stats = {"downloaded": 0, "failed": 0, "skipped": 0}
        self.check_yt_dlp()

    def setup_logging(self):
        """Setup logging with both file and console handlers"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Create log filename with timestamp
        log_file = (
            log_dir
            / f"youtube_downloader_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                RichHandler(console=self.console, show_time=False, show_path=False),
            ],
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"YouTube Downloader started - Log file: {log_file}")

    def load_config(self) -> dict:
        """Load configuration from config.json or create default"""
        config_file = Path("config.json")
        default_config = {
            "download_directory": "downloads",
            "audio_quality": "192",
            "video_quality": "best[height<=720]",
            "audio_format": "mp3",
            "video_format": "mp4",
            "naming_format": "%(artist)s - %(title)s.%(ext)s",
            "skip_existing": True,
            "embed_metadata": True,
            "embed_thumbnail": True,
            "write_description": False,
            "write_info_json": False,
        }

        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    return {**default_config, **config}
            except Exception as e:
                self.logger.warning(f"Error loading config: {e}. Using defaults.")
        else:
            # Create default config file
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
            self.logger.info("Created default config.json")

        return default_config

    def check_yt_dlp(self):
        """Check if yt-dlp is installed and accessible"""
        try:
            result = subprocess.run(
                ["yt-dlp", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.logger.info(f"Using yt-dlp version: {version}")
            else:
                raise Exception("yt-dlp not working properly")
        except Exception as e:
            self.console.print("[red]❌ yt-dlp is not installed or not working[/red]")
            self.console.print("[yellow]Install with: pip install yt-dlp[/yellow]")
            self.logger.error(f"yt-dlp check failed: {e}")
            sys.exit(1)

    def extract_artist_title(self, title: str) -> tuple[str, str]:
        """Extract artist and title from video title"""
        import re

        patterns = [
            r"^(.+?)\s*-\s*(.+)$",  # Artist - Title
            r"^(.+?)\s*\|\s*(.+)$",  # Artist | Title
            r"^(.+?)\s*:\s*(.+)$",  # Artist : Title
            r"^(.+?)\s*–\s*(.+)$",  # Artist – Title (em dash)
        ]

        for pattern in patterns:
            match = re.match(pattern, title.strip())
            if match:
                artist, song = match.groups()
                return artist.strip(), song.strip()

        # If no pattern matches, use "Unknown Artist"
        return "Unknown Artist", title.strip()

    def build_yt_dlp_args(self, url: str, audio_only: bool = False) -> List[str]:
        """Build yt-dlp command arguments"""
        download_dir = Path(self.config["download_directory"])
        download_dir.mkdir(exist_ok=True)

        args = ["yt-dlp"]

        # Output directory and template
        if audio_only:
            # For audio, use artist - title format
            output_template = str(
                download_dir / "%(uploader,artist)s - %(title)s.%(ext)s"
            )
        else:
            # For video, use title [id] format
            output_template = str(download_dir / "%(title)s [%(id)s].%(ext)s")

        args.extend(["-o", output_template])

        # Format selection
        if audio_only:
            # Extract audio and convert to specified format
            args.extend(
                [
                    "-x",  # Extract audio
                    "--audio-format",
                    self.config["audio_format"],
                    "--audio-quality",
                    self.config["audio_quality"],
                ]
            )
        else:
            # Download video in specified quality
            video_format = self.config["video_quality"]
            args.extend(["-f", f"{video_format}+bestaudio/best"])

        # Metadata and thumbnails
        if self.config["embed_metadata"]:
            args.append("--embed-metadata")

        if self.config["embed_thumbnail"]:
            args.append("--embed-thumbnail")

        if self.config["write_description"]:
            args.append("--write-description")

        if self.config["write_info_json"]:
            args.append("--write-info-json")

        # Skip if file exists
        if self.config["skip_existing"]:
            args.append("--no-overwrites")

        # Progress and other options
        args.extend(
            [
                "--no-warnings",
                "--newline",  # Progress on new lines for better parsing
            ]
        )

        # Add URL
        args.append(url)

        return args

    def download_video(self, url: str, audio_only: bool = False) -> bool:
        """Download a single video using yt-dlp"""
        try:
            # Get video info first
            with self.console.status("[cyan]Fetching video info..."):
                info_args = ["yt-dlp", "--dump-json", "--no-warnings", url]
                result = subprocess.run(
                    info_args, capture_output=True, text=True, timeout=30
                )

                if result.returncode != 0:
                    raise Exception(f"Failed to get video info: {result.stderr}")

                try:
                    info = json.loads(result.stdout)
                except json.JSONDecodeError:
                    raise Exception("Invalid JSON response from yt-dlp")

            # Display video info
            title = info.get("title", "Unknown Title")
            uploader = info.get("uploader", "Unknown Uploader")
            duration = info.get("duration", 0)
            view_count = info.get("view_count", 0)

            artist, song = self.extract_artist_title(title)

            info_table = Table(show_header=False, box=None)
            info_table.add_row("[bold]Title:", title)
            info_table.add_row("[bold]Uploader:", uploader)
            info_table.add_row("[bold]Artist:", artist)
            info_table.add_row("[bold]Song:", song)
            if duration:
                info_table.add_row(
                    "[bold]Duration:", f"{duration // 60}:{duration % 60:02d}"
                )
            if view_count:
                info_table.add_row("[bold]Views:", f"{view_count:,}")

            self.console.print(
                Panel(info_table, title="📹 Video Info", border_style="blue")
            )

            # Build download command
            args = self.build_yt_dlp_args(url, audio_only)

            mode = "Audio Only" if audio_only else "Video"
            self.console.print(f"[green]📥 Downloading {mode}...[/green]")

            # Execute download with progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Downloading..."),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console,
            ) as progress:
                task = progress.add_task("download", total=100)

                process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )

                output_lines = []
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break

                    if line:
                        output_lines.append(line.strip())
                        # Try to parse progress from yt-dlp output
                        if "%" in line and "ETA" in line:
                            try:
                                # Parse percentage from yt-dlp output
                                parts = line.split()
                                for part in parts:
                                    if "%" in part:
                                        percent_str = part.replace("%", "")
                                        try:
                                            percent = float(percent_str)
                                            progress.update(task, completed=percent)
                                            break
                                        except ValueError:
                                            pass
                            except Exception:
                                pass

                return_code = process.wait()

            if return_code == 0:
                self.console.print("[green]✅ Download completed successfully![/green]")
                self.logger.info(f"Successfully downloaded: {title}")
                self.stats["downloaded"] += 1
                return True
            else:
                # Log the output for debugging
                error_output = "\n".join(output_lines[-10:])  # Last 10 lines
                error_msg = f"Download failed with return code {return_code}"
                self.console.print(f"[red]❌ {error_msg}[/red]")
                self.logger.error(f"{error_msg}\nOutput: {error_output}")
                self.stats["failed"] += 1
                return False

        except subprocess.TimeoutExpired:
            self.console.print("[red]❌ Download timed out[/red]")
            self.logger.error(f"Download timed out for {url}")
            self.stats["failed"] += 1
            return False
        except Exception as e:
            error_msg = f"Failed to download {url}: {str(e)}"
            self.console.print(f"[red]❌ {error_msg}[/red]")
            self.logger.error(error_msg)
            self.stats["failed"] += 1
            return False

    def download_playlist(self, url: str, audio_only: bool = False) -> None:
        """Download entire playlist using yt-dlp"""
        try:
            # Get playlist info
            with self.console.status("[cyan]Fetching playlist info..."):
                info_args = [
                    "yt-dlp",
                    "--flat-playlist",
                    "--dump-json",
                    "--no-warnings",
                    url,
                ]
                result = subprocess.run(
                    info_args, capture_output=True, text=True, timeout=60
                )

                if result.returncode != 0:
                    raise Exception(f"Failed to get playlist info: {result.stderr}")

                # Parse playlist entries
                entries = []
                for line in result.stdout.strip().split("\n"):
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            entries.append(entry)
                        except json.JSONDecodeError:
                            continue

                if not entries:
                    raise Exception("No videos found in playlist")

            playlist_title = (
                entries[0].get("playlist_title", "Unknown Playlist")
                if entries
                else "Unknown Playlist"
            )

            playlist_info = Table(show_header=False, box=None)
            playlist_info.add_row("[bold]Playlist:", playlist_title)
            playlist_info.add_row("[bold]Videos:", f"{len(entries)}")
            playlist_info.add_row(
                "[bold]Mode:", f"{'Audio Only' if audio_only else 'Video'}"
            )

            self.console.print(
                Panel(playlist_info, title="📑 Playlist Info", border_style="green")
            )

            if not Confirm.ask(f"Download {len(entries)} videos?"):
                return

            self.console.print("\n[bold]Starting playlist download...[/bold]")

            failed_videos = []
            for idx, entry in enumerate(entries, 1):
                video_url = (
                    entry.get("url")
                    or f"https://www.youtube.com/watch?v={entry.get('id')}"
                )
                video_title = entry.get("title", "Unknown Title")

                self.console.print(
                    f"\n[bold cyan]({idx}/{len(entries)})[/bold cyan] {video_title}"
                )
                success = self.download_video(video_url, audio_only)
                if not success:
                    failed_videos.append((idx, video_title, video_url))

            # Report failed videos
            if failed_videos:
                self.console.print(
                    f"\n[yellow]⚠️  {len(failed_videos)} videos failed to download:[/yellow]"
                )
                for idx, title, url in failed_videos[:5]:  # Show first 5 failed videos
                    self.console.print(f"  {idx}: {title}")
                if len(failed_videos) > 5:
                    self.console.print(f"  ... and {len(failed_videos) - 5} more")

        except Exception as e:
            error_msg = f"Error processing playlist: {str(e)}"
            self.console.print(f"[red]❌ {error_msg}[/red]")
            self.logger.error(error_msg)

            # Provide helpful suggestions
            self.console.print("\n[yellow]💡 Troubleshooting suggestions:[/yellow]")
            self.console.print(
                "[yellow]1. Check if the playlist is public and accessible[/yellow]"
            )
            self.console.print(
                "[yellow]2. Try downloading individual videos instead[/yellow]"
            )
            self.console.print(
                "[yellow]3. Update yt-dlp: pip install --upgrade yt-dlp[/yellow]"
            )

    def show_stats(self):
        """Display download statistics"""
        stats_table = Table(show_header=False, box=None)
        stats_table.add_row("[green]✅ Downloaded:", f"{self.stats['downloaded']}")
        stats_table.add_row("[red]❌ Failed:", f"{self.stats['failed']}")
        stats_table.add_row("[yellow]⚠️  Skipped:", f"{self.stats['skipped']}")

        total = sum(self.stats.values())
        if total > 0:
            success_rate = (self.stats["downloaded"] / total) * 100
            stats_table.add_row("[bold]Success Rate:", f"{success_rate:.1f}%")

        self.console.print(
            Panel(stats_table, title="📊 Download Statistics", border_style="magenta")
        )

    def show_tips(self):
        """Show helpful tips"""
        tips = [
            "💡 [dim]Tips:[/dim]",
            "[dim]• Use Ctrl+C to exit anytime[/dim]",
            "[dim]• If downloads fail, try updating: pip install --upgrade yt-dlp[/dim]",
            "[dim]• For problematic playlists, try downloading videos individually[/dim]",
            "[dim]• Check logs/ directory for detailed error information[/dim]",
            "[dim]• Edit config.json to customize download settings[/dim]",
        ]

        for tip in tips:
            self.console.print(tip)

    def main_menu(self):
        """Interactive main menu"""
        self.console.print(
            Panel.fit(
                "[bold blue]🎵 YouTube Music Downloader 🎵[/bold blue]\n"
                "[dim]Powered by yt-dlp with enhanced features[/dim]",
                border_style="blue",
            )
        )

        self.show_tips()

        while True:
            try:
                # Get URL
                self.console.print()
                url = Prompt.ask("[bold]Enter YouTube URL[/bold]").strip()
                if not url:
                    continue

                # Basic URL validation
                if not any(
                    domain in url.lower()
                    for domain in ["youtube.com", "youtu.be", "music.youtube.com"]
                ):
                    self.console.print("[red]❌ Please enter a valid YouTube URL[/red]")
                    continue

                # Determine if it's a playlist
                is_playlist = any(
                    keyword in url.lower()
                    for keyword in ["playlist", "list=", "/c/", "/channel/", "/@"]
                )

                if is_playlist:
                    content_type = "playlist"
                    self.console.print("[yellow]ℹ️  Detected playlist URL[/yellow]")
                else:
                    content_type = Prompt.ask(
                        "Is this a [bold](v)[/bold]ideo or [bold](p)[/bold]laylist?",
                        choices=["v", "p", "video", "playlist"],
                        default="v",
                    )
                    is_playlist = content_type.startswith("p")

                # Get download format
                format_choice = Prompt.ask(
                    "Download [bold](a)[/bold]udio only or [bold](v)[/bold]ideo?",
                    choices=["a", "v", "audio", "video"],
                    default="a",
                )
                audio_only = format_choice.startswith("a")

                # Start download
                self.console.print()
                if is_playlist:
                    self.download_playlist(url, audio_only)
                else:
                    self.download_video(url, audio_only)

                # Show stats
                self.show_stats()

                # Ask to continue
                if not Confirm.ask("\n[bold]Download another?[/bold]", default=True):
                    break

            except KeyboardInterrupt:
                self.console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]❌ Unexpected error: {e}[/red]")
                self.logger.error(f"Unexpected error in main menu: {e}")

        self.logger.info("YouTube Downloader session ended")


def main():
    """Entry point"""
    try:
        downloader = YouTubeDownloader()
        downloader.main_menu()
    except ImportError as e:
        print(f"Missing required dependency: {e}")
        print("Please install required packages:")
        print("pip install yt-dlp rich")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
