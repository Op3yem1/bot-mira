# Mira: RAG-Based Chatbot Assistant

Mira is a Retrieval-Augmented Generation (RAG) chatbot that answers questions about Ope Johnson's professional work experience and background. Powered by [LangChain](https://python.langchain.com/), [Pinecone](https://www.pinecone.io/), and [OpenAI](https://platform.openai.com/), Mira leverages vector search and large language models to provide concise, context-aware responses based on Ope's CV and related documents.

## Features

- **Conversational Q&A**: Ask questions about Ope Johnson's work experience, education, certifications, and more.
- **Contextual Retrieval**: Uses Pinecone vector database to retrieve relevant information from ingested documents.
- **Streamlit UI**: Simple web interface for interactive chat.
- **Secure API Keys**: Uses environment variables for API credentials.

## Project Structure

```
mira/
  .env
  cv-ingestion.py
  cv-retrieval.py
  rag-chatbot.py
  requirements.txt
  documents/
    Certificate.pdf
    My_CV.pdf
    Work_Background.pdf
```

- `rag-chatbot.py`: Main Streamlit app for chatting with Mira.
- `cv-ingestion.py`: Script to ingest work-related documents into Pinecone.
- `cv-retrieval.py`: Script to test retrieval from the vector database.
- `documents/`: Folder containing Ope Johnson's CV and supporting documents.

## Setup

1. **Clone the repository** and navigate to the `mira` directory in your preferred IDE e.g VS Code.

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:

    Create a `.env` file in the `mira` directory with your API keys:
    ```
    PINECONE_API_KEY="your-pinecone-api-key"
    PINECONE_INDEX_NAME="ope-index"
    OPENAI_API_KEY="your-openai-api-key"
    ```

4. **Ingest documents**:

    Place your PDF documents in the `documents/` folder, then run:
    ```sh
    python cv-ingestion.py
    ```

5. **Run the chatbot**:

    ```sh
    python -m streamlit run rag-chatbot.py
    ```

## Usage

- Open the Streamlit app in your browser.
- Type your question about Ope Johnson's professional background.
- Mira will respond with concise, context-based answers.

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [LangChain](https://python.langchain.com/)
- [Pinecone](https://www.pinecone.io/)

## License

This project is for personal and demonstration purposes.

---

For more information, see the code in [rag-chatbot.py](mira/rag-chatbot.py), [cv-ingestion.py](mira/cv-ingestion.py), and [cv-retrieval.py](mira/cv-retrieval.py).
