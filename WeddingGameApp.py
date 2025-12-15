import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Shaadi Couple Trivia", page_icon="💖", layout="centered")

# ---------------- QUESTIONS ----------------
QUESTIONS = [
    ("Where did their love story begin? 💌",
     ["College", "Office", "Through friends", "Instagram"], "Through friends"),
    ("Who said 'I love you' first? ❤️",
     ["Bride", "Groom", "Both together", "No one remembers"], "Groom"),
    ("What was their first official date? 🍽️",
     ["Coffee date", "Movie night", "Long drive", "Street food outing"], "Coffee date"),
    ("Who is more likely to be late? ⏰",
     ["Bride", "Groom", "Both", "Neither"], "Bride"),
    ("Who usually plans their outings or trips? 🗺️",
     ["Bride", "Groom", "Both together", "Plans change last minute 😄"], "Both together"),
    ("Who clicks more selfies? 🤳",
     ["Bride", "Groom", "Both", "None"], "Bride"),
    ("What do they enjoy doing together the most on weekends? 🌤️",
     ["Watching movies at home", "Going out for food", "Long drives", "Spending time with family"],
     "Watching movies at home"),
    ("Who says sorry first after a small fight? 🙈",
     ["Bride", "Groom", "Both together", "They forget the fight 😄"], "Groom"),
    ("Who remembers important dates better? 📅",
     ["Bride", "Groom", "Both", "They set reminders 😄"], "Bride"),
    ("If they could go on a surprise trip tomorrow, where would they go? ✈️",
     ["Goa", "Maldives", "Switzerland", "Kashmir"], "Maldives")
]

TOTAL = len(QUESTIONS)

# ---------------- SCORE FILE ----------------
FILE = "scores.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["name", "team", "score"]).to_csv(FILE, index=False)

# ---------------- SESSION STATE ----------------
ss = st.session_state
ss.setdefault("page", "home")
ss.setdefault("q", 0)
ss.setdefault("score", 0)
ss.setdefault("played", False)   # 🔒 one play per browser

# =================================================
# HOME PAGE
# =================================================
if ss.page == "home":
    st.title("💖 Shaadi Couple Trivia")

    if ss.played:
        st.warning("🚫 You have already played this quiz on this device.")
        st.stop()

    ss.name = st.text_input("Your Name")
    ss.team = st.selectbox(
        "Your Team",
        ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]
    )

    if st.button("Start Quiz 🎯") and ss.name.strip():
        ss.q = 0
        ss.score = 0
        ss.page = "quiz"
        st.rerun()

# =================================================
# QUIZ PAGE
# =================================================
elif ss.page == "quiz":
    q, options, correct = QUESTIONS[ss.q]
    answer = st.radio(f"Q{ss.q + 1}. {q}", options)

    if st.button("Next ➜"):
        ss.score += (answer == correct)
        ss.q += 1
        ss.page = "leaderboard" if ss.q == TOTAL else "quiz"
        st.rerun()

# =================================================
# LEADERBOARD PAGE
# =================================================
else:
    st.title("🏆 Leaderboard")

    # Save score
    df = pd.read_csv(FILE)
    df = pd.concat(
        [df, pd.DataFrame([{
            "name": ss.name,
            "team": ss.team,
            "score": ss.score
        }])],
        ignore_index=True
    )
    df.to_csv(FILE, index=False)

    # Mark as played (LOCK 🔒)
    ss.played = True

    # Show personal score
    st.subheader("🎯 Your Result")
    st.success(f"{ss.name}, you answered {ss.score} out of {TOTAL} correctly.")

    st.write("---")

    # Show leaderboard
    st.subheader("📊 Leaderboard")
    st.table(df.sort_values("score", ascending=False).reset_index(drop=True))
