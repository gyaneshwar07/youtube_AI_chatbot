from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(transcript):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = splitter.create_documents([transcript])

    return chunks