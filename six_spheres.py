"""
Example that generates an image of a sphere with a flat color (no lighting).
"""
import numpy as np
from PIL import Image
import os.path

# Local Modules
from camera import Camera
from constants import MAX_QUALITY
from light import DirectionalLight
from material import BRDFMaterial
from object import Sphere
from render import render, render_mp
from scene import Scene
import constants
import utils

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
OUT_DIR = "output"
OUTPUT_IMG_FILENAME = f"{OUT_DIR}/4_six_spheres.jpg"
RGB_IMG_FILENAME = f'{OUT_DIR}/rgb_spheres.jpg'
MULTICOLOR_SPECTRAL_CHANNELS = 7


def set_camera():
    camera_pos = np.array([0.0, 0.0, 0.0])
    v_view = np.array([0.0, 0.0, 1.0])
    v_up = np.array([0.0, 1.0, 0.0])
    return Camera(camera_pos, v_view, v_up, d=0.5, scale_x=0.6, scale_y=0.4)


def set_scene():
    z = 1
    y = [0.2, -0.2]
    x = [-0.4, 0, 0.4]
    # light_direction = np.array([30, -100, 25])
    light_direction = np.array([0, -0.13, 1])
    radius = 0.15
    positions = []
    for j in range(len(y)):
        for i in range(len(x)):
            positions.append(np.array([x[i], y[j], z]))

    materials = []
    # Chrome
    ks = 0.2
    m = 0.1
    materials.append(BRDFMaterial(ks, constants.CR_IOR, constants.CR_K, m))
    m = 0.4
    materials.append(BRDFMaterial(ks, constants.CR_IOR, constants.CR_K, m))
    m = 0.8
    materials.append(BRDFMaterial(ks, constants.CR_IOR, constants.CR_K, m))
    # PVC
    m = 0.1
    k = np.zeros(MULTICOLOR_SPECTRAL_CHANNELS)
    materials.append(BRDFMaterial(ks, constants.PVC_IOR, k, m))
    m = 0.3
    materials.append(BRDFMaterial(ks, constants.PVC_IOR, k, m))
    # SILK
    m = 0.05
    materials.append(BRDFMaterial(ks, constants.SILK_IOR, k, m))

    spheres = []
    for i in range(len(positions)):
        spheres.append(Sphere(positions[i], materials[i], radius))
    cameras = [set_camera()]
    light = DirectionalLight(light_direction, constants.SUNLIGHT)
    return Scene(cameras, [light], spheres)


def main():
    scene = set_scene()
    main_camera = scene.get_main_camera()
    # ------------------------------------------------------------------------
    # Rendering
    timer = utils.Timer()
    timer.start()
    rgb = True
    # rgb = False
    screen = render_mp(scene, main_camera, SCREEN_HEIGHT, SCREEN_WIDTH, rgb)
    timer.stop()
    # ------------------------------------------------------------------------
    print(f"Total time spent rendering: {timer}")
    img_output = Image.fromarray(screen)
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    img_output.save(OUTPUT_IMG_FILENAME, quality=MAX_QUALITY)
    print(f"Output image created in: {OUTPUT_IMG_FILENAME}")


if __name__ == '__main__':
    main()
