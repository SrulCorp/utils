import os
import subprocess
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def extract_chapters(m4b_file):
    """Use ffprobe to extract chapter information from the .m4b file."""
    cmd = [
        "ffprobe",
        "-i", m4b_file,
        "-print_format", "json",
        "-show_chapters",
        "-loglevel", "quiet"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Failed to run ffprobe. Is ffmpeg installed and on PATH?")
    data = json.loads(result.stdout)
    return data.get("chapters", [])

def convert_chapters_to_mp3(m4b_file, output_dir):
    """Extract and convert each chapter of the .m4b to separate .mp3 files."""
    chapters = extract_chapters(m4b_file)

    if not chapters:
        print("⚠️ No chapters found. Converting the entire file to a single MP3...")
        convert_whole_file(m4b_file, output_dir)
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\nFound {len(chapters)} chapters. Converting...\n")

    for i, chapter in enumerate(chapters):
        start = float(chapter['start_time'])
        end = float(chapter['end_time'])
        title = chapter.get('tags', {}).get('title', f"Chapter_{i+1}")
        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)

        output_path = os.path.join(output_dir, f"{safe_title}.mp3")

        print(f"[{i+1:02}] {safe_title} ({start:.2f}s - {end:.2f}s)")

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

    print("\n✅ All chapters converted successfully!")

def convert_whole_file(m4b_file, output_dir):
    """Convert the full .m4b file to one .mp3 file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(m4b_file))[0]
    output_path = os.path.join(output_dir, f"{base_name}.mp3")

    cmd = [
        "ffmpeg",
        "-i", m4b_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "128k",
        "-y",
        output_path
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\n✅ Converted entire file to: {output_path}")

def main():
    Tk().withdraw()
    print("🎧 Select the .m4b audiobook to convert...")
    m4b_file = askopenfilename(filetypes=[("M4B Audiobook", "*.m4b")])

    if not m4b_file:
        print("❌ No file selected. Exiting.")
        return

    base_dir = os.path.dirname(m4b_file)
    base_name = os.path.splitext(os.path.basename(m4b_file))[0]
    output_dir = os.path.join(base_dir, base_name)

    convert_chapters_to_mp3(m4b_file, output_dir)

if __name__ == "__main__":
    main()
