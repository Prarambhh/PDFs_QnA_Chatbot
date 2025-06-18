import os
os.environ["STREAMLIT_WATCH_FILE_CHANGES"] = "false"  # 👈 disable Streamlit's file watcher to fix torch.classes issue
import streamlit as st
import os
import pdf_reader
import text_splitter
import embedder
import vector_db
import hf_model_handler
import summarizer
import metadata_manager
import voice_input

import numpy as np

st.set_page_config(page_title="📖 AI PDF QA Bot", layout="wide")
st.title("📚 Hugging Face PDF QA Bot")

if not os.path.exists("data/pdfs"):
    os.makedirs("data/pdfs")

uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for pdf in uploaded_files:
        with open(os.path.join("data/pdfs", pdf.name), "wb") as f:
            f.write(pdf.read())
    st.success("PDFs uploaded!")

if st.button("Process PDFs"):
    pdf_names, texts = pdf_reader.load_all_pdfs("data/pdfs")
    all_chunks, metadata = [], []

    for idx, text in enumerate(texts):
        chunks = text_splitter.split_text(text)
        all_chunks.extend(chunks)
        metadata.extend([{"pdf": pdf_names[idx], "chunk_index": i, "text": chunk} for i, chunk in enumerate(chunks)])

    embeddings = embedder.generate_embeddings(all_chunks)
    embeddings_np = np.array(embeddings)
    index = vector_db.create_faiss_index(embeddings_np)

    metadata_manager.save_index(index, "data/faiss_index/index.faiss")
    metadata_manager.save_metadata(metadata, "data/faiss_index/metadata.json")
    st.success("✅ PDFs processed and indexed!")

query = st.text_input("Ask a question:")

if st.button("Search Answer"):
    index = metadata_manager.load_index("data/faiss_index/index.faiss")
    metadata = metadata_manager.load_metadata("data/faiss_index/metadata.json")

    query_embedding = embedder.generate_embeddings([query])
    _, indices = vector_db.search_index(index, np.array(query_embedding), top_k=5)

    selected_chunks = [metadata[i]["text"] for i in indices[0]]
    combined_context = "\n\n".join(selected_chunks)

    answer = hf_model_handler.get_answer(combined_context, query)

    st.subheader("📖 Answer:")
    st.success(answer)

    st.subheader("🔍 Relevant Context Chunks:")
    for chunk in selected_chunks:
        st.info(chunk)

if st.button("Summarize PDFs"):
    pdf_names, texts = pdf_reader.load_all_pdfs("data/pdfs")
    for idx, text in enumerate(texts):
        summary = summarizer.summarize(text)
        summary_path = f"data/summaries/{pdf_names[idx]}.txt"
        # Use UTF-8 encoding here
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        st.success(f"Summary saved: {summary_path}")

