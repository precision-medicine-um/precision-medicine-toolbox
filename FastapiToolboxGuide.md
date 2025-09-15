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
git clone --branch AIDAVA https://github.com/precision-medicine-um/precision-medicine-toolbox.git
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
# Build the Docker image
docker build -t precision-medicine-toolbox .

# Option 1: Run in foreground (you'll see logs)
docker compose up

# Option 2: Run in background (detached mode)
docker compose up -d
```

### Step 5: Verify the API is Running
```bash
# Test the root endpoint
curl http://localhost:8000/

# Expected response:
# {"status":"Precision Medicine Toolbox API is running"}
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
- `callback_url` (str): Webhook URL for completion notification

**Example:**
```bash
curl -X POST "http://localhost:8000/convert_to_nrrd/" \
  -H "Content-Type: application/json" \
  -d '{
    "data_path": "/app/data/mamo",
    "export_path": "/app/data/mamo_nrrd",
    "data_type": "dcm",
    "multi_rts_per_pat": false,
    "twod_image": true,
    "callback_url": "https://httpbin.org/post"
  }'
```

**Expected Response:**
```json
{"detail": "Conversion started – result will be POSTed to callback_url"}
```

---

### 2. `POST /preprocess/`
Preprocesses NRRD images into a standard format for ML with modality-specific parameters.

**Parameters:**
- `data_path` (str): Path to NRRD data
- `save_path` (str): Where to store preprocessed images
- `modality` (str, default=`mamo`): Processing modality - either "mamo" for mammography or "echo" for ultrasound
- `callback_url` (str): Webhook URL for completion notification

**Example:**
```bash
# For Mammography preprocessing
curl -X POST "http://localhost:8000/preprocess/" \
  -H "Content-Type: application/json" \
  -d '{
    "data_path": "/app/data/mamo_nrrd",
    "save_path": "/app/data/mamo_nrrd_processed",
    "modality": "mamo",
    "callback_url": "https://httpbin.org/post"
  }'


**Expected Response:**
```json
{"detail": "Pre-processing started – result will be POSTed to callback_url"}
```

---

### 3. `POST /convert_nrrd_to_dicom/`
Converts NRRD images back into DICOM format using reference DICOMs.

**Parameters:**
- `nrrd_path` (str): Path to the NRRD files
- `dcm_path` (str): Path to the source/reference DICOM files
- `output_dicom_dir` (str): Where to save converted DICOM files
- `callback_url` (str): Webhook URL for completion notification

**Example:**
```bash
curl -X POST "http://localhost:8000/convert_nrrd_to_dicom/" \
  -H "Content-Type: application/json" \
  -d '{
    "nrrd_path": "/app/data/mamo_nrrd_processed",
    "dcm_path": "/app/data/mamo,
    "output_dicom_dir": "/app/data/mamo_nrrd_processed_dcm",
    "callback_url": "https://httpbin.org/post"
  }'
```

**Expected Response:**
```json
{"detail": "DICOM conversion started – result will be POSTed to callback_url"}
```

---

## 🛑 5. Stopping the API

To stop the API:
```bash
# If running in foreground mode
CTRL + C

# If running in detached mode
docker compose down
```

---

## 📋 6. Webhook Responses

All endpoints use webhooks for asynchronous processing. Your callback URL will receive:

**Success Response:**
```json
{
  "status": "success",
  "output": "/app/data/nrrd"
}
```

**Error Response:**
```json
{
  "status": "failed",
  "error": "Error description",
  "traceback": "Detailed stack trace"
}
```

---

## 🔧 7. Troubleshooting

### Common Issues:

1. **Docker not running:**
   ```bash
   # Check if Docker is running
   docker --version
   docker info
   ```

2. **Port 8000 already in use:**
   ```bash
   # Check what's using port 8000
   netstat -ano | findstr :8000
   # Kill the process or change port in docker-compose.yml
   ```

3. **Volume path issues:**
   - Ensure the path in `docker-compose.yml` matches your actual data directory
   - Use forward slashes `/` even on Windows
   - Use absolute paths

4. **API not responding:**
   ```bash
   # Check container status
   docker compose ps
   
   # View container logs
   docker compose logs
   ```

### Data Structure Requirements:

Your `data2/` directory should be organized like:
```
data2/
├── mamo/
│   └── cmmd_d2_0749/
│       └── [DICOM files]
└── echo/
    └── echo1/
        └── [DICOM files]
```

---


