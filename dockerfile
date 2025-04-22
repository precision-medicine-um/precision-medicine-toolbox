FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the local requirements file into the container
COPY requirements.txt .

# Install Python packages including FastAPI and uvicorn
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install fastapi uvicorn

# Copy the local code into the container
COPY . .

# Run the FastAPI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
