import streamlit as st
import sys
import os

# =====================================================
# Ajouter backend au PythonPath
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
sys.path.append(BACKEND_DIR)

from rag_engine import ask


# =====================================================
# Custom CSS (belles bulles de chat)
# =====================================================
def load_css():
    st.markdown("""
    <style>

    /* Page background */
    .main {
        background-color: #f4f6f9;
    }

    /* Chat container */
    .chat-bubble {
        padding: 12px 18px;
        margin: 10px 0;
        border-radius: 15px;
        max-width: 80%;
        font-size: 16px;
        line-height: 1.5;
    }

    /* User bubble */
    .user-bubble {
        background-color: #d1e7ff;
        margin-left: auto;
        border-bottom-right-radius: 2px;
    }

    /* Assistant bubble */
    .bot-bubble {
        background-color: #ffffff;
        border: 1px solid #dedede;
        margin-right: auto;
        border-bottom-left-radius: 2px;
    }

    /* Avatars */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 20px;
        object-fit: cover;
        margin-right: 8px;
        border: 2px solid #dedede;
    }

    .msg-container {
        display: flex;
        align-items: flex-start;
        margin-bottom: 15px;
    }

    .msg-container-user {
        display: flex;
        flex-direction: row-reverse;
        align-items: flex-start;
        margin-bottom: 15px;
    }

    </style>
    """, unsafe_allow_html=True)


# =====================================================
# Streamlit UI
# =====================================================
st.set_page_config(page_title="Assistant Juridique", page_icon="⚖️", layout="centered")
load_css()

st.title("⚖️ Assistant Juridique Tunisien — Interface Moderne")
st.write("Posez vos questions concernant la Constitution ou le Code du Statut Personnel.")

# Avatars
avatar_user = "https://cdn-icons-png.flaticon.com/512/1946/1946429.png"
avatar_bot = "https://cdn-icons-png.flaticon.com/512/4712/4712105.png"

# Historique
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Afficher historique avec bulles modernes
for msg in st.session_state["messages"]:
    role, content = msg

    if role == "user":
        st.markdown(
            f"""
            <div class="msg-container-user">
                <img src="{avatar_user}" class="avatar">
                <div class="chat-bubble user-bubble">{content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="msg-container">
                <img src="{avatar_bot}" class="avatar">
                <div class="chat-bubble bot-bubble">{content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Champ de texte
question = st.text_input("Votre question :", "")

if st.button("Envoyer"):
    if question.strip():
        st.session_state["messages"].append(("user", question))

        with st.spinner("Analyse des textes juridiques…"):
            response = ask(question)

        st.session_state["messages"].append(("assistant", response))

        st.rerun()
