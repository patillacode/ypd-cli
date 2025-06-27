#!/usr/bin/env python3
"""
System Check Utility for YouTube Music Downloader
This script checks if all dependencies and requirements are properly installed.
"""

import importlib
import platform
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Python Version Check")
    print("=" * 30)

    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8+ is recommended for yt-dlp")
        return False
    else:
        print("✅ Python version is compatible")
        return True


def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name

    try:
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "Unknown")
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False


def check_python_packages():
    """Check all required Python packages"""
    print("\n📦 Python Packages Check")
    print("=" * 30)

    required_packages = [
        ("yt-dlp", "yt_dlp"),
        ("rich", "rich"),
    ]

    all_installed = True
    for package_name, import_name in required_packages:
        if not check_package(package_name, import_name):
            all_installed = False

    return all_installed


def check_yt_dlp_functionality():
    """Check if yt-dlp is working properly"""
    print("\n🔧 yt-dlp Functionality Check")
    print("=" * 30)

    try:
        # Check yt-dlp command line tool
        result = subprocess.run(
            ["yt-dlp", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ yt-dlp CLI: {version}")
            cli_works = True
        else:
            print("❌ yt-dlp CLI: Command failed")
            cli_works = False
    except (
        subprocess.TimeoutExpired,
        FileNotFoundError,
        subprocess.SubprocessError,
    ):
        print("❌ yt-dlp CLI: Not found in PATH")
        cli_works = False

    try:
        # Check yt-dlp Python module
        import yt_dlp

        print(f"✅ yt-dlp Python module: {yt_dlp.version.CHANNEL}")
        module_works = True
    except ImportError:
        print("❌ yt-dlp Python module: Not available")
        module_works = False

    return cli_works and module_works


def check_optional_tools():
    """Check optional external tools"""
    print("\n🔧 Optional Tools Check")
    print("=" * 30)

    tools = {
        "ffmpeg": "FFmpeg (recommended for video processing and format conversion)",
        "ffprobe": "FFprobe (part of FFmpeg suite, for media analysis)",
    }

    all_available = True
    for tool, description in tools.items():
        try:
            result = subprocess.run(
                [tool, "-version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                # Extract version from first line
                version_line = result.stdout.split("\n")[0]
                print(f"✅ {tool}: {version_line}")
            else:
                print(f"❌ {tool}: Command failed")
                all_available = False
        except (
            subprocess.TimeoutExpired,
            FileNotFoundError,
            subprocess.SubprocessError,
        ):
            print(f"⚠️  {tool}: Not found in PATH")
            print(f"   {description}")
            # Don't mark as failed since these are optional
            # all_available = False

    return all_available


def check_directories():
    """Check if required directories exist or can be created"""
    print("\n📁 Directory Check")
    print("=" * 30)

    directories = ["downloads", "logs"]
    all_good = True

    for dir_name in directories:
        dir_path = Path(dir_name)
        try:
            dir_path.mkdir(exist_ok=True)
            if dir_path.exists() and dir_path.is_dir():
                print(f"✅ {dir_name}/: Available")
            else:
                print(f"❌ {dir_name}/: Cannot create")
                all_good = False
        except PermissionError:
            print(f"❌ {dir_name}/: Permission denied")
            all_good = False

    return all_good


def check_config_files():
    """Check configuration files"""
    print("\n⚙️  Configuration Files Check")
    print("=" * 30)

    files = {
        "downloader.py": "Main application script",
        "requirements.txt": "Python dependencies list",
        "config.json": "Configuration file",
    }

    all_good = True
    for file_name, description in files.items():
        file_path = Path(file_name)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file_name}: {size} bytes")
        else:
            print(f"❌ {file_name}: Missing")
            all_good = False

    return all_good


def check_network_connectivity():
    """Check basic network connectivity"""
    print("\n🌐 Network Connectivity Check")
    print("=" * 30)

    try:
        import urllib.request

        urllib.request.urlopen("https://www.youtube.com", timeout=10)
        print("✅ YouTube.com: Accessible")
        return True
    except Exception as e:
        print(f"❌ YouTube.com: Not accessible ({e})")
        return False


def test_basic_extraction():
    """Test basic video information extraction"""
    print("\n🧪 Basic Extraction Test")
    print("=" * 30)

    try:
        import yt_dlp

        # Test with a simple, reliable video
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        print("   Testing video info extraction...")
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            title = info.get("title", "Unknown")
            duration = info.get("duration", 0)

        print("✅ Video info extraction successful")
        print(f"   Title: {title}")
        print(f"   Duration: {duration}s")
        return True

    except Exception as e:
        print(f"❌ Video info extraction failed: {e}")
        return False


def provide_installation_help():
    """Provide installation instructions for missing components"""
    print("\n🆘 Installation Help")
    print("=" * 30)

    print("If you're missing dependencies, try these commands:")
    print()

    print("📦 Install Python packages:")
    print("   pip install -r requirements.txt")
    print("   # or individually:")
    print("   pip install yt-dlp rich")
    print()

    print("🔧 Install FFmpeg (optional but recommended):")
    system = platform.system().lower()
    if system == "darwin":  # macOS
        print("   macOS: brew install ffmpeg")
    elif system == "linux":
        print("   Ubuntu/Debian: sudo apt install ffmpeg")
        print("   CentOS/RHEL: sudo yum install ffmpeg")
        print("   Arch Linux: sudo pacman -S ffmpeg")
    elif system == "windows":
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   Add to PATH environment variable")
    else:
        print("   Download from: https://ffmpeg.org/download.html")
    print()

    print("🐍 Update Python (if needed):")
    print("   Download from: https://python.org/downloads/")
    print("   Minimum version: Python 3.8")


def main():
    """Main system check function"""
    print("🔍 YouTube Music Downloader - System Check")
    print("=" * 50)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Python Packages", check_python_packages),
        ("yt-dlp Functionality", check_yt_dlp_functionality),
        ("Optional Tools", check_optional_tools),
        ("Directories", check_directories),
        ("Configuration Files", check_config_files),
        ("Network Connectivity", check_network_connectivity),
        ("Basic Extraction", test_basic_extraction),
    ]

    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error during {check_name} check: {e}")
            results.append((check_name, False))

    # Summary
    print("\n📋 Summary")
    print("=" * 30)

    all_passed = True
    critical_failed = False

    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
            # Mark critical failures
            if check_name in [
                "Python Version",
                "Python Packages",
                "yt-dlp Functionality",
            ]:
                critical_failed = True

    print()
    if all_passed:
        print(
            "🎉 All checks passed! Your system is ready to run the YouTube downloader."
        )
    elif critical_failed:
        print("⚠️  Critical checks failed. The application may not work properly.")
        provide_installation_help()
    else:
        print("⚠️  Some optional checks failed, but the application should work.")
        print(
            "    Consider installing missing optional components for better functionality."
        )

    print("\n" + "=" * 50)
    print("💡 Tips:")
    print("• Run 'make install' to set up the complete environment")
    print("• Run 'make update' to update yt-dlp to the latest version")
    print("• Check 'logs/' directory for detailed error information")

    return 0 if (all_passed or not critical_failed) else 1


if __name__ == "__main__":
    sys.exit(main())
