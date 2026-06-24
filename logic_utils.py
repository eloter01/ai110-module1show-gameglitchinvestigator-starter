import random


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a given difficulty level.

    Maps a human-readable difficulty label to the numeric bounds that the
    secret number and player guesses are constrained to. Used by the UI to
    display the active range and by ``new_secret_for_difficulty`` to seed a
    secret within that range.

    Args:
        difficulty: The difficulty label. Recognized values are ``"Easy"``,
            ``"Normal"``, and ``"Hard"``. Any unrecognized value falls back
            to the ``"Normal"`` range.

    Returns:
        tuple[int, int]: A ``(low, high)`` pair of inclusive bounds:

            * ``"Easy"`` -> ``(1, 20)``
            * ``"Normal"`` -> ``(1, 100)``
            * ``"Hard"`` -> ``(1, 50)``
            * anything else -> ``(1, 100)``
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def build_guess_instructions(low: int, high: int, attempts_left: int) -> str:
    """Build the player-facing prompt describing the range and attempts left.

    Produces the single-line instruction string shown above the guess input,
    keeping the displayed range and remaining-attempts count in sync with the
    current game state.

    Args:
        low: The lowest valid guess (inclusive) for the active difficulty.
        high: The highest valid guess (inclusive) for the active difficulty.
        attempts_left: The number of guesses the player has remaining. The
            caller is responsible for computing this (e.g.
            ``attempt_limit - attempts_used``); it is rendered verbatim.

    Returns:
        str: A formatted instruction such as
        ``"Guess a number between 1 and 100. Attempts left: 7"``.
    """
    return (
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left}"
    )


def new_secret_for_difficulty(difficulty: str) -> int:
    """Generate a fresh secret number for the given difficulty.

    Resolves the difficulty to its inclusive range via
    ``get_range_for_difficulty`` and draws a uniformly random integer within
    that range. Called when starting a new game or when the player switches
    difficulty mid-game and the secret must be regenerated for the new range.

    Args:
        difficulty: The difficulty label (see ``get_range_for_difficulty``
            for accepted values and fallback behavior).

    Returns:
        int: A random integer in ``[low, high]`` for the resolved range, with
        both bounds inclusive.

    Note:
        Uses ``random.randint`` and is therefore not seeded for
        reproducibility; each call may return a different value.
    """
    low, high = get_range_for_difficulty(difficulty)
    return random.randint(low, high)


# FIX: Extracted the difficulty-reset decision into a pure helper so it is
# unit-testable without Streamlit.
def should_reset_for_difficulty_change(
    active_difficulty: str, selected_difficulty: str
) -> bool:
    """Decide whether a difficulty change requires resetting the game.

    Pure, Streamlit-free predicate extracted so the reset decision can be unit
    tested in isolation. A difference between the active and newly selected
    difficulty means the in-progress secret was drawn from a different range
    and is no longer valid, so the caller should regenerate the secret and
    reset attempts, status, and history.

    Args:
        active_difficulty: The difficulty the current secret was generated for.
        selected_difficulty: The difficulty currently chosen in the UI.

    Returns:
        bool: ``True`` if the difficulties differ and the game state must be
        reset; ``False`` if they match and play can continue unchanged.
    """
    return active_difficulty != selected_difficulty


def parse_guess(raw: str | None):
    """Parse and validate raw text input into an integer guess.

    Converts the free-text value from the guess input box into an integer,
    tolerating numeric strings that include a decimal point (e.g. ``"42.0"``)
    by truncating toward zero via ``float`` then ``int``. Empty or missing
    input and non-numeric text are rejected with a user-facing error message
    rather than raising.

    Args:
        raw: The raw string from the text input, or ``None`` if unset.

    Returns:
        tuple[bool, int | None, str | None]: A ``(ok, guess, error)`` triple:

            * On success: ``(True, <int>, None)``.
            * On failure: ``(False, None, <error message>)``, where the
              message is ``"Enter a guess."`` for empty/missing input or
              ``"That is not a number."`` for unparseable text.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.9")
        (True, 3, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret) -> tuple[str, str]:
    """Compare a guess against the secret and classify the result.

    Determines whether the guess matches the secret or is too high/too low,
    returning both a machine-readable outcome (consumed by ``update_score``
    and the UI status logic) and a player-facing hint message. The hint for a
    too-high guess directs the player LOWER and vice versa.

    A ``TypeError`` fallback handles mismatched operand types (e.g. comparing
    a string against an int) by retrying the comparison on string forms, so
    the function never raises on type mismatches.

    Args:
        guess: The player's guess, normally an ``int`` from ``parse_guess``.
        secret: The secret value to compare against, normally an ``int``.

    Returns:
        tuple[str, str]: An ``(outcome, message)`` pair where ``outcome`` is
        one of ``"Win"``, ``"Too High"``, or ``"Too Low"``, and ``message``
        is the corresponding emoji hint (e.g. ``"📉 Go LOWER!"``).
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIX: Swapped hint messages so a too-high guess says "Go LOWER!" and a
        # too-low guess says "Go HIGHER!" (they were reversed).
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        # FIX: same message swap applied to the TypeError fallback branch.
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the new score after a guess, based on its outcome.

    Applies the game's scoring rules to the running score:

        * ``"Win"``: awards ``100 - 10 * (attempt_number + 1)`` points,
          floored at a minimum of ``10``, so faster wins score higher.
        * ``"Too High"``: adds ``5`` on even ``attempt_number`` values and
          subtracts ``5`` on odd ones.
        * ``"Too Low"``: always subtracts ``5``.
        * Any other outcome: leaves the score unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The outcome from ``check_guess`` (``"Win"``, ``"Too High"``,
            or ``"Too Low"``).
        attempt_number: The 1-based attempt count for this guess, used to
            scale the win bonus and to determine the too-high parity.

    Returns:
        int: The updated score after applying the rule for ``outcome``.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
