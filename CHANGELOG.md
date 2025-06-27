# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation
- GitHub repository setup

## [2.0.0] - 2024-12-27

### Added
- **NEW**: Complete rewrite using yt-dlp instead of pytube
- **NEW**: Virtual environment support with `make install`
- **NEW**: Simplified Makefile with essential commands only
- **NEW**: Enhanced error handling and user feedback
- **NEW**: Better progress tracking with yt-dlp integration
- **NEW**: Support for 1000+ websites (via yt-dlp)
- **NEW**: Automatic metadata and thumbnail embedding
- **NEW**: Comprehensive system check with `check_system.py`
- **NEW**: Rich terminal interface with colored output
- **NEW**: Interactive menu with URL validation
- **NEW**: Configurable quality settings for audio and video
- **NEW**: Smart artist/title extraction from video titles
- **NEW**: Playlist and channel download support
- **NEW**: Skip existing files functionality
- **NEW**: Detailed logging with timestamps
- **NEW**: Download statistics tracking

### Changed
- **BREAKING**: Switched from pytube to yt-dlp for better reliability
- **BREAKING**: Updated configuration format for yt-dlp compatibility
- **BREAKING**: Simplified Makefile commands (removed complex troubleshooting)
- **BREAKING**: Minimum Python version now 3.8+ (recommended for yt-dlp)
- **IMPROVEMENT**: Better error messages and recovery suggestions
- **IMPROVEMENT**: Faster and more reliable downloads
- **IMPROVEMENT**: Enhanced progress display with real-time updates
- **IMPROVEMENT**: Cleaner project structure
- **IMPROVEMENT**: Updated documentation with yt-dlp information

### Removed
- **BREAKING**: Removed pytube dependency
- **BREAKING**: Removed ffmpeg-python dependency (yt-dlp handles internally)
- **BREAKING**: Removed mutagen dependency (yt-dlp handles metadata)
- **BREAKING**: Removed complex troubleshooting commands from Makefile
- **BREAKING**: Removed Windows batch files (focus on cross-platform Makefile)
- **BREAKING**: Removed Docker support (simplified deployment)
- Removed troubleshoot.py (integrated into main application)

### Fixed
- Resolved playlist download reliability issues
- Fixed metadata embedding for various formats
- Improved error handling for network timeouts
- Better handling of restricted or unavailable videos
- Fixed progress tracking accuracy

### Security
- Improved input validation for URLs
- Better handling of malicious or malformed URLs

## [1.0.0] - 2024-12-27

### Added
- Initial implementation using pytube
- Basic video and playlist download functionality
- Audio conversion with ffmpeg
- Metadata tagging with mutagen
- Rich terminal interface
- Configuration file support
- Logging system
- Error handling and retry logic
- Progress tracking
- Interactive menu system

### Features
- YouTube video downloads
- YouTube playlist downloads
- Audio-only extraction (MP3)
- Video downloads (MP4)
- Artist/title extraction
- Progress bars
- Error logging
- Configuration management

---

## Migration Guide: v1.x to v2.x

### Breaking Changes

1. **Dependencies**: 
   - Old: `pytube`, `ffmpeg-python`, `mutagen`, `rich`
   - New: `yt-dlp`, `rich`

2. **Installation**:
   - Old: `pip install -r requirements.txt`
   - New: `make install` (creates virtual environment)

3. **Configuration Format**:
   - Updated `config.json` format for yt-dlp compatibility
   - New naming format uses yt-dlp template syntax

4. **Makefile Commands**:
   - Simplified from 20+ commands to essential ones
   - Removed troubleshooting and Docker commands

### Migration Steps

1. **Backup your downloads**: 
   ```bash
   cp -r downloads downloads_backup
   ```

2. **Clean installation**:
   ```bash
   make clean-all  # Remove old environment
   make install    # Install with yt-dlp
   ```

3. **Update configuration**:
   - Review and update `config.json` with new format
   - Test with a single video before batch operations

4. **Verify functionality**:
   ```bash
   make check  # Run system checks
   make test   # Test basic functionality
   ```

### Benefits of Migration

- **Better Reliability**: yt-dlp is actively maintained
- **More Sites**: Support for 1000+ websites
- **Better Performance**: Faster downloads and processing
- **Enhanced Features**: Better format selection and metadata
- **Simplified Setup**: Easier installation and maintenance

---

## Support

For questions about this changelog or migration:
- Check the [README.md](README.md) for usage instructions
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development info
- Open an issue on GitHub for support

## Links

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [Rich Python Library](https://github.com/Textualize/rich)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)