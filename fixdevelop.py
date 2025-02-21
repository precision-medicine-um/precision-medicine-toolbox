from main import convert_to_nrrd, preprocess, convert_nrrd_to_dicom


#  convert dicom to nrrds for processing
# data_path = r'data2\dcms2'
# export_path = r'data2'
# data_type = 'dcm'
# multi_rts_per_pat = False
# twod_image = True
# convert_to_nrrd(data_path, export_path, data_type, multi_rts_per_pat, twod_image)

# preprocess the nrrds
data_path =r'data2\converted_nrrds'
save_path = r'data2\preprocessed'
preprocess(data_path, save_path)

# # # convert processed nrrds to dicoms
data_path = r'data2\dcms2'
nrrd_path = r'data2\preprocessed'
output_dicom_dir = r'data2\converted_dicoms'
convert_nrrd_to_dicom(nrrd_path, data_path, output_dicom_dir)