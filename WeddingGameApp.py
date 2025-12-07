import streamlit as st
import pandas as pd
import os

# --------------------------
#  Page config
# --------------------------
st.set_page_config(page_title="Shaadi Couple Trivia", page_icon="💖", layout="centered")

# --------------------------
#  Custom CSS (HTML + CSS)
# --------------------------
st.markdown(
    """
    <style>
        /* App background */
        div[data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top left, #ffe4f2, #fff2d7, #e7f3ff);
        }

        /* Center content max width */
        div.block-container {
            max-width: 720px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Title */
        .title-text {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 900;
            color: #ff2e7a;
            margin-bottom: 0.1rem;
        }

        .subtitle-text {
            text-align: center;
            font-size: 1.05rem;
            color: #444;
            margin-bottom: 1.8rem;
        }

        /* Card style */
        .card {
            background: linear-gradient(135deg, #ffffff, #ffeef8);
            padding: 1.1rem 1.4rem;
            border-radius: 20px;
            box-shadow: 0 12px 26px rgba(0, 0, 0, 0.10);
            margin-bottom: 1.4rem;
            border: 1px solid #ffd3ea;
        }

        .card-soft {
            background: #ffffffdd;
            padding: 0.9rem 1.2rem;
            border-radius: 18px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.2rem;
        }

        .badge {
            display: inline-block;
            padding: 0.18rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            background: #ffe1f0;
            color: #c2185b;
            margin-right: 0.4rem;
        }

        .badge-team {
            background: #e3f2ff;
            color: #1459b3;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 999px;
            padding: 0.6rem 1.8rem;
            border: none;
            font-weight: 650;
            background: linear-gradient(135deg, #ff2e7a, #ff8a3b);
            color: white;
            cursor: pointer;
            font-size: 1rem;
        }

        .stButton>button:hover {
            opacity: 0.97;
            box-shadow: 0 6px 18px rgba(0,0,0,0.20);
        }

        /* Progress bar color */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #ff2e7a, #ffb300);
        }

        /* Dataframe tweaks */
        .stDataFrame, .stTable {
            background: #ffffffee;
            border-radius: 16px;
            padding: 0.4rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
#  Emoji Questions 🎉
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
     ["Bride 🍰", "Groom 🍗", "Both total foodies 🤤", "None, they diet 🙃"], 
     "Both total foodies 🤤"),
    ("Bride’s top complaint about Groom? 😏", 
     ["On phone all the time 📱", "Always late 🕒", "Doesn’t reply fast 💬", "Doesn’t plan surprises 🎁"], 
     "On phone all the time 📱"),
    ("What does the Groom secretly love most about the Bride? 💕", 
     ["Her smile 😊", "Her madness 🤪", "Her support 🤍", "Her cooking 👩‍🍳"], 
     "Her smile 😊"),
    ("If they could teleport right now, where would they go? 🌍", 
     ["Maldives 🌊", "Switzerland ❄️", "Kashmir 🏔️", "Paris 🗼"], 
     "Maldives 🌊")
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
    st.markdown('<div class="title-text">💖 Shaadi Couple Trivia 💥</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle-text">Fun quiz for guests! Let’s see who actually knows the couple and who just came for biryani 😋</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### Player Details")

    st.session_state.name = st.text_input("Your Name ✍️")
    st.session_state.team = st.selectbox(
        "Which side are you cheering for? 🎭",
        ["Bride Squad 💖", "Groom Gang 💙"]
    )

    start = st.button("Start Quiz 🎯")
    st.markdown('</div>', unsafe_allow_html=True)

    if start:
        if st.session_state.name.strip() == "":
            st.warning("Please enter your name first 😊")
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

    q_index = st.session_state.q
    question, options, correct = QUESTIONS[q_index]

    st.markdown(
        f'''
        <div class="card-soft">
            <span class="badge">Player</span> {st.session_state.name}
            &nbsp;&nbsp;
            <span class="badge badge-team">Team</span> {st.session_state.team}
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.progress(q_index / TOTAL)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"### Q{q_index + 1}. {question}")
    choice = st.radio("Choose your answer 👇", options, key=f"q{q_index}")
    next_btn = st.button("Next ➜")
    st.markdown('</div>', unsafe_allow_html=True)

    if next_btn:
        if choice == correct:
            st.session_state.score += 1
        st.session_state.q += 1
        st.rerun()


# --------------------------
# RESULT + LEADERBOARD
# --------------------------
elif st.session_state.page == "result":

    score = st.session_state.score
    name = st.session_state.name

    st.markdown('<div class="title-text">🎉 Quiz Completed!</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="subtitle-text">Nice game, <b>{name}</b>! Let\'s see how you did 👇</div>',
        unsafe_allow_html=True
    )

    # Score + reaction card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"### Your Score: {score} / {TOTAL}")

    if score == TOTAL:
        st.success("Absolute LEGEND! You know them better than they know themselves 😎")
    elif score >= TOTAL * 0.7:
        st.success("Amazing! You’re definitely part of the inner circle 💖")
    elif score >= TOTAL * 0.4:
        st.info("Not bad! You know them… but you clearly miss some gossip sessions 😜")
    else:
        st.warning("Acha toh aap bas khaane ke liye aaye the? 😆")
    st.markdown('</div>', unsafe_allow_html=True)

    # Save to leaderboard
    df = pd.read_csv(FILE)
    df.loc[len(df)] = [st.session_state.name, st.session_state.team, score]
    df.to_csv(FILE, index=False)

    # Leaderboard card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 🏆 Leaderboard (All Players)")
    df_sorted = df.sort_values("score", ascending=False).reset_index(drop=True)
    st.dataframe(df_sorted)
    st.markdown('</div>', unsafe_allow_html=True)

    # Bride vs Groom battle
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 💥 Bride Squad vs Groom Gang")

    team_scores = df.groupby("team")["score"].sum()

    if not team_scores.empty:
        st.bar_chart(team_scores)

        bride_label = "Bride Squad 💖"
        groom_label = "Groom Gang 💙"

        if bride_label in team_scores.index and groom_label in team_scores.index:
            bride_score = team_scores[bride_label]
            groom_score = team_scores[groom_label]

            if bride_score > groom_score:
                st.success(f"Bride Squad is CRUSHING it! 💖 ({bride_score} vs {groom_score})")
            elif groom_score > bride_score:
                st.success(f"Groom Gang is on FIRE! 💙 ({groom_score} vs {bride_score})")
            else:
                st.info("It’s a PERFECT TIE! Pure balance, pure love 😍")
        else:
            st.info("Need players from both sides to see the battle results.")
    else:
        st.write("No scores yet. Be the first one!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Play again
    st.markdown('<div class="card-soft">', unsafe_allow_html=True)
    if st.button("Play Again 🔁"):
        st.session_state.page = "home"
        st.session_state.q = 0
        st.session_state.score = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
