FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed by SimpleITK and your app
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    cmake \
    git \
    curl \
    zlib1g-dev \
    libexpat1-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install SimpleITK first (try a version with prebuilt wheels)
RUN pip install SimpleITK==2.4.0

# Install FastAPI and Uvicorn (you can keep this here or move to requirements.txt)
RUN pip install "fastapi[all]" "uvicorn[standard]"
RUN pip install packaging
# Install the rest of requirements without dependencies (to avoid reinstalling SimpleITK)
RUN pip install -r requirements.txt 

# Copy all other files
COPY . .

# Command to run your FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
