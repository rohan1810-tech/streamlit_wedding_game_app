import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Shaadi Couple Trivia", page_icon="💖", layout="centered")

# ---------------- QUESTIONS ----------------
QUESTIONS = [
    ("Where did they meet? 💌",
     ["College", "Office", "Through friends", "Instagram"],
     "Through friends"),

    ("Who said I love you first? ❤️",
     ["Bride", "Groom", "Both", "No one"],
     "Groom"),

    ("First trip together? ✈️",
     ["Goa", "Manali", "Jaipur", "Lonavala"],
     "Goa")
]

# ---------------- SCORE FILE ----------------
FILE = "scores.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["team", "score"]).to_csv(FILE, index=False)

# ---------------- SESSION STATE ----------------
ss = st.session_state
ss.setdefault("page", "home")
ss.setdefault("q", 0)
ss.setdefault("score", 0)

# ---------------- HOME ----------------
if ss.page == "home":
    st.title("💖 Shaadi Couple Trivia")

    ss.name = st.text_input("Your Name")
    ss.team = st.selectbox(
        "Your Team",
        ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]
    )

    if st.button("Start Quiz"):
        if ss.name.strip():
            ss.q = 0
            ss.score = 0
            ss.page = "quiz"
            st.rerun()
        else:
            st.warning("Please enter your name")

# ---------------- QUIZ ----------------
elif ss.page == "quiz":
    q, options, correct = QUESTIONS[ss.q]

    answer = st.radio(f"Q{ss.q+1}. {q}", options)

    if st.button("Next"):
        ss.score += (answer == correct)
        ss.q += 1
        ss.page = "leaderboard" if ss.q == len(QUESTIONS) else "quiz"
        st.rerun()

# ---------------- LEADERBOARD ----------------
else:
    st.title("🏆 Team Leaderboard")

    df = pd.read_csv(FILE)

    # SAFE SAVE (NO COLUMN MISMATCH EVER)
    df = pd.concat(
        [df, pd.DataFrame([{"team": ss.team, "score": ss.score}])],
        ignore_index=True
    )
    df.to_csv(FILE, index=False)

    team_scores = df.groupby("team")["score"].sum()

    st.subheader("💥 Team Scores")

    for team in ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]:
        st.metric(team, team_scores.get(team, 0))

    st.success(f"👑 Winning Team: {team_scores.idxmax()}")

    if st.button("Play Again"):
        ss.page = "home"
        st.rerun()
