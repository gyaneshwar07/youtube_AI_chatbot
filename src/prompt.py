from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer the user's question ONLY from the provided YouTube transcript context.

If the answer is not available in the context, simply reply:

"I don't know based on the video's transcript."

Context:
{context}

Question:
{question}

Answer:
"""
)