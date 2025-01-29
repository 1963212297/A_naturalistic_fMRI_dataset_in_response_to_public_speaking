import nilearn
from nilearn import plotting,surface,image
import nibabel as nb
import numpy as np
import os
import re
import scipy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.colors as mcolors

data_path = '..'#path to statistic images, e.g. average ISC map
save_path = '..'


lh_inflated = surface.load_surf_mesh("./Parcellations/FreeSurfer5.3/fsaverage5/surf/lh.inflated")
lh_pial = surface.load_surf_mesh("./Parcellations/FreeSurfer5.3/fsaverage5/surf/lh.pial")
rh_inflated = surface.load_surf_mesh("./Parcellations/FreeSurfer5.3/fsaverage5/surf/rh.inflated")
rh_pial = surface.load_surf_mesh("./Parcellations/FreeSurfer5.3/fsaverage5/surf/rh.pial")
labels_l, ctab_l, names_l = nb.freesurfer.io.read_annot("./Parcellations/FreeSurfer5.3/fsaverage5/label/lh.Schaefer2018_400Parcels_7Networks_order.annot")
labels_r, ctab_r, names_r = nb.freesurfer.io.read_annot("./Parcellations/FreeSurfer5.3/fsaverage5/label/rh.Schaefer2018_400Parcels_7Networks_order.annot")
labels = np.concatenate((labels_l,labels_r))
loc_l = 0.25*lh_pial[0]+0.75*lh_inflated[0] #adjust surf mesh
loc_r = 0.25*rh_pial[0]+0.75*rh_inflated[0]
surf_l = [loc_l, lh_pial[1]]
surf_r = [loc_r, rh_pial[1]]
surf_mesh = [surf_l,surf_r]  
view = ['lateral','medial']
hemisphere = ['left','right']

viridis = cm.get_cmap('viridis', 198) #colormap of the surface
red = cm.get_cmap('OrRd',56)
newcolors = np.vstack((black,grey,viridis(np.linspace(0,1,198)),red(np.linspace(0,1,56))))
newcmp = ListedColormap(newcolors)

img = image.load_img(data_path) #load the image
lh_surf = surface.vol_to_surf(img, lh_pial)
rh_surf = surface.vol_to_surf(img, rh_pial)
surf_data = [lh_surf,rh_surf]
for i in range(2):
    for j in range(2):  
        if i ==0 and j == 0:
            plotting.plot_surf(surf_mesh[i],surf_data[i],view=view[j],cmap=newcmp,engine='plotly',vmax=1,vmin=-1,
                                colorbar=True,title='..',
                                output_file=save_path+'/'+hemisphere[i]+'_'+ view[j] +'.png')
        else:
            plotting.plot_surf(surf_mesh[i],surf_data[i],view=view[j],cmap=newcmp,engine='plotly',vmax=1,vmin=-1,
                                       output_file=save_path+hemisphere[i]+'_'+ view[j] +'.png')