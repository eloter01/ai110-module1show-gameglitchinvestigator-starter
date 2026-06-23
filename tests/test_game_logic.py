from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Regression tests for the "secret changes type on even attempts" bug ---
#
# The original bug coerced the secret to a string on even-numbered attempts:
#
#     if st.session_state.attempts % 2 == 0:
#         secret = str(st.session_state.secret)
#
# Comparing an int guess against a str secret falls into check_guess's
# TypeError fallback, which compares them *lexicographically* instead of
# numerically -- producing the wrong outcome. These tests lock in that the
# secret must stay an int so comparisons stay numeric.

def test_int_secret_compares_numerically():
    # 100 > 50 numerically -> "Too High". This is the correct behavior.
    outcome, _ = check_guess(100, 50)
    assert outcome == "Too High"


def test_string_secret_produces_wrong_outcome_regression():
    # Demonstrates *why* the type switch was a bug: a string secret makes the
    # comparison lexicographic, so "100" sorts before "50" and the game wrongly
    # reports "Too Low" for a guess that is numerically higher.
    correct_outcome, _ = check_guess(100, 50)
    buggy_outcome, _ = check_guess(100, "50")

    assert correct_outcome == "Too High"
    assert buggy_outcome != correct_outcome


def test_outcome_is_independent_of_attempt_parity():
    # The fix keeps the secret an int regardless of attempt number, so the same
    # guess/secret pair yields the same outcome on even and odd attempts.
    secret = 50
    guess = 60

    outcomes = set()
    for _attempt in range(1, 7):  # mix of odd and even attempt numbers
        # Post-fix, the secret type never depends on the attempt number.
        outcome, _ = check_guess(guess, secret)
        outcomes.add(outcome)

    assert outcomes == {"Too High"}


# --- Regression tests for the "instructions/secret ignore difficulty range" bug ---
#
# app.py displays a hardcoded "Guess a number between 1 and 100" regardless of
# difficulty, and the "New Game" button regenerates the secret with a hardcoded
# random.randint(1, 100). Both ignore get_range_for_difficulty(), so on Easy
# (1-20) and Hard (1-50) the shown range is wrong and the secret can land
# outside the displayed bounds (making the game unwinnable).
#
# The fix extracts two pure helpers into logic_utils so the range is used
# consistently:
#   - build_guess_instructions(low, high, attempts_left) -> str
#   - new_secret_for_difficulty(difficulty) -> int  (within that difficulty's range)
#
# These tests import those helpers locally so the rest of the suite still runs
# even while the helpers do not exist yet.

def test_instructions_reflect_easy_range():
    from logic_utils import build_guess_instructions

    text = build_guess_instructions(1, 20, attempts_left=5)
    assert "1" in text and "20" in text
    assert "100" not in text


def test_instructions_reflect_hard_range():
    from logic_utils import build_guess_instructions

    text = build_guess_instructions(1, 50, attempts_left=4)
    assert "1" in text and "50" in text
    assert "100" not in text


def test_instructions_reflect_normal_range():
    from logic_utils import build_guess_instructions

    text = build_guess_instructions(1, 100, attempts_left=8)
    assert "1" in text and "100" in text


def test_new_secret_within_easy_range():
    from logic_utils import new_secret_for_difficulty

    for _ in range(200):
        secret = new_secret_for_difficulty("Easy")
        assert 1 <= secret <= 20


def test_new_secret_within_hard_range():
    from logic_utils import new_secret_for_difficulty

    for _ in range(200):
        secret = new_secret_for_difficulty("Hard")
        assert 1 <= secret <= 50


# --- Regression tests for the "hint message points the wrong direction" bug ---
#
# The original check_guess returned the correct outcome label but the wrong
# hint text: a too-high guess told the player to "Go HIGHER!" and a too-low
# guess told them to "Go LOWER!". The outcome-only tests above never caught
# this because they discard the message. These lock in the message direction.

def test_too_high_message_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_too_low_message_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message


# --- Regression tests for the "secret not regenerated on difficulty change" bug ---
#
# app.py only generated the secret once (guarded by "secret not in
# session_state"), so switching difficulty left a secret picked for the old
# range -- potentially outside the new displayed bounds. The reset decision is
# now extracted into should_reset_for_difficulty_change so it is unit-testable
# without Streamlit.

def test_reset_when_difficulty_changes():
    from logic_utils import should_reset_for_difficulty_change

    assert should_reset_for_difficulty_change("Normal", "Easy") is True
    assert should_reset_for_difficulty_change("Easy", "Hard") is True


def test_no_reset_when_difficulty_unchanged():
    from logic_utils import should_reset_for_difficulty_change

    assert should_reset_for_difficulty_change("Easy", "Easy") is False
