import streamlit as st
from io import BytesIO
import qrcode
import pandas as pd
import os

# ---------- BASIC SETUP ----------
st.set_page_config(
    page_title="Couple Trivia Battle",
    page_icon="💖",
    layout="centered"
)

SCORES_FILE = "scores.csv"

# Ensure scores file exists
if not os.path.exists(SCORES_FILE):
    pd.DataFrame(columns=["name", "team", "score"]).to_csv(SCORES_FILE, index=False)

# ---------- QUESTIONS (EDIT FOR REAL COUPLE DETAILS) ----------
QUESTIONS = [
    {
        "q": "Where did the couple first meet?",
        "options": ["College", "Office", "Through friends", "Social media"],
        "answer": "Through friends"
    },
    {
        "q": "Who said 'I love you' first?",
        "options": ["Bride", "Groom", "Same time", "No one remembers"],
        "answer": "Groom"
    },
    {
        "q": "What was their first movie together?",
        "options": ["Yeh Jawaani Hai Deewani", "3 Idiots", "Tamasha", "Kabir Singh"],
        "answer": "Yeh Jawaani Hai Deewani"
    },
    {
        "q": "Who takes more selfies?",
        "options": ["Bride", "Groom", "Both equally", "None, they hate selfies"],
        "answer": "Bride"
    },
    {
        "q": "What is their favourite cuisine for date nights?",
        "options": ["North Indian", "Chinese", "Italian", "Street food"],
        "answer": "Street food"
    },
    {
        "q": "Who usually apologises first after a fight?",
        "options": ["Bride", "Groom", "Both together", "They don’t fight 😉"],
        "answer": "Groom"
    },
    {
        "q": "Where did they go on their first trip together?",
        "options": ["Goa", "Manali", "Jaipur", "Lonavala"],
        "answer": "Goa"
    },
    {
        "q": "What is the bride’s go-to drink?",
        "options": ["Coffee", "Tea", "Cold coffee", "Mojito"],
        "answer": "Cold coffee"
    },
    {
        "q": "What is the groom’s favourite timepass?",
        "options": ["Gaming", "Watching series", "Cricket", "Sleeping"],
        "answer": "Cricket"
    },
    {
        "q": "Who is more likely to be late?",
        "options": ["Bride", "Groom", "Both", "They are always on time"],
        "answer": "Bride"
    },
    {
        "q": "Which song is ‘their’ song?",
        "options": ["Perfect", "Tum Hi Ho", "Raanjhanaa", "Kesariya"],
        "answer": "Kesariya"
    },
    {
        "q": "Who is the bigger foodie?",
        "options": ["Bride", "Groom", "Both equally", "Depends on mood"],
        "answer": "Both equally"
    },
    {
        "q": "What does the bride complain about the most?",
        "options": ["Groom on phone", "Groom being late", "Groom not replying", "Groom not planning dates"],
        "answer": "Groom on phone"
    },
    {
        "q": "What does the groom love most about the bride?",
        "options": ["Her smile", "Her madness", "Her support", "Her cooking"],
        "answer": "Her smile"
    },
    {
        "q": "If they could go anywhere right now, where would they go?",
        "options": ["Maldives", "Switzerland", "Kashmir", "Paris"],
        "answer": "Maldives"
    },
]

TOTAL_QUESTIONS = len(QUESTIONS)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "name" not in st.session_state:
    st.session_state.name = ""
if "team" not in st.session_state:
    st.session_state.team = ""
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = []  # list of dicts: {question, selected, correct, is_correct}
if "saved_score" not in st.session_state:
    st.session_state.saved_score = False  # to avoid saving multiple times


# ---------- INTRO PAGE ----------
if st.session_state.page == "intro":
    st.title("💖 Couple Trivia Battle")
    st.write("Scan. Play. Prove how well you know the couple!")

    name = st.text_input("Your Name")
    team = st.selectbox(
        "Which side are you on?",
        ["Bride Side 💖", "Groom Side 💙", "Both – I just want food 😋"]
    )

    if st.button("Start Quiz 🚀"):
        if name.strip() == "":
            st.warning("Please enter your name.")
        else:
            st.session_state.name = name.strip()
            st.session_state.team = team
            st.session_state.page = "quiz"
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.saved_score = False
            st.experimental_rerun()

    st.write("---")
    st.subheader("Generate QR Code for this Trivia (optional)")
    st.write("After you deploy this app, paste the URL here to create a QR code you can print.")

    qr_url = st.text_input("Enter app URL for QR (example: https://your-trivia-app.com)", "")
    if st.button("Generate QR Code"):
        if qr_url.strip() == "":
            st.warning("Please enter a URL first.")
        else:
            qr_img = qrcode.make(qr_url.strip())
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            st.image(buffer.getvalue(), caption="Scan to play!", width=200)

