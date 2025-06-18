# 📚 AI PDF Question-Answer Bot (Hugging Face + Streamlit)

A GPU-ready AI bot that can:
- 🔍 Search answers from multiple uploaded PDFs
- 📖 Summarize entire PDFs
- 🎙️ Accept voice input for questions
- 🚀 Run locally or in Docker with GPU acceleration

## 🚀 Features
- Mistral-7B Instruct QA via Hugging Face
- BART summarizer for PDF text
- FAISS vector search for multi-PDF lookup
- Streamlit frontend
- Embedding caching and metadata saving
- Voice input via SpeechRecognition

## 📦 Local Setup

```bash
pip install -r requirements.txt
streamlit run app/ui_app.py
