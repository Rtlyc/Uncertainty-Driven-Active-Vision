import sys,os
sys.path.insert(0, "../")

from utils import rendering
from PIL import Image
import trimesh
import numpy as np

# renderer = rendering.Renderer([128, 128])

# # load the object
# object_path = "our_mesh/luomo.obj"
# mesh = trimesh.load(object_path)
# scale = 0.013
# mesh.apply_scale([scale, scale, scale]) 
# renderer.remove_objects()
# renderer.add_object(mesh,  add_faces=True)

# location = renderer.random_position(radius=0.8, num=1, seed=3)
# print(location)
# orientation = renderer.cam_from_positions(location)
# renderer.update_camera_pose(location, orientation)
# image = Image.fromarray(renderer.render())


# image.save('image.png')

import trimesh
import numpy as np
import mathutils
import math

# Load the mesh and scale it
object_path = "our_mesh/luomo.obj"
mesh = trimesh.load(object_path)
scale = 0.013
mesh.apply_scale([scale, scale, scale])

# Create a renderer and add the mesh
renderer = rendering.Renderer([128, 128])
renderer.add_object(mesh,  add_faces=True)

# Define the range of y and x rotations
r = 0.8
theta = 180  # Change this value to change the number of rotations
y = 180 // theta
x = 360 // theta
idx = 0
output_dir = "luomo_raw"

# Loop over the rotations
for y_rot in range(y):
    y_mat_rot = mathutils.Matrix.Rotation(math.radians(theta*y_rot), 4, 'Y')
    for x_rot in range(x):
        x_mat_rot = mathutils.Matrix.Rotation(math.radians(theta*x_rot), 4, 'X')
        mat_rot = y_mat_rot @ x_mat_rot
        
        # Update the camera location and orientation
        camera_vec = mathutils.Vector((0, 0, r))
        camera_vec = mat_rot @ camera_vec 
        camera_rot = renderer.cam_from_positions(camera_vec)

        renderer.update_camera_pose(camera_vec, camera_rot)
        
        # Render the scene and save the image
        image = Image.fromarray(renderer.render())
        img_name = f"{idx}.png"
        image.save(os.path.join(output_dir, img_name))
        
        # Save the camera position and orientation
        d = {}
        d['position'] = np.array(camera_vec)
        d['rotation'] = np.array(camera_rot)
        npy_name = f"P_{idx}.npy"
        np.save(os.path.join(output_dir, npy_name), d)
        idx += 1







