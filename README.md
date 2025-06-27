# 🎵 YouTube Music Downloader

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

An enhanced Python script for downloading YouTube videos and playlists using yt-dlp with comprehensive error handling, logging, and a beautiful interactive interface.

## ✨ Features

- **Powered by yt-dlp**: Uses the actively maintained yt-dlp library for reliable downloads
- **Interactive UI**: Beautiful command-line interface with Rich library
- **Comprehensive Logging**: Detailed logs with timestamps saved to files
- **Error Handling**: Robust error handling and informative error messages
- **Progress Tracking**: Real-time download progress bars
- **Smart Naming**: Automatic artist/title extraction from video titles
- **Format Support**: Download as video (MP4) or audio-only (MP3/AAC/etc.)
- **Playlist Support**: Download entire playlists with batch processing
- **Configurable**: Customizable settings via JSON configuration
- **Metadata Embedding**: Automatic metadata and thumbnail embedding
- **Duplicate Detection**: Skip already downloaded files
- **Statistics**: Track download success rates and statistics
- **Virtual Environment**: Isolated Python environment for clean installation
- **Open Source**: MIT licensed, contributions welcome

## 🚀 Installation

### Quick Installation with Make
```bash
make install
```

### Manual Installation
1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install FFmpeg** (optional but recommended for advanced features):
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)



## 📋 Requirements

- Python 3.8+
- FFmpeg (optional but recommended)
- Internet connection

### Python Dependencies
- `yt-dlp` - YouTube video downloading (actively maintained)
- `rich` - Beautiful terminal interface

## 🎯 Usage

### Quick Start with Make
```bash
# Install and run in one command
make install && make run

# Or use shortcuts
make i && make r
```

### Basic Usage
```bash
# With virtual environment (recommended)
make run

# Or directly
python downloader.py
```

### Using Make Commands
```bash
# Show all available commands
make help

# Check system requirements
make check

# Update yt-dlp
make update

# View logs
make logs

# Show application status
make status
```




The script will launch an interactive menu where you can:
1. Paste YouTube URLs (videos, playlists, or channels)
2. Choose between video or audio-only downloads
3. Monitor download progress in real-time
4. View statistics and logs
5. Automatic metadata and thumbnail embedding

### Configuration

The script creates a `config.json` file with the following customizable options:

```json
{
    "download_directory": "downloads",
    "audio_quality": "192",
    "video_quality": "best[height<=720]",
    "audio_format": "mp3",
    "video_format": "mp4",
    "naming_format": "%(uploader,artist)s - %(title)s.%(ext)s",
    "skip_existing": true,
    "embed_metadata": true,
    "embed_thumbnail": true,
    "write_description": false,
    "write_info_json": false
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `download_directory` | Where to save downloaded files | `"downloads"` |
| `audio_quality` | Audio quality (bitrate) | `"192"` |
| `video_quality` | Video quality selector | `"best[height<=720]"` |
| `audio_format` | Audio format for extraction | `"mp3"` |
| `naming_format` | File naming pattern (yt-dlp format) | `"%(uploader,artist)s - %(title)s.%(ext)s"` |
| `skip_existing` | Skip files that already exist | `true` |
| `embed_metadata` | Embed metadata in files | `true` |
| `embed_thumbnail` | Embed thumbnails in files | `true` |

## 📁 Directory Structure

After running, your directory will look like:
```
youtube/
├── downloader.py          # Enhanced main script
├── requirements.txt       # Python dependencies
├── config.json           # Configuration file
├── check_system.py       # System check utility
├── run.sh                # Unix launch script
├── Makefile              # Simplified build automation
├── README.md             # Documentation
├── venv/                 # Virtual environment (created by make install)
├── downloads/            # Downloaded files (created automatically)
│   ├── Artist - Song.mp3
│   └── Artist - Video.mp4
└── logs/                 # Log files (created automatically)
    └── youtube_downloader_20240101_120000.log
```

## 🎵 Supported Formats

### Audio Downloads
- **Formats**: MP3, AAC, FLAC, OGG, WAV, M4A, OPUS
- **Quality**: Configurable bitrate (default: 192k)
- **Metadata**: Automatic metadata and thumbnail embedding

### Video Downloads
- **Formats**: MP4, WEBM, MKV, AVI, MOV
- **Quality**: Configurable quality selection (default: 720p max)
- **Resolution**: Up to 4K (depending on source and selection)
- **Features**: Automatic metadata and thumbnail embedding

## 📋 Make Commands Reference

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Complete installation with virtual environment |
| `make run` | Run the YouTube downloader |
| `make check` | Check system requirements |
| `make status` | Show application status |
| `make logs` | View recent log entries |
| `make clean` | Clean temporary files |
| `make update` | Update yt-dlp to latest version |
| `make deps` | Show installed dependencies |

### Quick Aliases
- `make i` → `make install`
- `make r` → `make run`
- `make s` → `make status`
- `make c` → `make check`
- `make u` → `make update`

## 🔧 Advanced Features

### Artist/Title Extraction
The script intelligently extracts artist and song names from video titles using patterns:
- `Artist - Title`
- `Artist | Title`
- `Artist : Title`
- `Artist – Title`

### yt-dlp Integration
- **Format Selection**: Advanced format selection with quality preferences
- **Metadata Embedding**: Automatic metadata and thumbnail embedding
- **Multiple Sites**: Support for 1000+ websites beyond YouTube
- **Playlist Processing**: Robust playlist and channel downloading

### Logging
- **File Logging**: Detailed logs saved with timestamps
- **Console Logging**: Real-time status updates with colors
- **Error Tracking**: Comprehensive error reporting

### Progress Tracking
- Real-time download progress bars
- yt-dlp native progress parsing
- Success/failure statistics

### Environment Management
- **Virtual Environment**: Isolated Python environment
- **Dependency Management**: Clean dependency installation
- **Easy Updates**: Simple yt-dlp updates via make

## 🛠️ Troubleshooting

### Quick Diagnostics
```bash
# Run system check
make check

