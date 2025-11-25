# Multi-stage build for Face Recognition Attendance System
FROM python:3.9-bullseye

# Install system dependencies including OpenGL libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgomp1 \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir streamlit

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p TrainingImage TrainingImageLabel StudentDetails Attendance

# Expose port for Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--logger.level=info"]
