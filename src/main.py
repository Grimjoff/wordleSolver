import tkinter as tk
from dataclasses import dataclass
from src.wordle_solver_logic import WordleSolverLogic  # Adjusted import
from pathlib import Path

# Load word list
def load_words_from_csv(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file if line.strip()]

wordle_words = load_words_from_csv("../data/oldList.csv")  # Adjusted path


@dataclass
class Guess:
    word: str
    states: list[int]


class WordleSolverUI:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Wordle Solver")
        self.word_length = 5
        self.logic = WordleSolverLogic(wordle_words)
        self.guesses = []

        ranked = self.logic.get_ranked_words(self.guesses)
        self.letters = list(ranked[0][0] if ranked else "apple")
        self.states = [0] * self.word_length

        self.suggestion_labels = []
        for i in range(3):
            lbl = tk.Label(master, text="", font=("Arial", 12))
            lbl.grid(row=i + 2, column=0, columnspan=5, sticky="w", padx=5, pady=2)
            self.suggestion_labels.append(lbl)

        self.buttons = []
        for i in range(self.word_length):
            btn = tk.Button(master, text=self.letters[i], width=5, command=lambda i=i: self.on_letter_click(i))
            btn.grid(row=0, column=i, padx=2)
            self.buttons.append(btn)
            self.update_button_color(i)

        self.update_button = tk.Button(master, text="Update", width=10, bg="lightblue", command=self.on_update_click)
        self.update_button.grid(row=0, column=self.word_length, padx=5)

        self.entry = tk.Entry(master, width=10)
        self.entry.grid(row=1, column=0, columnspan=3, pady=10)

        self.set_button = tk.Button(master, text="Set Word", command=self.set_manual_word)
        self.set_button.grid(row=1, column=3, columnspan=2)

        self.reset_button = tk.Button(master, text="Reset", width=10, bg="lightcoral", command=self.reset)
        self.reset_button.grid(row=0, column=self.word_length + 1, padx=5)

    def reset(self):
        self.guesses.clear()
        self.logic.reset()
        ranked = self.logic.get_ranked_words(self.guesses)
        self.letters = list(ranked[0][0] if ranked else "apple")
        self.states = [0] * self.word_length
        self.update_buttons(self.letters)

    def set_manual_word(self):
        word = self.entry.get().strip().lower()
        if len(word) == self.word_length and word.isalpha():
            self.letters = list(word)
            self.states = [0] * self.word_length
            self.update_buttons(self.letters)

    def update_buttons(self, new_letters):
        for i in range(self.word_length):
            self.buttons[i].config(text=new_letters[i])
            self.update_button_color(i)

    def on_letter_click(self, index):
        self.states[index] = (self.states[index] + 1) % 3
        self.update_button_color(index)

    def update_button_color(self, index):
        color = ["lightgray", "yellow", "green"][self.states[index]]
        self.buttons[index].config(bg=color)

    def show_suggestions(self, suggestions):
        for i, word in enumerate(suggestions[:3]):
            self.suggestion_labels[i].config(text=word[0])

    def on_update_click(self):
        word = "".join([btn.cget("text") for btn in self.buttons])
        self.guesses.append((word, self.states.copy()))

        ranked = self.logic.get_ranked_words(self.guesses)
        self.show_suggestions(ranked)

        if ranked:
            next_word = list(ranked[0][0])
            self.letters = next_word
            self.states = [0] * self.word_length
            self.update_buttons(next_word)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x200")
    app = WordleSolverUI(root)
    root.mainloop()
