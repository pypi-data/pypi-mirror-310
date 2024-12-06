import os
import shutil
import argparse
from pathlib import Path
import subprocess
from pydub.utils import mediainfo
import eyed3

def extract_vocals_and_beats(input_file, output_folder):
    """
    Uses Demucs to extract vocals (acapella) and beats (instrumental) from the input file
    and save them in the output folder.
    """
    try:
        subprocess.run(
            ["demucs", "--two-stems=vocals", "--out", str(output_folder), str(input_file)],
            check=True
        )

        model_folder = next(output_folder.iterdir())
        result_folder = model_folder / input_file.stem
        vocals_file = result_folder / "vocals.wav"
        beat_file = result_folder / "no_vocals.wav"  # Instrumental (no vocals)

        if not vocals_file.exists() or not beat_file.exists():
            raise FileNotFoundError(f"Expected files not found: {vocals_file}, {beat_file}")

        return vocals_file, beat_file
    except Exception as e:
        print(f"Error extracting vocals and beats from {input_file}: {e}")
        return None, None

def get_bpm(file_path):
    """
    Extract BPM from an audio file using TinyTag and Pydub.
    """
    try:
        audio_info = mediainfo(str(file_path))
        bpm = audio_info.get("bpm", 120)  # Default to 120 if not found
        return bpm
    except Exception as e:
        print(f"Error getting BPM for {file_path}: {e}")
        return None

def add_bpm_tag(file_path, bpm):
    """
    Add BPM tag to an MP3 or WAV file.
    """
    try:
        if file_path.suffix.lower() == ".mp3":
            audiofile = eyed3.load(str(file_path))
            audiofile.tag.bpm = bpm
            audiofile.tag.save()

        elif file_path.suffix.lower() == ".wav":
            print(f"BPM tag cannot be added directly to WAV files. Please check BPM manually in FL Studio.")
        
        print(f"BPM {bpm} added to {file_path}")
    except Exception as e:
        print(f"Error adding BPM to {file_path}: {e}")

def process_files(input_dir, output_dir):
    """
    Process all audio files in the input directory, extract vocals and beats,
    and save them in the output directory.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    for root, _, files in os.walk(input_dir):
        relative_path = Path(root).relative_to(input_dir)
        destination_folder = output_dir / relative_path
        destination_folder.mkdir(parents=True, exist_ok=True)

        for file in files:
            if not file.lower().endswith(('.mp3', '.wav', '.flac')):
                print(f"Skipping non-audio file: {file}")
                continue

            source_path = Path(root) / file
            print(f"Processing {source_path}...")

            temp_output = output_dir / "temp_demucs"
            temp_output.mkdir(parents=True, exist_ok=True)

            vocals_file, beat_file = extract_vocals_and_beats(source_path, temp_output)
            if vocals_file is None or beat_file is None:
                print(f"Skipping {source_path} due to extraction failure.")
                continue

            # Rename and move vocals and beat files
            vocals_name = f"{source_path.stem}_acapella.wav"
            beat_name = f"{source_path.stem}_beat.wav"
            vocals_path = destination_folder / vocals_name
            beat_path = destination_folder / beat_name

            try:
                shutil.move(vocals_file, vocals_path)
                shutil.move(beat_file, beat_path)
                print(f"Saved acapella to: {vocals_path}")
                print(f"Saved beat to: {beat_path}")

                # Add BPM metadata to vocals and beat files
                bpm = get_bpm(source_path)
                if bpm:
                    add_bpm_tag(vocals_path, bpm)
                    add_bpm_tag(beat_path, bpm)
            except Exception as e:
                print(f"Failed to move files for {source_path}: {e}")

            shutil.rmtree(temp_output, ignore_errors=True)

def main():
    parser = argparse.ArgumentParser(description="Extract vocals (acapella) and beats (instrumental) from audio files, add BPM, and save them in the same folder structure.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input folder containing audio files.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output folder where extracted files will be stored.")

    args = parser.parse_args()
    process_files(args.input, args.output)
    
if __name__ == "__main__":
    main()