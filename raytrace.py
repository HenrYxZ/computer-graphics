import numpy as np
import warnings
# Local Modules
from brdf import brdf, brdf_rgb, color_matching, xyz_to_rgb
from constants import MAX_COLOR_VALUE, RGB_CHANNELS
from ray import Ray
import utils


DEFAULT_COLOR = np.array([20, 20, 200])


def compute_color(ph, eye, obj, lights, rgb=False):
    """
    Compute the color for the given object at the given point.

    Args:
        ph(numpy.array): 3D point of hit between ray and object
        eye(numpy.array): Unit vector in the direction of the viewer
        obj(Object): The object that was hit
        lights([Light]): List of the lights in the scene

    Returns:
        np.array: The color for this ray in numpy array of RGB channels
    """
    nh = obj.normal_at(ph)
    if nh is None:
        warnings.warn("Normal is 0 for obj: {} at ph: {}".format(obj, ph))
        return np.zeros(RGB_CHANNELS)
    color = np.zeros(RGB_CHANNELS)
    for light in lights:
        l = light.get_l(ph)
        # Choose the corresponding shader
        mtl = obj.material
        if rgb:
            multi_color = brdf_rgb(
                light.intensity, nh, l, eye, mtl.ks, mtl.ior, mtl.m, mtl.k
            )
        else:
            multi_color = brdf(
                light.intensity, nh, l, eye, mtl.ks, mtl.ior, mtl.m, mtl.k
            )
        xyz_color = color_matching(multi_color)
        rgb_color = xyz_to_rgb(xyz_color)
        color += rgb_color
    color /= len(lights)
    color *= MAX_COLOR_VALUE
    # Ensure the colors are between 0 and 255
    final_color = np.clip(color, 0, MAX_COLOR_VALUE)
    final_color.astype(np.uint8)
    return final_color


def raytrace(ray, scene, rgb=False):
    """
    Trace the ray to the closest intersection point with an object and get the
    color at that point.

    Args:
        ray(Ray): The ray to be traced
        scene(Scene): This object contains things like objects, lights, etc

    Returns:
        np.array: The color for this ray in numpy array of 3 channels
    """
    # Get closest intersection point
    t_min = np.inf
    # The closest object hit by the ray
    obj_h = None
    objects = scene.objects
    lights = scene.lights
    for obj in objects:
        t = ray.intersect(obj)
        if 0 < t < t_min:
            t_min = t
            obj_h = obj
    # There is a hit with an object
    if obj_h:
        ph = ray.at(t_min)
        eye = utils.normalize(ray.pr - ph)
        color = compute_color(ph, eye, obj_h, lights, rgb)
        return color
    else:
        return np.zeros(RGB_CHANNELS)
