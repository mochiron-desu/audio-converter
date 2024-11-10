# Audio and Video Converter

This is a Python script that converts audio files and extracts audio from video files, outputting to a specified audio format. It features configurable directory paths, automated file handling, and backup options.

## Features

- Converts various audio formats to a specified output format (default is MP3)
- Extracts audio from video files
- Automatically detects input file type (audio or video)
- Creates a new output folder for each run, named with the current date and time
- Handles files that are already in the target format efficiently
- Configurable through JSON configuration file
- Flexible file handling options:
  - Optional backup of original files
  - Optional deletion of processed input files
  - Configurable input and output directories

## Prerequisites

- Python 3.x
- FFmpeg (must be installed and accessible from the command line)

## Installation

1. Clone this repository or download the script files
```bash
git clone https://github.com/mochiron-desu/audio-converter
```

2. Ensure FFmpeg is installed on your system and accessible from the command line
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS (using Homebrew)
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

3. Create the necessary directories as specified in your config.json (or use the defaults)
```bash
mkdir input output
```

## Configuration

The script uses a JSON configuration file (`config.json`) to manage settings:

```json
{
    "directories": {
        "input": "input",
        "base_output": "output"
    },
    "conversion": {
        "output_format": "mp3"
    },
    "file_handling": {
        "backup_input_files": true,
        "delete_input_files": true
    }
}
```

### Configuration Options

- **directories**
  - `input`: Directory where input files are located
  - `base_output`: Base directory for output files

- **conversion**
  - `output_format`: Target format for audio conversion (default: "mp3")

- **file_handling**
  - `backup_input_files`: Whether to backup original files (true/false)
  - `delete_input_files`: Whether to delete original files after processing (true/false)

### File Handling Modes

1. **Full Processing** (default)
   - `backup_input_files: true, delete_input_files: true`
   - Original files are backed up and then deleted from the input directory

2. **Safe Mode**
   - `backup_input_files: true, delete_input_files: false`
   - Original files are backed up but preserved in the input directory

3. **Direct Processing**
   - `backup_input_files: false, delete_input_files: false`
   - Original files are preserved in place with no backup

4. **Clean Processing**
   - `backup_input_files: false, delete_input_files: true`
   - Original files are deleted without backup after successful conversion

## Usage

1. Place your input audio and video files in the `input` directory
2. (Optional) Modify the `config.json` file to customize settings
3. Run the script:
```bash
python main.py
```

The script will process the files according to your configuration settings and create a new timestamped output directory containing the converted files.

## Directory Structure

```
audio_video_converter/
│
├── input/                      # Place input files here
│   ├── song.m4a
│   └── video.mp4
│
├── output/
│   └── 20240817_220130/       # Timestamped output folder
│       ├── input/             # Backup of original files (if enabled)
│       │   ├── song.m4a
│       │   └── video.mp4
│       ├── song.mp3           # Converted audio file
│       └── video.mp3          # Extracted audio from video
│
├── config.json                 # Configuration file
└── main.py                    # Main script
```

## How It Works

1. The script loads configuration from `config.json` (or uses defaults if not found)
2. Creates a new timestamped output directory
3. If backup is enabled, creates an "input" subfolder in the output directory
4. For each file in the input directory:
   - Backs up the original file (if enabled)
   - Uses FFprobe to determine if it's an audio or video file
   - Converts to the target format or extracts audio from video
   - Places the converted file in the output directory
5. If deletion is enabled, removes original files from the input directory
6. Provides detailed status messages for all operations

## Error Handling

The script includes comprehensive error handling:

- Skips files that aren't recognized as audio or video
- Reports conversion errors for individual files without stopping the process
- Uses safe file operations with proper error reporting
- Provides fallback to default settings if config file is missing
- Reports but continues if file deletion fails

## Examples

### Basic Usage
```bash
# Place files in input directory
cp mysong.m4a input/
python main.py
```

### Custom Configuration
```json
{
    "directories": {
        "input": "my_music",
        "base_output": "converted_files"
    },
    "conversion": {
        "output_format": "wav"
    },
    "file_handling": {
        "backup_input_files": false,
        "delete_input_files": false
    }
}
```

## Supported Formats

Input formats are determined by FFmpeg support, which includes:

### Audio Formats
- MP3
- WAV
- M4A
- FLAC
- OGG
- WMA
- AAC

### Video Formats (for audio extraction)
- MP4
- AVI
- MKV
- MOV
- WMV
- FLV

## Troubleshooting

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your system PATH
   - Try running `ffmpeg -version` in terminal/command prompt

2. **Permission errors**
   - Ensure you have write permissions in both input and output directories
   - Run the script with appropriate permissions

3. **Config file errors**
   - Verify your config.json is valid JSON
   - Use a JSON validator if necessary

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FFmpeg for media processing capabilities
- Python's standard library for file operations
- JSON for configuration management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Version History

- 1.0.0
  - Initial release
  - Basic conversion functionality
- 1.1.0
  - Added JSON configuration
  - Added flexible file handling options
  - Added backup functionality

## Contact

If you have any questions or suggestions, please open an issue in the repository.