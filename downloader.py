#!/usr/bin/env python3
"""
YouTube Music Downloader using yt-dlp
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import yt_dlp
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
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = (
            log_dir
            / f"youtube_downloader_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

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
        config_file = Path("config.json")
        default_config = {
            "download_directory": "downloads",
            "audio_quality": "192",
            "video_quality": "bestvideo[height<=720]",
            "audio_format": "mp3",
            "video_format": "mp4",
            "naming_format": "%(uploader,artist)s - %(title)s.%(ext)s",
            "skip_existing": True,
            "embed_metadata": True,
            "embed_thumbnail": True,
            "write_description": False,
            "write_info_json": False,
            "cookies_file": None,
            "cookies_from_browser": None,
            "download_archive": "downloads/.archive",
        }

        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                self.logger.warning(f"Error loading config: {e}. Using defaults.")
        else:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
            self.logger.info("Created default config.json")

        return default_config

    def check_yt_dlp(self):
        try:
            self.logger.info(f"Using yt-dlp version: {yt_dlp.version.__version__}")
        except Exception as e:
            self.console.print("[red]❌ yt-dlp is not installed or not working[/red]")
            self.console.print("[yellow]Install with: pip install yt-dlp[/yellow]")
            self.logger.error(f"yt-dlp check failed: {e}")
            sys.exit(1)

    def _base_ydl_opts(self) -> dict:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "remote_components": {"ejs:github"},
        }
        cookies_file = self.config.get("cookies_file")
        if cookies_file and Path(cookies_file).exists():
            opts["cookiefile"] = cookies_file
        elif self.config.get("cookies_from_browser"):
            opts["cookiesfrombrowser"] = (self.config["cookies_from_browser"],)
        return opts

    def build_yt_dlp_opts(self, audio_only: bool = False) -> dict:
        download_dir = Path(self.config["download_directory"])
        download_dir.mkdir(exist_ok=True)

        opts = self._base_ydl_opts()
        opts["nooverwrites"] = self.config["skip_existing"]

        if self.config.get("download_archive"):
            opts["download_archive"] = self.config["download_archive"]

        postprocessors = []

        if audio_only:
            opts["format"] = "bestaudio/best"
            opts["outtmpl"] = str(
                download_dir / "%(uploader,artist)s - %(title)s.%(ext)s"
            )
            postprocessors.append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.config["audio_format"],
                    "preferredquality": self.config["audio_quality"],
                }
            )
        else:
            opts["format"] = f"{self.config['video_quality']}+bestaudio/best"
            opts["outtmpl"] = str(download_dir / "%(title)s [%(id)s].%(ext)s")
            opts["merge_output_format"] = self.config["video_format"]

        if self.config["embed_metadata"]:
            postprocessors.append({"key": "FFmpegMetadata", "add_metadata": True})

        if self.config["embed_thumbnail"]:
            opts["writethumbnail"] = True
            postprocessors.append({"key": "EmbedThumbnail"})

        if self.config.get("write_description"):
            opts["writedescription"] = True

        if self.config.get("write_info_json"):
            opts["writeinfojson"] = True

        if postprocessors:
            opts["postprocessors"] = postprocessors

        return opts

    def extract_artist_title(self, title: str) -> tuple[str, str]:
        import re

        patterns = [
            r"^(.+?)\s*-\s*(.+)$",
            r"^(.+?)\s*\|\s*(.+)$",
            r"^(.+?)\s*:\s*(.+)$",
            r"^(.+?)\s*–\s*(.+)$",
        ]

        for pattern in patterns:
            match = re.match(pattern, title.strip())
            if match:
                artist, song = match.groups()
                return artist.strip(), song.strip()

        return "Unknown Artist", title.strip()

    def download_video(self, url: str, audio_only: bool = False) -> bool:
        try:
            with self.console.status("[cyan]Fetching video info..."):
                with yt_dlp.YoutubeDL(self._base_ydl_opts()) as ydl:
                    info = ydl.extract_info(url, download=False, process=False)

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

            mode = "Audio Only" if audio_only else "Video"
            self.console.print(f"[green]📥 Downloading {mode}...[/green]")

            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Downloading..."),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console,
            ) as progress:
                task = progress.add_task("download", total=100)

                def progress_hook(d):
                    if d["status"] == "downloading":
                        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                        downloaded = d.get("downloaded_bytes", 0)
                        if total:
                            progress.update(task, completed=(downloaded / total) * 100)
                    elif d["status"] == "finished":
                        progress.update(task, completed=100)

                download_opts = self.build_yt_dlp_opts(audio_only)
                download_opts["progress_hooks"] = [progress_hook]

                with yt_dlp.YoutubeDL(download_opts) as ydl:
                    ret = ydl.download([url])

            if ret == 0:
                self.console.print("[green]✅ Download completed successfully![/green]")
                self.logger.info(f"Successfully downloaded: {title}")
                self.stats["downloaded"] += 1
                return True
            else:
                self.console.print("[red]❌ Download failed[/red]")
                self.logger.error(f"Download failed for: {url}")
                self.stats["failed"] += 1
                return False

        except yt_dlp.utils.DownloadError as e:
            error_msg = f"Failed to download {url}: {e}"
            self.console.print(f"[red]❌ {error_msg}[/red]")
            self.logger.error(error_msg)
            self.stats["failed"] += 1
            return False
        except Exception as e:
            error_msg = f"Failed to download {url}: {e}"
            self.console.print(f"[red]❌ {error_msg}[/red]")
            self.logger.error(error_msg)
            self.stats["failed"] += 1
            return False

    def download_playlist(self, url: str, audio_only: bool = False) -> None:
        try:
            with self.console.status("[cyan]Fetching playlist info..."):
                flat_opts = self._base_ydl_opts()
                flat_opts["extract_flat"] = True
                with yt_dlp.YoutubeDL(flat_opts) as ydl:
                    playlist_data = ydl.extract_info(url, download=False)

            entries = playlist_data.get("entries", [])
            if not entries:
                raise Exception("No videos found in playlist")

            playlist_title = playlist_data.get("title", "Unknown Playlist")

            playlist_table = Table(show_header=False, box=None)
            playlist_table.add_row("[bold]Playlist:", playlist_title)
            playlist_table.add_row("[bold]Videos:", f"{len(entries)}")
            playlist_table.add_row(
                "[bold]Mode:", f"{'Audio Only' if audio_only else 'Video'}"
            )

            self.console.print(
                Panel(playlist_table, title="📑 Playlist Info", border_style="green")
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

            if failed_videos:
                self.console.print(
                    f"\n[yellow]⚠️  {len(failed_videos)} videos failed to download:[/yellow]"
                )
                for idx, title, url in failed_videos[:5]:
                    self.console.print(f"  {idx}: {title}")
                if len(failed_videos) > 5:
                    self.console.print(f"  ... and {len(failed_videos) - 5} more")

        except Exception as e:
            error_msg = f"Error processing playlist: {e}"
            self.console.print(f"[red]❌ {error_msg}[/red]")
            self.logger.error(error_msg)

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
                self.console.print()
                url = Prompt.ask("[bold]Enter YouTube URL[/bold]").strip()
                if not url:
                    continue

                if not any(
                    domain in url.lower()
                    for domain in ["youtube.com", "youtu.be", "music.youtube.com"]
                ):
                    self.console.print("[red]❌ Please enter a valid YouTube URL[/red]")
                    continue

                is_playlist = any(
                    keyword in url.lower()
                    for keyword in ["playlist", "list=", "/c/", "/channel/", "/@"]
                )

                if is_playlist:
                    self.console.print("[yellow]ℹ️  Detected playlist URL[/yellow]")
                else:
                    content_type = Prompt.ask(
                        "Is this a [bold](v)[/bold]ideo or [bold](p)[/bold]laylist?",
                        choices=["v", "p", "video", "playlist"],
                        default="v",
                    )
                    is_playlist = content_type.startswith("p")

                format_choice = Prompt.ask(
                    "Download [bold](a)[/bold]udio only or [bold](v)[/bold]ideo?",
                    choices=["a", "v", "audio", "video"],
                    default="a",
                )
                audio_only = format_choice.startswith("a")

                self.console.print()
                if is_playlist:
                    self.download_playlist(url, audio_only)
                else:
                    self.download_video(url, audio_only)

                self.show_stats()

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
