from collections import Counter
import random

class WordleSolverLogic:
    def __init__(self, word_list):
        self.word_list = word_list
        self.reset()

    def reset(self):
        self.words_copy = self.word_list.copy()
        self.index_letter_scores = self.compute_index_letter_frequencies(self.words_copy)
        self.invalid_words = set()
        self.grey_letters = set()
        self.yellow_letters = {}  # letter -> set of forbidden positions
        self.green_letters = {}   # pos -> set of allowed letters

    def compute_index_letter_frequencies(self, word_list):
        index_letter_counts = [Counter() for _ in range(5)]
        for word in word_list:
            for i, c in enumerate(word):
                index_letter_counts[i][c] += 1

        index_letter_scores = []
        for i in range(5):
            max_count = max(index_letter_counts[i].values(), default=1)
            scores = {letter: count / max_count for letter, count in index_letter_counts[i].items()}
            index_letter_scores.append(scores)
        return index_letter_scores

    def rank_word(self, word):
        total_score = 0
        seen = set()
        for i, c in enumerate(word):
            if c in seen:
                total_score -= 1
            seen.add(c)
            total_score += self.index_letter_scores[i].get(c, 0)
        return total_score

    def update_constraints(self, guesses):
        # guesses: list of (word, states), states = list of ints 0=gray,1=yellow,2=green
        self.invalid_words.clear()
        self.grey_letters.clear()
        self.yellow_letters.clear()
        self.green_letters.clear()

        for guess_word, states in guesses:
            for i, state in enumerate(states):
                c = guess_word[i]
                if state == 2:  # green
                    if i not in self.green_letters:
                        self.green_letters[i] = set()
                    self.green_letters[i].add(c)
                    if c in self.yellow_letters:
                        self.yellow_letters.pop(c)
                elif state == 1:  # yellow
                    if c not in self.yellow_letters:
                        self.yellow_letters[c] = set()
                    self.yellow_letters[c].add(i)
                else:  # gray
                    # Only add to grey if not already yellow or green somewhere
                    if c not in self.yellow_letters and not any(c in v for v in self.green_letters.values()):
                        self.grey_letters.add(c)

    def filter_words(self, guesses):
        self.update_constraints(guesses)
        filtered = []

        for word in self.words_copy:
            valid = True
            for i, c in enumerate(word):
                if c in self.grey_letters:
                    if not (i in self.green_letters and c in self.green_letters[i]):
                        valid = False
                        break

                for yl_letter, forbidden_positions in self.yellow_letters.items():
                    if yl_letter not in word:
                        valid = False
                        break
                    if any(word[pos] == yl_letter for pos in forbidden_positions):
                        valid = False
                        break
                if not valid:
                    break

                if i in self.green_letters and c not in self.green_letters[i]:
                    valid = False
                    break
            if valid:
                filtered.append(word)

        self.words_copy = [w for w in filtered if w not in self.invalid_words]
        self.index_letter_scores = self.compute_index_letter_frequencies(self.words_copy)
        return self.words_copy

    def get_ranked_words(self, guesses):
        filtered_words = self.filter_words(guesses)
        ranked_words = []
        for w in filtered_words:
            ranked_words.append((w, self.rank_word(w)))
        ranked_words.sort(key=lambda x: x[1], reverse=True)
        return ranked_words

    # For testing: run solver for a chosen target word and return number of guesses needed
    def solve_word(self, target_word, verbose=False):
        guesses = []
        possible_words = self.words_copy.copy()
        while len(guesses) < 7:
            ranked = self.get_ranked_words(guesses)
            if not ranked:
                return None  # no solution
            guess_word = ranked[0][0]
            guesses.append((guess_word, self.get_letter_states(guess_word, target_word)))
            # if verbose:
                # print(f"Guess: {guess_word}, States: {guesses[-1][1]}")
            if guess_word == target_word:
                return len(guesses)

    def get_letter_states(self, guess, target):
        # returns list[int] 0=gray,1=yellow,2=green for each letter
        states = [0]*5
        target_list = list(target)
        # First pass: green
        for i in range(5):
            if guess[i] == target[i]:
                states[i] = 2
                target_list[i] = None
        # Second pass: yellow
        for i in range(5):
            if states[i] == 0 and guess[i] in target_list:
                states[i] = 1
                target_list[target_list.index(guess[i])] = None
        return states
