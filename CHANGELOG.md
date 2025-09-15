# Precision Medicine Toolbox API - Changelog

## Version 2.0.0 - Webhook Integration & API Refactoring

**Release Date:** July 7, 2025

### 🚀 Major Features Added

#### **Webhook Callback System**
- **Asynchronous Processing with Notifications**: All API endpoints now support webhook callbacks to notify clients when long-running operations complete
- **Reliable Delivery**: Automatic retry mechanism for webhook notifications with timeout handling
- **Status Reporting**: Comprehensive status updates including success/failure states and error details
- **Real-time Updates**: Clients receive immediate notifications without polling

#### **Enhanced API Architecture**
- **Modular Design**: Separated concerns into distinct modules (`schemas.py`, `worker.py`, `api.py`)
- **Type Safety**: Full Pydantic model validation for all request/response data
- **HTTP Status Codes**: Proper REST API status codes (202 Accepted for async operations)
- **Background Task Processing**: Improved FastAPI background task implementation

### 📋 API Endpoint Changes

#### **1. Convert to NRRD Endpoint**
- **Endpoint**: `POST /convert_to_nrrd/`
- **Status Code**: `202 Accepted` (previously `200`)
- **New Required Field**: `callback_url` - URL where completion status will be POSTed
- **Response Format**: 
  ```json
  {"detail": "Conversion started – result will be POSTed to callback_url"}
  ```

#### **2. Preprocess Endpoint**
- **Endpoint**: `POST /preprocess/`
- **Status Code**: `202 Accepted` (previously `200`)
- **New Required Field**: `callback_url` - URL where completion status will be POSTed
- **New Optional Field**: `modality` - Processing modality ("mamo" or "echo", default: "mamo")
- **Enhanced Processing**: Now supports modality-specific preprocessing with optimized parameters for mammography and ultrasound imaging
- **Response Format**: 
  ```json
  {"detail": "Pre-processing started – result will be POSTed to callback_url"}
  ```

#### **3. Convert NRRD to DICOM Endpoint**
- **Endpoint**: `POST /convert_nrrd_to_dicom/`
- **Status Code**: `202 Accepted` (previously `200`)
- **New Required Field**: `callback_url` - URL where completion status will be POSTed
- **Response Format**: 
  ```json
  {"detail": "DICOM conversion started – result will be POSTed to callback_url"}
  ```

### 🔧 Technical Improvements

#### **Code Architecture**
- **schemas.py**: Centralized Pydantic models for type-safe API contracts
- **worker.py**: Dedicated module for background task processing and webhook notifications
- **api.py**: Streamlined API endpoints with cleaner separation of concerns
- **api_backup.py**: Preserved original API implementation for rollback purposes

#### **Error Handling**
- **Comprehensive Exception Handling**: All background tasks wrapped with try/catch blocks
- **Detailed Error Reporting**: Error messages include stack traces and contextual information
- **Guaranteed Webhook Delivery**: Webhook notifications sent regardless of task success/failure

### 📊 Webhook Notification Format

#### **Success Notification**
```json
{
  "status": "success",
  "output": "/path/to/output/directory"
}
```

#### **Failure Notification**
```json
{
  "status": "failed",
  "error": "Error description",
  "traceback": "Detailed stack trace (limited to 3 levels)"
}
```

### 🔄 Migration Guide

#### **For Existing Clients**

**Before (v1.x):**
```python
response = requests.post("/convert_to_nrrd/", params={
    "data_path": "/input/path",
    "export_path": "/output/path"
})
# Blocking - had to wait for completion
```

**After (v2.0):**
```python
response = requests.post("/convert_to_nrrd/", json={
    "data_path": "/input/path",
    "export_path": "/output/path",
    "callback_url": "https://your-server.com/webhook/nrrd-complete"
})
# Non-blocking - receive notification at callback_url when done

# For preprocessing with modality selection:
response = requests.post("/preprocess/", json={
    "data_path": "/nrrd/path",
    "save_path": "/output/path",
    "modality": "mamo",  # or "echo"
    "callback_url": "https://your-server.com/webhook/preprocess-complete"
})
```

#### **Setting Up Webhook Endpoint**
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/webhook/nrrd-complete")
async def handle_nrrd_completion(notification: dict):
    if notification["status"] == "success":
        print(f"NRRD conversion completed: {notification['output']}")
    else:
        print(f"NRRD conversion failed: {notification['error']}")
```

### 🛡️ Reliability Features

- **Network Resilience**: Automatic retry mechanism for webhook delivery
- **Timeout Protection**: 10-second timeout for webhook requests
- **Error Isolation**: Task failures don't prevent webhook notifications
- **Process Isolation**: Background tasks run independently of API requests

### 📈 Performance Benefits

- **Non-blocking Operations**: API endpoints return immediately, allowing concurrent processing
- **Resource Efficiency**: Background task processing doesn't block HTTP connections
- **Scalable Architecture**: Clean separation allows for easier horizontal scaling
- **Monitoring Ready**: Structured logging and error reporting for operational monitoring

### 🔍 Breaking Changes

1. **Request Format**: All endpoints now require JSON body instead of query parameters
2. **Required callback_url**: All endpoints now require a webhook URL for notifications
3. **Response Format**: Immediate response with 202 status instead of waiting for completion
4. **Modality Selection**: Preprocess endpoint now supports modality-specific processing ("mamo" or "echo")

### 📝 Files Modified

- **api.py**: Complete refactoring with webhook integration
- **schemas.py**: *(New)* Pydantic models for request validation
- **worker.py**: *(New)* Background task processing with webhook notifications
- **api_backup.py**: *(New)* Backup of original API implementation

### 🎯 Future Enhancements

- **Job Status Endpoint**: Query job status by ID
- **Webhook Authentication**: Support for authenticated webhook endpoints
- **Batch Processing**: Support for multiple file operations in single request
- **Progress Updates**: Intermediate progress notifications for long-running tasks
- **Job Queuing**: Advanced job queue management with priority handling

---

**Note**: This release maintains backward compatibility for the root endpoint (`GET /`) but introduces breaking changes for all processing endpoints. Please update client applications to use the new webhook-based architecture.
