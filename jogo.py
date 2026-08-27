import streamlit as st
import random

st.set_page_config(page_title="Game of Emotions", page_icon="🎭", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
    }
    .phrase-box {
        background-color: rgba(255,255,255,0.05);
        border-left: 5px solid #7c5cff;
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        font-size: 1.3rem;
        font-style: italic;
        margin: 1rem 0;
    }
    .difficulty-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ---------- TEXTS ----------
TEXTS = {
    "en": {
        "title": "🎭 Game of Emotions",
        "subtitle": "Read the sentence and guess which sentiment the person is feeling!",
        "question_label": "What sentiment is this person feeling?",
        "submit": "Submit Answer",
        "next": "Next question ➡️",
        "restart": "🔄 Restart game",
        "score": "Score",
        "streak": "Streak",
        "level": "Level",
        "correct": "Correct! That's",
        "wrong": "Not quite. The correct answer was",
        "levels": ["Easy", "Medium", "Hard", "Expert"],
    },
    "pt": {
        "title": "🎭 Jogo das Emoções",
        "subtitle": "Leia a frase e adivinhe qual sentimento a pessoa está sentindo!",
        "question_label": "Qual sentimento essa pessoa está sentindo?",
        "submit": "Enviar Resposta",
        "next": "Próxima pergunta ➡️",
        "restart": "🔄 Reiniciar jogo",
        "score": "Pontos",
        "streak": "Sequência",
        "level": "Nível",
        "correct": "Correto! Esse sentimento é",
        "wrong": "Quase. A resposta certa era",
        "levels": ["Fácil", "Médio", "Difícil", "Especialista"],
    },
}

SENTIMENT_LABELS = {
    "en": {"Happy": "Happy", "Sad": "Sad", "Angry": "Angry", "Scared": "Scared", "Surprised": "Surprised", "Anxious": "Anxious", "Jealous": "Jealous", "Guilty": "Guilty", "Proud": "Proud", "Embarrassed": "Embarrassed"},
    "pt": {"Happy": "Feliz", "Sad": "Triste", "Angry": "Bravo(a)", "Scared": "Assustado(a)", "Surprised": "Surpreso(a)", "Anxious": "Ansioso(a)", "Jealous": "Com ciúmes", "Guilty": "Culpado(a)", "Proud": "Orgulhoso(a)", "Embarrassed": "Envergonhado(a)"},
}

EMOJIS = {"Happy": "😄", "Sad": "😢", "Angry": "😠", "Scared": "😱", "Surprised": "😲",
          "Anxious": "😰", "Jealous": "😒", "Guilty": "😔", "Proud": "😌", "Embarrassed": "😳"}

# ---------- QUESTION BANK BY DIFFICULTY ----------
QUESTIONS = {
    1: [  # Easy — obvious, explicit
        {"en": "I just got the job I always dreamed of!", "pt": "Acabei de conseguir o emprego dos meus sonhos!", "answer": "Happy"},
        {"en": "I can't believe you broke my favorite mug.", "pt": "Não acredito que você quebrou minha caneca favorita.", "answer": "Angry"},
        {"en": "I miss my family so much right now.", "pt": "Estou com muita saudade da minha família agora.", "answer": "Sad"},
        {"en": "There's someone standing outside my window at night.", "pt": "Tem alguém parado do lado de fora da minha janela à noite.", "answer": "Scared"},
        {"en": "Wow, I did not expect that plot twist at all!", "pt": "Uau, eu não esperava essa reviravolta!", "answer": "Surprised"},
        {"en": "I finally passed my driving test on the first try!", "pt": "Finalmente passei na prova de direção na primeira tentativa!", "answer": "Happy"},
        {"en": "He promised he would call, and it's been three days.", "pt": "Ele prometeu que ligaria, e já se passaram três dias.", "answer": "Sad"},
    ],
    2: [  # Medium — a bit more subtle
        {"en": "You went through my phone without asking me?!", "pt": "Você mexeu no meu celular sem me perguntar?!", "answer": "Angry"},
        {"en": "I heard footsteps behind me but no one was there.", "pt": "Ouvi passos atrás de mim, mas não tinha ninguém lá.", "answer": "Scared"},
        {"en": "I opened the door and everyone yelled 'Surprise!'", "pt": "Abri a porta e todo mundo gritou 'Surpresa!'", "answer": "Surprised"},
        {"en": "My hands won't stop shaking before the interview starts.", "pt": "Minhas mãos não param de tremer antes da entrevista começar.", "answer": "Anxious"},
        {"en": "She got the promotion I've been working toward for years.", "pt": "Ela conseguiu a promoção pela qual eu venho trabalhando há anos.", "answer": "Jealous"},
        {"en": "I should have double-checked before sending that email to the whole team.", "pt": "Eu deveria ter conferido antes de mandar aquele e-mail pra equipe toda.", "answer": "Guilty"},
    ],
    3: [  # Hard — indirect, requires inference
        {"en": "This is the third time you've canceled on me this week.", "pt": "Essa é a terceira vez que você cancela comigo essa semana.", "answer": "Angry"},
        {"en": "I keep checking my phone even though I know they're not going to text.", "pt": "Fico checando o celular mesmo sabendo que não vão me mandar mensagem.", "answer": "Anxious"},
        {"en": "Everyone at the table went quiet after I mentioned it.", "pt": "Todo mundo na mesa ficou quieto depois que eu mencionei aquilo.", "answer": "Embarrassed"},
        {"en": "I keep replaying what I said to her, wishing I could take it back.", "pt": "Fico repassando o que falei pra ela, querendo poder voltar atrás.", "answer": "Guilty"},
        {"en": "My name was the only one they mentioned during the whole ceremony.", "pt": "Meu nome foi o único que mencionaram durante toda a cerimônia.", "answer": "Proud"},
        {"en": "I noticed they took a photo together and didn't tag me this time.", "pt": "Percebi que eles tiraram uma foto juntos e não me marcaram dessa vez.", "answer": "Jealous"},
    ],
    4: [  # Expert — very subtle, tone/context-based
        {"en": "I laughed along with everyone, then went to the bathroom for a few minutes.", "pt": "Ri junto com todo mundo, depois fui pro banheiro por uns minutos.", "answer": "Embarrassed"},
        {"en": "I told them it was fine, then spent the night rereading the messages.", "pt": "Eu disse que estava tudo bem, mas passei a noite relendo as mensagens.", "answer": "Anxious"},
        {"en": "I congratulated her and meant it, mostly.", "pt": "Eu a parabenizei e falei sério, quase totalmente.", "answer": "Jealous"},
        {"en": "I kept the certificate in a drawer, but I take it out sometimes.", "pt": "Guardei o certificado numa gaveta, mas às vezes eu o pego pra olhar.", "answer": "Proud"},
        {"en": "I said I forgot, but I remember exactly what I did that day.", "pt": "Eu disse que tinha esquecido, mas lembro exatamente o que fiz naquele dia.", "answer": "Guilty"},
    ],
}

