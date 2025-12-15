import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Shaadi Couple Trivia",
    page_icon="💖",
    layout="centered"
)

# ---------------- QUESTIONS ----------------
QUESTIONS = [
    ("Where did their love story begin? 💌",
     ["College", "Office", "Through friends", "Instagram"],
     "Through friends"),

    ("Who said 'I love you' first? ❤️",
     ["Bride", "Groom", "Both together", "No one remembers"],
     "Groom"),

    ("What was their first official date? 🍽️",
     ["Coffee date", "Movie night", "Long drive", "Street food outing"],
     "Coffee date"),

    ("Who is more likely to be late? ⏰",
     ["Bride", "Groom", "Both", "Neither"],
     "Bride"),

    ("Who usually plans their outings or trips? 🗺️",
     ["Bride", "Groom", "Both together", "Plans change last minute 😄"],
     "Both together"),

    ("Who clicks more selfies? 🤳",
     ["Bride", "Groom", "Both", "None"],
     "Bride"),

    ("What do they enjoy doing together the most on weekends? 🌤️",
     ["Watching movies at home", "Going out for food", "Long drives", "Spending time with family"],
     "Watching movies at home"),

    ("Who says sorry first after a small fight? 🙈",
     ["Bride", "Groom", "Both together", "They forget the fight 😄"],
     "Groom"),

    ("Who remembers important dates better? 📅",
     ["Bride", "Groom", "Both", "They set reminders 😄"],
     "Bride"),

    ("If they could go on a surprise trip tomorrow, where would they go? ✈️",
     ["Goa", "Maldives", "Switzerland", "Kashmir"],
     "Maldives")
]

TOTAL = len(QUESTIONS)

# ---------------- SCORE FILE ----------------
FILE = "scores.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["name", "team", "score"]).to_csv(FILE, index=False)

# ---------------- SESSION STATE (INITIALIZE EVERYTHING) ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "q" not in st.session_state:
    st.session_state.q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "name" not in st.session_state:
    st.session_state.name = ""
if "team" not in st.session_state:
    st.session_state.team = ""

# =================================================
# 1️⃣ HOME PAGE
# =================================================
if st.session_state.page == "home":
    st.title("💖 Shaadi Couple Trivia")

    st.session_state.name = st.text_input("Your Name", st.session_state.name)
    st.session_state.team = st.selectbox(
        "Your Team",
        ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"],
        index=0 if st.session_state.team == "" else
        ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"].index(st.session_state.team)
    )

    if st.button("Start Quiz 🎯"):
        if st.session_state.name.strip() == "":
            st.warning("Please enter your name")
        else:
            st.session_state.q = 0
            st.session_state.score = 0
            st.session_state.page = "quiz"
            st.rerun()

# =================================================
# 2️⃣ QUIZ PAGE
# =================================================
elif st.session_state.page == "quiz":
    q, options, correct = QUESTIONS[st.session_state.q]

    st.subheader(f"Q{st.session_state.q + 1}. {q}")
    answer = st.radio("Choose one", options)

    if st.button("Next ➜"):
        if answer == correct:
            st.session_state.score += 1

        st.session_state.q += 1
        if st.session_state.q == TOTAL:
            st.session_state.page = "leaderboard"

        st.rerun()

# =================================================
# 3️⃣ LEADERBOARD PAGE
# =================================================
else:
    st.title("🏆 Leaderboard")

    # Save current player score
    df = pd.read_csv(FILE)
    df = pd.concat(
        [df, pd.DataFrame([{
            "name": st.session_state.name,
            "team": st.session_state.team,
            "score": st.session_state.score
        }])],
        ignore_index=True
    )
    df.to_csv(FILE, index=False)

    # Show personal score
    st.subheader("🎯 Your Score")
    st.success(
        f"{st.session_state.name}, you scored "
        f"{st.session_state.score} / {TOTAL}"
    )

    st.write("---")

    # Team-wise scores
    st.subheader("💥 Team Scores")
    team_scores = df.groupby("team")["score"].sum()

    for team in ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]:
        st.metric(team, team_scores.get(team, 0))

    st.success(f"👑 Winning Team: **{team_scores.idxmax()}**")

    st.write("---")

    # Top 3 scorers
    st.subheader("🏅 Top 3 Scorers")
    top3 = (
        df.sort_values("score", ascending=False)
          .head(3)[["name", "score"]]
          .reset_index(drop=True)
    )
    top3.index = top3.index + 1
    st.table(top3)

    if st.button("Play Again 🔁"):
        st.session_state.page = "home"
        st.rerun()
