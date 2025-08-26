# app.py

import streamlit as st
from dotenv import load_dotenv
from chatbot import PDFChatbot
import os

# Set Streamlit page config as early as possible
st.set_page_config(page_title="PDF Chatbot", page_icon="📄")

# Load environment variables (.env with OPENAI_API_KEY)
load_dotenv()

st.title("PDF Chatbot")
st.write("Upload a PDF and ask questions about its contents.")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

# Ensure the data directory exists to avoid file write errors
if not os.path.exists("data"):
    os.makedirs("data")

# Main app logic
def main():
    if uploaded_file is not None:
        # Save uploaded PDF to a temporary file
        pdf_path = f"data/{uploaded_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Uploaded `{uploaded_file.name}` successfully!")

        # Build chatbot pipeline
        try:
            chatbot = PDFChatbot(pdf_path)
        except Exception as e:
            error_message = str(e)
            if (
                "api_key client option must be set" in error_message
                or "OPENAI_API_KEY" in error_message
            ):
                st.error(
                    "Failed to initialize chatbot: The OpenAI API key is missing. "
                    "Please set the OPENAI_API_KEY environment variable in your .env file or environment. "
                    "See the documentation for details."
                )
            else:
                st.error(f"Failed to initialize chatbot: {e}")
            return

        # Chat interface
        user_question = st.text_input("Ask a question about the PDF:")

        if user_question:
            with st.spinner("Thinking..."):
                try:
                    answer, sources = chatbot.ask(user_question)
                except Exception as e:
                    st.error(f"Error during question answering: {e}")
                    return

            st.subheader("Answer")
            st.write(answer)

            if sources:
                st.markdown("**Sources:**")
                for src in sources:
                    st.write(f"- {src}")
    else:
        st.info("Please upload a PDF to get started.")

main()
