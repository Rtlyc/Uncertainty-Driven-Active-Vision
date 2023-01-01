import sys,os
sys.path.insert(0, "../")

from utils import rendering
from PIL import Image
import trimesh

renderer = rendering.Renderer([128, 128])

# load the object
object_path = "our_mesh/luomo.obj"
mesh = trimesh.load(object_path)
renderer.remove_objects()
renderer.add_object(mesh)
print(renderer.scene.get_nodes())

location = renderer.random_position(radius=0.05, num=1, seed=0)
orientation = renderer.cam_from_positions(location)
renderer.update_camera_pose(location, orientation)
image = Image.fromarray(renderer.render())


image.save('image.png')






