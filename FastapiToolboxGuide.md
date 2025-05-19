# Precision Medicine Toolbox API Documentation

This document provides step-by-step instructions for setting up, running, and using the Precision Medicine Toolbox API built with FastAPI and Docker.

---

## 📦 1. Prerequisites

Ensure the following are installed on your machine:

- **Docker Desktop** ([Download here](https://www.docker.com/products/docker-desktop))
- Git (to clone the repository)

---

## 🚀 2. Setup Instructions

### Step 1: Clone the Repository (AIDAVA Branch)
```bash
git git clone --branch AIDAVA https://github.com/precision-medicine-um/precision-medicine-toolbox.git
cd precision-medicine-toolbox
```

### Step 2: Directory Structure
Ensure you have a data directory like this:
```
precision-medicine-toolbox/
├── api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── data2/
```

> `data2/` should contain the raw DICOM or NRRD data you want to process.

### Step 3: Update `docker-compose.yml`
Make sure the volume path in your `docker-compose.yml` reflects your local path correctly:
```yaml
services:
  toolbox:
    build: .
    volumes:
      - "C:/absolute/path/to/data2:/app/data"
    environment:
      DATA_PATH: /app/data
      DATA_TYPE: dcm
      MULTI_RTS_PER_PAT: "False"
      TWOD_IMAGE: "True"
      PRE_PROCESSED_PATH: /app/data/preprocessed
      OUT_DICOM_PATH: /app/data/converted_dicoms
    ports:
      - "8000:8000"
```

### Step 4: Build and Run the API
```bash
docker build --no-cache -t precision-medicine-toolbox .
docker compose up --build
```

---

## 🔍 3. Accessing the API

Once the server is running, visit:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Root endpoint: [http://localhost:8000](http://localhost:8000)

---

## 🧪 4. API Endpoints and Usage

### 1. `POST /convert_to_nrrd/`
Converts DICOM files to NRRD format.

**Parameters:**
- `data_path` (str): Path to DICOM data (e.g., `/app/data`)
- `export_path` (str): Output path to store NRRD files
- `data_type` (str, default=`dcm`): Type of input data
- `multi_rts_per_pat` (bool, default=`False`): Whether there are multiple RTStructs per patient
- `twod_image` (bool, default=`True`): If images are 2D

**Example:**
```bash
curl -X POST "http://localhost:8000/convert_to_nrrd/?data_path=/app/data&export_path=/app/data/nrrd"
```

---

### 2. `POST /preprocess/`
Preprocesses NRRD images into a standard format for ML.

**Parameters:**
- `data_path` (str): Path to NRRD data
- `save_path` (str): Where to store preprocessed images

**Example:**
```bash
curl -X POST "http://localhost:8000/preprocess/?data_path=/app/data/nrrd&save_path=/app/data/preprocessed"
```

---

### 3. `POST /convert_nrrd_to_dicom/`
Converts NRRD images back into DICOM format using reference DICOMs.

**Parameters:**
- `nrrd_path` (str): Path to the NRRD files
- `dcm_path` (str): Path to the source/reference DICOM files
- `output_dicom_dir` (str): Where to save converted DICOM files

**Example:**
```bash
curl -X POST "http://localhost:8000/convert_nrrd_to_dicom/?nrrd_path=/app/data/nrrd&dcm_path=/app/data&output_dicom_dir=/app/data/converted_dicoms"
```

---

## 🛑 5. Stopping the API

To stop the API:
```bash
CTRL + C
```
To shut everything down:
```bash
docker compose down
```

---


