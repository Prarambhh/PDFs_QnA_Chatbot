# Base image with CUDA for GPU support
FROM pytorch/pytorch:2.2.2-cuda11.8-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app/ui_app.py", "--server.port=8501", "--server.enableCORS=false"]
