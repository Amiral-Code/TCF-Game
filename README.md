# TSF Game

## Overview

TSF Game (Ten Sefirot Finder) is a deductive logic game where players try to guess a secret multi-digit number. For each guess, clues are provided to help deduce the correct number. The game offers both a Graphical User Interface (GUI) and a Command-Line Interface (CLI) for different playing experiences.

Tags: short, game, puzzle, logic, number-guessing, deductive-reasoning, python

## Features

*   **Classic Gameplay:** Based on the traditional "Bulls and Cows" or "Code Breaker" style games.
*   **Configurable Game:** Set the number of digits in the secret number (1-9) and the maximum number of guesses (1-100).
*   **Graphical User Interface (GUI):** A user-friendly interface built with Tkinter for an interactive gameplay experience.
*   **Command-Line Interface (CLI):** A text-based version for those who prefer the terminal.
*   **Multiple Game Modes (CLI):**
    *   **Player Guesses Computer's Number:** The classic mode where you try to find the computer's secret number.
    *   **Bot Guesses Player's Number:** Challenge the AI! You think of a number, and the bot tries to guess it.
*   **In-Game Rules:** Access game rules directly from the GUI or CLI.

## Project Structure

The project is organized into the following key files:

*   `tsf_gui.py`: Main application file for the Tkinter-based GUI version of the game.
*   `TSF_Game.py`: Main application file for the command-line (CLI) version of the game.
*   `core_game_logic.py`: Contains the essential game logic, including secret number generation and clue calculation ('T', 'S', 'F'). This module is shared by both the GUI and CLI versions.
*   `bots.py`: Defines the `BotPlayer` class, which implements the AI strategy for the "Bot Guesses Player's Number" mode in the CLI version.
*   `TSF_Game_Rules.txt`: A plain text file containing the rules of the TSF game, accessible from both game interfaces.
*   `LICENSE`: Contains the MIT License for the project.

## How to Run

Ensure you have Python 3 installed on your system.

### GUI Version

To play the graphical version of TSF Game:

1.  Navigate to the project directory in your terminal.
2.  Run the command:
    ```bash
    python tsf_gui.py
    ```
    This will launch the TSF Game window.

### CLI Version

To play the command-line version of TSF Game:

1.  Navigate to the project directory in your terminal.
2.  Run the command:
    ```bash
    python TSF_Game.py
    ```
3.  The game will start in your terminal, and you'll be prompted to choose a game mode.

## Game Rules Summary

The goal is to guess a secret number composed of unique digits. After each guess, you receive clues:

*   **T (True):** A correct digit is in the correct position.
*   **S (Sefirah/Shuffled):** A correct digit is in the wrong position.
*   **F (False):** An incorrect digit (not in the secret number).

Use these clues to deduce the secret number within the allowed number of guesses. For detailed rules, please refer to the "View Rules" option in the GUI or CLI, or read the `TSF_Game_Rules.txt` file.

---
*This project was developed as part of a guided software engineering task.*
