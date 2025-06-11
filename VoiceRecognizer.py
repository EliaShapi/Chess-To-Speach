import re
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


# Initialize speech recognition
listener = sr.Recognizer()


def take_command():
    """Capture and process voice commands."""
    try:
        with sr.Microphone() as source:
            print('Adjusting for ambient noise...')
            listener.adjust_for_ambient_noise(source, duration=1)  # Adjust to ambient noise
            print('Listening...')
            voice = listener.listen(source, timeout=5, phrase_time_limit=10)  # Add timeout limits
            print('Processing...')
            command = listener.recognize_google(voice)
            return command.lower()
            #return command.lower()
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for input.")
        talk("I didn't hear anything. Please try again.")
    except sr.UnknownValueError:
        print("Speech was unclear.")
        talk("I didn't understand that. Could you repeat?")
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; {e}")
        talk("There seems to be an issue with the speech recognition service.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return ""  # Return an empty string if something went wrong


def preprocess_command(command):
    """Handle common misinterpretations in the speech recognition output."""
    # Fix common misheard phrases
    command = re.sub(r'\b96\b', 'Nc6', command, flags=re.IGNORECASE)
    command = re.sub(r'\b93\b', 'Nc3', command, flags=re.IGNORECASE)
    command = re.sub(r'\basics\b', 'a6', command, flags=re.IGNORECASE)
    command = re.sub(r'\b85\b', 'a5', command, flags=re.IGNORECASE)
    command = re.sub(r'\b84\b', 'a4', command, flags=re.IGNORECASE)
    command = re.sub(r'\bbefore\b', 'b4', command, flags=re.IGNORECASE)
    return command


def normalize_command(command):
    """Normalize the command to match chess notation."""
    # Normalize chess pieces
    command = re.sub(r'\b(rook|roof|rk|luke|rock|brooke)\b', 'R', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(knight|knigt|knite|nite|nai|knyte|kni|kn)\b', 'N', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(bishop|bisop|bishp|bshp|bisp|bsh|bis|bsp|bi)\b', 'B', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(queen|qeuen|qeen|qun|qn)\b', 'Q', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(king|kng|knght|kngt|kg)\b', 'K', command, flags=re.IGNORECASE)

    # Normalize board square coordinates
    command = re.sub(r'\b(play)\s?(\d)\b', r'h\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(be)\s?(\d)\b', r'b\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(see|sea|cee)\s?(\d)\b', r'c\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(dee|deer)\s?(\d)\b', r'd\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(it|he|knee|hee)\s?(\d)\b', r'e\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(s)\s?(\d)\b', r'f\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(gee|je)\s?(\d)\b', r'g\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(aitch|age|aich)\s?(\d)\b', r'h\2', command, flags=re.IGNORECASE)

    command = re.sub(r'\b(four)\s?(\d)\b', r'4\2', command, flags=re.IGNORECASE)
    command = re.sub(r'\b(fire)\s?(\d)\b', r'5\2', command, flags=re.IGNORECASE)

    # Replace "takes" with "x"
    command = re.sub(r'\b(takes|take|capture|captures|steaks|states|eat|eats)\b', 'x', command, flags=re.IGNORECASE)

    # Handle promotions (e.g., "pawn takes h8 and promote to rook" -> "gxh8=R")
    command = re.sub(r'\b(promote to|promotion to|and promote to|promotes to|and promotes to)\b', '=', command, flags=re.IGNORECASE)

    # Remove any spaces
    command = command.replace(" ", "")
    return command


def run_alexa():
    """Process the command, provide feedback, and return the move if valid."""
    command = take_command()
    if not command:
        return None  # Skip processing if no valid command

    print(f"Original command: {command}")

    # Preprocess the command to fix common issues
    command = preprocess_command(command)
    print(f"Preprocessed command: {command}")

    # Normalize the command for chess
    command = normalize_command(command)
    print(f"Normalized command: {command}")

    # Recognize the move
    if re.match(r'^([NBKRQ])?([a-h])?([1-8])?[\-x]?([a-h][1-8])(=?[nbrqkNBRQK])?[\+#]?\Z', command):
        talk(f"You played: {command}")
        print(f"Move: {command}")
        return command  # Return the valid move as a string

    else:
        talk("I didn't understand the move. Please try again.")
        return None  # Return None for invalid moves


# Main loop
'''
while True:
    run_alexa()
'''