# ---------- QUIZ PAGE ----------
elif st.session_state.page == "quiz":
    q_idx = st.session_state.q_index

    if q_idx >= TOTAL_QUESTIONS:
        st.session_state.page = "result"
        st.experimental_rerun()

    current_q = QUESTIONS[q_idx]

    st.write(f"Player: **{st.session_state.name}**")
    st.write(f"Team: **{st.session_state.team}**")
    st.progress(q_idx / TOTAL_QUESTIONS)

    st.subheader(f"Q{q_idx + 1}. {current_q['q']}")

    option = st.radio(
        "Choose your answer:",
        current_q["options"],
        index=0,
        key=f"q_{q_idx}"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        next_btn = st.button("Submit & Next 👉")
    with col2:
        st.write(f"Question {q_idx + 1} of {TOTAL_QUESTIONS}")

    if next_btn:
        correct_ans = current_q["answer"]
        is_correct = (option == correct_ans)
        if is_correct:
            st.session_state.score += 1  # 1 point per correct answer

        st.session_state.answers.append({
            "question": current_q["q"],
            "selected": option,
            "correct": correct_ans,
            "is_correct": is_correct
        })

        st.session_state.q_index += 1
        st.experimental_rerun()

# ---------- RESULT + LEADERBOARD PAGE ----------
elif st.session_state.page == "result":
    score = st.session_state.score
    name = st.session_state.name
    team = st.session_state.team

    st.title("🎉 Quiz Completed!")
    st.write(f"Well played, **{name}**!")
    st.subheader(f"Your Score: {score} / {TOTAL_QUESTIONS}")

    # Fun feedback
    if score == TOTAL_QUESTIONS:
        st.success("Legend! You know them better than they know themselves 😎")
    elif score >= TOTAL_QUESTIONS * 0.7:
        st.success("Awesome! You're definitely close to the couple 💖")
    elif score >= TOTAL_QUESTIONS * 0.4:
        st.info("Not bad! You know them, but you can still gossip more 😜")
    else:
        st.warning("Uff! Maybe you came just for the food? 😆")

    # ---- Save score to leaderboard (only once per session) ----
    if not st.session_state.saved_score:
        df_scores = pd.read_csv(SCORES_FILE)
        new_row = {"name": name, "team": team, "score": score}
        df_scores = pd.concat([df_scores, pd.DataFrame([new_row])], ignore_index=True)
        df_scores.to_csv(SCORES_FILE, index=False)
        st.session_state.saved_score = True
    else:
        df_scores = pd.read_csv(SCORES_FILE)

    st.write("---")
    st.subheader("Answers Review")

    with st.expander("Click to see all questions with correct answers"):
        for i, ans in enumerate(st.session_state.answers, start=1):
            status = "✅ Correct" if ans["is_correct"] else "❌ Wrong"
            st.write(f"**Q{i}. {ans['question']}**")
            st.write(f"- Your answer: {ans['selected']}")
            st.write(f"- Correct answer: {ans['correct']} ({status})")
            st.write("")

    st.write("---")
    st.subheader("🏆 Overall Leaderboard")

    if not df_scores.empty:
        df_sorted = df_scores.sort_values("score", ascending=False).reset_index(drop=True)
        st.dataframe(df_sorted)
    else:
        st.write("No scores yet. Be the first to play!")

    st.write("---")
    st.subheader("💥 Bride Side vs Groom Side")

    if not df_scores.empty:
        # Filter only Bride Side and Groom Side (ignore the 'Both' option)
        df_filtered = df_scores[df_scores["team"].isin(["Bride Side 💖", "Groom Side 💙"])]
        if not df_filtered.empty:
            team_scores = df_filtered.groupby("team")["score"].sum()
            st.bar_chart(team_scores)

            # Show who is winning
            if "Bride Side 💖" in team_scores.index and "Groom Side 💙" in team_scores.index:
                bride_score = team_scores.get("Bride Side 💖", 0)
                groom_score = team_scores.get("Groom Side 💙", 0)

                if bride_score > groom_score:
                    st.success(f"Bride Side is leading by {bride_score - groom_score} points! 💖")
                elif groom_score > bride_score:
                    st.success(f"Groom Side is leading by {groom_score - bride_score} points! 💙")
                else:
                    st.info("It's a perfect tie between Bride and Groom side! 😍")
        else:
            st.write("No team scores yet. Ask guests to choose Bride or Groom side while playing.")
    else:
        st.write("No data for team scores yet.")

    st.write("---")
    if st.button("Play Again 🔁"):
        st.session_state.page = "intro"
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.saved_score = False
        st.experimental_rerun()