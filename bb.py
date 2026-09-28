import streamlit as st
import ollama 
st.title("Friendly AI Bot")
st.write("Ask me anything!")
question = st.text_input("Enter your question:")
if st.button("Ask AI"):
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": """
                You are a friendly and funny AI assistant.Explain things in simple language.Be helpful and encouraging."""
            },
            {
                "role": "user",
                "content": question
            }

        ]
    )
    answer = response["message"]["content"]
    st.write("AI Response")
    st.write(answer)