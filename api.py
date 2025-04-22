from fastapi import FastAPI, BackgroundTasks
import os
from pmtool.ToolBox import ToolBox

app = FastAPI()

def convert_to_nrrd_task(data_path, export_path, data_type, multi_rts_per_pat, twod_image):
    parameters = {
        'data_path': data_path,
        'data_type': data_type,
        'multi_rts_per_pat': multi_rts_per_pat,
        'twod_image': twod_image,
        'image_only': True
    }
    dataset = ToolBox(**parameters)
    dataset.convert_to_nrrd(export_path)


@app.post("/convert_to_nrrd/")
def convert_to_nrrd_endpoint(background_tasks: BackgroundTasks,
                             data_path: str, 
                             export_path: str,
                             data_type: str = "dcm",
                             multi_rts_per_pat: bool = False,
                             twod_image: bool = True):
    
    background_tasks.add_task(convert_to_nrrd_task, data_path, export_path, data_type, multi_rts_per_pat, twod_image)
    return {"message": "Conversion to NRRD started"}

def preprocess_task(data_path, save_path):
    os.makedirs(save_path, exist_ok=True)
    dataset = ToolBox(data_path, data_type='nrrd', twod_image=True, image_only=True)

    dataset.pre_process(
        save_path=save_path,
        verbosity=True,
        visualize=False,
        clahe_apply=False,
        z_score=False,
        percentile_scaling=True,
        hist_equalize=False,
    )

@app.post("/preprocess/")
def preprocess_endpoint(background_tasks: BackgroundTasks, data_path: str, save_path: str):
    background_tasks.add_task(preprocess_task, data_path, save_path)
    return {"message": "Preprocessing started"}

def convert_nrrd_to_dicom_task(nrrd_path, dcm_path, output_dicom_dir):
    os.makedirs(output_dicom_dir, exist_ok=True)
    dataset = ToolBox(data_path=nrrd_path, data_type='nrrd', twod_image=True, image_only=True)
    dataset.convert_nrrd_to_dicom(nrrd_path=nrrd_path, dcm_path=dcm_path, output_dicom_dir=output_dicom_dir)

@app.post("/convert_nrrd_to_dicom/")
def convert_nrrd_to_dicom_endpoint(background_tasks: BackgroundTasks, nrrd_path: str, dcm_path: str, output_dicom_dir: str):
    background_tasks.add_task(convert_nrrd_to_dicom_task, nrrd_path, dcm_path, output_dicom_dir)
    return {"message": "Conversion to DICOM started"}

@app.get("/")
def root():
    return {"status": "Precision Medicine Toolbox API is running"}
