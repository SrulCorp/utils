import subprocess
import pathlib
import tempfile

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv"}

def update_title(video_path: pathlib.Path):
    title = video_path.stem

    with tempfile.NamedTemporaryFile(delete=False, suffix=video_path.suffix) as tmp:
        temp_path = pathlib.Path(tmp.name)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-map", "0",
        "-metadata", f"title={title}",
        "-codec", "copy",
        str(temp_path)
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        print(f"\nFFmpeg failed on: {video_path}")
        print(result.stderr)
        temp_path.unlink(missing_ok=True)
        return False

    temp_path.replace(video_path)
    print(f"Updated: {video_path.name}")
    return True

def main():
    folder = input("Enter folder path containing videos: ").strip('"').strip()
    base_path = pathlib.Path(folder)

    if not base_path.exists() or not base_path.is_dir():
        print("Invalid folder path.")
        return

    count = 0

    for video in base_path.rglob("*"):
        if video.suffix.lower() in VIDEO_EXTENSIONS:
            if update_title(video):
                count += 1

    print(f"\nDone. Updated {count} video files.")

if __name__ == "__main__":
    main()
