# worker.py
import traceback, requests, os
from pmtool.ToolBox import ToolBox
from pathlib import Path
from schemas import ConvertToNRRDJob, PreprocessJob, NrrdToDicomJob

# -------- helpers -------------------------------------------------

def _notify(url: str, payload: dict) -> None:
    """POST the payload to the client; retries once if network hiccups."""
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.RequestException:
        requests.post(url, json=payload, timeout=10)   # one quick retry

def _wrap(job_obj, run_fn):
    """Shared try/except so every job ALWAYS calls the webhook."""
    try:
        output = run_fn(job_obj)           # does the heavy work
        _notify(job_obj.callback_url, {"status": "success", "output": output})
    except Exception as exc:
        _notify(
            job_obj.callback_url,
            {
                "status": "failed",
                "error": str(exc),
                "traceback": traceback.format_exc(limit=3),
            },
        )

# -------- concrete job functions ---------------------------------

def convert_to_nrrd(job: ConvertToNRRDJob):
    def _run(j):
        params = {
            "data_path": j.data_path,
            "data_type": j.data_type,
            "multi_rts_per_pat": j.multi_rts_per_pat,
            "twod_image": j.twod_image,
            "image_only": True,
        }
        ds = ToolBox(**params)
        ds.convert_to_nrrd(j.export_path)
        return j.export_path

    _wrap(job, _run)


def preprocess(job: PreprocessJob):
    def _run(j):
        os.makedirs(j.save_path, exist_ok=True)
        ds = ToolBox(j.data_path, data_type="nrrd", twod_image=True, image_only=True)
        ds.pre_process(
            save_path=j.save_path,
            verbosity=True,
            visualize=False,
            clahe_apply=False,
            z_score=False,
            percentile_scaling=True,
            hist_equalize=False,
        )
        return j.save_path

    _wrap(job, _run)


def nrrd_to_dicom(job: NrrdToDicomJob):
    def _run(j):
        os.makedirs(j.output_dicom_dir, exist_ok=True)
        ds = ToolBox(j.nrrd_path, data_type="nrrd", twod_image=True, image_only=True)
        ds.convert_nrrd_to_dicom(
            nrrd_path=j.nrrd_path, dcm_path=j.dcm_path, output_dicom_dir=j.output_dicom_dir
        )
        return j.output_dicom_dir

    _wrap(job, _run)
