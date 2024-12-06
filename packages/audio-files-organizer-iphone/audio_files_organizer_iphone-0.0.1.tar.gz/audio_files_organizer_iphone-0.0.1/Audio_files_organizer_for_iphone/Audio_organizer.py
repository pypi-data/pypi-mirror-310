# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 23:50:15 2024

@author: David Sandeep
"""

import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import subprocess
from datetime import datetime
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.aac import AAC
from mutagen.oggvorbis import OggVorbis

SUPPORTED_AUDIO_FORMATS = (".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma")

def normalize_path(path):
    """Normalize paths for cross-platform compatibility."""
    return os.path.normpath(path)

def get_audio_files(base_directory):
    """Recursively find all audio files in the base directory."""
    audio_files = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.lower().endswith(SUPPORTED_AUDIO_FORMATS):
                audio_files.append(normalize_path(os.path.join(root, file)))
    return audio_files

def get_audio_duration(file_path):
    """Get the duration of the audio file in seconds."""
    try:
        if file_path.lower().endswith(".mp3"):
            audio = MP3(file_path)
        elif file_path.lower().endswith(".flac"):
            audio = FLAC(file_path)
        elif file_path.lower().endswith(".wav"):
            audio = WAVE(file_path)
        elif file_path.lower().endswith(".m4a") or file_path.lower().endswith(".aac"):
            audio = AAC(file_path)
        elif file_path.lower().endswith(".ogg"):
            audio = OggVorbis(file_path)
        else:
            return None

        duration = audio.info.length  # Duration in seconds
        return duration
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return None

def update_album_metadata(file_path):
    """Update the album metadata of an audio file."""
    parent_folder = os.path.basename(os.path.dirname(file_path))
    try:
        try:
            audio = EasyID3(file_path)
        except ID3NoHeaderError:
            audio = EasyID3()
            audio.save(file_path)

        audio["album"] = parent_folder
        audio["artist"] = parent_folder
        audio.save()
        return True, None
    except Exception as e:
        return False, str(e)

def reencode_audio(file_path, temp_path):
    """Re-encode audio file using FFmpeg to resolve issues."""
    try:
        output_file = os.path.join(temp_path, os.path.basename(file_path))
        subprocess.run(
            ["ffmpeg", "-i", file_path, "-acodec", "libmp3lame", output_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return output_file if os.path.exists(output_file) else None
    except Exception:
        return None

def move_audio_files(audio_files, target_folder):
    """Move audio files to the target folder, preserving the folder structure."""
    print("\nMoving processed files to the 'audio songs' folder...")
    moving_failed_log = []
    for file_path in audio_files:
        relative_path = os.path.relpath(file_path, os.path.commonpath(audio_files))
        target_path = os.path.join(target_folder, "audio songs", relative_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        try:
            shutil.move(file_path, target_path)
            print(f"Moved: {relative_path}")
        except OSError as e:
            moving_failed_log.append(file_path)
            print(f"Failed to move {file_path}: {str(e)}")
            continue
    return moving_failed_log

def save_log(file_path, log_data, file_count):
    """Save log data to a file with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{file_path}_{timestamp}.txt"
    try:
        with open(log_file, "w", encoding="utf-8") as log:
            log.write(f"Total Files: {file_count}\n")
            log.write("\n".join(log_data))
        print(f"\nLog saved: {log_file}")
    except Exception as e:
        print(f"Failed to save log: {e}")
    return log_file


def calculate_total_size(file_paths):
    """Calculate total size of all given files."""
    return sum(os.path.getsize(file) for file in file_paths)


def process_files(base_directory, target_directory):
    """Main processing function."""
    print(f"Scanning for audio files in '{base_directory}'...\n")
    success_log = []
    failed_log = []
    retry_failed_log = []

    # Normalize paths and get all audio files
    audio_files = get_audio_files(base_directory)
    total_files = len(audio_files)
    print(f"Total audio files found: {total_files}\n")

    if total_files == 0:
        print("No audio files found. Exiting.")
        return

    # Process each audio file
    for idx, file_path in enumerate(audio_files, start=1):
        print(f"[{idx}/{total_files}] Processing: {file_path}")
        
        # Get the duration of the audio file
        duration = get_audio_duration(file_path)
        if duration is None or duration < 60:
            print(f"    Skipping file (Duration less than 1 minute): {file_path}")
            continue
        
        success, error = update_album_metadata(file_path)
        if success:
            success_log.append(file_path)
            print("    Successfully updated metadata.")
        else:
            failed_log.append((file_path, error))
            print(f"    Failed: {error}")

    # Save logs for successful and failed files
    save_log("success_files", success_log, len(success_log))
    save_log("failed_files", [f"{file}: {error}" for file, error in failed_log], len(failed_log))

    print(f"\nSummary: Successfully processed {len(success_log)} files.")
    print(f"Summary: Failed to process {len(failed_log)} files.\n")

    # Calculate the size of successfully processed files
    print("\nCalculating size of successfully processed files...")
    total_size = calculate_total_size(success_log)
    print(f"Total size of files to move: {total_size / (1024**3):.2f} GB")

    # Retry failed files with re-encoding
    if failed_log:
        print("\nRetrying failed files using re-encoding...\n")
        temp_path = os.path.join(target_directory, "temp_reencode")
        os.makedirs(temp_path, exist_ok=True)
        for file_path, _ in failed_log:
            print(f"Attempting to re-encode: {file_path}")
            reencoded_file = reencode_audio(file_path, temp_path)
            if reencoded_file:
                success, error = update_album_metadata(reencoded_file)
                if success:
                    success_log.append(reencoded_file)
                    shutil.move(reencoded_file, file_path)  # Replace original file
                    print("    Successfully re-encoded and updated metadata.")
                else:
                    retry_failed_log.append((file_path, error))
                    print(f"    Failed after re-encoding: {error}")
            else:
                retry_failed_log.append((file_path, "Re-encoding failed"))
                print("    Re-encoding failed.")

    # Save retry failed log
    save_log("failed_retry", [f"{file}: {error}" for file, error in retry_failed_log], len(retry_failed_log))

    print(f"\nSummary: Successfully reprocessed {len(failed_log) - len(retry_failed_log)} files after retry.")
    print(f"Summary: Still failed to process {len(retry_failed_log)} files after retry.\n")

    print("Moving process started..")
    usrpmt = input("Please make sure you have enough space in target directory\n 1. Yes 2. No: ")
    if usrpmt == '1' or usrpmt.lower() == 'yes':
        # Move all successfully processed files to the target folder
        move_audio_files(success_log, target_directory)
        print("\nAll successfully processed files moved to 'audio songs' folder.")

def processit():
    """Handles user interaction for selecting directories."""
    Tk().withdraw()  # Hide tkinter root window
    base_directory = askdirectory(title="Select the base folder containing audio files")
    if not base_directory:
        print("No base folder selected. Exiting.")
        return

    target_directory = askdirectory(title="Select the target folder to organize audio files")
    if not target_directory:
        print("No target folder selected. Exiting.")
        return

    process_files(base_directory, target_directory)
    print("\nProcessing completed.")    


