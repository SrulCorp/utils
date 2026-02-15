import os
import subprocess
import tempfile
import shutil

# Common audio extensions to process
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".aac", ".m4a", ".ogg", ".opus", ".wma"}

def normalize_path_input(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1].strip()
    return value

def is_audio_file(filename):
    return os.path.splitext(filename)[1].lower() in AUDIO_EXTENSIONS

def build_atempo_filters(speed):
    """
    ffmpeg's atempo only supports 0.5–2.0 per filter.
    Chain filters if speed is outside that range.
    """
    filters = []
    remaining = speed

    while remaining > 2.0:
        filters.append("atempo=2.0")
        remaining /= 2.0

    while remaining < 0.5:
        filters.append("atempo=0.5")
        remaining /= 0.5

    filters.append(f"atempo={remaining}")
    return ",".join(filters)

def process_file(filepath, speed):
    dirname, filename = os.path.split(filepath)

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        temp_path = tmp.name

    atempo_filter = build_atempo_filters(speed)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", filepath,
        "-filter:a", atempo_filter,
        temp_path
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Replace original file
    shutil.move(temp_path, filepath)

def main():
    folder = normalize_path_input(input("Enter folder path containing audio files: "))
    speed = float(input("Enter playback speed (e.g., 0.8, 1.25, 2.0): ").strip())

    if not os.path.isdir(folder):
        raise ValueError("Provided path is not a valid folder.")

    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isfile(path) and is_audio_file(entry):
            print(f"Processing: {entry}")
            process_file(path, speed)

    print("Done.")

if __name__ == "__main__":
    main()

