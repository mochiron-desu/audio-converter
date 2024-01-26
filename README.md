# Audio Converter

This is a Python script to convert audio files from one format to another.

## Prerequisites

- Python 3.x
- pydub library (`pip install pydub`)

## Usage

1. Clone this repository or download the `audio_converter.py` file.
2. Place your input audio files in the `input` directory.
3. Run the `audio_converter.py` script.

The converted audio files will be saved in the `output` directory with the specified format.

## Configuration

- Input Format: Currently set to `m4a`. You can change it by modifying the `input_format` variable in the script.
- Output Format: Currently set to `wav`. You can change it by modifying the `output_format` variable in the script.

## Example

Suppose you have the following directory structure:

```
audio_converter/
│
├── input/
│   ├── input_file1.m4a
│   ├── input_file2.m4a
│   └── ...
│
├── output/
│
└── audio_converter.py
```

After running the script, the converted files will be saved in the `output` directory with the `.wav` extension.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This script utilizes the [pydub](https://github.com/jiaaro/pydub) library for audio file manipulation.