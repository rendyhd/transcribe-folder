# Local Media-to-PDF Transcription Pipeline

This project provides a set of Python scripts to create a simple, powerful, and private transcription pipeline. It uses a local AI model (via an OpenAI-compatible server) to transcribe audio and video files and then compiles the resulting text files into a single, chapterized PDF document.

This approach is ideal for users who want to transcribe sensitive media or avoid the costs associated with cloud-based transcription services.

## Features

- **Local First**: All processing is done locally. Your files are never sent to a third-party service.
- **Broad Format Support**: Transcribes common audio (`.mp3`, `.wav`, `.m4a`) and video (`.mp4`, `.mkv`, `.mov`) formats.
- **Automatic Chapter Generation**: Each media file is treated as a chapter in the final PDF, with the filename used as the chapter title.
- **Configurable**: Easily change the target folder, API endpoint, and AI model in the scripts.
- **Unicode Support**: Includes support for DejaVu fonts to correctly render a wide range of characters in the PDF.

## Requirements

1.  **Python 3.6+**
2.  **Project Dependencies**:
    - `openai`
    - `fpdf2`
3.  **A Local AI Server**: You must have a local application running that serves a transcription model (like Whisper) through an OpenAI-compatible API endpoint.
    - **Examples**: [Speaches](https://speaches.ai/)
4.  **(Optional) DejaVu Fonts**: For the best PDF output with full character support, download the [DejaVu fonts](https://dejavu-fonts.github.io/) and place `DejaVuSans.ttf` and `DejaVuSans-Bold.ttf` in the root directory of this project.

## Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Your Local AI Server**:
    - Launch your local AI server (e.g., LM Studio).
    - Load a transcription model (e.g., a GGUF version of Whisper).
    - Start the server and note the URL of the local API endpoint (e.g., `http://localhost:1234/v1`).

4.  **Configure the Scripts**:
    - Open `transcribe_audio_script.py` and/or `transcribe_video_script.py`.
    - Set the `API_BASE_URL` to match your local server's address.
    - (If needed) Update the `MODEL_NAME` to match the model identifier used by your server.

## Usage Workflow

The pipeline is designed to be run in three main steps:

### Step 1: Place Your Media Files

Create a folder named `to_transcribe` in the project's root directory (the scripts will create it for you on the first run). Place all the audio or video files you want to transcribe into this folder.

```
.
├── to_transcribe/
│   ├── 01_introduction.mp4
│   ├── 02_main_topic.mp3
│   └── 03_conclusion.wav
├── transcribe_video_script.py
├── txt_to_pdf_chapters_script.py
└── ...
```

### Step 2: Run Transcription

Run the appropriate script to turn your media files into text files. The script will process each file in the `to_transcribe` folder and save a corresponding `.txt` file in the same location.

-   **For both audio and video files**:
    ```bash
    python transcribe_video_script.py
    ```
-   **For audio-only files**:
    ```bash
    python transcribe_audio_script.py
    ```

After this step, your `to_transcribe` folder will look like this:

```
to_transcribe/
├── 01_introduction.mp4
├── 01_introduction.txt
├── 02_main_topic.mp3
├── 02_main_topic.txt
├── 03_conclusion.wav
└── 03_conclusion.txt
```

### Step 3: Generate the PDF

Run the PDF generation script. It will find all the `.txt` files, sort them alphabetically (which is why numbering them is helpful), and combine them into a single PDF named `output.pdf`.

```bash
python txt_to_pdf_chapters_script.py
```

The final `output.pdf` will be saved in the root directory of the project. Each chapter will be titled based on the original filename (e.g., "01 Introduction").
