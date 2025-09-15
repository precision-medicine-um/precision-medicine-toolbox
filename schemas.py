# schemas.py
from pydantic import BaseModel, HttpUrl

class ConvertToNRRDJob(BaseModel):
    data_path: str
    export_path: str
    data_type: str = "dcm"
    multi_rts_per_pat: bool = False
    twod_image: bool = True
    callback_url: HttpUrl     # <— NEW

class PreprocessJob(BaseModel):
    data_path: str
    save_path: str
    modality: str = "mamo"  # "mamo" or "echo"
    callback_url: HttpUrl

class NrrdToDicomJob(BaseModel):
    nrrd_path: str
    dcm_path: str
    output_dicom_dir: str
    callback_url: HttpUrl
