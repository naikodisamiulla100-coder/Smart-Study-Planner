"""Smart Study Planner - core logic (plain Python, no Streamlit needed)."""
from datetime import date, timedelta

DIFFICULTY = {"Easy": 1, "Medium": 2, "Hard": 3}

def build_plan(subjects, hours_per_day, start=None):
    """subjects: list of dicts {name, exam (date), level (1-3)}.
    Returns a list of days: {date, exams: [names], sessions: [(subject, hours)]}."""
    start = start or date.today()
    subs = [dict(s, got=0) for s in subjects if s["name"].strip() and s["exam"] > start]
    if not subs:
        return []
    last_exam = max(s["exam"] for s in subs)
    blocks_per_day = round(hours_per_day * 2)          # half-hour blocks
    plan, day = [], start
    while day < last_exam:                              # loop over every study day
        active = [s for s in subs if s["exam"] > day]
        counts = {}
        for _ in range(blocks_per_day):                 # hand out each block
            if not active:
                break
            def score(s):
                days_left = (s["exam"] - day).days
                return s["level"] * (1 + 4 / days_left) / (1 + s["got"])
            best = max(active, key=score)
            best["got"] += 1
            counts[best["name"]] = counts.get(best["name"], 0) + 0.5
        exams = [s["name"] for s in subs if s["exam"] == day]
        plan.append({"date": day, "exams": exams,
                     "sessions": sorted(counts.items(),
                         key=lambda kv: next(s["exam"] for s in subs if s["name"] == kv[0]))})
        day += timedelta(days=1)
    return plan

def reminders(subjects, plan, today=None):
    """Messages for today: what to study and which exams are close."""
    today = today or date.today()
    msgs = []
    for d in plan:
        if d["date"] == today and d["sessions"]:
            msgs.append("Today: " + ", ".join(f"{n} {h}h" for n, h in d["sessions"]))
    for s in subjects:
        left = (s["exam"] - today).days
        if 0 < left <= 3:
            msgs.append(f"{s['name']} exam in {left} day{'s' if left > 1 else ''}. Final revision time.")
    return msgs
