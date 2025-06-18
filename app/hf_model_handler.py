from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Model name
model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.model_max_length = 4096  # safely allow up to 4k tokens

model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Set up pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")

def get_answer(context, question):
    # Combine context and question into a prompt
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

    # Truncate prompt if it exceeds 4000 characters (safe cutoff)
    max_prompt_chars = 4000
    if len(prompt) > max_prompt_chars:
        prompt = prompt[-max_prompt_chars:]

    # Generate answer with controlled max_new_tokens
    result = pipe(prompt, num_return_sequences=1, max_new_tokens=512)

    # Extract and return generated text
    answer = result[0]["generated_text"].split("Answer:")[-1].strip()
    return answer
