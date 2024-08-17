import os
import subprocess
from pydub import AudioSegment
from datetime import datetime

def get_file_extension(filename):
    return os.path.splitext(filename)[1][1:].lower()

def get_audio_format(file_path):
    try:
        # First, try using pydub
        audio = AudioSegment.from_file(file_path)
        return audio.format_info
    except:
        # If pydub fails, try using ffprobe
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'a:0', 
                 '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()
        except:
            # If both methods fail, return the file extension
            return get_file_extension(file_path)

# Create the input and output directories
input_dir = "input"
base_output_dir = "output"

# Create a new folder with current date and time
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(base_output_dir, current_time)
os.makedirs(output_dir, exist_ok=True)

output_format = "mp3"

# Iterate over the files in the input directory
for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)
    
    # Check if it's a file and not a directory
    if os.path.isfile(input_path):
        input_format = get_audio_format(input_path)
        
        if input_format:
            output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
            output_path = os.path.join(output_dir, output_filename)

            # Convert the file to output_format
            try:
                if input_format == output_format:
                    # If input and output formats are the same, just copy the file
                    subprocess.run(['ffmpeg', '-i', input_path, '-acodec', 'copy', output_path])
                else:
                    # Convert using ffmpeg
                    subprocess.run(['ffmpeg', '-i', input_path, output_path])
                print(f"Converted: {filename} to {output_filename}")
            except Exception as e:
                print(f"Error converting {filename}: {str(e)}")
        else:
            print(f"Skipped: {filename} (not a recognized audio file)")

print(f"Conversion complete. Output files are in the folder: {output_dir}")