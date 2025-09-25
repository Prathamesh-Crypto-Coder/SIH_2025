import os
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import pandas as pd
import tempfile
import pygame

# --- Gemini API Configuration ---
# CAUTION: For testing only. For a real project, set this as an environment variable.
genai.configure(api_key="AIzaSyBfETlgiegFBN91IAwVY7bnJd5dtsEc4BI")

# Initialize the Gemini model for conversation
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

# --- Data Loading (from previous step) ---
# This part is included for future functionality, but the current chatbot
# does not use the CSV data. It's a good practice to include it for when
# you want to integrate data retrieval.
try:
    groundwater_df = pd.read_csv('Maharashtra_Nashik_ground_water_level_2023.csv', 
                                 engine='python', 
                                 sep=',', 
                                 quotechar='"')
    print("Groundwater data loaded successfully.")
except FileNotFoundError:
    print("Warning: The groundwater CSV file was not found. Data-related queries will not work.")
    groundwater_df = None
except pd.errors.ParserError as e:
    print(f"Pandas Parsing Error: {e}. Data-related queries will not work.")
    groundwater_df = None

# --- Voice Engine Initialization ---
recognizer = sr.Recognizer()

# Initialize Pygame Mixer for more reliable audio playback
pygame.mixer.init()

def speak_text(text):
    """Converts text to speech and plays it using a more reliable method."""
    print(f"Bot speaking: {text}") # Log the text that's about to be spoken
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
            temp_filename = fp.name
            tts.save(temp_filename)
        
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        os.remove(temp_filename) # Clean up the temporary file
    except Exception as e:
        print(f"Error during Text-to-Speech: {e}")

def get_gemini_response(user_query):
    """Gets a text response from the Gemini API."""
    try:
        response = chat.send_message(user_query)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# --- Main Chatbot Loop ---
def main():
    print("Starting Voice Assistant. Please speak after the 'Listening...' prompt.")
    speak_text("Hello! How can I help you today?")
    
    while True:
        user_input = ""
        try:
            # Listen for user's voice
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1) 
                audio = recognizer.listen(source)

            # Transcribe audio to text
            user_input = recognizer.recognize_google(audio, language="en-IN")
            print(f"You said: {user_input}")

            if "exit" in user_input.lower() or "stop" in user_input.lower():
                speak_text("Goodbye!")
                print("Goodbye!")
                break
            
            # Add this line to provide immediate feedback to the user
            speak_text("Just a moment, please...")
            
            # Get response from Gemini
            response_text = get_gemini_response(user_input)
            print(f"Bot: {response_text}")

            # Speak the response
            speak_text(response_text)

        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            speak_text("I'm sorry, I didn't catch that. Could you repeat?")
        except sr.RequestError as e:
            print(f"Could not request results from service; {e}")
            speak_text("There was an error with the speech service. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            speak_text("An error occurred. I'm shutting down.")
            break

if __name__ == "__main__":
    main()
