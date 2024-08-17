import os
import subprocess
from datetime import datetime

def get_media_info(file_path):
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a:0', 
             '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        audio_codec = result.stdout.strip()
        
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', 
             '-count_packets', '-show_entries', 'stream=nb_read_packets', 
             '-of', 'csv=p=0', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        video_packets = int(result.stdout.strip() or 0)
        
        return audio_codec, (video_packets > 0)
    except:
        return None, None

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
        audio_codec, has_video = get_media_info(input_path)
        
        if audio_codec or has_video:
            output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
            output_path = os.path.join(output_dir, output_filename)

            # Convert the file to output_format
            try:
                if has_video:
                    # Extract audio from video
                    subprocess.run(['ffmpeg', '-i', input_path, '-vn', '-acodec', output_format, output_path])
                    print(f"Extracted audio from video: {filename} to {output_filename}")
                elif audio_codec == output_format:
                    # If input and output formats are the same, just copy the file
                    subprocess.run(['ffmpeg', '-i', input_path, '-acodec', 'copy', output_path])
                    print(f"Copied: {filename} to {output_filename}")
                else:
                    # Convert audio
                    subprocess.run(['ffmpeg', '-i', input_path, output_path])
                    print(f"Converted: {filename} to {output_filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
        else:
            print(f"Skipped: {filename} (not a recognized audio or video file)")

print(f"Conversion complete. Output files are in the folder: {output_dir}")