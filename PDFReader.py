"""
A Python program that reads a PDF file aloud using text-to-speech.
It allows the user to select a voice, set the starting page, adjust
playback speed, and optionally save the audio as a WAV file.
"""
import pyttsx3
import PyPDF2
from tkinter.filedialog import askopenfilename

def set_voice(engine):
    """Prompt the user to choose and set the voice for text-to-speech."""
    voices = engine.getProperty('voices')
    print("Please choose a voice from the following options:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.id})")
    try:
        choice = int(input("\nEnter the number of the voice you want to use: "))
        if 0 <= choice < len(voices):
            engine.setProperty('voice', voices[choice].id)
            print(f"Voice set to: {voices[choice].name}")
        else:
            print("Invalid choice. Default voice will be used.")
    except ValueError:
        print("Invalid input. Default vy7oice will be used.")

def save_wav(engine, reader, start_page, end_page):
    """Optionally save the PDF audio as a WAV file."""
    save = input("Do you want to save the audio as a WAV file? (yes/no): ").strip().lower()
    if save == 'yes':
        output_filename = input("Enter the output WAV file name (with .wav extension): ")
        full_save_text = ""
        for num in range(start_page, end_page):
            print(f"Processing page {num + 1} of {end_page}...")
            page = reader.pages[num]
            text = page.extract_text()
            if text:
                full_save_text += text + "\n"
        engine.save_to_file(full_save_text, output_filename)
        engine.runAndWait()
        print(f"Audio saved as {output_filename}")
    elif save == 'no':
        print("Proceeding without saving a file.")
    else:
        print("Invalid input. Proceeding without saving a file.")

def speak(engine, reader, start_page, end_page):
    """Extract text from the given page range and read it aloud."""
    full_text = ""
    for num in range(start_page, end_page):
        page = reader.pages[num]
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    engine.say(full_text)
    engine.runAndWait()

def main():
    """Main entry point for the PDF text-to-speech program."""
    engine = pyttsx3.init()
    set_voice(engine)
    book = askopenfilename()
    if not book:
        print("No file selected. Exiting.")
        return
    reader = PyPDF2.PdfReader(book)
    number_of_pages = len(reader.pages)
    print(f"Total pages: {number_of_pages}")
    start_page = int(input("Enter the starting page number: ")) - 1
    end_page = int(input("Enter the ending page number: "))
    if not (0 <= start_page < end_page <= number_of_pages):
        print("Invalid page range. Exiting.")
        return
    rate = int(input("Enter playback speed (default is 200): "))
    engine.setProperty('rate', rate)
    save_wav(engine, reader, start_page, end_page)
    speak(engine, reader, start_page, end_page)

if __name__ == "__main__":
    main()