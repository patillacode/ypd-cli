#!/bin/bash

# YouTube Music Downloader - Launch Script
# This script sets up the environment and runs the downloader

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed or not in PATH"
        exit 1
    fi

    print_success "Found Python: $($PYTHON_CMD --version)"
}

# Check if pip is available
check_pip() {
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        print_error "pip is not available"
        exit 1
    fi

    print_success "pip is available"
}

# Check if FFmpeg is installed
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        print_warning "FFmpeg is not installed or not in PATH"
        print_warning "Audio conversion may not work properly"
        print_warning "Install FFmpeg:"
        print_warning "  macOS: brew install ffmpeg"
        print_warning "  Ubuntu/Debian: sudo apt install ffmpeg"
        print_warning "  Windows: Download from https://ffmpeg.org/"
        echo
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "FFmpeg is available"
    fi
}

# Install Python dependencies
install_dependencies() {
    print_status "Checking Python dependencies..."

    if [ -f "requirements.txt" ]; then
        print_status "Installing dependencies from requirements.txt..."
        $PYTHON_CMD -m pip install -r requirements.txt --user
        print_success "Dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Create necessary directories
setup_directories() {
    print_status "Setting up directories..."

    mkdir -p downloads
    mkdir -p logs

    print_success "Directories created"
}

# Main execution
main() {
    echo "🎵 YouTube Music Downloader Setup 🎵"
    echo "===================================="
    echo

    # Change to script directory
    cd "$(dirname "$0")"

    # Run checks
    check_python
    check_pip
    check_ffmpeg

    # Setup
    install_dependencies
    setup_directories

    echo
    print_success "Setup complete! Starting YouTube Downloader..."
    echo

    # Run the downloader
    $PYTHON_CMD downloader.py
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n${YELLOW}Interrupted by user${NC}"; exit 1' INT

# Run main function
main "$@"
