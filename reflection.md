# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game, it looked like a decent Streamlit number guessing app with a sidebar for difficulty, a text input for guesses, and a debug panel. But after a couple rounds of playing, it was clear that pretty much everything under the surface was broken. I couldn't win even when I followed the hints, and the scoring made no sense.

**Bug 1, The hints are backwards:** When I guessed a number higher than the secret, the game told me to "Go HIGHER!" and when I guessed lower, it said "Go LOWER!" The hint messages in `check_guess()` are swapped, so the `"Too High"` outcome is paired with the "Go HIGHER" emoji message and the other way around. This makes the game basically unwinnable if you trust the hints because they push you in the wrong direction every single time.

**Bug 2, The secret turns into a string on even attempts:** Using the Developer Debug Info panel, I noticed my correct guesses weren't being recognized as wins. Looking at the code, I found that on every even numbered attempt, `app.py` converts the secret number to a string before passing it to `check_guess()`. This means the comparison becomes `int` vs `str`, which triggers a `TypeError` fallback that does string comparison, where `"9"` is considered greater than `"50"`. So the game's logic is completely unreliable on half of all attempts.

**Bug 3, Hard mode is actually easier than Normal:** The `get_range_for_difficulty()` function sets Hard mode's range to 1 to 50, while Normal is 1 to 100. That means Hard mode gives you a smaller range to guess from, which is actually easier. Hard should have a wider range like 1 to 200 so it's actually more challenging.

**Bug 4, The info bar always says "1 to 100":** No matter which difficulty you pick, the prompt always reads "Guess a number between 1 and 100" because the `low` and `high` values aren't actually used in the `st.info()` message. This is especially confusing on Easy mode where the real range is only 1 to 20.

**Bug 5, Attempts counter is inconsistent:** The attempts counter starts at `1` instead of `0`, so you effectively lose one attempt before you even play. Then when you click "New Game," it resets to `0`, which is inconsistent with that initial value of `1`. The "Attempts left" display is off by one right from the start.

---

## 2. How did you use AI as a teammate?

I used VS Code Copilot throughout this project, mainly through Chat with `#file` context variables and Agent mode for the bigger refactors.

**A correct suggestion:** When I asked Copilot about the swapped hints in `check_guess()`, I gave it context with `#file:app.py` and described that guessing higher than the secret was returning "Go HIGHER!" It immediately identified that the messages were paired with the wrong outcomes and suggested swapping them. I verified this by running the game and guessing a number I knew was above the secret (using the debug panel), and the hint now correctly said "Go LOWER!"

**An incorrect suggestion:** When I asked Copilot to fix the Hard mode range, it suggested changing it to `(1, 500)`. While technically that would make it harder, a range of 1 to 500 with only 5 attempts felt nearly impossible to win. I rejected that and went with `(1, 200)` instead, which felt challenging but still fair. I tested it by playing a few rounds on Hard and confirming that winning was difficult but doable with smart guessing.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by checking two things: first that the pytest tests passed, and then that the actual game behaved correctly when I played it in the browser. Tests alone weren't enough because some bugs only showed up in the Streamlit UI, like the hardcoded "1 to 100" message.

One specific test I wrote was `test_too_high_hint_says_go_lower()`, which calls `check_guess(60, 50)` and asserts that "LOWER" appears in the returned message. Before the fix this test would have failed because the message contained "HIGHER" instead. After fixing the swap, this test passed along with all 15 others when I ran `pytest`.

Copilot helped me write several of the test functions. I'd describe what I wanted to verify (like "test that Hard mode has a bigger range than Normal") and it would generate the assertion. Most of what it generated was usable right away, though I did have to fix the original starter tests myself since they expected `check_guess` to return a plain string when it actually returns a tuple.

---

## 4. What did you learn about Streamlit and state?

Streamlit works by rerunning your entire Python script from top to bottom every time the user interacts with anything on the page, like clicking a button or typing in an input. That means any regular variable you set at the top of the script gets reset to its initial value on every interaction. To keep data between reruns, you have to store it in `st.session_state`, which is like a persistent dictionary that survives reruns. So if you want your secret number to stay the same between guesses, you check if it already exists in session state before creating it. That was actually the root cause of several bugs in this project, the original code initialized attempts to 1 and then the rest of the logic assumed it started at 0.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is starting new Copilot Chat sessions for each separate bug. When I tried to discuss multiple issues in one chat, the suggestions got muddled and referenced the wrong parts of the code. Keeping each session focused on one problem gave me much cleaner and more accurate help.

Next time I work with AI on a coding task, I'd spend more time reading through the generated code before running it. On this project I ran the buggy app first and then went hunting for problems, but looking back, a quick read of `check_guess()` would have revealed the swapped hints immediately without even needing to play the game.

This project changed how I think about AI generated code because it showed me that AI can produce something that looks completely reasonable at a glance but is subtly broken in ways that only show up when you actually test it. The string conversion on even attempts is a perfect example. Nobody would write that on purpose, but an AI produced it and it looked like real code. I'm going to be a lot more skeptical going forward and always verify behavior rather than trusting that "it looks right."