# app.py
from fastapi import FastAPI, BackgroundTasks, status
from schemas import ConvertToNRRDJob, PreprocessJob, NrrdToDicomJob
from worker import convert_to_nrrd, preprocess, nrrd_to_dicom

app = FastAPI()

@app.post("/convert_to_nrrd/", status_code=status.HTTP_202_ACCEPTED)
async def convert_to_nrrd_endpoint(job: ConvertToNRRDJob, bg: BackgroundTasks):
    bg.add_task(convert_to_nrrd, job)
    return {"detail": "Conversion started – result will be POSTed to callback_url"}

@app.post("/preprocess/", status_code=status.HTTP_202_ACCEPTED)
async def preprocess_endpoint(job: PreprocessJob, bg: BackgroundTasks):
    bg.add_task(preprocess, job)
    return {"detail": "Pre-processing started – result will be POSTed to callback_url"}

@app.post("/convert_nrrd_to_dicom/", status_code=status.HTTP_202_ACCEPTED)
async def convert_nrrd_to_dicom_endpoint(job: NrrdToDicomJob, bg: BackgroundTasks):
    bg.add_task(nrrd_to_dicom, job)
    return {"detail": "DICOM conversion started – result will be POSTed to callback_url"}

@app.get("/")
def root():
    return {"status": "Precision Medicine Toolbox API is running"}
