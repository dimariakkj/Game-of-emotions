import streamlit as st
import random

st.set_page_config(page_title="Mirror of Emotions", page_icon="🎭", layout="centered")

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
        "title": "🎭 Mirror of Emotions",
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
        "title": "🎭 espelho das emoções",
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

    1: [  # Easy — clear and obvious

        {"en": "I got the best birthday present ever!", "pt": "Ganhei o melhor presente de aniversário de todos!", "answer": "Happy"},

        {"en": "Someone ruined my favorite shirt.", "pt": "Alguém estragou minha camisa favorita.", "answer": "Angry"},

        {"en": "I wish my best friend were here with me.", "pt": "Queria que meu melhor amigo estivesse aqui comigo.", "answer": "Sad"},

        {"en": "I heard a strange noise coming from downstairs.", "pt": "Ouvi um barulho estranho vindo do andar de baixo.", "answer": "Scared"},

        {"en": "Wait... you actually remembered my birthday?", "pt": "Espera... você realmente lembrou do meu aniversário?", "answer": "Surprised"},

        {"en": "I can't stop smiling after hearing the good news.", "pt": "Não consigo parar de sorrir depois de ouvir a boa notícia.", "answer": "Happy"},

        {"en": "Nobody came to the event like they said they would.", "pt": "Ninguém veio ao evento como disseram que viriam.", "answer": "Sad"},

        {"en": "I saw a shadow moving behind the curtain.", "pt": "Vi uma sombra se mexendo atrás da cortina.", "answer": "Scared"},

    ],

    2: [  # Medium — recognizable, but requires some interpretation

        {"en": "You used my computer without even asking me first.", "pt": "Você usou meu computador sem nem me perguntar antes.", "answer": "Angry"},

        {"en": "I kept looking at the clock while waiting for them to arrive.", "pt": "Fiquei olhando para o relógio enquanto esperava eles chegarem.", "answer": "Anxious"},

        {"en": "Everyone suddenly started clapping when I walked into the room.", "pt": "Todo mundo começou a bater palmas quando entrei na sala.", "answer": "Surprised"},

        {"en": "She got the award I had been hoping to win.", "pt": "Ela ganhou o prêmio que eu esperava ganhar.", "answer": "Jealous"},

        {"en": "I shouldn't have said that about him. I feel terrible.", "pt": "Eu não deveria ter falado aquilo sobre ele. Estou me sentindo péssimo.", "answer": "Guilty"},

        {"en": "I practiced my presentation five times, but my stomach still feels weird.", "pt": "Pratiquei minha apresentação cinco vezes, mas meu estômago ainda está estranho.", "answer": "Anxious"},

        {"en": "I couldn't stop thinking about how everyone laughed when I answered.", "pt": "Não conseguia parar de pensar em como todos riram quando respondi.", "answer": "Embarrassed"},

        {"en": "I couldn't believe they chose me for the team.", "pt": "Não conseguia acreditar que me escolheram para o time.", "answer": "Happy"},

    ],

    3: [  # Hard — indirect, requires inference

        {"en": "I smiled when she showed me the trophy, but I suddenly became very quiet.", "pt": "Sorri quando ela me mostrou o troféu, mas de repente fiquei muito quieto.", "answer": "Jealous"},

        {"en": "I typed a message, deleted it, typed another one, and checked the phone again.", "pt": "Digitei uma mensagem, apaguei, escrevi outra e olhei o celular novamente.", "answer": "Anxious"},

        {"en": "Nobody said anything after my joke, so I pretended to laugh.", "pt": "Ninguém falou nada depois da minha piada, então fingi que estava rindo.", "answer": "Embarrassed"},

        {"en": "I knew I shouldn't have taken it, but I did it anyway.", "pt": "Eu sabia que não deveria ter pegado, mas mesmo assim peguei.", "answer": "Guilty"},

        {"en": "I didn't say much during the ceremony, but I couldn't stop smiling.", "pt": "Não falei muito durante a cerimônia, mas não conseguia parar de sorrir.", "answer": "Proud"},

        {"en": "They were all invited except me. I told myself it didn't matter.", "pt": "Todos foram convidados menos eu. Disse a mim mesmo que não importava.", "answer": "Jealous"},

        {"en": "I kept thinking about tomorrow even though there was nothing left to prepare.", "pt": "Fiquei pensando no dia seguinte mesmo não tendo mais nada para preparar.", "answer": "Anxious"},

        {"en": "I wanted to disappear when I realized everyone had heard what I said.", "pt": "Queria desaparecer quando percebi que todos tinham ouvido o que eu disse.", "answer": "Embarrassed"},

    ],

    4: [  # Expert — very subtle, context and tone are important

        {"en": "I told everyone I was happy for him, and I really tried to mean it.", "pt": "Disse a todos que estava feliz por ele, e realmente tentei falar sério.", "answer": "Jealous"},

        {"en": "I put the medal away somewhere safe, but I still look at it whenever I need motivation.", "pt": "Guardei a medalha em um lugar seguro, mas ainda olho para ela quando preciso de motivação.", "answer": "Proud"},

        {"en": "I apologized before anyone even asked me what happened.", "pt": "Pedi desculpas antes mesmo de alguém perguntar o que aconteceu.", "answer": "Guilty"},

        {"en": "I laughed when everyone else did, even though I wanted the conversation to end.", "pt": "Ri quando todo mundo riu, mesmo querendo que a conversa acabasse.", "answer": "Embarrassed"},

        {"en": "I said 'don't worry about it,' then spent the next hour wondering if they were upset with me.", "pt": "Disse 'não se preocupe com isso', mas passei a próxima hora pensando se estavam chateados comigo.", "answer": "Anxious"},

        {"en": "I wasn't expecting them to remember something I had mentioned only once.", "pt": "Eu não esperava que eles lembrassem de algo que mencionei apenas uma vez.", "answer": "Surprised"},

        {"en": "I didn't tell anyone about the result, but I kept looking at it with a smile.", "pt": "Não contei a ninguém sobre o resultado, mas continuei olhando para ele com um sorriso.", "answer": "Proud"},

        {"en": "I said it was no big deal, but I couldn't stop thinking about what happened.", "pt": "Disse que não era nada demais, mas não conseguia parar de pensar no que aconteceu.", "answer": "Sad"},

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

 
