# Audio and Video Converter

This is a Python script that converts audio files and extracts audio from video files, outputting to a specified audio format.

## Features

- Converts various audio formats to a specified output format (default is MP3)
- Extracts audio from video files
- Automatically detects input file type (audio or video)
- Creates a new output folder for each run, named with the current date and time
- Handles files that are already in the target format efficiently

## Prerequisites

- Python 3.x
- FFmpeg (must be installed and accessible from the command line)

## Installation

1. Clone this repository or download the `audio_video_converter.py` file.
2. Ensure FFmpeg is installed on your system and accessible from the command line.

## Usage

1. Place your input audio and video files in the `input` directory.
2. Run the `audio_video_converter.py` script:
   ```
   python audio_video_converter.py
   ```
3. The converted audio files will be saved in a new folder within the `output` directory, with the folder name formatted as `YYYYMMDD_HHMMSS`.

## Configuration

- Output Format: Currently set to `mp3`. You can change it by modifying the `output_format` variable in the script.

## Example

Suppose you have the following directory structure:

```
audio_video_converter/
│
├── input/
│   ├── audio_file.m4a
│   ├── video_file.mp4
│   └── ...
│
├── output/
│
└── audio_video_converter.py
```

After running the script, a new folder will be created in the `output` directory with a name like `20240817_220130`. This folder will contain all the converted audio files in the specified format (default is MP3).

## How It Works

1. The script scans the `input` directory for files.
2. For each file, it uses FFprobe to determine if it's an audio file or a video file.
3. If it's a video file, the script extracts the audio.
4. If it's an audio file, the script converts it to the target format (unless it's already in that format, in which case it's simply copied).
5. All output files are placed in a newly created folder within the `output` directory.

## Error Handling

The script will skip files that are not recognized as audio or video and will print error messages for any files it fails to process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This script utilizes FFmpeg for media manipulation and information extraction.