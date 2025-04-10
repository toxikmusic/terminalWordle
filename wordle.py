#!/usr/bin/env python3
"""
Terminal-based Wordle Game
--------------------------
A command-line implementation of the popular word guessing game Wordle.
Players have 6 attempts to guess a 5-letter word, with Unicode block
feedback on their guesses.
"""

import random
import sys
import os
from words import WORD_LIST
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

class Wordle:
    """Main Wordle game class that handles game logic and display."""
    
    def __init__(self):
        """Initialize a new game of Wordle."""
        self.max_attempts = 6
        self.word_length = 5
        self.target_word = self._select_random_word()
        self.attempts = []
        self.game_over = False
        
        # Unicode character mappings
        self.filled_letters = {
            'A': '🅐', 'B': '🅑', 'C': '🅒', 'D': '🅓', 'E': '🅔', 
            'F': '🅕', 'G': '🅖', 'H': '🅗', 'I': '🅘', 'J': '🅙', 
            'K': '🅚', 'L': '🅛', 'M': '🅜', 'N': '🅝', 'O': '🅞', 
            'P': '🅟', 'Q': '🅠', 'R': '🅡', 'S': '🅢', 'T': '🅣', 
            'U': '🅤', 'V': '🅥', 'W': '🅦', 'X': '🅧', 'Y': '🅨', 
            'Z': '🅩'
        }
        
        self.empty_letters = {
            'A': '🄰', 'B': '🄱', 'C': '🄲', 'D': '🄳', 'E': '🄴', 
            'F': '🄵', 'G': '🄶', 'H': '🄷', 'I': '🄸', 'J': '🄹', 
            'K': '🄺', 'L': '🄻', 'M': '🄼', 'N': '🄽', 'O': '🄾', 
            'P': '🄿', 'Q': '🅀', 'R': '🅁', 'S': '🅂', 'T': '🅃', 
            'U': '🅄', 'V': '🅅', 'W': '🅆', 'X': '🅇', 'Y': '🅈', 
            'Z': '🅉'
        }
        
        self.yellow_letters = {
            'A': 'Ⓐ', 'B': 'Ⓑ', 'C': 'Ⓒ', 'D': 'Ⓓ', 'E': 'Ⓔ', 
            'F': 'Ⓕ', 'G': 'Ⓖ', 'H': 'Ⓗ', 'I': 'Ⓘ', 'J': 'Ⓙ', 
            'K': 'Ⓚ', 'L': 'Ⓛ', 'M': 'Ⓜ', 'N': 'Ⓝ', 'O': 'Ⓞ', 
            'P': 'Ⓟ', 'Q': 'Ⓠ', 'R': 'Ⓡ', 'S': 'Ⓢ', 'T': 'Ⓣ', 
            'U': 'Ⓤ', 'V': 'Ⓥ', 'W': 'Ⓦ', 'X': 'Ⓧ', 'Y': 'Ⓨ', 
            'Z': 'Ⓩ'
        }
        
        self.empty_block = '⬜'
    
    def _select_random_word(self):
        """Select a random 5-letter word from the word list."""
        return random.choice(WORD_LIST).upper()
    
    def display_instructions(self):
        """Display game instructions to the player."""
        print("\n" + "=" * 50)
        print(f"{Fore.CYAN}WORDLE - TERMINAL EDITION{Style.RESET_ALL}")
        print("=" * 50)
        print("\nGuess the WORDLE in 6 tries.")
        print("Each guess must be a valid 5-letter word.")
        print("After each guess, the Unicode blocks will")
        print("change to show how close your guess was to the word.\n")
        
        print(f"🅐 - The letter is in the word and in the correct spot.")
        print(f"Ⓐ - The letter is in the word but in the wrong spot.")
        print(f"🄰 - The letter is not in the word.\n")
        
        print(f"Type {Fore.RED}'!quit'{Style.RESET_ALL} to exit the game at any time.")
        print(f"Type {Fore.GREEN}'!restart'{Style.RESET_ALL} to start a new game.")
        print("=" * 50 + "\n")
    
    def display_game_state(self):
        """Display the current game state including previous guesses and their feedback."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_instructions()
        
        # Display game board with Unicode blocks
        print(f"{Fore.CYAN}Game Board:{Style.RESET_ALL}")
        
        # Display previous attempts with Unicode feedback
        for i in range(self.max_attempts):
            if i < len(self.attempts):
                guess, feedback = self.attempts[i]
                self._display_unicode_guess(guess, feedback)
            else:
                # Display empty blocks for remaining attempts
                print(" ".join([self.empty_block] * self.word_length))
        
        print()
        
        # Display attempts remaining
        attempts_remaining = self.max_attempts - len(self.attempts)
        print(f"Attempts remaining: {attempts_remaining}\n")
    
    def _display_unicode_guess(self, guess, feedback):
        """Display a guess with Unicode character blocks."""
        unicode_guess = ""
        for i, letter in enumerate(guess):
            if feedback[i] == 'G':  # Correct letter, correct position
                unicode_guess += self.filled_letters[letter] + " "
            elif feedback[i] == 'Y':  # Correct letter, wrong position
                unicode_guess += self.yellow_letters[letter] + " "
            else:  # Incorrect letter
                unicode_guess += self.empty_letters[letter] + " "
        print(unicode_guess)
    
    def evaluate_guess(self, guess):
        """Evaluate the player's guess and provide feedback."""
        guess = guess.upper()
        
        # Validate the guess
        if len(guess) != self.word_length:
            return False, f"Your guess must be {self.word_length} letters long."
        
        if not guess.isalpha():
            return False, "Your guess must contain only letters."
        
        # Generate feedback for the guess
        feedback = ['X'] * self.word_length  # Default to incorrect
        
        # First pass: check for correct positions (Green)
        for i in range(self.word_length):
            if guess[i] == self.target_word[i]:
                feedback[i] = 'G'
        
        # Second pass: check for correct letters in wrong positions (Yellow)
        # We need to account for duplicates, so we'll track which target letters have been matched
        remaining_target_letters = {}
        for i in range(self.word_length):
            if feedback[i] != 'G':  # Only count letters that weren't already matched as green
                if self.target_word[i] in remaining_target_letters:
                    remaining_target_letters[self.target_word[i]] += 1
                else:
                    remaining_target_letters[self.target_word[i]] = 1
        
        for i in range(self.word_length):
            if feedback[i] != 'G' and guess[i] in remaining_target_letters and remaining_target_letters[guess[i]] > 0:
                feedback[i] = 'Y'
                remaining_target_letters[guess[i]] -= 1
        
        self.attempts.append((guess, feedback))
        
        # Check win condition
        if guess == self.target_word:
            self.game_over = True
            return True, "You win! You've guessed the word correctly!"
        
        # Check lose condition
        if len(self.attempts) >= self.max_attempts:
            self.game_over = True
            return True, f"Game over! The word was {self.target_word}."
        
        return True, ""  # Valid guess, game continues
    
    def play(self):
        """Main game loop."""
        self.display_game_state()
        
        while not self.game_over:
            guess = input("Enter your guess: ").strip()
            
            # Check for special commands
            if guess.lower() == "!quit":
                print(f"\nThanks for playing! The word was {self.target_word}.")
                sys.exit(0)
            elif guess.lower() == "!restart":
                print("\nStarting a new game...")
                return True  # Signal to start a new game
            elif guess.lower() == "!word":
                # Debugging backdoor to reveal the current word
                print(f"\n[DEBUG] The current word is: {self.target_word}")
                input("Press Enter to continue...")
                self.display_game_state()
                continue
            
            valid, message = self.evaluate_guess(guess)
            
            if not valid:
                print(f"{Fore.RED}{message}{Style.RESET_ALL}")
                input("Press Enter to continue...")
            else:
                self.display_game_state()
                if message:  # Win or lose message
                    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            
            if self.game_over:
                play_again = input("\nPlay again? (y/n): ").strip().lower()
                if play_again == 'y':
                    return True  # Signal to start a new game
                else:
                    print("\nThanks for playing!")
                    return False  # Signal to exit
        
        return False

def main():
    """Main function to run the Wordle game."""
    play_again = True
    
    while play_again:
        game = Wordle()
        play_again = game.play()
    
    print("Goodbye!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
