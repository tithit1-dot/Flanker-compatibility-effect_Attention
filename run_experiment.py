

# Caught in the Flank: The Flanker Compatibility Effect
# PSY412 Attention — Solo Project
# Tithi Thakker | AU24L20003
#
# PsychoPy Coder version
#
# Experimental design:
#   IV: Flanker compatibility (Congruent vs Incongruent)
#   DV: Reaction time (ms) and accuracy
#   Within-subjects
#   120 experimental trials: 60 congruent + 60 incongruent
#   8 practice trials
#
# Response mapping:
#   H -> F key
#   S -> J key
#
# Trial timing:
#   Fixation: 500 ms
#   Stimulus: remains until response
#   ITI: 500 ms
#
# Data are saved as a CSV file in the data/ folder.

from psychopy import visual, core, event, gui
import csv
import random
from pathlib import Path
from datetime import datetime


# -----------------------------
# SETTINGS
# -----------------------------

N_EXPERIMENTAL_TRIALS = 120
N_PRACTICE_TRIALS = 8
FIXATION_DURATION = 0.5
ITI_DURATION = 0.5

KEY_H = "f"
KEY_S = "j"
RESPONSE_KEYS = [KEY_H, KEY_S]

BG_COLOR = "black"
TEXT_COLOR = "white"

# Slight, consistent spacing between letters.
# The same spacing is used for every letter and condition.
LETTER_ADVANCE = 0.075
LETTER_HEIGHT = 0.12


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def make_display(condition, target):
    """Return the five-letter stimulus for a condition and target."""
    if condition == "congruent":
        return target * 5

    # Incongruent: flankers require the opposite response.
    opposite = "S" if target == "H" else "H"
    return opposite + opposite + target + opposite + opposite


def make_trials(n_trials):
    """Create a balanced, randomized set of experimental trials."""
    if n_trials % 4 != 0:
        raise ValueError("N_EXPERIMENTAL_TRIALS must be divisible by 4.")

    per_cell = n_trials // 4
    trials = []

    for condition in ["congruent", "incongruent"]:
        for target in ["H", "S"]:
            for _ in range(per_cell):
                trials.append({
                    "condition": condition,
                    "target": target,
                    "stimulus": make_display(condition, target),
                    "correct_key": KEY_H if target == "H" else KEY_S
                })

    random.shuffle(trials)
    return trials


def make_practice_trials():
    """Create 8 balanced practice trials."""
    trials = []
    for condition in ["congruent", "incongruent"]:
        for target in ["H", "S"]:
            for _ in range(2):
                trials.append({
                    "condition": condition,
                    "target": target,
                    "stimulus": make_display(condition, target),
                    "correct_key": KEY_H if target == "H" else KEY_S
                })
    random.shuffle(trials)
    return trials


def draw_centered_word(win, text_stim):
    """Draw a centered five-letter flanker display with slight, even spacing."""
    letters = list(text_stim)
    positions = [-2, -1, 0, 1, 2]

    for letter, position in zip(letters, positions):
        stim = visual.TextStim(
            win,
            text=letter,
            color=TEXT_COLOR,
            height=LETTER_HEIGHT,
            pos=(position * LETTER_ADVANCE, 0),
            units="height",
            bold=False,
            alignText="center"
        )
        stim.draw()


def show_message(win, text, wait_keys=None):
    """Show a centered instruction/message screen."""
    msg = visual.TextStim(
        win,
        text=text,
        color=TEXT_COLOR,
        height=0.045,
        wrapWidth=1.2,
        units="height"
    )
    msg.draw()
    win.flip()

    if wait_keys is None:
        event.waitKeys()
    else:
        event.waitKeys(keyList=wait_keys)


