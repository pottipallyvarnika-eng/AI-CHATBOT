import streamlit as st
import ollama
from pypdf import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Friendly AI Bot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
}

.block-container {
    max-width: 850px;
    padding-top: 35px;
}

.title {
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #eeeeee;
    font-size: 17px;
    margin-bottom: 25px;
}

.user-message {
    background: white;
    color: #333333;
    padding: 15px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 12px 0 12px 80px;
}

.ai-message {
    background: rgba(255,255,255,0.18);
    color: white;
    padding: 15px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 12px 80px 12px 0;
}

.footer {
    text-align: center;
    color: #eeeeee;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">🤖 Friendly AI Bot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Chat with AI and ask questions from your PDF</div>',
    unsafe_allow_html=True
)


# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""


# ---------------- PDF UPLOAD ----------------
st.subheader("📄 Upload a PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


# ---------------- READ PDF ----------------
if uploaded_file is not None:

    if st.button("📖 Read PDF"):

        try:

            reader = PdfReader(uploaded_file)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            st.session_state.pdf_text = text

            st.success("✅ PDF loaded successfully!")

            st.info(
                f"📄 Pages: {len(reader.pages)} | "
                f"Characters extracted: {len(text)}"
            )

        except Exception as e:

            st.error(f"Error reading PDF: {e}")


# ---------------- SHOW PDF STATUS ----------------
if st.session_state.pdf_text:

    st.success("🟢 PDF is ready. You can ask questions about it.")


# ---------------- CHAT HISTORY ----------------
for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                👤 <b>You</b><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-message">
                🤖 <b>AI</b><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------- QUESTION ----------------
question = st.text_input(
    "💬 Ask your question:",
    placeholder="Example: What is this PDF about?"
)


# ---------------- ASK AI ----------------
if st.button("✨ Ask AI"):

    if not question.strip():

        st.warning("⚠️ Please enter a question.")

    else:

        # Add question to history
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Create prompt
        if st.session_state.pdf_text:

            # Limit context to avoid sending extremely large PDFs
            pdf_context = st.session_state.pdf_text[:15000]

            prompt = f"""
You are a helpful AI assistant.

Answer the user's question using the PDF content below.

If the answer is not available in the PDF, clearly say:
"I couldn't find this information in the uploaded PDF."

Explain the answer in simple language.

PDF CONTENT:
{pdf_context}

USER QUESTION:
{question}
"""

        else:

            prompt = question


        # ---------------- OLLAMA ----------------
        with st.spinner("🤔 AI is thinking..."):

            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly assistant. "
                            "Explain things in simple language. "
                            "Be helpful and encouraging."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )


        answer = response["message"]["content"]


        # Add AI answer
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()


# ---------------- CLEAR CHAT ----------------
if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">Powered by Ollama • Llama 3.2 • PDF AI 🚀</div>',
    unsafe_allow_html=True
)