# Streak thresholds to level up
LEVEL_UP_AT = 3  # every N correct in a row, level increases

# ---------- STATE ----------
def new_question():
    level = st.session_state.level
    pool = QUESTIONS[level]
    q = random.choice(pool)
    st.session_state.current = q
    st.session_state.answered = False
    st.session_state.last_correct = None

def start_new_game():
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.level = 1
    new_question()

if "level" not in st.session_state or "score" not in st.session_state or "current" not in st.session_state:
    start_new_game()

# ---------- LANGUAGE SWITCH ----------
lang = st.radio("🌐 Language / Idioma", ["en", "pt"], format_func=lambda x: "English 🇺🇸" if x == "en" else "Português 🇧🇷", horizontal=True)
t = TEXTS[lang]
labels = SENTIMENT_LABELS[lang]

# ---------- HEADER ----------
st.title(t["title"])
st.write(t["subtitle"])

level = st.session_state.level
level_name = t["levels"][level - 1]
level_colors = {1: "#4caf50", 2: "#2196f3", 3: "#ff9800", 4: "#e53935"}

col1, col2, col3 = st.columns(3)
col1.metric(t["score"], st.session_state.score)
col2.metric(t["streak"], st.session_state.streak)
col3.markdown(
    f"<div style='text-align:center'>{t['level']}<br>"
    f"<span class='difficulty-badge' style='background-color:{level_colors[level]}22; "
    f"color:{level_colors[level]}; border:1px solid {level_colors[level]}'>{level_name}</span></div>",
    unsafe_allow_html=True,
)

st.divider()

# ---------- QUESTION ----------
q = st.session_state.current
phrase = q[lang]
answer = q["answer"]

st.markdown(f'<div class="phrase-box">"{phrase}"</div>', unsafe_allow_html=True)

options = list(labels.keys())
option_display = [labels[o] for o in options]

choice_display = st.radio(
    t["question_label"], option_display, index=None,
    key=f"choice_{id(q)}_{st.session_state.score}_{st.session_state.streak}"
)
choice = options[option_display.index(choice_display)] if choice_display else None

if not st.session_state.answered:
    if st.button(t["submit"], disabled=choice is None):
        st.session_state.answered = True
        st.session_state.last_correct = (choice == answer)
        if st.session_state.last_correct:
            st.session_state.score += 1
            st.session_state.streak += 1
            if st.session_state.streak % LEVEL_UP_AT == 0 and st.session_state.level < max(QUESTIONS.keys()):
                st.session_state.level += 1
                st.toast(f"⬆️ {t['level']}: {t['levels'][st.session_state.level - 1]}!")
        else:
            st.session_state.streak = 0
            if st.session_state.level > 1:
                st.session_state.level -= 1
        st.rerun()
else:
    if st.session_state.last_correct:
        st.success(f"{t['correct']} **{labels[answer]}** {EMOJIS[answer]}")
    else:
        st.error(f"{t['wrong']} **{labels[answer]}** {EMOJIS[answer]}")

    if st.button(t["next"]):
        new_question()
        st.rerun()

st.divider()
if st.button(t["restart"]):
    start_new_game()
    st.rerun()

 
