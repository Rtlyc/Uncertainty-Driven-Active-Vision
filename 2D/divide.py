import os
import shutil

# Set the directory containing the images
img_dir = 'luomo_raw'

# Set the destination directory for the folders
dest_dir = 'luomo'

# Iterate through the images and copy them to the destination in groups of 5
group_size = 6
for i in range(0, 600):
    img_name = str(i) + '.png'
    npy_name = "P_" + str(i) + '.npy'
    img_path = os.path.join(img_dir, img_name)
    npy_path = os.path.join(img_dir, npy_name)
    if i % group_size == 0:
        folder_name =  str((i + group_size-1) // group_size)
        folder_path = os.path.join(dest_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    shutil.copy(img_path, folder_path)
    shutil.copy(npy_path, folder_path)
    new_image_name = os.path.join(folder_path, str(i%group_size)+'.png')
    new_npy_name = os.path.join(folder_path, "P_" + str(i%group_size)+'.npy')
    os.rename(os.path.join(folder_path, img_name), new_image_name)
    os.rename(os.path.join(folder_path, npy_name), new_npy_name)
