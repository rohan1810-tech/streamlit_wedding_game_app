import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Shaadi Couple Trivia", page_icon="💖", layout="centered")

# --------------------------
#  Questions with emojis
# --------------------------
QUESTIONS = [
    ("Where did their love story begin? 💌",
     ["College canteen 😋", "Office pantry ☕", "Through friends 🧑‍🤝‍🧑", "Instagram DMs 📱"],
     "Through friends 🧑‍🤝‍🧑"),
    ("Who said 'I love you' first? ❤️",
     ["Bride 👰", "Groom 🤵", "Same time ⏱️", "No one remembers 🤔"],
     "Groom 🤵"),
    ("Their first movie together on a date night? 🎬",
     ["YJHD 🎒", "3 Idiots 🤓", "Tamasha 🎭", "Kabir Singh 💔"],
     "YJHD 🎒"),
    ("Who clicks more selfies? 🤳",
     ["Bride 👰", "Groom 🤵", "Both equally 😎", "They hate selfies 🙈"],
     "Bride 👰"),
    ("Perfect date-night food for them? 🍽️",
     ["North Indian thali 🍛", "Chinese noodles 🍜", "Italian pizza 🍕", "Street food pani puri 🤤"],
     "Street food pani puri 🤤"),
    ("After a cute fight, who says sorry first? 🙈",
     ["Bride 👰", "Groom 🤵", "Both together 🤝", "They just start laughing 😂"],
     "Groom 🤵"),
    ("Their first trip together? ✈️",
     ["Goa 🏖️", "Manali 🏔️", "Jaipur 🏰", "Lonavala 🌧️"],
     "Goa 🏖️"),
    ("Bride’s go-to drink? 🥤",
     ["Coffee ☕", "Tea 🍵", "Cold Coffee 🧋", "Mojito 🥂"],
     "Cold Coffee 🧋"),
    ("Groom’s favourite timepass? 🎮",
     ["Mobile gaming 🎮", "Web series binge 📺", "Cricket 🏏", "Sleeping all day 😴"],
     "Cricket 🏏"),
    ("Who is more likely to be late? ⏰",
     ["Bride 👰", "Groom 🤵", "Both 😅", "Shockingly, none 😇"],
     "Bride 👰"),
    ("Which song feels like 'their' song? 🎵",
     ["Perfect – Ed Sheeran 🎻", "Tum Hi Ho 🎹", "Raanjhanaa 🎺", "Kesariya 🧡"],
     "Kesariya 🧡"),
    ("Who is the bigger foodie? 🍕", 
     ["Bride 🍰", "Groom 😋", "Both total foodies 🤤", "None, they diet 🙃"],
     "Both total foodies 🤤"),
    ("Bride’s top complaint about Groom? 😏",
     ["On phone all the time 📱", "Always late 🕒", "Doesn’t reply fast 💬", "Doesn’t plan surprises 🎁"],
     "On phone all the time 📱"),
    ("What does the Groom secretly love most about the Bride? 💕",
     ["Her smile 😊", "Her madness 🤪", "Her support 🤍", "Her cooking 👩‍🍳"],
     "Her smile 😊"),
    ("If they could teleport right now, where would they go? 🌍",
     ["Maldives 🌊", "Switzerland ❄️", "Kashmir 🏔️", "Paris 🗼"],
     "Maldives 🌊"),
]

TOTAL = len(QUESTIONS)

# --------------------------
#  Leaderboard file
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
# flag: to avoid saving same result multiple times
if "saved_score" not in st.session_state:
    st.session_state.saved_score = False


# --------------------------
# HOME SCREEN
# --------------------------
if st.session_state.page == "home":
    st.title("💖 Shaadi Couple Trivia 💥")
    st.write("Fun quiz for guests! Let’s see who really knows the couple 😉")

    st.subheader("Player Details")
    st.session_state.name = st.text_input("Your Name ✍️")
    st.session_state.team = st.selectbox(
        "You are from…",
        ["Bride Side 💖", "Groom Side 💙", "Know Both Very Well 🤝"]
    )

    if st.button("Start Quiz 🎯"):
        if st.session_state.name.strip() == "":
            st.warning("Please enter your name first 😊")
        else:
            st.session_state.page = "quiz"
            st.session_state.q = 0
            st.session_state.score = 0
            st.session_state.saved_score = False
            st.rerun()


# --------------------------
# QUIZ SCREEN
# --------------------------
elif st.session_state.page == "quiz":

    if st.session_state.q >= TOTAL:
        st.session_state.page = "result"
        st.rerun()

    q_index = st.session_state.q
    question, options, correct = QUESTIONS[q_index]

    st.write(f"**Player:** {st.session_state.name}")
    st.write(f"**Team:** {st.session_state.team}")
    st.progress(q_index / TOTAL)

    st.subheader(f"Q{q_index + 1}. {question}")
    choice = st.radio("Choose your answer 👇", options, key=f"q{q_index}")

    if st.button("Next ➜"):
        if choice == correct:
            st.session_state.score += 1
        st.session_state.q += 1
        st.rerun()


# --------------------------
# RESULT + CROWN LEADER PANEL
# --------------------------
elif st.session_state.page == "result":
    score = st.session_state.score
    name = st.session_state.name

    st.title("🎉 Quiz Completed!")
    st.write(f"Nice game, **{name}**!")
    st.subheader(f"Your Score: {score} / {TOTAL}")

    if score == TOTAL:
        st.success("Absolute LEGEND! You know them better than they know themselves 😎")
    elif score >= TOTAL * 0.7:
        st.success("Amazing! You’re definitely part of the inner circle 💖")
    elif score >= TOTAL * 0.4:
        st.info("Not bad! You know them… but some gossip is still missing 😜")
    else:
        st.warning("Looks like you came mainly for the food 😆")

    # Read existing scores
    df = pd.read_csv(FILE)

    # Save this run ONLY once (avoid duplicate rows on rerun)
    if not st.session_state.saved_score:
        df.loc[len(df)] = [st.session_state.name, st.session_state.team, score]
        df.to_csv(FILE, index=False)
        st.session_state.saved_score = True

    # Refresh df after possible write
    df = pd.read_csv(FILE)

    st.write("---")
    st.subheader("🏆 Leaderboard (Top 3 Players)")
