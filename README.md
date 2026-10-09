# Smart-Study-Planner
# Smart Study Planner

A Streamlit web app that turns a student's exam dates into a day-by-day revision timetable, with reminders and a progress checklist.

Built for a college hackathon with plain Python.

## The problem

Students know their exam dates but not how to split their time. They spend too long on easy subjects, start hard ones late, and lose track of what they have finished.

## What it does

- Takes subjects, exam dates, a difficulty level (Easy, Medium, Hard) and study hours per day
- Builds a day-by-day timetable from today until the last exam
- Gives harder subjects and nearer exams more time
- Shows reminders: today's sessions, and a warning when an exam is 3 days away or less
- Tracks progress with a tick box for each session and a progress bar

## How it works (the algorithm)

Each day is split into half-hour blocks. For every block, the planner scores each subject whose exam is still ahead, and the highest score wins the block.

```
score = difficulty x (1 + 4 / days_left) / (1 + blocks_given)
```

| Part | Meaning | Effect |
|---|---|---|
| `difficulty` | Easy = 1, Medium = 2, Hard = 3 | Harder subjects score higher |
| `1 + 4 / days_left` | Urgency | Nearer exams score higher |
| `1 + blocks_given` | Blocks already given that day | Time is shared; no subject takes the whole day |

### Steps

```
for each day from today until the last exam:
    active = subjects whose exam is after this day
    for each half-hour block in the day:
        give the block to the subject in `active` with the highest score
        increase that subject's blocks_given by 1
    merge each subject's blocks into one session (for example "Maths 2h")
    mark the day as an exam day if a subject's exam falls on it
```

Once an exam day arrives, that subject drops out of the plan and its hours go to the other subjects.

### Worked example

Maths (Hard, 6 days left), Physics (Medium, 9 days left), English (Easy, 12 days left), 3 hours per day (6 blocks):

| Block | Maths | Physics | English | Winner |
|---|---|---|---|---|
| 1 | 5.00 | 2.89 | 1.33 | Maths |
| 2 | 2.50 | 2.89 | 1.33 | Physics |
| 3 | 2.50 | 1.44 | 1.33 | Maths |
| 4 | 1.67 | 1.44 | 1.33 | Maths |
| 5 | 1.25 | 1.44 | 1.33 | Physics |
| 6 | 1.25 | 0.96 | 1.33 | English |

Result for the day: Maths 1.5h, Physics 1h, English 0.5h.

The `4` in the urgency term is a tuning value. A bigger number pushes harder toward near exams. A smaller number spreads time more evenly.

## Tech stack

| Tool | Used for |
|---|---|
| Python 3 | All the logic: loops, functions, dictionaries |
| `datetime` | Exam dates, days left, looping day by day |
| Streamlit | The web interface |
| pandas | The editable subjects table |

## Project structure

```
.
├── app.py             # Streamlit interface
├── planner.py         # Scheduling and reminder logic (no interface code)
├── test_planner.py    # 14 edge-case tests for the logic
└── README.md
```

Keeping the logic in `planner.py` means it can be tested without the interface.

## How to run

1. Install Python 3.9 or newer.
2. Install the libraries:
   ```
   pip install streamlit pandas
   ```
3. Open a terminal in the project folder and start the app:
   ```
   streamlit run app.py
   ```
   If `streamlit` is not recognized, use `python -m streamlit run app.py`.
4. Open `http://localhost:8501` if the browser does not open by itself.

Streamlit may ask for an email on first run. Press Enter to skip it.

## Run the tests

```
python test_planner.py
```

Expected output ends with `14/14 passed`. The tests cover past and same-day exam dates, blank rows, duplicate subject names, one-day and 400-day plans, and daily hours never going over the limit.

## Limitations

- Ticked sessions are kept only while the browser tab is open.
- Reminders show when the app is opened. They are not push notifications.
- The scoring rule is fixed and does not learn how fast each student studies.

## Future scope

- Save progress to a file or database
- Re-plan automatically when a day is missed
- Weekly rest days and fixed busy slots
- Email or phone notifications
- Learn study speed per subject from past sessions (machine learning)

## Team

- [Member 1]
- [Member 2]
- [Member 3]
- [Member 4]

