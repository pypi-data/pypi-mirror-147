from typing import Sequence

import numpy as np
from PIL import Image
import pyrender
import trimesh
from trimesh.transformations import rotation_matrix, concatenate_matrices


def render_frames(mesh: trimesh.Trimesh, w: int, h: int, num_frames: int) -> Sequence[Image.Image]:
    return _render_trimesh_frames(mesh, w, h, num_frames)


def _render_trimesh_frames(mesh: trimesh.Trimesh, w: int, h: int, num_frames: int) -> Sequence[Image.Image]:
    # normalize size + swap axes (mesh is Z-up blender style, scene is Y-up)
    s = 0.33 / mesh.scale
    scale = np.array([
        [s, 0, 0, 0],
        [0, 0, s, 0],
        [0, s, 0, 0],
        [0, 0, 0, 1],
    ])

    bound = mesh.bounding_box
    recenter = np.linalg.inv(bound.primitive.transform)

    # print(recenter)
    mat = concatenate_matrices(scale, recenter)
    # print(mat)
    mesh.apply_transform(mat)
    scene = pyrender.Scene()
    scene.add(pyrender.Mesh.from_trimesh(mesh))
    # scene.add(mesh)
    # pyrender.Viewer(scene, use_raymond_lighting=True)
    # scene = scene

    imgs = []

    r = pyrender.OffscreenRenderer(w, h)

    for rot_z in np.linspace(0, np.pi * 2, num_frames, endpoint=False):
        camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
        s = np.sqrt(2)/2
        camera_pose = np.array([
            [0.0, -s,   s,   0.3],
            [1.0,  0.0, 0.0, 0.0],
            [0.0,  s,   s,   0.35],
            [0.0,  0.0, 0.0, 1.0],
        ])
        rot = rotation_matrix(rot_z, [0, 0, 1])
        # print(rot)
        camera_pose = concatenate_matrices(rot, camera_pose)
        n1 = scene.add(camera, pose=camera_pose)
        # TODO https://pyrender.readthedocs.io/en/latest/generated/pyrender.light.DirectionalLight.html#pyrender.light.DirectionalLight
        light = pyrender.SpotLight(color=np.ones(3), intensity=3.0,
                                   innerConeAngle=np.pi/16.0,
                                   outerConeAngle=np.pi/6.0)
        n2= scene.add(light, pose=camera_pose)

        color, depth = r.render(scene, flags=pyrender.RenderFlags.SKIP_CULL_FACES)

        scene.remove_node(n1)
        scene.remove_node(n2)

        imgs.append(Image.frombytes("RGB", color.shape[:2], color.copy()))

    return imgs
