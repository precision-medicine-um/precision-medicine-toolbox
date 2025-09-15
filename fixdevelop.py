from main import convert_to_nrrd, preprocess, convert_nrrd_to_dicom, preprocess_Mamo_Echo


# #  convert dicom to nrrds for processing
# data_path = r'data2\mamo'
# export_path = r'data2\converted_mamo'
# data_type = 'dcm'
# multi_rts_per_pat = False
# twod_image = True
# convert_to_nrrd(data_path, export_path, data_type, multi_rts_per_pat, twod_image)

# # # preprocess the nrrds
# data_path =r'data2\converted_mamo'
# save_path = r'data2\processed_mamo'
# # preprocess(data_path, save_path)
# preprocess_Mamo_Echo(data_path, save_path, modality='mamo')

# # # # # convert processed nrrds to dicoms
# data_path = r'data2\mamo'
# nrrd_path = r'data2\processed_mamo'
# output_dicom_dir = r'data2\converted_dicoms_mamo'
# convert_nrrd_to_dicom(nrrd_path, data_path, output_dicom_dir)



# for echo
#  convert dicom to nrrds for processing
data_path = r'data2\echo'
export_path = r'data2\converted_echo'
data_type = 'dcm'
multi_rts_per_pat = False
twod_image = True
convert_to_nrrd(data_path, export_path, data_type, multi_rts_per_pat, twod_image)

# # preprocess the nrrds
data_path =r'data2\converted_echo'
save_path = r'data2\processed_echo'
# preprocess(data_path, save_path)
preprocess_Mamo_Echo(data_path, save_path, modality='echo')

# # # # convert processed nrrds to dicoms
data_path = r'data2\echo'
nrrd_path = r'data2\processed_echo'
output_dicom_dir = r'data2\converted_dicoms_echo'
convert_nrrd_to_dicom(nrrd_path, data_path, output_dicom_dir)