def run_trial(win, trial, trial_number, phase, data_rows):
    """Run one fixation -> stimulus -> response -> ITI trial."""

    # Check for quit before each trial.
    if "escape" in event.getKeys():
        raise KeyboardInterrupt

    # Clear any old keyboard events.
    event.clearEvents(eventType="keyboard")

    # Fixation cross: 500 ms.
    fixation = visual.TextStim(
        win,
        text="+",
        color=TEXT_COLOR,
        height=0.06,
        units="height"
    )
    fixation.draw()
    win.flip()
    core.wait(FIXATION_DURATION)

    # Prepare stimulus.
    event.clearEvents(eventType="keyboard")
    draw_centered_word(win, trial["stimulus"])

    # Start RT clock at stimulus onset.
    rt_clock = core.Clock()
    win.callOnFlip(rt_clock.reset)
    win.flip()

    # Wait until participant responds.
    response = event.waitKeys(
        keyList=RESPONSE_KEYS + ["escape"],
        timeStamped=rt_clock
    )

    if response is None:
        return

    key, rt = response[0]

    if key == "escape":
        raise KeyboardInterrupt

    accuracy = int(key == trial["correct_key"])

    data_rows.append({
        "participant_id": PARTICIPANT_ID,
        "date_time": datetime.now().isoformat(timespec="seconds"),
        "phase": phase,
        "trial": trial_number,
        "condition": trial["condition"],
        "target": trial["target"],
        "stimulus": trial["stimulus"],
        "correct_key": trial["correct_key"],
        "response": key,
        "accuracy": accuracy,
        "rt_seconds": round(rt, 6),
        "rt_ms": round(rt * 1000, 3)
    })

    # Inter-trial interval: 500 ms.
    win.flip()
    core.wait(ITI_DURATION)


# -----------------------------
# PARTICIPANT INFORMATION
# -----------------------------

participant_info = {
    "Participant ID": "",
}

dialog = gui.DlgFromDict(
    participant_info,
    title="Caught in the Flank — Participant Information"
)

if not dialog.OK:
    core.quit()

PARTICIPANT_ID = participant_info["Participant ID"].strip()

if not PARTICIPANT_ID:
    PARTICIPANT_ID = "P_UNKNOWN"


# -----------------------------
# OUTPUT SETUP
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = DATA_DIR / f"{PARTICIPANT_ID}_{timestamp}.csv"


# -----------------------------
# WINDOW
# -----------------------------

win = visual.Window(
    size=(1000, 700),
    fullscr=False,
    color=BG_COLOR,
    units="height"
)

# Hide mouse during the experiment.
mouse = event.Mouse(visible=False, win=win)

data_rows = []


# -----------------------------
# INSTRUCTIONS
# -----------------------------

instructions = (
    "WELCOME\n\n"
    "In this task, you will see five letters on the screen.\n\n"
    "Your task is to identify the CENTRAL letter only.\n"
    "Ignore the two letters on either side of it.\n\n"
    "If the central letter is H, press F.\n"
    "If the central letter is S, press J.\n\n"
    "Please respond as quickly and accurately as you can.\n\n"
    "Press SPACE to begin the practice trials."
)

show_message(win, instructions, wait_keys=["space"])


# -----------------------------
# PRACTICE
# -----------------------------

practice_trials = make_practice_trials()

for i, trial in enumerate(practice_trials, start=1):
    run_trial(
        win=win,
        trial=trial,
        trial_number=i,
        phase="practice",
        data_rows=data_rows
    )

show_message(
    win,
    "Practice complete.\n\n"
    "The experimental trials will now begin.\n\n"
    "Remember: identify the CENTRAL letter and ignore the flankers.\n\n"
    "Press SPACE to begin.",
    wait_keys=["space"]
)


# -----------------------------
# EXPERIMENTAL TRIALS
# -----------------------------

experimental_trials = make_trials(N_EXPERIMENTAL_TRIALS)

for i, trial in enumerate(experimental_trials, start=1):
    run_trial(
        win=win,
        trial=trial,
        trial_number=i,
        phase="experimental",
        data_rows=data_rows
    )


# -----------------------------
# SAVE DATA
# -----------------------------

fieldnames = [
    "participant_id",
    "date_time",
    "phase",
    "trial",
    "condition",
    "target",
    "stimulus",
    "correct_key",
    "response",
    "accuracy",
    "rt_seconds",
    "rt_ms"
]

with output_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_rows)


# -----------------------------
# END SCREEN
# -----------------------------

show_message(
    win,
    "The experiment is complete.\n\n"
    "Thank you for participating!\n\n"
    "The experimenter will now save your data.",
    wait_keys=["space"]
)

win.close()
core.quit()
