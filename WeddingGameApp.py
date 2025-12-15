import streamlit as st

st.set_page_config(page_title="Shaadi Couple Trivia", page_icon="💖")

# Questions
questions = [
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

st.title("💖 Shaadi Couple Trivia")

name = st.text_input("Your Name")
team = st.selectbox("Your Team", ["Bride Side", "Groom Side", "Know Both"])

st.write("----")

# Ask questions (VERY SIMPLE)
a1 = st.radio("1. Where did they meet?", questions[0][1])
a2 = st.radio("2. Who said I love you first?", questions[1][1])
a3 = st.radio("3. First trip together?", questions[2][1])

if st.button("Submit"):
    score = 0

    if a1 == questions[0][2]:
        score += 1
    if a2 == questions[1][2]:
        score += 1
    if a3 == questions[2][2]:
        score += 1

    st.success(f"{name}, your score is {score}/3")

    if team == "Bride Side":
        st.write("💖 Bride Side gains points!")
    elif team == "Groom Side":
        st.write("💙 Groom Side gains points!")
    else:
        st.write("🤝 You know both well!")
