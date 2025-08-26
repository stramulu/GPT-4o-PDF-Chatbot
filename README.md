# PDF Summarizer & Chatbot

A powerful PDF document analysis tool that uses AI to extract, summarize, and answer questions about PDF content. Built with LangChain and OpenAI models.

## Features

- **PDF Text Extraction**: Extract text from PDF documents using pdfplumber
- **Semantic Search**: Find relevant content using vector embeddings
- **Question Answering**: Ask questions about your PDF content and get AI-powered answers
- **Source Attribution**: See which parts of the PDF were used to generate answers
- **AI-Powered**: Uses OpenAI's latest GPT models for intelligent responses
- **Web Interface**: Streamlit-based web UI for easy interaction

## Prerequisites

- Python 3.8+
- OpenAI API key

## 🛠Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd pdfSummarizer
```

### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

```python
from chatbot import PDFChatbot

# Initialize the chatbot
chatbot = PDFChatbot("path/to/your/document.pdf")

# Ask questions
answer, sources = chatbot.ask("What are the main topics discussed?")
print(f"Answer: {answer}")
print(f"Sources: {sources}")
```

### Web Interface

Run the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## Model Options

- **LLM**: `gpt-4o-mini`, `gpt-3.5-turbo`, `gpt-4`
- **Embeddings**: `text-embedding-3-small`, `text-embedding-ada-002`

## 📁 Project Structure

```
pdfSummarizer/
├── app.py                 # Streamlit web interface
├── chatbot.py            # Main chatbot implementation
├── utils.py              # PDF text extraction utilities
├── requirements.txt      # Dependencies
└── .chromadb/           # Vector database storage
```

## Configuration

### Text Chunking
Adjust chunk size and overlap in the chatbot initialization:
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # Size of each text chunk
    chunk_overlap=200   # Overlap between chunks
)
```

### Retrieval Settings
Modify the number of retrieved documents:
```python
retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
```

## Privacy & Security

- **API Models**: Data is sent to external services
- **Vector Storage**: Embeddings are stored locally in `.chromadb/`

## Future Enhancements

- [ ] Support for more document formats (DOCX, TXT, etc.)
- [ ] Multi-document analysis
- [ ] Custom model fine-tuning
- [ ] Advanced summarization features
- [ ] Export capabilities
- [ ] Batch processing interface

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [OpenAI](https://openai.com/) for GPT models
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Streamlit](https://streamlit.io/) for the web interface
