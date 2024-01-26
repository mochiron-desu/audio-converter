import os
from pydub import AudioSegment

# Create the output directory if it doesn't exist
input_dir = "input"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

input_format = "m4a"
output_format = "wav"

# Iterate over the files in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(f".{input_format}"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(f".{input_format}", f".{output_format}"))

        # Convert the file to output_format
        wav_audio = AudioSegment.from_file(input_path, format=f"{input_format}")
        wav_audio.export(output_path, format=output_format)