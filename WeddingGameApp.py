import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Shaadi Couple Trivia", page_icon="💖", layout="centered")

# --------------------------
# QUESTIONS
# --------------------------
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

TOTAL = len(QUESTIONS)

# --------------------------
# SCORE FILE
# --------------------------
FILE = "scores.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["team", "score"]).to_csv(FILE, index=False)

# --------------------------
# SESSION STATE
# --------------------------
ss = st.session_state
ss.setdefault("page", "home")
ss.setdefault("q", 0)
ss.setdefault("score", 0)

# --------------------------
# HOME PAGE
# --------------------------
if ss.page == "home":
    st.title("💖 Shaadi Couple Trivia")

    ss.name = st.text_input("Your Name")
    ss.team = st.selectbox(
        "Your Team",
        ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]
    )

    if st.button("Start Quiz 🎯"):
        if ss.name.strip() == "":
            st.warning("Please enter your name")
        else:
            ss.q = 0
            ss.score = 0
            ss.page = "quiz"
            st.rerun()

# --------------------------
# QUIZ PAGE
# --------------------------
elif ss.page == "quiz":
    q, options, correct = QUESTIONS[ss.q]

    st.subheader(f"Q{ss.q + 1}. {q}")
    answer = st.radio("Choose one", options)

    if st.button("Next ➜"):
        if answer == correct:
            ss.score += 1

        ss.q += 1
        if ss.q == TOTAL:
            ss.page = "leaderboard"

        st.rerun()

# --------------------------
# LEADERBOARD PAGE
# --------------------------
else:
    st.title("🏆 Team Leaderboard")

    # Save current score
    df = pd.read_csv(FILE)
    df.loc[len(df)] = [ss.team, ss.score]
    df.to_csv(FILE, index=False)

    # Team-wise totals
    team_scores = df.groupby("team")["score"].sum()

    st.subheader("💥 Team Scores")

    col1, col2, col3 = st.columns(3)
    teams = ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]
    cols = [col1, col2, col3]

    max_score = team_scores.max()

    for team, col in zip(teams, cols):
        score = team_scores.get(team, 0)
        with col:
            if score == max_score and score > 0:
                st.markdown(f"### 👑 {team}")
            else:
                st.markdown(f"### {team}")
            st.metric("Score", score)

    st.write("---")
    st.success(f"🎉 Winning Team: **{team_scores.idxmax()}**")

    if st.button("Play Again 🔁"):
        ss.page = "home"
        st.rerun()
