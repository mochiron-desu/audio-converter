import os
import subprocess
import shutil
import json
from datetime import datetime

def load_config(config_path='config.json'):
    """Load configuration from JSON file"""
    default_config = {
        "directories": {
            "input": "input",
            "base_output": "output"
        },
        "conversion": {
            "output_format": "mp3"
        },
        "file_handling": {
            "backup_input_files": True,
            "delete_input_files": True
        }
    }
    
    try:
        with open(config_path, 'r') as f:
            user_config = json.load(f)
            # Merge with defaults, preserving user settings
            default_config.update(user_config)
            return default_config
    except FileNotFoundError:
        print(f"Config file not found at {config_path}. Using default configuration.")
        return default_config

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

def main():
    # Load configuration
    config = load_config()
    
    # Extract configuration values
    input_dir = config['directories']['input']
    base_output_dir = config['directories']['base_output']
    output_format = config['conversion']['output_format']
    backup_files = config['file_handling']['backup_input_files']
    delete_files = config['file_handling']['delete_input_files']

    # Create a new folder with current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_output_dir, current_time)
    os.makedirs(output_dir, exist_ok=True)

    # Create input backup folder within output directory if backup is enabled
    backup_input_dir = None
    if backup_files:
        backup_input_dir = os.path.join(output_dir, "input")
        os.makedirs(backup_input_dir, exist_ok=True)

    # List of files to process
    input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # Process each file
    for filename in input_files:
        input_path = os.path.join(input_dir, filename)
        
        # Backup original file if enabled
        if backup_files:
            backup_path = os.path.join(backup_input_dir, filename)
            shutil.copy2(input_path, backup_path)
            print(f"Backed up original file: {filename}")
        
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

    # Delete original files if enabled
    if delete_files:
        for filename in input_files:
            input_path = os.path.join(input_dir, filename)
            try:
                os.remove(input_path)
                print(f"Deleted original file: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {str(e)}")

    print(f"Processing complete. Output files are in the folder: {output_dir}")
    if backup_files:
        print(f"Original files are backed up in: {backup_input_dir}")

if __name__ == "__main__":
    main()