import sys,os
sys.path.insert(0, "../")

from utils import rendering
from PIL import Image
import trimesh

renderer = rendering.Renderer([128, 128])

# load the object
object_path = "our_mesh/luomo.obj"
# mesh = trimesh.load(object_path)
# renderer.remove_objects()
# renderer.add_object(mesh)

# location = renderer.random_position(radius=1, num=1, seed=0)
# orientation = renderer.cam_from_positions(location)
# renderer.update_camera_pose(location, orientation)
# image = Image.fromarray(renderer.render())


# image.save('image.png')


import pyrender

# Load the mesh data using trimesh
mesh = trimesh.load(object_path)

# Create a pyrender Mesh object from the trimesh object
pr_mesh = pyrender.Mesh.from_trimesh(mesh)

# Add the mesh to a pyrender Scene
scene = pyrender.Scene()
scene.add(pr_mesh)

# Render the scene
renderer = pyrender.OffscreenRenderer(viewport_width=640, viewport_height=480)
color, depth = renderer.render(scene)

# Save the rendered image
image = pyrender.imwrite.imwrite("render.jpg", color)




