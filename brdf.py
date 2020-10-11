import numpy as np

# Local Modules
import constants
# 6 is wavelength index for red, 3 for green and 2 for blue
RGB_INDEX = [6, 3, 2]


def fresnel_function(vh, ior, k):
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


def cook_torrance(n, l, v, nl, ior, m, k, radiance=1):
    # Half-vector between v and l
    h = (v + l) / 2
    nv = np.dot(n, v)
    nh = np.dot(n, h)
    vh = np.dot(v, h)
    alpha = np.arccos(nh)
    f = fresnel_function(nl, ior, k)
    d = beckman_distribution(alpha, m)
    g = shadowing_masking(nl, nv, nh, vh)
    # This is not including radiance
    r = (f / (4 * radiance)) * (d / nl) * (g / nv)
    return r


def brdf(intensity, n, l, v, ks, ior, m, k):
    nl = np.dot(n, l)
    f0 = ((ior - 1) / (ior + 1)) ** 2
    reflectance = (1 - ks) * f0 + ks * cook_torrance(n, l, v, nl, ior, m, k)
    reflected_intensity = intensity * np.dot(n, l) * reflectance
    return reflected_intensity


def brdf_rgb(intensity, n, l, v, ks, ior, m, k):
    new_intensity = np.array([
        intensity[RGB_INDEX[0]],
        intensity[RGB_INDEX[1]],
        intensity[RGB_INDEX[2]]
    ])
    new_ior = np.array([
        ior[RGB_INDEX[0]],
        ior[RGB_INDEX[1]],
        ior[RGB_INDEX[2]]
    ])
    new_k = np.array([
        k[RGB_INDEX[0]],
        k[RGB_INDEX[1]],
        k[RGB_INDEX[2]]])
    return brdf(new_intensity, n, l, v, ks, new_ior, m, new_k)


# ----------------------------------------------------------------------------
def color_matching(color):
    xyz = np.zeros(3)
    # Exception for color in RGB
    if len(color) == 3:
        new_color_matching = np.array([
            constants.COLOR_MATCHING[RGB_INDEX[0]],
            constants.COLOR_MATCHING[RGB_INDEX[1]],
            constants.COLOR_MATCHING[RGB_INDEX[2]]
        ])
        for i in range(len(color)):
            intensity = color[i]
            xyz[0] += intensity * new_color_matching[i][1]
            xyz[1] += intensity * new_color_matching[i][2]
            xyz[2] += intensity * new_color_matching[i][3]
    else:
        for i in range(len(color)):
            intensity = color[i]
            xyz[0] += intensity * constants.COLOR_MATCHING[i][1]
            xyz[1] += intensity * constants.COLOR_MATCHING[i][2]
            xyz[2] += intensity * constants.COLOR_MATCHING[i][3]
    return xyz


def xyz_to_rgb(color):
    rgb_color = np.matmul(constants.XYZ_TO_RGB, color)
    return rgb_color
