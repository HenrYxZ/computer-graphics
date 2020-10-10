import numpy as np

# Local Modules
import constants


def fresnel_function(vh, ior, k=0):
    rs = (
        ((ior ** 2 + k ** 2) - 2 * ior * vh + vh ** 2) /
        ((ior ** 2 + k ** 2) + 2 * ior * vh + vh ** 2)
    )
    rp = (
        ((ior ** 2 + k ** 2) * vh ** 2 - 2 * ior * vh + 1) /
        ((ior ** 2 + k ** 2) * vh ** 2 + 2 * ior * vh + 1)
    )
    f = (rs + rp) / 2
    return f


def beckman_distribution(alpha, m):
    d = 1 / (m ** 2 * np.cos(alpha) ** 4) * np.exp(
        -(np.tan(alpha) ** 2 / (m ** 2))
    )
    return d


def shadowing_masking(nl, nv, nh, vh):
    c = 2 * nh / vh
    masking = c * nv
    shadowing = c * nl
    return min(1, masking, shadowing)


def cook_torrance(n, l, v, nl, ior, m, k=0, radiance=1):
    # Half-vector between v and l
    h = (n + l) / 2
    nv = np.dot(n, v)
    nh = np.dot(n, h)
    vh = np.dot(v, h)
    # TODO: see if you can use arc cos like that
    alpha = np.arccos(nl)
    f = fresnel_function(vh, ior, k)
    d = beckman_distribution(alpha, m)
    g = shadowing_masking(nl, nv, nh, vh)
    # This is not including radiance
    r = (f / (4 * radiance)) * (d / nl) * (g / nv)
    return r


def brdf(intensity, n, l, v, ks, ior, m, k=0):
    nl = np.dot(n, l)
    f0 = ((ior - 1) / (ior + 1)) ** 2
    reflectance = (1 - ks) * f0 + ks * cook_torrance(n, l, v, nl, ior, m, k)
    reflected_intensity = intensity * np.dot(n, l) * reflectance
    return reflected_intensity


# ----------------------------------------------------------------------------
def color_matching(color):
    xyz = np.zeros(3)
    for i in range(len(color)):
        intensity = color[i]
        xyz[0] += intensity * constants.COLOR_MATCHING[i][1]
        xyz[1] += intensity * constants.COLOR_MATCHING[i][2]
        xyz[2] += intensity * constants.COLOR_MATCHING[i][3]
    return xyz


def xyz_to_rgb(color):
    rgb_color = np.matmul(constants.XYZ_TO_RGB, color)
    return rgb_color
