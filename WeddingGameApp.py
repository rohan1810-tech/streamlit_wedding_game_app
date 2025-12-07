import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Couple Trivia", page_icon="💖")

# --------------------------
#  Questions
# --------------------------
QUESTIONS = [
    ("Where did the couple first meet?", ["College", "Office", "Through friends", "Social media"], "Through friends"),
    ("Who said 'I love you' first?", ["Bride", "Groom", "Same time", "Can't remember"], "Groom"),
    ("First movie together?", ["YJHD", "3 Idiots", "Tamasha", "Kabir Singh"], "YJHD"),
    ("Who takes more selfies?", ["Bride", "Groom", "Both", "None"], "Bride"),
    ("Favourite date-night food?", ["North Indian", "Chinese", "Italian", "Street food"], "Street food"),
    ("Who apologises first?", ["Bride", "Groom", "Both", "They don’t fight"], "Groom"),
    ("First trip location?", ["Goa", "Manali", "Jaipur", "Lonavala"], "Goa"),
    ("Bride’s favourite drink?", ["Coffee", "Tea", "Cold coffee", "Mojito"], "Cold coffee"),
    ("Groom’s favourite timepass?", ["Gaming", "Series", "Cricket", "Sleeping"], "Cricket"),
    ("Who is late more often?", ["Bride", "Groom", "Both", "None"], "Bride"),
    ("Their song?", ["Perfect", "Tum Hi Ho", "Raanjhanaa", "Kesariya"], "Kesariya"),
    ("Who is the bigger foodie?", ["Bride", "Groom", "Both", "None"], "Both"),
    ("Bride's top complaint?", ["Phone", "Late", "No reply", "No dates"], "Phone"),
    ("Groom loves most about Bride?", ["Smile", "Support", "Cooking", "Kindness"], "Smile"),
    ("Dream destination?", ["Maldives", "Switzerland", "Kashmir", "Paris"], "Maldives")
]

TOTAL = len(QUESTIONS)

# --------------------------
#  Leaderboard File
# --------------------------
FILE = "scores.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["name", "team", "score"]).to_csv(FILE, index=False)

# --------------------------
#  Session State
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "name" not in st.session_state:
    st.session_state.name = ""
if "team" not in st.session_state:
    st.session_state.team = ""
if "q" not in st.session_state:
    st.session_state.q = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# --------------------------
# HOME SCREEN
# --------------------------
if st.session_state.page == "home":
    st.title("💖 Couple Trivia Game")

    st.session_state.name = st.text_input("Your Name:")
    st.session_state.team = st.selectbox("Which side are you on?", ["Bride", "Groom"])

    if st.button("Start Quiz ▶️"):
        if st.session_state.name.strip() == "":
            st.warning("Enter your name!")
        else:
            st.session_state.page = "quiz"
            st.session_state.q = 0
            st.session_state.score = 0
            st.rerun()

# --------------------------
# QUIZ SCREEN
# --------------------------
elif st.session_state.page == "quiz":

    if st.session_state.q >= TOTAL:
        st.session_state.page = "result"
        st.rerun()

    question, options, correct = QUESTIONS[st.session_state.q]

    st.subheader(f"Question {st.session_state.q + 1} of {TOTAL}")
    st.write(question)

    choice = st.radio("Choose one:", options, key=f"q{st.session_state.q}")

    if st.button("Next"):
        if choice == correct:
            st.session_state.score += 1

        st.session_state.q += 1
        st.rerun()

# --------------------------
# RESULT + LEADERBOARD
# --------------------------
elif st.session_state.page == "result":
    st.title("🎉 Quiz Completed!")

    score = st.session_state.score
    st.write(f"**Your Score:** {score} / {TOTAL}")

    # Save score
    df = pd.read_csv(FILE)
    df.loc[len(df)] = [st.session_state.name, st.session_state.team, score]
    df.to_csv(FILE, index=False)

    st.write("---")
    st.subheader("🏆 Leaderboard")
    df = df.sort_values("score", ascending=False)
    st.dataframe(df)

    st.write("---")
    st.subheader("💥 Bride Side vs Groom Side")

    team_scores = df.groupby("team")["score"].sum()
    st.bar_chart(team_scores)

    if len(team_scores) == 2:
        bride, groom = team_scores["Bride"], team_scores["Groom"]
        if bride > groom:
            st.success("Bride Side is winning! 💖")
        elif groom > bride:
            st.success("Groom Side is winning! 💙")
        else:
            st.info("It's a tie!")

    st.write("---")
    if st.button("Play Again 🔁"):
        st.session_state.page = "home"
        st.session_state.q = 0
        st.session_state.score = 0
        st.rerun()
