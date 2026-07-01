import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from src.transcript import get_transcript
from src.text_splitter import split_text
from src.vector_store import create_vector_store
from src.retriever import create_retriever
from src.chatbot import ask_question


# Load .env
load_dotenv()


# Streamlit Page Config
st.set_page_config(
    page_title="YouTube AI Chatbot",
    page_icon="🎥",
    layout="wide"
)


st.title("🎥 YouTube AI Chatbot")
st.write("Ask questions about any YouTube video ")


# Create Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# Session State
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "video_processed" not in st.session_state:
    st.session_state.video_processed = False


# -------------------------------
# YouTube URL
# -------------------------------

youtube_url = st.text_input(
    "Paste YouTube URL"
)


# -------------------------------
# Process Video
# -------------------------------

if st.button("Process Video"):

    if youtube_url.strip() == "":
        st.warning("Please enter a YouTube URL.")

    else:

        try:

            with st.spinner("Processing Video..."):

                transcript = get_transcript(youtube_url)

                chunks = split_text(transcript)

                vector_store = create_vector_store(chunks)

                retriever = create_retriever(vector_store)

                st.session_state.retriever = retriever
                st.session_state.video_processed = True

            st.success("✅ Video processed successfully!")

        except Exception as e:

            st.error(str(e))


st.divider()


# -------------------------------
# Question Section
# -------------------------------

question = st.text_input(
    "Ask a Question"
)


if st.button("Ask"):

    if not st.session_state.video_processed:

        st.warning("Please process a YouTube video first.")

    elif question.strip() == "":

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Generating Answer..."):

                answer = ask_question(
                    llm,
                    st.session_state.retriever,
                    question
                )

            st.subheader("Answer")

            st.write(answer)

        except Exception as e:

            st.error(str(e))