import chess
import speech_recognition as sr
import pyttsx3

import VoiceRecognizer as vr

# Initialize speech recognition and text-to-speech
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

board = chess.Board()

print("Legal Moves: ", board.legal_moves)
print(board)

# Function to handle a single move
def tick():
    try:
        # Get input for the move
        move_input = vr.run_alexa()

        if not move_input:  # <-- Check for None or empty string
            print("No move was recognized.")
            talk("I didn't catch that. Please try again.")
            return

        # Convert the input move to a Move object (except SAN format input)
        try:
            move = board.parse_san(move_input)
        except ValueError as e:
            print(f"Invalid move: {e}")
            talk("That move isn't valid. Try again.")
            return

        # Push the move onto the board
        board.push(move)

        # Display updated board state
        print("Legal Moves: ", board.legal_moves)
        print(board)

        # Retrieve and speak the last move in SAN format
        if board.move_stack:  # Ensure there is a move to retrieve
            try:
                last_move = board.pop()  # Get the last move as a Move object
                uci_move = board.san(last_move)  # Convert Move object to SAN
                board.push(last_move)  # Restore the move after popping
                talk(f"{uci_move}")
            except Exception as e:
                print(f"Error converting move to SAN: {e}")
        else:
            print("No moves have been made yet.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main game loop
while not board.is_game_over():
    tick()

# Game over
talk("Game over!")
print("Game over!")