import tkinter as tk
from dataclasses import dataclass
from collections import Counter


# Loading words
def load_words_from_csv(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file if line.strip()]


wordleWords = load_words_from_csv("oldList.csv")
WordsCopy = wordleWords.copy()
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
        self.reset_data()

        self.word_length = 5
        self.WordsCopy = WordsCopy.copy()
        self.letter_scores = compute_letter_frequencies(self.WordsCopy)

        words = self.getNewWords()
        firstWord = list(words[0][0])
        self.letters = firstWord
        self.states = [0] * self.word_length  # 0 = gray, 1 = yellow, 2 = green
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

        # Update button to trigger next word guess
        self.update_button = tk.Button(master, text="Update", width=10, bg="lightblue", command=self.on_update_click)
        self.update_button.grid(row=0, column=self.word_length, padx=5)
        self.entry = tk.Entry(master, width=10)
        self.entry.grid(row=1, column=0, columnspan=3, pady=10)

        self.set_button = tk.Button(master, text="Set Word", command=self.set_manual_word)
        self.set_button.grid(row=1, column=3, columnspan=2)
        self.reset_button = tk.Button(master, text="Reset", width=10, bg="lightcoral", command=self.reset)
        self.reset_button.grid(row=0, column=self.word_length + 1, padx=5)

    def reset_data(self):
        global wordleWords, invalidWords, greyLetters, yellowLetters, greenLetters
        self.WordsCopy = WordsCopy.copy()
        self.letter_scores = compute_letter_frequencies(self.WordsCopy)
        self.guesses.clear()
        invalidWords.clear()
        greyLetters.clear()
        yellowLetters.clear()
        greenLetters.clear()
    def reset(self):
        self.reset_data()
        initial_words = self.getNewWords()
        self.letters = list(initial_words[0][0])
        self.update_buttons(list(initial_words[0][0]))
        self.states = [0] * self.word_length

        for i in range(self.word_length):
            self.buttons[i].config(text=self.letters[i])
            self.update_button_color(i)
    def set_manual_word(self):
        manual_word = self.entry.get().strip().lower()
        if len(manual_word) != 5 or not manual_word.isalpha():
            print("Invalid word. Please enter a 5-letter word.")
            return

        self.letters = list(manual_word)
        self.states = [0] * self.word_length  # Reset states
        for i in range(self.word_length):
            self.buttons[i].config(text=self.letters[i])
            self.update_button_color(i)

    def update_buttons(self, new_word):
        for i in range(5):
            self.buttons[i].config(text=new_word[i])

    def on_letter_click(self, index):
        self.states[index] = (self.states[index] + 1) % 3
        self.update_button_color(index)

    def update_button_color(self, index):
        color = ["lightgray", "yellow", "green"][self.states[index]]
        self.buttons[index].config(bg=color)

    def show_suggestions(self, suggestions):
        for i, word in enumerate(suggestions):
            if i < len(self.suggestion_labels):
                self.suggestion_labels[i].config(text=word)
    def on_update_click(self):
        current_letters = [btn.cget("text") for btn in self.buttons]
        current_states = self.states.copy()
        self.guesses.append(Guess(current_letters.copy(), current_states))

        self.updateList()
        top_words = self.getNewWords()
        self.show_suggestions(top_words)
        # Only use best word
        bestWord = list(top_words[0][0])
        self.update_buttons(bestWord)
        self.WordsCopy = list(filter(lambda x: x not in invalidWords, self.WordsCopy))
        self.letter_scores = compute_letter_frequencies(self.WordsCopy)
        for i in range(self.word_length):
            if self.states[i] == 1:
                self.states[i] = 0
                self.update_button_color(i)

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

    def getNewWords(self):
        bestranking = 0
        bestword = None
        ranked_words = []
        for word in wordleWords:
            wordValid = True
            for i in range(5):
                letter = word[i]
                # If letter is known to be gray
                if letter in greyLetters:
                    # But allow it if it's explicitly green at this position
                    if not (i in greenLetters and letter in greenLetters[i]):
                        wordValid = False
                        break

                # If letter is yellow but appears in a previously yellowed position
                for yl_letter, forbidden_positions in yellowLetters.items():
                    #check if letter is in the word at all
                    if yl_letter not in word:
                        wordValid = False
                        break
                    # check that letter is NOT in forbidden positions
                    for pos in forbidden_positions:
                        if word[pos] == yl_letter:
                            wordValid = False
                            break
                    if not wordValid:
                        break

                if i in greenLetters:
                    if letter not in greenLetters[i]:
                        wordValid = False
                        break

            if wordValid:
                ranking = self.rankword(word)
                ranked_words.append((word, ranking))
                bestranking = ranking
            else:
                invalidWords.append(word)
        ranked_words.sort(key=lambda x: x[1], reverse=True)

        return ranked_words

    # Iterate through the word and get the frequency scores. if it includes a letter that was yellow before its
    # already a top contender.
    def rankword(self, word):
        total_score = 0
        seen = set()
        for i, c in enumerate(word):
            if c in yellowLetters and i not in yellowLetters.get(c):
                total_score += 1
                seen.add(c)
            if c in seen:
                total_score -= 1
            seen.add(c)
            total_score += self.letter_scores.get(c, 0)
        if word == 'swing': print(total_score)
        return total_score


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x200")
    app = WordleSolverUI(root)
    root.mainloop()
