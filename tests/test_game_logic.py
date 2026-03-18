from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_hint_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message


def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_range_is_harder_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_win_on_first_attempt_gives_90():
    score = update_score(0, "Win", 1)
    assert score == 90


def test_too_high_always_deducts():
    score = update_score(50, "Too High", 1)
    assert score == 45
    score2 = update_score(50, "Too High", 2)
    assert score2 == 45


def test_too_low_deducts():
    score = update_score(50, "Too Low", 1)
    assert score == 45


def test_parse_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."


def test_parse_valid_int():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None


def test_parse_non_number():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."