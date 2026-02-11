import os
import subprocess
import json
import math

def sanitize_path(path):
    """Removes surrounding quotes and strips whitespace."""
    return path.strip().strip('"').strip("'")

def extract_chapters(m4b_file):
    cmd = [
        "ffprobe",
        "-i", m4b_file,
        "-print_format", "json",
        "-show_chapters",
        "-loglevel", "quiet"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout).get('chapters', [])
    except json.JSONDecodeError:
        return []

def get_duration(m4b_file):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        m4b_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0

def convert_chapters_to_mp3(m4b_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chapters = extract_chapters(m4b_file)
    if chapters:
        print(f"Found {len(chapters)} chapters in {os.path.basename(m4b_file)}")
        for i, chapter in enumerate(chapters):
            start = float(chapter['start_time'])
            end = float(chapter['end_time'])
            title = chapter.get('tags', {}).get('title', f"Chapter_{i+1}")
            safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
            output_path = os.path.join(output_dir, f"{safe_title}.mp3")

            print(f"Processing: {safe_title} ({start:.2f}s - {end:.2f}s)")

            cmd = [
                "ffmpeg",
                "-i", m4b_file,
                "-ss", str(start),
                "-to", str(end),
                "-vn",
                "-acodec", "libmp3lame",
                "-ab", "128k",
                "-y",
                output_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(f"No chapters found in {os.path.basename(m4b_file)}. Splitting into 2-hour segments.")
        duration = get_duration(m4b_file)
        segment_length = 2 * 60 * 60  # 2 hours in seconds
        num_segments = math.ceil(duration / segment_length)

        for i in range(num_segments):
            start = i * segment_length
            segment_duration = min(segment_length, duration - start)
            output_path = os.path.join(output_dir, f"Segment_{i+1:02d}.mp3")

            print(f"Processing: Segment {i+1} ({start:.2f}s for {segment_duration:.2f}s)")

            cmd = [
                "ffmpeg",
                "-ss", str(start),
                "-t", str(segment_duration),
                "-i", m4b_file,
                "-vn",
                "-acodec", "libmp3lame",
                "-ab", "128k",
                "-y",
                output_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Verify output exists
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                print(f"⚠️ Failed to create: {output_path}")
            else:
                print(f"✅ Created: {output_path}")

def process_path(path):
    path = sanitize_path(path)
    if os.path.isfile(path) and path.lower().endswith(".m4b"):
        base_dir = os.path.dirname(path)
        base_name = os.path.splitext(os.path.basename(path))[0]
        output_dir = os.path.join(base_dir, base_name)
        convert_chapters_to_mp3(path, output_dir)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(".m4b"):
                    full_path = os.path.join(root, file)
                    base_name = os.path.splitext(file)[0]
                    output_dir = os.path.join(root, base_name)
                    convert_chapters_to_mp3(full_path, output_dir)
    else:
        print("Invalid path. Please provide a valid .m4b file or folder containing .m4b files.")

if __name__ == "__main__":
    input_path = input("Enter the path to the .m4b file or folder: ")
    process_path(input_path)
