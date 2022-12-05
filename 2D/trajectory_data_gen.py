# this file serves for generating the nerf dataset based on the trajectory data

"""
1. set up the renderer
2. import mesh
3. iterate through trajectory data
4. sample images and poses
5. save the images and poses
"""

import sys, os
sys.path.insert(0, "../")

from utils import rendering
from PIL import Image
import trimesh
import numpy as np
from scipy.spatial.transform import Rotation as R

# Create a renderer and add the mesh
renderer = rendering.Renderer([128, 128])

# read the trajectory data
action_paths = ["our_output_27"]
all_positions = []
for action_path in action_paths:
    # iterate through files under the action path
    positions = []
    for filename in sorted(os.listdir(action_path)):
        # TODO: check the sequence of the files
        if filename.endswith('.npy'):
            file_path = os.path.join(action_path, filename)
            data = np.load(file_path, allow_pickle=True).item()
            positions.append(data['position'])
            print(file_path)
    all_positions.append(positions)


paths = ["../data/objects/60.obj"]
output_dir = "trajectory_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i, object_path in enumerate(paths):
    # load the object
    renderer.remove_objects()
    mesh = trimesh.load(object_path)
    renderer.add_object(mesh,  add_faces=True)

    # create the output directory
    save_dir = os.path.join(output_dir, str(i))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # iterate through the positions
    sample_num = 10
    radius = 0.8
    sample_positions = [all_positions[i][0]]
    for j in range(len(all_positions[i])-1):
        current_position = all_positions[i][j]
        next_position = all_positions[i][j+1]
        delta_position = next_position - current_position
        for k in range(1, sample_num+1):
            target = current_position + delta_position * (k / (sample_num))
            target = target / np.linalg.norm(target) * radius
            sample_positions.append(target)
    for j, position in enumerate(sample_positions):
        orientation = renderer.cam_from_positions(position)
        renderer.update_camera_pose(position, orientation)
        image = Image.fromarray(renderer.render())
        # save the image
        image.save(os.path.join(save_dir, str(j).zfill(3) + ".png"))
    





