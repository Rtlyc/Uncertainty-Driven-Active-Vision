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
import math
from scipy.spatial.transform import Rotation as R

DEBUG = True

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
theta = 30  # Change this value to change the number of rotations
y = 180 // theta
x = 360 // theta
idx = 0
output_dir = "../luomo_raw"
output_dir = "luomo_raw"

r'''

# Loop over the rotations
for y_rot in range(1):
    # Create a rotation matrix for the y-axis
    y_mat_rot = np.array([
        [np.cos(np.deg2rad(theta * y_rot)), 0, np.sin(np.deg2rad(theta * y_rot))],
        [0, 1, 0],
        [-np.sin(np.deg2rad(theta * y_rot)), 0, np.cos(np.deg2rad(theta * y_rot))]
    ])
    for x_rot in range(2):
        # Create a rotation matrix for the x-axis
        x_mat_rot = np.array([
            [1, 0, 0],
            [0, np.cos(np.deg2rad(theta * x_rot)), -np.sin(np.deg2rad(theta * x_rot))],
            [0, np.sin(np.deg2rad(theta * x_rot)), np.cos(np.deg2rad(theta * x_rot))]])

        mat_rot = np.dot(y_mat_rot, x_mat_rot)
        if DEBUG: print(f"Rotation matrix: {mat_rot}")
        camera_vec = np.array([0, 0, r])
        camera_vec = np.dot(mat_rot, camera_vec)

        # camera_rot = R.from_quat([0, 0, 0, 1])
        # rotation = R.from_matrix(mat_rot)
        # camera_rot = camera_rot * rotation
        # camera_rot = camera_rot.as_euler("xyz", degrees=True)
        # camera_rot = R.from_euler("xyz", [theta * x_rot, theta * y_rot, 0], degrees=True).as_euler("xyz", degrees=True)

        # camera_rot = R.from_matrix(mat_rot)
        # camera_rot = camera_rot.as_euler("xyz", degrees=True)
        # camera_rot = renderer.cam_from_positions(camera_vec)

        quaternion = R.from_quat([0, 0, 0, 1])
        rotation = R.from_matrix(mat_rot)
        rot_quat = rotation * quaternion
        camera_rot = rot_quat.as_euler("xyz", degrees=True)

        if DEBUG: 
            print(f"Camera position: {camera_vec}")
            print(f"Camera rotation: {camera_rot}")

        renderer.update_camera_pose(camera_vec, camera_rot)

        
        # # Render the scene and save the image
        # image = Image.fromarray(renderer.render())
        # img_name = f"{idx}.png"
        # image.save(os.path.join(output_dir, img_name))
        
        # # Save the camera position and orientation
        # d = {}
        # d['position'] = np.array(camera_vec)
        # d['rotation'] = np.array(camera_rot)
        # npy_name = f"P_{idx}.npy"
        # np.save(os.path.join(output_dir, npy_name), d)
        # idx += 1



'''






import math

def calculate_camera_position_and_orientation(distance, rotation_degree_x, rotation_degree_y):
    # Calculate the camera position
    camera_x = distance * math.sin(math.radians(rotation_degree_y)) * math.cos(math.radians(rotation_degree_x))
    camera_y = distance * math.sin(math.radians(rotation_degree_x))
    camera_z = distance * math.cos(math.radians(rotation_degree_y)) * math.cos(math.radians(rotation_degree_x))
    camera_position = (camera_x, camera_y, camera_z)
    
    # # Calculate the camera orientation (in euler angles)
    # camera_roll = 0
    # camera_pitch = -rotation_degree_x
    # camera_yaw = 180 - rotation_degree_y
    # camera_orientation = (camera_roll, camera_pitch, camera_yaw)
    
    return camera_position

camera_vec = calculate_camera_position_and_orientation(0.8, 190, 0)
camera_rot = renderer.cam_from_positions(np.array(camera_vec))
print(f"Camera position: {camera_vec}")
print(f"Camera rotation: {camera_rot}")
renderer.update_camera_pose(camera_vec, camera_rot)
# Render the scene and save the image
image = Image.fromarray(renderer.render())
img_name = f"{idx}.png"
image.save(os.path.join(output_dir, img_name))


