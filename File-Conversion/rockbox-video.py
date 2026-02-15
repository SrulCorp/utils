import subprocess
from pathlib import Path

# ---------------- PROFILES ----------------
# Format: name, video bitrate, audio bitrate, fps, VBV buffer (bytes)

PROFILES = {
    "1": ("Ultra-small", "350k", "64k",  "20", "65536"),    # VBV = 16 KB
    "2": ("Balanced",    "500k", "96k",  "24", "65536"),    # VBV = 64 KB
    "3": ("High quality","700k", "128k", "24", "98304"),    # VBV = 96 KB
}

VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".mpg", ".mpeg"}

# ------------------------------------------

def normalize_path_input(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1].strip()
    return value

def ask(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    val = input(prompt).strip()
    return val if val else default


def main():
    print("\nRockbox MPEG Encoder — Maximum Stability Profile\n")

    src_dir = Path(normalize_path_input(ask("Source directory", "D:\\Videos")))
    out_dir = Path(normalize_path_input(ask("Output directory", "D:\\iPodVideos")))

    print("\nQuality profiles:")
    for k, (name, *_ ) in PROFILES.items():
        print(f" {k}) {name}")

    profile = ask("Select profile", "2")

    if profile not in PROFILES:
        print("Invalid selection.")
        return

    name, vb, ab, fr, bufsize = PROFILES[profile]

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
            out_path = out_path.with_suffix(".mpg")
            out_path.parent.mkdir(parents=True, exist_ok=True)

            if out_path.exists():
                print(f"Skipping: {out_path}")
                continue

            print(f"Encoding: {video}")

            cmd = [
                "ffmpeg", "-y",
                "-i", str(video),

                # Video scaling & timing
                "-vf", vf,
                "-r", fr,

                # Video — MPEG-1 tuned for Rockbox stability
                "-c:v", "mpeg1video",
                "-b:v", vb,
                "-maxrate", vb,
                "-bufsize", bufsize,
                "-g", "12",
                "-bf", "0",
                "-pix_fmt", "yuv420p",

                # Audio — MP2 (Rockbox native)
                "-c:a", "mp2",
                "-b:a", ab,
                "-ar", "44100",
                "-ac", "2",

                # Container
                "-f", "mpeg",

                str(out_path)
            ]

            subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
