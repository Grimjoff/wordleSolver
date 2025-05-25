import tkinter as tk
from dataclasses import dataclass
from collections import Counter


# Loading words
def load_words_from_csv(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file if line.strip()]


wordleWords = load_words_from_csv("oldList.csv")

# setting globals
invalidWords = []
greyLetters = set()
yellowLetters = {}
greenLetters = {}


@dataclass
class Guess:
    letters: list[str]
    states: list[int]


# For better results compute frequencies, letter has more value if high frequency, a > z
def compute_letter_frequencies(word_list):
    letter_counts = Counter()
    for word in word_list:
        unique_letters = set(word)  # Count each letter once per word
        letter_counts.update(unique_letters)

    # Normalize to values between 0 and 1
    max_freq = max(letter_counts.values())
    letter_scores = {letter: count / max_freq for letter, count in letter_counts.items()}

    return letter_scores


letter_scores = compute_letter_frequencies(wordleWords)


class WordleSolverUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Solver")
        self.guesses = []
        self.word_length = 5
        word = self.getNewWord()
        self.letters = list(word)  # Current best guess is atone
        self.states = [0] * self.word_length  # 0 = gray, 1 = yellow, 2 = green

        self.buttons = []
        for i in range(self.word_length):
            btn = tk.Button(master, text=self.letters[i], width=5, command=lambda i=i: self.on_letter_click(i))
            btn.grid(row=0, column=i, padx=2)
            self.buttons.append(btn)
            self.update_button_color(i)

        # Update button to trigger next word guess
        self.update_button = tk.Button(master, text="Update", width=10, bg="lightblue", command=self.on_update_click)
        self.update_button.grid(row=0, column=self.word_length, padx=5)

    def update_buttons(self, new_word):
        for i in range(5):
            self.buttons[i].config(text=new_word[i])

    def on_letter_click(self, index):
        self.states[index] = (self.states[index] + 1) % 3
        self.update_button_color(index)

    def update_button_color(self, index):
        color = ["lightgray", "yellow", "green"][self.states[index]]
        self.buttons[index].config(bg=color)

    def on_update_click(self):
        global wordleWords, letter_scores
        current_letters = [btn.cget("text") for btn in self.buttons]
        current_states = self.states.copy()
        self.guesses.append(Guess(current_letters.copy(), current_states))

        self.updateList()
        newWord = self.getNewWord()
        self.update_buttons(newWord)
        wordleWords = list(filter(lambda x: x not in invalidWords, wordleWords))
        letter_scores = compute_letter_frequencies(wordleWords)

    # update the grey, yellow and green letters,
    # Current small fix possible: Dont iterate through guesses multiple times if possible
    def updateList(self):
        for guess in self.guesses:
            for i in range(5):
                # if green set greenletter on that index to that letter
                if guess.states[i] == 2:
                    if guess.letters[i] not in greenLetters:
                        greenLetters[i] = set()
                    greenLetters[i].add(guess.letters[i])
                    # if green but was yellow before, clear out the yellow dict
                    if guess.letters[i] in yellowLetters:
                        del yellowLetters[guess.letters[i]]
                # if yellow save it in yellowletters
                elif guess.states[i] == 1:
                    if guess.letters[i] not in yellowLetters:
                        yellowLetters[guess.letters[i]] = set()
                    yellowLetters[guess.letters[i]].add(i)
                # if neither add it to grey
                elif guess.letters[i] not in yellowLetters:
                    greyLetters.add(guess.letters[i])

    def getNewWord(self):
        bestranking = 0
        bestword = None
        # iterate through the words
        for word in wordleWords:
            wordValid = True
            for i in range(5):
                # if letter is grey or yellow in a spot it was already at once, not valid
                if word[i] in greyLetters or (word[i] in yellowLetters and i in yellowLetters[word[i]]):
                    wordValid = False
                    break
                # if letter doesnt match a greenletter set at that index
                elif i in greenLetters and word[i] not in greenLetters[i]:
                    wordValid = False
            # if valid keep updating ranking and word
            if wordValid:
                ranking = self.rankword(word)
                if ranking > bestranking:
                    bestranking = ranking
                    bestword = word
            # append to invalidWords list to strip them out of the total list
            else:
                invalidWords.append(word)

        return bestword
    # Iterate through the word and get the frequency scores. if it includes a letter that was yellow before its already a top contender.
    def rankword(self, word):
        total_score = 0
        word = set(word)
        for i, c in enumerate(word):
            if c in yellowLetters and i not in yellowLetters.get(c):
                total_score += 1
            total_score += letter_scores.get(c, 0)

        return total_score


if __name__ == "__main__":
    root = tk.Tk()
    app = WordleSolverUI(root)
    root.mainloop()
