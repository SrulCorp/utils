import subprocess
import sys
import tempfile
from pathlib import Path

def run(cmd):
    subprocess.run(cmd, check=True)

def get_duration(file):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file)
    ]
    return float(subprocess.check_output(cmd).decode().strip())

def get_artist(file):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format_tags=artist",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file)
    ]
    try:
        return subprocess.check_output(cmd).decode().strip()
    except:
        return ""

def extract_cover(file, out):
    cmd = [
        "ffmpeg", "-y",
        "-i", str(file),
        "-an", "-vcodec", "copy",
        str(out)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def prompt_folder():
    while True:
        folder = input("Enter folder containing MP3 files: ").strip('" ')
        path = Path(folder)
        if path.exists() and path.is_dir():
            return path
        print("Invalid folder. Try again.\n")

def main():
    if len(sys.argv) > 1:
        folder = Path(sys.argv[1])
    else:
        folder = prompt_folder()

    mp3s = sorted(folder.glob("*.mp3"))
    if not mp3s:
        print("No mp3 files found in that folder.")
        input("Press Enter to exit...")
        sys.exit(1)

    first = mp3s[0]
    artist = get_artist(first)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        list_file = tmp / "list.txt"
        meta_file = tmp / "metadata.txt"
        merged_file = tmp / "merged.wav"
        cover_file = tmp / "cover.jpg"

        with open(list_file, "w", encoding="utf-8") as f:
            for m in mp3s:
                f.write(f"file '{m.as_posix()}'\n")

        # Decode + concatenate → WAV (clean intermediate)
        run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(list_file),
            "-vn",
            str(merged_file)
        ])

        # Chapters
        start = 0.0
        lines = []

        for m in mp3s:
            dur = get_duration(m)
            end = start + dur

            title = m.stem.replace("_", " ").replace("-", " ")

            lines.append("[CHAPTER]")
            lines.append("TIMEBASE=1/1000")
            lines.append(f"START={int(start * 1000)}")
            lines.append(f"END={int(end * 1000)}")
            lines.append(f"title={title}")
            lines.append("")

            start = end

        meta_file.write_text("\n".join(lines), encoding="utf-8")

        # Extract cover
        extract_cover(first, cover_file)
        cover_exists = cover_file.exists() and cover_file.stat().st_size > 0

        out_file = folder / (folder.name + ".m4b")

        cmd = [
            "ffmpeg", "-y",
            "-i", str(merged_file),
            "-i", str(meta_file)
        ]

        if cover_exists:
            cmd += ["-i", str(cover_file)]

        cmd += [
            "-map_metadata", "1",
            "-map", "0:a",
            "-c:a", "aac",
            "-b:a", "96k"
        ]

        if cover_exists:
            cmd += ["-map", "2:v", "-c:v", "copy", "-disposition:v", "attached_pic"]

        if artist:
            cmd += ["-metadata", f"artist={artist}"]

        cmd.append(str(out_file))

        run(cmd)

        print("\nDone.")
        print(f"Output: {out_file}")
        print(f"Artist: {artist or 'Not found'}")
        print(f"Cover: {'Embedded' if cover_exists else 'None'}")

        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
