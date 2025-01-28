import numpy as np
import os
from scipy import stats
from nilearn.maskers import NiftiMasker


data_path = '...'#path to preprocessed fMRI files(HSS or LSS separately)
save_path = '...'#path to store results
nifti_masker = NiftiMasker(mask_strategy='whole-brain-template',standardize=True)#mask to extract signals
signal_average = []
signal_all = []
subject_list = []


for subject in os.listdir(data_path):
    signal_temp = nifti_masker.fit_transform(os.path.join(data_path,subject))[0:1425,:] #extract fMRI signal during 0-1425 seconds
    signal_all.append(signal_temp)
    subject_list.append(subject)

signal_average = np.mean(signal_all,axis=0)

for i in range(np.shape(subject_list)[0]):
    signal_1 = signal_all[i]
    ISC = []
    for j in range(np.shape(subject_list)[0]):
        if i != j:
            ISC_temp = []
            signal_2 = signal_all[j]
            for k in range(np.shape(signal_1)[1]):
                ISC_temp = stats.pearsonr(signal_1[:,k],signal_2[:,k]).statistic
            ISC.append(ISC_temp)
    ISC_average = np.mean(ISC,axis=0)
    np.save(os.path.join(save_path,subject[i]),ISC_average)



