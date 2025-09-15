import os
import argparse
from pmtool.ToolBox import ToolBox


def convert_to_nrrd(data_path, export_path, data_type, multi_rts_per_pat, twod_image):
    parameters = {
        'data_path': data_path,
        'data_type': data_type,
        'multi_rts_per_pat': multi_rts_per_pat,
        'twod_image': twod_image,
        'image_only': True
    }
    dataset = ToolBox(**parameters)
    dataset.convert_to_nrrd(export_path)


def preprocess(data_path, save_path):
    os.makedirs(save_path, exist_ok=True)

    parameters = {'data_path': data_path,  # path to your DICOM data
                  'data_type': 'nrrd',
                  'multi_rts_per_pat': False,
                  'twod_image': True}  # when False, it will look only

    mg_nnrd = ToolBox(data_path, data_type='nrrd', twod_image='True',image_only='True')

    mg_nnrd.pre_process(
        save_path=save_path,
        verbosity=True,
        visualize=False,
        clahe_apply=False,
        z_score = False,
        percentile_scaling=True,
        hist_equalize=False,
        # clahe_clip_limit=2.0,
        # clahe_tile_grid_size=(8, 8)
    )

def preprocess_Mamo_Echo(data_path, save_path, modality='mamo'):
    os.makedirs(save_path, exist_ok=True)
    echo_params = {
    "denoise":   {"enabled": False, "method": "log_aniso", "iterations": 5, "conductance": 3.0, "time_step": 0.0625},
    "contrast":  {"enabled": False, "method": "percentile_stretch", "stretch_low": 5.0, "stretch_high": 95.0},
    "sharpen":   {"enabled": False, "sigma": 1.0, "amount": 1.3, "threshold": 0.02},
    "postprocess": {"opening_enabled": False, "opening_radius": 1},
    "normalize": {"enabled": False, "method": "none"},
    }
    mamo_params = dict(
                            denoise=dict(
                                enabled=True,
                                method="median",        # "median" or "gaussian"
                                median_radius=(2, 2)    # small radius to avoid harming microcalcifications
                            ),
                            contrast=dict(
                                enabled=True,
                                method="percentile_stretch",         # "clahe", "gentle_gamma", or "percentile_stretch"
                                clahe_radius=(32, 32),  # Increased radius for gentler local enhancement
                                alpha=0.3,              # Higher alpha for more conservative enhancement
                                beta=0.05,              # Much lower beta for subtle clipping
                                stretch_low=0.5,        # percentiles for global stretch
                                stretch_high=99.5,
                                gamma=0.8               # for gentle_gamma method
                            ),
                            sharpen=dict(
                                enabled=True,
                                sigma=0.5,              # slightly smaller sigma for high-res MG
                                amount=1.2,
                                threshold=0.0
                            ),
                            normalize=dict(
                                enabled=True,
                                method="rescale_uint8",
                                perc_low=0.5,
                                perc_high=99.5
                            )
                        )


    mg_nnrd = ToolBox(data_path, data_type='nrrd', twod_image='True',image_only='True')
    if modality == 'mamo':
        mg_nnrd.pre_process_MAMO(save_path=save_path, mg_params=mamo_params, verbosity=True)
    elif modality == 'echo':
        mg_nnrd.pre_process_ECHO(save_path=save_path, us_params=echo_params, verbosity=True)
    else:
        raise ValueError("Unsupported modality. Choose 'mamo' or 'echo'.")
    
  




def convert_nrrd_to_dicom(nrrd_path, dcm_path, output_dicom_dir):
    os.makedirs(output_dicom_dir, exist_ok=True)

    dataset = ToolBox(data_path=nrrd_path, data_type='nrrd', twod_image='True',image_only='True')
    dataset.convert_nrrd_to_dicom(nrrd_path=nrrd_path,dcm_path=dcm_path, output_dicom_dir=output_dicom_dir)


def main():
    parser = argparse.ArgumentParser(description="Run different functions of the Toolbox.")
    subparsers = parser.add_subparsers(dest="command")

    #  convert_to_nrrd
    parser_convert = subparsers.add_parser("convert_to_nrrd")
    parser_convert.add_argument("--data_path", required=True, help="Path to the DICOM data")
    parser_convert.add_argument("--export_path", required=True, help="Path to save the converted NRRD files")
    parser_convert.add_argument("--data_type", default="dcm", help="Type of the data (default: dcm)")
    parser_convert.add_argument("--multi_rts_per_pat", type=bool, default=False,
                                help="Multiple RTStruct per patient (default: False)")
    parser_convert.add_argument("--twod_image", type=bool, default=True, help="2D images (default: True)")

    # preprocess
    parser_preprocess = subparsers.add_parser("preprocess")
    parser_preprocess.add_argument("--data_path", required=True, help="Path to the NRRD data")
    parser_preprocess.add_argument("--save_path", required=True, help="Path to save the preprocessed images")
    parser_preprocess.add_argument("--modality", default="mamo", choices=["mamo", "echo"], 
                                   help="Modality to preprocess (default: mamo)")

    # preprocess_mamo_echo
    parser_preprocess_me = subparsers.add_parser("preprocess_mamo_echo")
    parser_preprocess_me.add_argument("--data_path", required=True, help="Path to the NRRD data")
    parser_preprocess_me.add_argument("--save_path", required=True, help="Path to save the preprocessed images")
    parser_preprocess_me.add_argument("--modality", default="mamo", choices=["mamo", "echo"], 
                                      help="Modality to preprocess (default: mamo)")

    #  convert_nrrd_to_dicom
    parser_convert_back = subparsers.add_parser("convert_nrrd_to_dicom")
    parser_convert_back.add_argument("--data_path", required=True, help="Path to the DICOM data")
    parser_convert_back.add_argument("--nrrd_path", required=True, help="Path to the NRRD data")
    parser_convert_back.add_argument("--output_dicom_dir", required=True, help="Path to save the converted DICOM files")

    args = parser.parse_args()

    if args.command == "convert_to_nrrd":
        convert_to_nrrd(args.data_path, args.export_path, args.data_type, args.multi_rts_per_pat, args.twod_image)
    elif args.command == "preprocess":
        preprocess_Mamo_Echo(args.data_path, args.save_path, args.modality)
    elif args.command == "preprocess_mamo_echo":
        preprocess_Mamo_Echo(args.data_path, args.save_path, args.modality)
    elif args.command == "convert_nrrd_to_dicom":
        convert_nrrd_to_dicom(args.nrrd_path, args.data_path, args.output_dicom_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
