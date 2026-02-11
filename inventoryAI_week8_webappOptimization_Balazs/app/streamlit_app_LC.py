import time
import streamlit as st
import os
import html

USE_LANGCHAIN_BACKEND = os.getenv("USE_LANGCHAIN_BACKEND", "0") == "1"

if USE_LANGCHAIN_BACKEND:
    try:
        from backend.answer_langchain import answer_question
    except Exception:
        from backend.answer import answer_question
else:
    from backend.answer import answer_question

# ====================================================== INVENTORY AI\app> streamlit run streamlit_app.py
#  XSS védelem
# ======================================================
def safe_html(text: str) -> str:
    return html.escape(text)

# ======================================================
# UI beállítások
# ======================================================
st.set_page_config(
    page_title="InventoryAI",
    page_icon="🧭",
    layout="wide"
)

# ======================================================
# Stílusok - kurzor módosítás a selectbox-hoz is
# ======================================================
st.markdown("""
<style>
    .main {background-color: #f2f4f7;}
    .top-header {
        background: linear-gradient(90deg, #2d3436, #636e72);
        color: white;
        padding: 28px;
        border-radius: 12px;
        text-align: left;
        margin-bottom: 20px;
    }
    .query-box input {
        border-radius: 12px !important;
        border: 1px solid #ced6e0 !important;
        font-size: 18px !important;
        padding: 14px !important;
    }
    .response-box {
        background: #ffffff;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e0e0e0;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.06);
        font-size: 18px;
        line-height: 1.7;
    }
    .user_msg {
        background:#2d6cdf;
        color:white;
        padding:10px 15px;
        border-radius:12px;
        margin:8px 0;
        max-width:70%;
        align-self:flex-end;
    }
    .bot_msg {
        background:#f0f2f6;
        padding:10px 15px;
        border-radius:12px;
        margin:8px 0;
        max-width:70%;
    }
    div[role="combobox"] {
        cursor: pointer !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# nyelv kiválasztása
# ======================================================
with st.sidebar:
    st.header("⚙️ Beállítások")
    language = st.selectbox("Nyelv / Language", options=["Magyar", "English"], index=0)

# ======================================================
# header
# ======================================================
header_title = "📦 InventoryAI – Leltár Kérdés-Válasz" if language=="Magyar" else "📦 InventoryAI – Inventory Q&A"
header_subtitle = "Intelligens keresés a leltáradatok között (RAG + GPT)" if language=="Magyar" else "Intelligent search across your inventory (RAG + GPT)"

st.markdown(f"""
<div class="top-header">
    <h1 style="margin:0;">{header_title}</h1>
    <p style="margin-top:8px; font-size:18px;">{header_subtitle}</p>
</div>
""", unsafe_allow_html=True)

LOGO_URL = "https://uni-obuda.hu/wp-content/uploads/2021/11/kep3.jpg"
st.logo(LOGO_URL, link="https://uni-obuda.hu", icon_image=LOGO_URL)

# ======================================================
#  Sidebar beállítások
# ======================================================
with st.sidebar:
    top_k_label = "Találatok száma a Qdrantből" if language=="Magyar" else "Number of Qdrant results"
    top_k = st.slider(top_k_label, 1, 10, 5)
    info_text = "A Qdrantból beemelt rekordok száma. Több rekord = részletesebb válasz." if language=="Magyar" else \
                "Number of records fetched from Qdrant. More records = more detailed answer."
    st.info(info_text)

# ======================================================
#  Kérdés mező
# ======================================================
question_label = "Írd be a kérdésed:" if language=="Magyar" else "Enter your question:"
placeholder_text = "Pl.: Hol található a projektor?" if language=="Magyar" else "Ex.: Where is the projector located?"
question = st.text_input(question_label, placeholder=placeholder_text, key="query")

search_button_label = "🔎 Keresés" if language=="Magyar" else "🔎 Search"
search_button = st.button(search_button_label, use_container_width=True)

# ======================================================
#  Chat előzmények kezelése
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================================================
#  Válasz generálás
# ======================================================
if search_button:
    if not question.strip():
        warning_msg = "Előbb írj be egy kérdést!" if language=="Magyar" else "Please enter a question first!"
        st.warning(warning_msg)
    else:
        with st.spinner("Keresés folyamatban..." if language=="Magyar" else "Fetching answer..."):
            answer = answer_question(question, top_k=top_k)

        st.session_state.messages.append({"role":"user", "content":question})
        st.session_state.messages.append({"role":"bot", "content":answer})

        response_placeholder = st.empty()
        displayed_text = ""

        for char in answer:
            displayed_text += char
            safe_text = safe_html(displayed_text)
            response_placeholder.markdown(f"<div class='response-box'>{safe_text}</div>", unsafe_allow_html=True)
            time.sleep(0.002)

# ======================================================
#   Buborékos chat előzmények
# ======================================================
for msg in st.session_state.messages:
    safe_msg = safe_html(msg['content'])
    if msg["role"] == "user":
        st.markdown(f"<div class='user_msg'>{safe_msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot_msg'>{safe_msg}</div>", unsafe_allow_html=True)

# ======================================================
#  További segítség blokk
# ======================================================
help_title = "📞 További segítség" if language=="Magyar" else "📞 Additional help"
help_text = "Ha kérdésed van, vagy a válasz nem volt egyértelmű, keresd az illetékes kollégát:" \
            if language=="Magyar" else "If you have a question or the answer was unclear, contact the responsible colleague:"

st.markdown(f"""
<div style="
    margin-top:20px;
    padding:18px;
    border-radius:10px;
    background:#f0f2f6;
    border-left:5px solid #2d6cdf;
">
    <h4>{help_title}</h4>
    <p>{help_text}</p>
    <a href="https://uni-obuda.hu/telefonkonyv/" target="_blank" style="
        font-size:18px;
        text-decoration:none;
        font-weight:bold;
    ">
        🔗 Óbudai Egyetem telefonkönyv
    </a>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Footer
# ======================================================
footer_text = "© 2025 InventoryAI – Modern UI • Streamlit • RAG + GPT" if language=="Magyar" else \
              "© 2025 InventoryAI – Modern UI • Streamlit • RAG + GPT"
st.write("---")
st.caption(footer_text)
