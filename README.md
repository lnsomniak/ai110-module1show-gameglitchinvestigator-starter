# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit. It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.**
   - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

The game is a Streamlit number guessing app where you pick a difficulty, guess a secret number, and get hints telling you to go higher or lower. The AI that built it left behind a mess of bugs that made the game essentially unwinnable.

Here are the main bugs I found and fixed:

**Backwards hints.** The biggest issue was that `check_guess()` had the hint messages swapped. Guessing too high would tell you "Go HIGHER!" which sent you further from the answer. I corrected the messages so "Too High" pairs with "Go LOWER!" and vice versa.

**String conversion on even attempts.** On every even numbered attempt, the code converted the secret number to a string before comparing it to your guess. This caused integer vs string comparisons where Python's string ordering made results completely unreliable. For example, `"9"` would be considered greater than `"50"`. I removed that conversion entirely so the secret is always compared as an integer.

**Hard mode was easier than Normal.** The difficulty ranges were wrong. Hard returned a range of 1 to 50 while Normal was 1 to 100, making Hard actually easier. I changed Hard to 1 to 200.

**Hardcoded range in the UI.** The info bar always said "Guess a number between 1 and 100" regardless of difficulty. I updated it to display the actual range for whatever difficulty is selected.

**Off by one in the attempts counter.** Attempts initialized at 1 instead of 0, costing you a turn before you even played. New Game also reset to 0 while init was 1, which was inconsistent. Fixed both to start at 0.

**Scoring inconsistencies.** The win formula had an extra `+1` that over penalized you, and "Too High" guesses alternated between giving and taking points depending on attempt parity. Cleaned up both so scoring is fair and predictable.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]