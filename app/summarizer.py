from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize(text, max_length=300, min_length=100):
    text = text.strip().replace("\n", " ")
    if len(text) > 1024:
        text = text[:1024]
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]