import os
from openai import OpenAI

# --- Configuration ---
# 1. Set the base URL of your local OpenAI-compatible server.
#    This is the address where your local model (e.g., Whisper) is being served.
#    - For LM Studio: "http://localhost:1234/v1"
#    - For many others: "http://localhost:8080/v1"
API_BASE_URL = "http://localhost:8002/v1" 

# 2. Set an API key. For most local servers, this can be any string.
API_KEY = "not-needed"

# 3. Specify the model name your local server uses for transcription.
#    This must match the model loaded in your local application.
MODEL_NAME = "Systran/faster-distil-whisper-large-v3" # Common default, but check your server's model name.

# 4. Set the path to the folder containing your audio files.
#    Use "." for the current directory or provide an absolute/relative path.
AUDIO_FOLDER = "./to_transcribe" 

# 5. Define which audio file extensions the script should look for.
SUPPORTED_EXTENSIONS = ('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.mp4', '.webm')

# --- Main Script Logic ---

def transcribe_audio_in_folder(folder_path: str):
    """
    Loops through a folder, transcribes supported audio files using a local
    server, and saves the transcription as a .txt file next to the original.
    """
    print(f"Attempting to connect to local server at: {API_BASE_URL}")
    try:
        # Initialize the OpenAI client to point to the local server
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    except Exception as e:
        print(f"Error: Could not initialize the OpenAI client.")
        print(f"Please ensure your API_BASE_URL is correct and the server is running.")
        print(f"Details: {e}")
        return

    # Check if the specified folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' was not found.")
        print("Please create it and add your audio files.")
        return

    print(f"\nScanning folder: '{folder_path}'...")
    print("-" * 50)

    # Get a list of all files in the directory
    files_in_folder = os.listdir(folder_path)
    
    # Filter for only the audio files
    audio_files = [f for f in files_in_folder if f.lower().endswith(SUPPORTED_EXTENSIONS)]

    if not audio_files:
        print(f"No audio files with supported extensions found in '{folder_path}'.")
        return

    for filename in audio_files:
        audio_file_path = os.path.join(folder_path, filename)
        # Define the output path for the transcription .txt file
        transcription_file_path = os.path.splitext(audio_file_path)[0] + ".txt"

        # Skip the file if a transcription already exists
        if os.path.exists(transcription_file_path):
            print(f"Skipping '{filename}': Transcription file already exists.")
            continue

        print(f"Processing '{filename}'...")
        try:
            # Open the audio file in binary read mode
            with open(audio_file_path, "rb") as audio_file:
                # Send the file to the local server for transcription
                transcription_response = client.audio.transcriptions.create(
                    model=MODEL_NAME,
                    file=audio_file
                )
                
                transcribed_text = transcription_response.text
                
                # Save the transcribed text to the output file
                with open(transcription_file_path, "w", encoding="utf-8") as f:
                    f.write(transcribed_text)
                
                print(f"-> Successfully saved transcription to '{os.path.basename(transcription_file_path)}'")

        except Exception as e:
            print(f"-> Error transcribing '{filename}': {e}")
        
        print("-" * 50)

    print("\nBatch transcription process finished.")

# This block runs when the script is executed directly
if __name__ == "__main__":
    # Create the audio folder if it doesn't exist to prevent errors on first run
    if not os.path.exists(AUDIO_FOLDER):
        print(f"Creating sample directory '{AUDIO_FOLDER}'.")
        os.makedirs(AUDIO_FOLDER)
    
    transcribe_audio_in_folder(AUDIO_FOLDER)