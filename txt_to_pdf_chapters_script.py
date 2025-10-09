import os
from pathlib import Path
from fpdf import FPDF

# --- Configuration ---
# Specify the folder containing your .txt files
INPUT_FOLDER = "./to_transcribe" 
# Specify the name of the output PDF file
OUTPUT_PDF = "output.pdf"

def create_chapterized_pdf(input_dir, output_file):
    """
    Finds all .txt files in a directory, sorts them, and combines them
    into a single chapterized PDF file.
    """
    folder_path = Path(input_dir)
    if not folder_path.is_dir():
        print(f"Error: The specified folder '{input_dir}' does not exist.")
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Created folder '{input_dir}'. Please add your .txt files there and run the script again.")
        return

    text_files = sorted(folder_path.glob("*.txt"))

    if not text_files:
        print(f"No .txt files found in the '{input_dir}' folder.")
        return

    pdf = FPDF()
    
    # --- Font Setup ---
    # Using a Unicode font (DejaVu) to support a wide range of characters.
    # Requires DejaVuSans.ttf and DejaVuSans-Bold.ttf to be in the same folder as this script.
    try:
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf")
        pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf")
        FONT_FAMILY = "DejaVu"
    except RuntimeError:
        print("---")
        print("WARNING: DejaVu font not found. Falling back to Arial.")
        print("Special characters may not be rendered correctly.")
        print("Download DejaVu fonts and place them next to the script for full Unicode support.")
        print("---")
        FONT_FAMILY = "Arial"


    print("Starting PDF creation...")

    for txt_file in text_files:
        print(f"Processing: {txt_file.name}")

        chapter_title = txt_file.stem.replace("_", " ").replace("-", " ").title()

        pdf.add_page()
        pdf.set_font(FONT_FAMILY, "B", 24) # Bold font for the title
        pdf.cell(0, 20, chapter_title, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font(FONT_FAMILY, "", 12) # Regular font for the body text
        
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read()
            pdf.multi_cell(0, 10, content)

        except Exception as e:
            # We convert the error to a simple string to avoid the error-within-an-error problem
            error_message = str(e)
            print(f"  Could not process file {txt_file.name}: {error_message}")
            pdf.set_text_color(255, 0, 0)
            pdf.multi_cell(0, 10, f"Error processing this file. See console for details. Error: {error_message}")
            pdf.set_text_color(0, 0, 0)

    try:
        pdf.output(output_file)
        print(f"\nSuccessfully created PDF: {output_file}")
    except Exception as e:
        print(f"\nError saving PDF file: {e}")


if __name__ == "__main__":
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Created a folder named '{INPUT_FOLDER}'.")
        print("Please place your .txt files in this folder and run the script again.")
    else:
        create_chapterized_pdf(INPUT_FOLDER, OUTPUT_PDF)