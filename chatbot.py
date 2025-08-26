# chatbot.py

import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from utils import extract_text_from_pdf

class PDFChatbot:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self._ensure_openai_api_key()
        self.vectorstore = self._build_vectorstore()
        self.qa_chain = self._build_qa_chain()

    def _ensure_openai_api_key(self):
        """
        Ensure that the OPENAI_API_KEY environment variable is set.
        Raise a clear error if not set.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or not api_key.strip():
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it in your environment or in a .env file."
            )

    def _build_vectorstore(self):
        """Extract text from PDF, split into chunks, embed, and store in ChromaDB."""
        text = extract_text_from_pdf(self.pdf_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)

        docs = [Document(page_content=chunk, metadata={"source": self.pdf_path})
                for chunk in chunks]

        # Pass the API key explicitly if needed
        api_key = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
        vectorstore = Chroma.from_documents(docs, embedding=embeddings, persist_directory=".chromadb")
        return vectorstore

    def _build_qa_chain(self):
        """Create a RetrievalQA pipeline using GPT + Chroma retriever."""
        api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=True,
        )
        return qa

    def ask(self, query: str):
        """Answer a user query with sources."""
        result = self.qa_chain.invoke(query)
        answer = result["result"]

        sources = []
        if "source_documents" in result:
            sources = list({doc.metadata.get("source", "Unknown") for doc in result["source_documents"]})

        return answer, sources