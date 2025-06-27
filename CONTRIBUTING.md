# Contributing to YouTube Music Downloader

Thank you for your interest in contributing to the YouTube Music Downloader! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and help them learn
- **Be collaborative**: Work together constructively
- **Be professional**: Keep discussions focused and productive

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic familiarity with command line
- Understanding of Python and yt-dlp

### Fork and Clone

1. Fork this repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/youtube-music-downloader.git
   cd youtube-music-downloader
   ```

## Development Setup

1. **Set up the development environment:**
   ```bash
   make install
   make dev-install
   ```

2. **Verify the setup:**
   ```bash
   make check
   make test
   ```

3. **Create a new branch for your feature/fix:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix existing issues
- **Feature additions**: Add new functionality
- **Documentation**: Improve docs, README, or code comments
- **Testing**: Add or improve tests
- **Code quality**: Refactoring, optimization, or cleanup

### Areas Where Help is Needed

- 🐛 **Bug fixes**: Check open issues for bugs
- 📚 **Documentation**: Improve README, add examples
- 🧪 **Testing**: Add unit tests and integration tests
- 🎨 **UI/UX**: Improve the interactive interface
- 🔧 **Configuration**: Enhance configuration options
- 🌐 **Internationalization**: Add support for multiple languages

## Pull Request Process

### Before Submitting

1. **Check existing issues and PRs** to avoid duplicates
2. **Test your changes** thoroughly
3. **Update documentation** if needed
4. **Follow coding standards** (see below)

### Submission Steps

1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

2. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference any related issues
   - Screenshots or examples if applicable

### Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
- `feat: add playlist shuffle option`
- `fix: resolve download timeout issue`
- `docs: update installation instructions`

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions focused and reasonably sized

### Code Quality

```bash
# Format code
make format

# Check linting
make lint

# Run type checking (if available)
mypy downloader.py
```

### Example Code Style

```python
def download_video(self, url: str, audio_only: bool = False) -> bool:
    """
    Download a single video using yt-dlp.
    
    Args:
        url: YouTube video URL to download
        audio_only: Whether to extract audio only
        
    Returns:
        True if download succeeded, False otherwise
        
    Raises:
        ValueError: If URL is invalid
        ConnectionError: If network issue occurs
    """
    # Implementation here
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run system check
make check

# Test specific functionality
python -c "from downloader import YouTubeDownloader; print('Import test passed')"
```

### Writing Tests

If adding new functionality, please include tests:

1. Create test files in a `tests/` directory
2. Use descriptive test names
3. Test both success and failure cases
4. Mock external dependencies when possible

### Test Example

```python
def test_extract_artist_title():
    """Test artist and title extraction from video titles."""
    downloader = YouTubeDownloader()
    
    # Test standard format
    artist, title = downloader.extract_artist_title("Artist - Song Title")
    assert artist == "Artist"
    assert title == "Song Title"
    
    # Test fallback
    artist, title = downloader.extract_artist_title("Just a Title")
    assert artist == "Unknown Artist"
    assert title == "Just a Title"
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **System information**:
   - OS and version
   - Python version
   - yt-dlp version
5. **Log files** (from `logs/` directory)
6. **Example URLs** that cause the issue (if applicable)

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots/Logs**
If applicable, add screenshots or log files.

**System Info**
- OS: [e.g. macOS 12.0]
- Python: [e.g. 3.9.7]
- yt-dlp: [e.g. 2024.12.13]

**Additional Context**
Any other context about the problem.
```

## Feature Requests

### Before Requesting

1. Check if the feature already exists
2. Search existing issues for similar requests
3. Consider if it fits the project's scope

### Feature Request Template

```markdown
**Feature Description**
A clear description of what you want to happen.

**Problem/Use Case**
Explain the problem this feature would solve.

**Proposed Solution**
Describe how you envision this working.

**Alternatives**
Any alternative solutions you've considered.

**Additional Context**
Any other context, screenshots, or examples.
```

## Development Guidelines

### Project Structure

```
youtube/
├── downloader.py          # Main application
├── check_system.py       # System diagnostics
├── config.json          # Default configuration
├── requirements.txt     # Python dependencies
├── Makefile            # Build automation
├── README.md           # Project documentation
├── CONTRIBUTING.md     # This file
├── LICENSE             # MIT License
└── logs/              # Application logs (gitignored)
└── downloads/         # Downloaded files (gitignored)
```

### Key Design Principles

- **Simplicity**: Keep the interface simple and intuitive
- **Reliability**: Robust error handling and logging
- **Performance**: Efficient downloads and processing
- **Maintainability**: Clean, well-documented code
- **User Experience**: Clear feedback and progress indication

### Dependencies

- Minimize external dependencies
- Use well-maintained libraries
- Document any new dependencies in requirements.txt
- Explain why new dependencies are needed

## Getting Help

If you need help with contributing:

1. **Check the documentation** first
2. **Search existing issues** for similar questions
3. **Create a new issue** with the "question" label
4. **Join discussions** on existing issues

## Recognition

Contributors will be recognized in:

- The project's README.md file
- Release notes for significant contributions
- GitHub's contributor statistics

## Questions?

Feel free to open an issue with the "question" label if you have any questions about contributing!

---

Thank you for contributing to YouTube Music Downloader! 🎵