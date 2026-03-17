# Rag-Chatbot-Custom-Code-Library-Assistant
AI-powered RAG chatbot trained on a custom Angular component library to generate accurate Angular code using project-specific wrapper components instead of Angular Material.



This project is an AI-powered RAG (Retrieval Augmented Generation) chatbot designed to assist developers by generating accurate Angular code based on a custom Angular component library.

Unlike traditional AI coding assistants, this system is trained on a project's internal UI library and documentation. It ensures that all generated code strictly follows the project's architecture, coding conventions, and custom wrapper components.

The assistant understands and generates Angular code using custom components such as:

- lib-button
- lib-text-field
- lib-date-picker
- lib-time-picker
- lib-week
- other internal UI components

instead of directly using Angular Material components.

## Key Features

- RAG-based architecture for context-aware responses
- Trained on a custom Angular component library
- Semantic search using FAISS vector database
- Context retrieval from project documentation
- AI responses powered by Groq LLM
- FastAPI backend for chatbot API
- Angular-focused coding assistant

## Tech Stack

- Python
- FastAPI
- LangChain
- FAISS Vector Database
- HuggingFace Embeddings
- Groq LLM
- Retrieval Augmented Generation (RAG)

## How It Works

1. Project documentation and library code are converted into text datasets.
2. The system creates embeddings using HuggingFace models.
3. FAISS stores vectors for fast similarity search.
4. When a user asks a question, relevant context is retrieved.
5. The LLM generates responses using both the prompt and retrieved context.

## Use Case

This assistant helps developers:

- Understand internal component libraries
- Generate Angular code aligned with project standards
- Avoid incorrect usage of Angular Material
- Speed up development in large enterprise Angular projects

## Future Improvements

- Chat history and conversation memory
- Streaming responses
- GitHub repository ingestion
- Automatic codebase training
- Web-based chat UI



https://github.com/user-attachments/assets/5b6868fe-944f-47a3-87ac-32494038d932

