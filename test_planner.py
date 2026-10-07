"""Edge-case tests. Run:  python test_planner.py"""
from datetime import date, timedelta
from planner import build_plan, reminders

T = date(2026, 10, 7)
def sub(name, days, level=2): return {"name": name, "exam": T + timedelta(days), "level": level}
def hours(plan): return sum(h for d in plan for _, h in d["sessions"])
results = []
def check(name, cond): results.append((name, cond)); print(("PASS " if cond else "FAIL ") + name)

check("no subjects -> empty plan", build_plan([], 3, T) == [])
check("past exam ignored", build_plan([sub("A", -2)], 3, T) == [])
check("exam today ignored", build_plan([sub("A", 0)], 3, T) == [])
check("blank name ignored", build_plan([sub("  ", 5)], 3, T) == [])
p = build_plan([sub("A", 1)], 3, T)
check("exam tomorrow -> 1 day, 3h", len(p) == 1 and hours(p) == 3)
p = build_plan([sub("A", 10)], 0.5, T)
check("0.5h/day -> half hour each day", all(h == 0.5 for d in p for _, h in d["sessions"]) and len(p) == 10)
p = build_plan([sub("A", 6, 3), sub("B", 9, 2), sub("C", 12, 1)], 3, T)
check("daily hours never exceed limit", all(sum(h for _, h in d["sessions"]) <= 3 for d in p))
check("no study on/after a subject's exam day", all(not (n == "A" and d["date"] >= T + timedelta(6)) for d in p for n, _ in d["sessions"]))
check("exam day flagged", any(d["exams"] == ["A"] for d in p))
a = sum(h for d in p for n, h in d["sessions"] if n == "A"); c = sum(h for d in p for n, h in d["sessions"] if n == "C")
check("hard+near exam gets more than easy+far", a > c)
p = build_plan([sub("Same", 5), sub("Same", 8)], 3, T)
check("duplicate names stay separate entries", any(len(d["sessions"]) == 2 and d["sessions"][0][0] == d["sessions"][1][0] for d in p))
p = build_plan([sub("A", 400)], 3, T)
check("very far exam does not crash", len(p) == 400)
check("reminder: exam in 2 days", any("2 days" in m for m in reminders([sub("A", 2)], build_plan([sub("A", 2)], 3, T), T)))
check("reminder: none when exams far", not any("exam in" in m for m in reminders([sub("A", 20)], build_plan([sub("A", 20)], 3, T), T)))
print(f"\n{sum(ok for _, ok in results)}/{len(results)} passed")
