"""
TSF Game - Graphical User Interface (GUI)

This module implements the Tkinter-based GUI for the TSF (Ten Sefirot Finder) game.
It allows users to play the game by interacting with visual elements,
including setting game parameters, submitting guesses, and viewing game history and rules.
It uses `core_game_logic.py` for the underlying game mechanics.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Toplevel, Text
from core_game_logic import generate_secret_number, calculate_clues

class TSFGameGUI:
    """
    Main class for the TSF Game GUI.

    This class encapsulates all the UI elements, game state variables,
    and methods required to run the TSF game with a graphical interface.
    """
    def __init__(self, master: tk.Tk):
        """
        Initializes the TSF Game GUI.

        Args:
            master: The root Tkinter window for the application.
        """
        self.master = master
        master.title("TSF Game")
        master.geometry("500x600") # Adjusted window size for better layout

        # --- Game State Variables ---
        self.secret_number: list[str] = []         # The computer-generated secret number
        self.num_digits_setting: int = 0           # Number of digits chosen for the current game
        self.max_guesses_setting: int = 0          # Max guesses chosen for the current game
        self.current_guesses_count: int = 0        # How many guesses the player has made in the current game
        self.game_active: bool = False             # Flag to indicate if a game is currently in progress

        self._setup_menu()
        self._setup_settings_frame()
        self._setup_message_area()
        self._setup_gameplay_area()

    def _setup_menu(self):
        """Sets up the menu bar for the application."""
        menubar = tk.Menu(self.master)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.start_new_game)
        game_menu.add_command(label="View Rules", command=self.display_rules)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.master.config(menu=menubar)

    def _setup_settings_frame(self):
        """Sets up the frame containing game settings inputs and start button."""
        settings_frame = ttk.LabelFrame(self.master, text="Game Settings", padding=(10, 5))
        settings_frame.pack(padx=10, pady=10, fill="x")

        # Number of Digits input
        ttk.Label(settings_frame, text="Number of Digits (1-9):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.num_digits_entry = ttk.Entry(settings_frame, width=5)
        self.num_digits_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.num_digits_entry.insert(0, "3") # Default value

        # Max Guesses input
        ttk.Label(settings_frame, text="Max Guesses (1-100):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.max_guesses_entry = ttk.Entry(settings_frame, width=5)
        self.max_guesses_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.max_guesses_entry.insert(0, "10") # Default value

        # Start Game button
        self.start_game_button = ttk.Button(settings_frame, text="Start Game", command=self.start_new_game)
        self.start_game_button.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")

    def _setup_message_area(self):
        """Sets up the label for displaying game messages and status updates."""
        self.message_label = ttk.Label(self.master, text="Set parameters and start the game!", font=("Arial", 10), wraplength=480)
        self.message_label.pack(pady=5, padx=10, fill="x")

    def _setup_gameplay_area(self):
        """Sets up the frame for guess input and guess history display."""
        game_play_frame = ttk.LabelFrame(self.master, text="Gameplay", padding=(10, 5))
        game_play_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Guess Input sub-frame
        guess_input_frame = ttk.Frame(game_play_frame)
        guess_input_frame.pack(pady=5, fill="x")

        ttk.Label(guess_input_frame, text="Enter your guess:").pack(side=tk.LEFT, padx=5)
        self.guess_entry = ttk.Entry(guess_input_frame, width=15)
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        self.guess_entry.config(state=tk.DISABLED) # Disabled until game starts

        self.submit_guess_button = ttk.Button(guess_input_frame, text="Submit Guess", command=self.submit_guess, state=tk.DISABLED)
        self.submit_guess_button.pack(side=tk.LEFT, padx=5)

        # Guess History display
        ttk.Label(game_play_frame, text="Guess History:").pack(pady=(10,0), anchor="w")
        self.guess_history_text = scrolledtext.ScrolledText(game_play_frame, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.guess_history_text.pack(padx=5, pady=5, fill="both", expand=True)

    def start_new_game(self):
        """
        Starts a new game.
        Validates game settings, generates a new secret number,
        and resets the UI for a new game session.
        """
        # Validate number of digits input
        try:
            num_digits = int(self.num_digits_entry.get())
            if not (1 <= num_digits <= 9): # Max 10 for core_game_logic, but UI limits to 9 for simplicity
                self.message_label.config(text="Error: Number of digits must be between 1 and 9.")
                return
        except ValueError:
            self.message_label.config(text="Error: Invalid input for Number of Digits.")
            return

        # Validate max guesses input
        try:
            max_guesses = int(self.max_guesses_entry.get())
            if not (1 <= max_guesses <= 100):
                self.message_label.config(text="Error: Max guesses must be between 1 and 100.")
                return
        except ValueError:
            self.message_label.config(text="Error: Invalid input for Max Guesses.")
            return

        # Store validated settings
        self.num_digits_setting = num_digits
        self.max_guesses_setting = max_guesses
        
        # Generate secret number using core logic
        try:
            self.secret_number = generate_secret_number(self.num_digits_setting)
        except ValueError as e: # Catch errors from core_game_logic (e.g., num_digits > 10, though UI prevents)
            self.message_label.config(text=f"Error generating secret number: {e}")
            return

        # Reset game state variables
        self.current_guesses_count = 0
        self.game_active = True

        # Reset UI elements for a new game
        self.guess_history_text.config(state=tk.NORMAL) # Enable to clear
        self.guess_history_text.delete('1.0', tk.END)
        self.guess_history_text.config(state=tk.DISABLED) # Disable again

        self.guess_entry.config(state=tk.NORMAL)
        self.guess_entry.delete(0, tk.END)
        self.submit_guess_button.config(state=tk.NORMAL)
        
        # Allow settings to be changed for a subsequent game, so keep them enabled.
        # self.num_digits_entry.config(state=tk.DISABLED) # Optionally disable during active game
        # self.max_guesses_entry.config(state=tk.DISABLED)
        
        self.message_label.config(text=f"Game started! I've thought of a {self.num_digits_setting}-digit number. You have {self.max_guesses_setting} guesses.")
        # For debugging purposes:
        # print(f"Secret Number (for debugging): {self.secret_number}")

    def display_rules(self):
        """
        Displays the game rules in a new Toplevel window.
        Reads rules from 'TSF_Game_Rules.txt'.
        """
        try:
            with open("TSF_Game_Rules.txt", "r") as f:
                rules_content = f.read()
            
            rules_window = Toplevel(self.master)
            rules_window.title("TSF Game Rules")
            rules_window.geometry("450x400") # Set a reasonable size for the rules window
            rules_window.transient(self.master) # Keep it on top of the main window
            rules_window.grab_set() # Make it modal (user must interact with it before main window)

            text_area = Text(rules_window, wrap=tk.WORD, padx=10, pady=10, font=("Arial", 10))
            text_area.insert(tk.END, rules_content)
            text_area.config(state=tk.DISABLED) # Make text area read-only
            text_area.pack(expand=True, fill="both")

            close_button = ttk.Button(rules_window, text="Close", command=rules_window.destroy)
            close_button.pack(pady=10)

        except FileNotFoundError:
            messagebox.showerror("Error", "TSF_Game_Rules.txt not found in the application directory.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while trying to load the rules: {e}")

    def submit_guess(self):
        """
        Processes the player's guess.
        Validates the guess, calculates clues using core_game_logic,
        updates the guess history, and checks for win/loss conditions.
        """
        if not self.game_active:
            self.message_label.config(text="Please start a new game first!")
            return

        guess_str = self.guess_entry.get().strip() # Get guess and remove leading/trailing whitespace

        # Validate the guess format
        if len(guess_str) != self.num_digits_setting:
            self.message_label.config(text=f"Error: Guess must have {self.num_digits_setting} digits.")
            return
        if not guess_str.isdigit():
            self.message_label.config(text="Error: Guess must contain only digits.")
            return
        if len(set(guess_str)) != self.num_digits_setting: # Check for unique digits
            self.message_label.config(text="Error: Digits in guess must be unique.")
            return

        player_guess_list = list(guess_str) # Convert guess string to list of characters (strings)
        self.current_guesses_count += 1

        # Calculate clues using core logic
        try:
            clues = calculate_clues(player_guess_list, self.secret_number)
        except Exception as e: # Catch any unexpected errors from clue calculation
            self.message_label.config(text=f"Error calculating clues: {e}")
            self.current_guesses_count -=1 # Rollback guess count as it failed
            return

        clues_str_display = "".join(clues) # Format clues for display (e.g., "TSF")

        # Update guess history
        self.guess_history_text.config(state=tk.NORMAL) # Enable to modify
        self.guess_history_text.insert(tk.END, f"Guess #{self.current_guesses_count}: {guess_str} -> Clues: {clues_str_display}\n")
        self.guess_history_text.see(tk.END) # Scroll to the latest guess
        self.guess_history_text.config(state=tk.DISABLED) # Disable again
        
        self.guess_entry.delete(0, tk.END) # Clear the guess entry field

        # Check for win condition
        if all(c == 'T' for c in clues):
            self.message_label.config(text=f"Congratulations! You guessed the number {''.join(self.secret_number)} in {self.current_guesses_count} tries!")
            self.end_game()
            return

        # Check for loss condition
        if self.current_guesses_count >= self.max_guesses_setting:
            self.message_label.config(text=f"Game Over! You ran out of guesses. The secret number was {''.join(self.secret_number)}.")
            self.end_game()
            return
        
        # If game continues, update status message
        guesses_remaining = self.max_guesses_setting - self.current_guesses_count
        self.message_label.config(text=f"Guess #{self.current_guesses_count} submitted. Clues: {clues_str_display}. You have {guesses_remaining} guesses remaining.")

    def end_game(self):
        """
        Handles the end of a game (win or loss).
        Disables gameplay elements and updates game state.
        """
        self.game_active = False
        self.guess_entry.config(state=tk.DISABLED)
        self.submit_guess_button.config(state=tk.DISABLED)
        
        # Re-enable settings entries for a new game configuration
        self.num_digits_entry.config(state=tk.NORMAL) 
        self.max_guesses_entry.config(state=tk.NORMAL)
        # The "Start Game" button remains enabled, allowing a new game to be started.

def main():
    """
    Main function to create and run the TSF Game GUI.
    """
    root = tk.Tk()
    app = TSFGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
