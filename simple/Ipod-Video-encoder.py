import subprocess
from pathlib import Path

# ---------------- PROFILES ----------------

PROFILES = {
    "1": ("Ultra-small", "6", "64k", "20"),
    "2": ("Balanced",    "4", "96k", "24"),
    "3": ("High quality","3", "128k","24"),
}

VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".mpg", ".mpeg"}

# ------------------------------------------

def ask(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    val = input(prompt).strip()
    return val if val else default


def main():
    print("\nRockbox iPod Classic 6G Video Encoder\n")

    src_dir = Path(ask("Source directory", "D:\\Videos"))
    out_dir = Path(ask("Output directory", "D:\\iPodVideos"))

    print("\nQuality profiles:")
    for k, (name, *_ ) in PROFILES.items():
        print(f" {k}) {name}")

    profile = ask("Select profile", "2")

    if profile not in PROFILES:
        print("Invalid selection.")
        return

    name, qv, ab, fr = PROFILES[profile]

    mode = ask("Aspect ratio mode: letterbox or crop", "letterbox").lower()

    if mode not in ("letterbox", "crop"):
        print("Invalid aspect ratio mode.")
        return

    if mode == "letterbox":
        vf = "scale=320:240:force_original_aspect_ratio=decrease,pad=320:240:(ow-iw)/2:(oh-ih)/2"
    else:
        vf = "scale=320:240:force_original_aspect_ratio=increase,crop=320:240"

    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nProfile: {name}")
    print(f"Aspect: {mode}")
    print(f"Source: {src_dir}")
    print(f"Output: {out_dir}\n")

    for video in src_dir.rglob("*"):
        if video.suffix.lower() in VIDEO_EXTS:
            out_path = out_dir / video.relative_to(src_dir)
            out_path = out_path.with_suffix(".avi")
            out_path.parent.mkdir(parents=True, exist_ok=True)

            if out_path.exists():
                print(f"Skipping: {out_path}")
                continue

            print(f"Encoding: {video}")
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video),
                "-vf", vf,
                "-c:v", "mpeg4",
                "-q:v", qv,
                "-maxrate", "800k",
                "-bufsize", "800k",
                "-r", fr,
                "-c:a", "mp3",
                "-b:a", ab,
                str(out_path)
            ]

            subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
