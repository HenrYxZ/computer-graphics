import math
import numpy as np
from PIL import Image

# Local Modules
import filters


IMG_FILENAME = "mickey.jpg"
OUTPUT_FILENAME = "output.jpg"
IMG_CHANNELS = 3
MAX_RGB = 255


def apply_filter(im, filter_function, filter_size):
    im_arr = np.array(im)
    # Normalize the image array
    im_arr = im_arr / MAX_RGB
    width = im_arr.shape[0]
    new_width = width // filter_size
    new_image_arr = np.zeros([new_width, new_width, IMG_CHANNELS])
    filter_window = np.zeros([filter_size, filter_size, IMG_CHANNELS])
    for j in range(new_width):
        for i in range(new_width):
            for k in range(filter_size):
                row = filter_size * j + k
                col = filter_size * i
                filter_window[k] = im_arr[row][col:col + filter_size]
            new_image_arr[j][i] = filter_function(filter_window, filter_size)
    return new_image_arr


def reduce_im(im, level, filter_function):
    """
    Reduce an Image to a given mip map level. This will only work for order 2
    square images.
    :param Image im: A pillow Image
    :param int level: the level wanted
    :param filter_function: The filter to be used
    :return: The imaged reduced to the given level
    """
    width = im.size[0]
    current_level = int(math.log2(width))
    filter_size = 2 ** (current_level - level)
    filtered_im_arr = apply_filter(im, filter_function, filter_size)
    rgb_im_arr = (filtered_im_arr * MAX_RGB).astype(np.uint8)
    filtered_im = Image.fromarray(rgb_im_arr)
    return filtered_im


# MAIN FUNCTION ---------------------------------------------------------------
def main():
    print("Enter [1] ")
    img = Image.open(IMG_FILENAME)
    reduced_img = reduce_im(img, 6, filters.gaussian)
    reduced_img.save("output.jpg", quality=95)


if __name__ == '__main__':
    main()
