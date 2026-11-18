# Caught in the Flank — Final PsychoPy Experiment

**Course:** PSY412: Attention  
**Project:** Solo Project — Flanker Compatibility Effect

## Design

- Within-subjects design
- Independent variable: flanker compatibility (congruent vs. incongruent)
- Dependent variables: reaction time and accuracy
- Target letters: H and S
- Response mapping: H → F; S → J
- 120 experimental trials: 60 congruent and 60 incongruent
- Each of the four condition × target combinations appears 30 times
- 8 practice trials (not counted among the 120 experimental trials)
- Fixation cross: 500 ms
- Stimulus remains on screen until a response
- Inter-trial interval: 500 ms
- Slight, consistent letter spacing across all stimuli and conditions
- Experimental trials randomized

## Stimuli

| Condition | Central target | Display | Correct key |
|---|---|---|---|
| Congruent | H | `HHHHH` | F |
| Congruent | S | `SSSSS` | J |
| Incongruent | H | `SSHSS` | F |
| Incongruent | S | `HHSHH` | J |

## Run the experiment

1. Install and open PsychoPy.
2. Open `run_experiment.py` in PsychoPy's **Coder** view.
3. Click **Run**.
4. Enter a participant ID in the dialog.
5. Read the instructions and press Space to start practice.
6. Complete the 8 practice trials, then press Space to start the experiment.
7. Complete all 120 experimental trials.
8. Press Space on the completion screen to close the task.
9. Find the participant CSV in the `data/` folder beside `run_experiment.py`.

Press **Escape** during a trial to stop the task. If interrupted before completion, the current version may not save a CSV; complete the task for a full data file.

## Output data

The CSV contains participant ID, timestamp, phase, trial number, condition, target, stimulus, correct key, response, accuracy, reaction time in seconds, and reaction time in milliseconds. Practice trials are included in the CSV and labelled `practice`; the 120 main trials are labelled `experimental`.

## Verification status

The Python syntax check passed. An automated **simulated smoke test** also completed the task flow using a mock PsychoPy interface and confirmed that a CSV was generated with 8 practice rows and 120 experimental rows, balanced as 30 trials in each condition × target cell. This checks the program flow and data-writing logic, but it does **not** verify actual screen rendering, physical letter spacing, or real keyboard/timing behaviour. PsychoPy is not installed in the build environment, so a final graphical run must still be completed on a computer with PsychoPy before submission.

## Before submitting

Run the experiment yourself from beginning to end and confirm:

- Instructions appear and fit on screen.
- Letters display with the desired slight spacing.
- Congruent and incongruent stimuli both appear.
- F and J responses are accepted and correctly scored.
- The full task reaches the completion screen without crashing.
- A CSV appears in the `data/` folder and contains 120 experimental trials.
- Another person can run the experiment using this folder and these instructions.

This experiment is a simplified replication of the flanker-compatibility manipulation in the proposal; it is not a full reproduction of every condition in Eriksen and Eriksen (1974).
