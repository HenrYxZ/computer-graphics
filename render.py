import numpy as np
from progress.bar import Bar

# Local Modules
import utils
from ray import Ray
from raytrace import raytrace

PERCENTAGE_STEP = 1
RGB_CHANNELS = 3


def render(scene, camera, height, width):
    """
    Render the image for the given scene and camera using raytracing.

    Args:
        scene(Scene): The scene that contains objects, cameras and lights.
        camera(Camera): The camera that is rendering this image.
        height(int): The height of the screen
        width(int): Width of the screen

    Returns:
        numpy.array: The pixels with the raytraced colors.
    """
    output = np.zeros((height, width, RGB_CHANNELS), dtype=np.uint8)
    if not scene or not scene.objects or not camera or camera.inside(
            scene.objects
    ):
        print("Cannot generate an image")
        return output
    # This is for showing progress %
    iterations = height * width
    step_size = np.ceil((iterations * PERCENTAGE_STEP) / 100).astype('int')
    counter = 0
    bar = Bar('Raytracing', max=100 / PERCENTAGE_STEP, suffix='%(percent)d%%')
    for j in range(height):
        for i in range(width):
            x = i
            y = height - 1 - j
            # Get x projected in view coord
            xp = (x / float(width)) * camera.scale_x
            # Get y projected in view coord
            yp = (y / float(height)) * camera.scale_y
            pp = camera.p00 + xp * camera.n0 + yp * camera.n1
            npe = utils.normalize(pp - camera.position)
            ray = Ray(pp, npe)
            color = raytrace(ray, scene)
            output[j][i] = color
            counter += 1
            if counter % step_size == 0:
                bar.next()
    bar.finish()
    return output
