﻿# 🧠 Wordle Solver (Hard Mode)

A Python-based **Wordle solver** that plays in **hard mode**, using positional letter frequencies and guess validation logic. Includes a GUI for manual play and a test mode for benchmarking solver performance.

---

## 📊 Performance Summary

- **Accuracy**: 93.1% (solved 93 out of 100 words)
- **Average Guesses**: 4.52
- **Max Guesses**: 6 (hard mode fail condition)

---

## 🗂️ Project Structure

WordleSolver/ <br>
├── data/<br>
│ └── oldList.csv # Word list (5-letter words)
<br>│
<br>├── src/
<br>│ ├── main.py # Tkinter GUI for interactive solving
<br>│ ├── solver_test.py # Benchmark script for automated testing
<br>│ ├── wordle_solver.py # Interface between GUI and solver logic
<br>│ └── wordle_solver_logic.py # Core filtering & ranking logic
<br>│
<br>└── README.md


---

## 🚀 Features

- ✅ **Hard Mode**: Guesses must follow green/yellow feedback from previous guesses
- 🔢 **Positional Frequency Scoring**: Ranks words based on how common letters are in each position
- 🧠 **Smart Filtering**: Excludes invalid words based on color feedback
- 🧪 **Benchmarking Script**: Automatically tests solver accuracy and efficiency
- 🖥️ **Interactive GUI**: Play Wordle manually with suggestions and feedback buttons

---

## 🧪 Running Tests

To test solver performance on 100 random words:

```bash
cd src
python solver_test.py
```
You’ll get output like:
```
Solved words 93/100
Average guesses: 4.52
```

## 🖱️ Using the GUI
To launch the interactive solver:

```bash
cd src
python main.py
```
### GUI Controls
Set Word: Enter a custom guess

Click Letters: Toggle colors (Gray → Yellow → Green)

Update: Apply feedback and get a new suggestion

Reset: Start over with a fresh word

## 📦 Requirements
Python 3.7+

No external libraries needed — uses only Python standard library:

tkinter

dataclasses

collections

## 🔧 Future Improvements
🧠 Improve repeated-letter handling (especially yellow logic)

📈 Export detailed test reports

📊 Track per-word performance stats

