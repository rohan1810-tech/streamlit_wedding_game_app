import streamlit as st

st.set_page_config(page_title="Shaadi Couple Trivia", page_icon="💖", layout="centered")

# --------------------------
# QUESTIONS
# --------------------------
QUESTIONS = [
    ("Where did their love story begin? 💌",
     ["College canteen 😋", "Office pantry ☕", "Through friends 🧑‍🤝‍🧑", "Instagram DMs 📱"],
     "Through friends 🧑‍🤝‍🧑"),

    ("Who said 'I love you' first? ❤️",
     ["Bride 👰", "Groom 🤵", "Same time ⏱️", "No one remembers 🤔"],
     "Groom 🤵"),

    ("Their first trip together? ✈️",
     ["Goa 🏖️", "Manali 🏔️", "Jaipur 🏰", "Lonavala 🌧️"],
     "Goa 🏖️"),

    ("Who clicks more selfies? 🤳",
     ["Bride 👰", "Groom 🤵", "Both 😎", "None 🙈"],
     "Bride 👰"),

    ("Perfect date-night food? 🍽️",
     ["Pizza 🍕", "Pani Puri 🤤", "Chinese 🍜", "Thali 🍛"],
     "Pani Puri 🤤")
]

TOTAL = len(QUESTIONS)

# --------------------------
# SESSION STATE
# --------------------------
if "started" not in st.session_state:
    st.session_state.started = False
if "q" not in st.session_state:
    st.session_state.q = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# --------------------------
# HOME SCREEN
# --------------------------
if not st.session_state.started:
    st.title("💖 Shaadi Couple Trivia")
    st.write("Fun quiz for wedding guests 🎉")

    name = st.text_input("Your Name ✍️")
    team = st.selectbox(
        "You belong to:",
        ["Bride Side 💖", "Groom Side 💙", "Know Both 🤝"]
    )

    if st.button("Start Quiz 🎯"):
        if name.strip() == "":
            st.warning("Please enter your name 😊")
        else:
            st.session_state.started = True
            st.session_state.name = name
            st.session_state.team = team
            st.session_state.q = 0
            st.session_state.score = 0
            st.rerun()

# --------------------------
# QUIZ SCREEN
# --------------------------
elif st.session_state.q < TOTAL:
    q_no = st.session_state.q
    question, options, correct = QUESTIONS[q_no]

    st.subheader(f"Q{q_no + 1}. {question}")
    answer = st.radio("Choose one 👇", options)

    if st.button("Next ➜"):
        if answer == correct:
            st.session_state.score += 1
        st.session_state.q += 1
        st.rerun()

# --------------------------
# RESULT SCREEN
# --------------------------
else:
    st.title("🎉 Quiz Completed!")

    st.write(f"**Name:** {st.session_state.name}")
    st.write(f"**Team:** {st.session_state.team}")
    st.subheader(f"Score: {st.session_state.score} / {TOTAL}")

    score = st.session_state.score

    if score == TOTAL:
        st.success("LEGEND! You know them perfectly 😎")
    elif score >= TOTAL * 0.6:
        st.success("Great job! You know them well 💖")
    elif score >= TOTAL * 0.3:
        st.info("Not bad! Enjoy the wedding 🎉")
    else:
        st.warning("Looks like you came mainly for the food 😆")

    if st.button("Play Again 🔁"):
        st.session_state.started = False
        st.session_state.q = 0
        st.session_state.score = 0
        st.rerun()
