import numpy as np


def box_square(window, size):
    total = 0
    for j in range(size):
        for i in range(size):
            total += window[j][i]
    total /= size ** 2
    return total


def box_circular(window, size, radius=0):
    if radius <= 0:
        radius = size / 2
    total = 0
    center = np.array([size / 2, size / 2])
    counter = 0
    for j in range(size):
        for i in range(size):
            xp = np.array([i + 0.5, j + 0.5])
            difference = xp - center
            dist_sqr = np.dot(difference, difference)
            if dist_sqr <= radius ** 2:
                # We are inside the circle
                total += window[j][i]
                counter += 1
    total /= counter
    return total


def tent_square(window, size):
    total = 0
    center = np.array([size / 2, size / 2])
    max_dist = np.linalg.norm(center)
    sum_of_weights = 0
    for j in range(size):
        for i in range(size):
            xp = np.array([i + 0.5, j + 0.5])
            distance = np.linalg.norm(xp - center)
            weight = (max_dist - distance) / max_dist
            total += weight * window[j][i]
            sum_of_weights += weight
    total /= sum_of_weights
    return total


def tent_circular(window, size, radius=0):
    if radius <= 0:
        radius = size / 2
    total = 0
    center = np.array([size / 2, size / 2])
    max_dist = np.linalg.norm(center)
    sum_of_weights = 0
    for j in range(size):
        for i in range(size):
            xp = np.array([i + 0.5, j + 0.5])
            distance = np.linalg.norm(xp - center)
            if distance <= radius:
                weight = (max_dist - distance) / max_dist
                total += weight * window[j][i]
                sum_of_weights += weight
    total /= sum_of_weights
    return total


def gaussian(window, size, sigma=None):
    """
    Using the equation from
    https://medium.com/@akumar5/computer-vision-gaussian-filter-from-scratch-b485837b6e09
    """
    if not sigma:
        sigma = max(size // 6, 2)
    total = 0
    center = np.array([size / 2, size / 2])
    sum_of_weights = 0
    for j in range(size):
        for i in range(size):
            xp = np.array([i + 0.5, j + 0.5])
            difference = xp - center
            x, y = difference
            weight = (1 / (2 * np.pi * sigma ** 2)) * np.exp(
                -(x ** 2 + y ** 2) / (2 * sigma ** 2)
            )
            total += weight * window[j][i]
            sum_of_weights += weight
    total /= sum_of_weights
    return total
