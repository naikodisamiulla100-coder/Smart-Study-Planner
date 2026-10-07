"""Smart Study Planner - Streamlit app. Run:  streamlit run app.py"""
from datetime import date, timedelta
import pandas as pd
import streamlit as st
from planner import build_plan, reminders, DIFFICULTY

st.set_page_config(page_title="Smart Study Planner", layout="wide")
st.title("Smart Study Planner")
st.caption("Enter subjects, exam dates and daily hours. Get a day-by-day revision timetable with a checklist.")

today = date.today()
with st.sidebar:
    st.header("Your exams")
    hours = st.number_input("Study hours per day", 0.5, 14.0, 3.0, 0.5)
    sample = pd.DataFrame({
        "Subject": ["Mathematics", "Physics", "English"],
        "Exam date": [today + timedelta(days=6), today + timedelta(days=9), today + timedelta(days=12)],
        "Difficulty": ["Hard", "Medium", "Easy"]})
    table = st.data_editor(sample, num_rows="dynamic", use_container_width=True,
        column_config={"Exam date": st.column_config.DateColumn(),
                       "Difficulty": st.column_config.SelectboxColumn(options=list(DIFFICULTY))})

subjects = [{"name": str(r["Subject"]), "exam": r["Exam date"], "level": DIFFICULTY.get(r["Difficulty"], 2)}
            for _, r in table.dropna().iterrows() if r["Subject"]]
plan = build_plan(subjects, hours)

if not plan:
    st.info("Add a subject with a future exam date in the sidebar.")
    st.stop()

for msg in reminders(subjects, plan):                  # reminders
    st.warning(msg)

if "done" not in st.session_state:
    st.session_state.done = set()
total = sum(len(d["sessions"]) for d in plan)
done = sum(1 for d in plan for n, _ in d["sessions"] if (str(d["date"]), n) in st.session_state.done)
st.progress(done / total if total else 0, text=f"{done} of {total} sessions done")   # progress bar

for d in plan:
    label = d["date"].strftime("%a %d %b") + ("  (today)" if d["date"] == today else "")
    with st.expander(label, expanded=d["date"] == today):
        for e in d["exams"]:
            st.error(f"Exam today: {e}")
        for n, h in d["sessions"]:
            key = (str(d["date"]), n)
            ticked = st.checkbox(f"{n} - {h}h", value=key in st.session_state.done, key=f"{key}")
            (st.session_state.done.add if ticked else st.session_state.done.discard)(key)
