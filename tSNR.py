import os
import numpy 
from nilearn.maskers import NiftiMasker

data_path = '...'#path to preprocessed fMRI files
save_path = '...'#path to store results
nifti_masker = NiftiMasker(mask_strategy='whole-brain-template',standardize=True)#mask to extract signals
tSNR_all = []


for subject in os.listdir(data_path):
    signal_temp = nifti_masker.fit_transform(os.path.join(data_path,subject))[0:1425,:] #extract fMRI signal during 0-1425 seconds
    signal_average = np.mean(signal_temp,axis=0)
    signal_std = np.std(signal_temp,axis=0)
    tSNR = signal_average/signal_std #to calculate tSNR across the brain
    tSNR_all.append(tSNR)
    tSNR_temp_img = nifti_masker.inverse_transform(tSNR)
    tSNR_temp_img.to_filename(os.path.join(save_path,subject))
    tSNR_averange = np.mean(tSNR_all,axis=0) #average tSNR across subjects
    tSNR_average_img = nifti_masker.inverse_transform(tSNR)
    tSNR_average_img.to_filename(os.path.join(save_path,"average_tSNR.nii"))
