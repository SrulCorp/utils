import os
import subprocess
import json
from pydub import AudioSegment

def extract_chapters(m4b_file):
    """Extract chapter info using ffmpeg"""
    cmd = [
        "ffprobe",
        "-i", m4b_file,
        "-print_format", "json",
        "-show_chapters",
        "-loglevel", "quiet"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    chapters = json.loads(result.stdout)['chapters']
    return chapters

def convert_chapters_to_mp3(m4b_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chapters = extract_chapters(m4b_file)
    print(f"Found {len(chapters)} chapters")

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

    print("Conversion complete!")

if __name__ == "__main__":
    m4b_file = input("Enter the path to the .m4b file: ").strip()
    base_dir = os.path.dirname(m4b_file)
    base_name = os.path.splitext(os.path.basename(m4b_file))[0]
    output_dir = os.path.join(base_dir, base_name)
    convert_chapters_to_mp3(m4b_file, output_dir)
