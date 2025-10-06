import time
import os
from app.models.transcription import TranscriptionJob
from app.core.config import settings

def transcribe_audio(job: TranscriptionJob) -> str:
    """
    Transcribes the audio file associated with the given job.
    This is a placeholder and does not perform actual transcription.
    """
    print(f"Transcribing {job.file_path} with model {settings.whisper_model}...")

    # Simulate transcription time
    time.sleep(10)

    # Simulate a successful transcription
    output_filename = os.path.splitext(job.file_path)[0] + ".txt"

    # Handle duplicate filenames
    counter = 1
    while os.path.exists(output_filename):
        output_filename = f"{os.path.splitext(job.file_path)[0]} ({counter}).txt"
        counter += 1

    transcribed_text = f"This is a simulated transcription for the file {job.file_name}."

    with open(output_filename, "w") as f:
        f.write(transcribed_text)

    print(f"Transcription complete for {job.file_path}. Output at {output_filename}")

    return output_filename