import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# ---------------- CONFIG ----------------
st.set_page_config("Shaadi Couple Trivia", "💖")
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

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

FILE = "scores.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["team", "score"]).to_csv(FILE, index=False)

# ---------------- STATE ----------------
ss = st.session_state
ss.setdefault("page", "home")
ss.setdefault("q", 0)
ss.setdefault("score", 0)

# ---------------- HOME ----------------
if ss.page == "home":
    st.title("💖 Shaadi Couple Trivia")

    ss.name = st.text_input("Your Name")
    ss.team = st.selectbox("Your Team",
                           ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"])

    if st.button("Start Quiz"):
        if ss.name:
            ss.q = 0
            ss.score = 0
            ss.page = "quiz"
            st.rerun()

# ---------------- QUIZ ----------------
elif ss.page == "quiz":
    q, options, correct = QUESTIONS[ss.q]
    ans = st.radio(f"Q{ss.q+1}. {q}", options)

    if st.button("Next"):
        ss.score += (ans == correct)
        ss.q += 1
        ss.page = "leaderboard" if ss.q == len(QUESTIONS) else "quiz"
        st.rerun()

# ---------------- LEADERBOARD ----------------
else:
    st.title("🏆 Team Leaderboard")

    df = pd.read_csv(FILE)
    df.loc[len(df)] = [ss.team, ss.score]
    df.to_csv(FILE, index=False)

    team_scores = df.groupby("team")["score"].sum()
    winner = team_scores.idxmax()

    for team in ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]:
        st.metric(team, team_scores.get(team, 0))

    prompt = f"""
    Team scores:
    {team_scores.to_dict()}
    Winning team: {winner}

    Announce the winner in a fun wedding-friendly way.
    """

    st.success(model.generate_content(prompt).text)

    if st.button("Play Again"):
        ss.page = "home"
        st.rerun()
