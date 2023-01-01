import sys,os
sys.path.insert(0, "../")

from utils import rendering
from PIL import Image
import trimesh
import numpy as np

renderer = rendering.Renderer([128, 128])

# load the object
object_path = "our_mesh/luomo.obj"
mesh = trimesh.load(object_path)
scale = 0.2
mesh.apply_scale([scale, scale, scale]) 
renderer.remove_objects()
renderer.add_object(mesh,  add_faces=True)

location = renderer.random_position(radius=10, num=1, seed=2)
print(location)
# location = np.array([[5,0,0]])
orientation = renderer.cam_from_positions(location)
renderer.update_camera_pose(location, orientation)
image = Image.fromarray(renderer.render())


image.save('image.png')