# Or manually
python check_system.py
```

### Common Issues

**"yt-dlp not found"**
```bash
make install
# or manually: pip install yt-dlp
```

**"Virtual environment issues"**
```bash
make clean-all  # Remove everything and start fresh
make install    # Reinstall with fresh environment
```

**"FFmpeg not found"** (Optional)
- FFmpeg is optional but recommended for advanced features
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

**"Video unavailable"**
- Video might be private, deleted, or region-locked
- Try a different video or check the URL

**"Download failed"**
- Check internet connection
- Update yt-dlp: `make update`
- Some videos may have restrictions

### Log Analysis
```bash
# View recent logs
make logs

# Or manually check files
tail -f logs/youtube_downloader_*.log
```

### Clean Installation
```bash
# Clean and reinstall with fresh virtual environment
make clean-all
make install
```

## 📊 Statistics & Monitoring

The script tracks and displays:
- Total downloads attempted
- Successful downloads
- Failed downloads
- Skipped files (already exist)
- Success rate percentage

### View Statistics
```bash
# Application status
make status
## 🆕 What's New in yt-dlp Version

### Advantages over pytube
- **Active Maintenance**: yt-dlp is actively maintained with frequent updates
- **Better Compatibility**: Handles YouTube API changes more reliably
- **More Sites**: Supports 1000+ websites, not just YouTube
- **Advanced Features**: Better format selection, metadata handling, and more
- **Robust Error Handling**: More informative error messages and recovery
- **Performance**: Generally faster and more efficient downloads

### Migration from pytube
This version replaces pytube with yt-dlp for better reliability and features. Your existing downloads and configuration will work the same way, but with improved functionality under the hood.

## 🔗 Links

- **GitHub Repository**: [https://github.com/yourusername/youtube-music-downloader](https://github.com/yourusername/youtube-music-downloader)
- **Issues & Bug Reports**: [GitHub Issues](https://github.com/yourusername/youtube-music-downloader/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/youtube-music-downloader/discussions)
- **yt-dlp Documentation**: [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)

# Recent activity
make logs

# Storage usage
du -sh downloads/
```

## 🚀 Getting Started

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/youtube-music-downloader.git
   cd youtube-music-downloader
   ```

2. **Install and run:**
   ```bash
   make install
   make run
   ```

3. **Enter a YouTube URL and enjoy!**

### Development

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/youtube-music-downloader.git
   ```
3. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make your changes and test:**
   ```bash
   make install
   make check
   ```
5. **Submit a pull request**

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 **Report bugs** - Help us identify and fix issues
- ✨ **Suggest features** - Share ideas for improvements
- 📚 **Improve documentation** - Help others understand the project
- 🧪 **Add tests** - Improve code reliability
- 💻 **Submit code** - Fix bugs or implement features

### Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/youtube-music-downloader.git
cd youtube-music-downloader
make install
make dev-install

# Run checks
make check
make test
```

## 📋 Project Status

- ✅ **Stable**: Core functionality working reliably
- 🔄 **Active Development**: Regular updates and improvements
- 📈 **Growing**: New features and enhancements planned
- 🌍 **Cross-Platform**: Works on Linux, macOS, and Windows

### Roadmap

- [ ] GUI interface option
- [ ] Batch processing from file
- [ ] Custom format profiles
- [ ] Integration with music libraries
- [ ] Multi-language support

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/youtube-music-downloader?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/youtube-music-downloader?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/youtube-music-downloader)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/youtube-music-downloader)



## 🔒 Legal Notice

This tool is for personal use only. Respect YouTube's Terms of Service and copyright laws. Only download content you have permission to download or that is in the public domain.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - The powerful library that makes this project possible
- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal interface
- **Contributors** - Thank you to everyone who has contributed to this project!

## 💬 Support

- 📖 **Documentation**: Start with this README and check the [wiki](https://github.com/yourusername/youtube-music-downloader/wiki)
- 🐛 **Bug Reports**: [Create an issue](https://github.com/yourusername/youtube-music-downloader/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Create an issue](https://github.com/yourusername/youtube-music-downloader/issues/new?template=feature_request.md)
- ❓ **Questions**: [Create a discussion](https://github.com/yourusername/youtube-music-downloader/discussions)

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/youtube-music-downloader&type=Date)](https://star-history.com/#yourusername/youtube-music-downloader&Date)

---

**Happy downloading! 🎵**
