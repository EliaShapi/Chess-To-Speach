import chess
import speech_recognition as sr
import pyttsx3


# Initialize speech recognition and text-to-speech
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    """Speak out text."""
    engine.say(text)
    engine.runAndWait()


board = chess.Board()


def get_legal_moves():
    """Get all legal moves as strings."""
    return [board.san(move) for move in board.legal_moves]


def interpret_move(command):
    """Interpret complex move inputs."""
    try:
        # Directly parse the move if it's in SAN or UCI format
        move = board.parse_san(command)
        return move
    except ValueError:
        pass  # Proceed to advanced interpretation if direct parsing fails

    # Preprocess approximations for promotions, captures, etc.
    command = command.replace(" takes ", "x").replace(" and promote to ", "=")

    # Try parsing the move again
    try:
        move = board.parse_san(command)
        return move
    except ValueError:
        return None


def tick():
    """Process a single move."""
    try:
        # Input move
        print(f"Legal Moves: {', '.join(get_legal_moves())}")
        print(board)
        command = input("Write your move (or speak your move): ").lower()

        # Interpret the move
        move = interpret_move(command)
        if move and move in board.legal_moves:
            board.push(move)
            print(board)

            # Speak the last move
            talk(f"Move played: {board.san(move)}")
        else:
            # Handle ambiguous or invalid move
            legal_moves = get_legal_moves()
            if len(legal_moves) > 0:
                talk("I couldn't understand your move. Did you mean one of these?")
                print(f"Possible moves: {', '.join(legal_moves)}")
                talk("Please type or say the move again.")
            else:
                talk("No legal moves available.")

    except Exception as e:
        print(f"An error occurred: {e}")
        talk("An unexpected error occurred. Please try again.")


# Main game loop
while not board.is_game_over():
    tick()

# Game over
talk("Game over!")
print("Game over!")
