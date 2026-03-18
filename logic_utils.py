def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Was (1, 50) which made Hard easier than Normal. Copilot suggested 1-500
    # but that felt too extreme, went with 1-200 as a middle ground.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns:
        (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    # FIX: Hint messages were swapped. "Too High" was saying "Go HIGHER!" which
    # sent players the wrong way. Also removed the TypeError string fallback since
    # we now always pass ints in from app.py.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: Was 100 - 10 * (attempt_number + 1), the +1 penalized you an extra
        # 10 points for no reason. Copilot caught this one right away.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points
    # FIX: "Too High" used to alternate between +5 and -5 depending on even/odd
    # attempts which made scoring feel random. Made both outcomes a flat -5.
    if outcome == "Too High":
        return current_score - 5
    if outcome == "Too Low":
        return current_score - 5
    return current_score
