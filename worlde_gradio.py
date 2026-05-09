import random

import gradio as gr # import gradio library

 

with open("FiveLetterWords.txt", "r") as fobj:

    contents = fobj.read()

 

listofwords = contents.split(",")

 

# ============================================================

# Function to start a new game.

# ============================================================

def start_new_game():

    # correctword1 = listofwords[random.randint(0, 5757)].upper()

    correct_word = random.choice(listofwords).upper()

 

    # game_state remembers the state of the game as the game progresses in a dictionary

    game_state = {

        "correct_word": correct_word,

        "count": 0,

        "successful": False,

        "game_over": False,

        "history": []

    }

 

    return game_state

 

# ============================================================

# This function contains the Wordle checking logic.

# ============================================================

 

def check_guess(guess, correctword1):

    correctword = list(correctword1)

    guess_list = list(guess)

 

    feedback = ["⬛", "⬛", "⬛", "⬛", "⬛"]

 

    # First pass: check for green letters

    for i in range(5):

        if guess_list[i] == correctword[i]:

            feedback[i] = "🟩"

            correctword[i] = "Guessed"

            guess_list[i] = "Guessed"

 

    # Second pass: check for yellow letters

    for i in range(5):

        if guess_list[i] in correctword:

            feedback[i] = "🟨"

            index = correctword.index(guess_list[i])

            correctword[index] = "Guessed"

            guess_list[i] = "Guessed"

 

    return feedback

 

# ============================================================

# This function formats the board so it can be displayed in Gradio.

# ============================================================

 

def render_board(game_state):

    if len(game_state["history"]) == 0:

        return "No guesses yet."

 

    board_text = ""

 

    for item in game_state["history"]:

        guess = item["guess"]

        feedback = item["feedback"]

 

        board_text += f"### {' '.join(guess)}\n"

        board_text += f"## {''.join(feedback)}\n\n"

 

    return board_text

 

# ============================================================

# This function runs whenever the player clicks "Submit Guess".

# ============================================================

 

def submit_guess(guess, game_state):

    # If Gradio state is empty for some reason, start a new game

    if game_state is None:

        game_state = start_new_game()

 

    # Clean up user input

    guess = guess.strip().upper()

 

    # If the game has already ended, do not allow more guesses

    if game_state["game_over"]:

        message = "Game is already over. Click 'New Game' to play again."

        return "", game_state, render_board(game_state), message

 

    # Validate guess

    if len(guess) != 5 or not guess.isalpha():

        message = "Please enter a valid 5-letter word."

        return "", game_state, render_board(game_state), message

 

    # Optional validation:

    # Uncomment this if you want guesses to be restricted to your word list.

    #

    # if guess.lower() not in listofwords:

    #     message = "That word is not in the word list."

    #     return "", game_state, render_board(game_state), message

 

    # Increase attempt count

    game_state["count"] += 1

 

    # Check guess against correct word

    feedback = check_guess(guess, game_state["correct_word"])

 

    # Store guess history

    game_state["history"].append({

        "guess": guess,

        "feedback": feedback

    })

 

    # Check if all feedback symbols are green

    if feedback.count("🟩") == 5:

        game_state["successful"] = True

        game_state["game_over"] = True

        message = "You have guessed the word successfully."

 

    # Your original code used while count < 7,

    # which gives the player 7 attempts.

    elif game_state["count"] >= 6:

        game_state["game_over"] = True

        message = f"Game over. The correct word is {game_state['correct_word']}."

 

    else:

        attempts_left = 6 - game_state["count"]

        message = f"Guess submitted. You have {attempts_left} guesses left."

 

    return "", game_state, render_board(game_state), message

 

# ============================================================

# This function runs when the player clicks "New Game".

# ============================================================

def reset_game():

    game_state = start_new_game()

 

    board = "No guesses yet."

    message = "New game started. Guess a 5-letter word."

 

    return "", game_state, board, message

 

# ============================================================

# Build the Gradio UI. Using markdown syntax

# ============================================================

 

with gr.Blocks() as demo:

    gr.Markdown("# Wordle Game")

    gr.Markdown("""

    Guess the 5-letter word.

 

    **Legend:**  

    ⬛ = letter is not in word  

    🟨 = letter is in word, but wrong position  

    🟩 = letter is in word and correct position

    """)

 

    # Stores the current game's correct word, count, result, and history

    game_state = gr.State(start_new_game())

 

    guess_input = gr.Textbox(

        label="Guess a 5-letter word",

        placeholder="Type your guess here",

        max_lines=1

    )

 

    submit_button = gr.Button("Submit Guess")

    new_game_button = gr.Button("New Game")

 

    board_output = gr.Markdown("No guesses yet.")

    message_output = gr.Markdown("Game started. Guess a 5-letter word.")

 

    submit_button.click(

        fn=submit_guess,

        inputs=[guess_input, game_state],

        outputs=[guess_input, game_state, board_output, message_output]

    )

 

    new_game_button.click(

        fn=reset_game,

        inputs=[],

        outputs=[guess_input, game_state, board_output, message_output]

    )

 
demo.launch(

    server_name="0.0.0.0",

    server_port=7860,

    share=True
)
# ============================================================