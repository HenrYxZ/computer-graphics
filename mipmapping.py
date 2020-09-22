import math
import numpy as np
from PIL import Image


TEXTURES_DIR = "textures"
OUTPUT_DIR = "output"
CHECKERBOARD_FILENAME = f"{TEXTURES_DIR}/checkerboard.png"
MICKEY_FILENAME = f"{TEXTURES_DIR}/mickey.jpg"
SEATTLE_FILENAME = f"{TEXTURES_DIR}/Seattle-1024x1024.jpg"
IMG_CHANNELS = 3
MAX_RGB = 255


def apply_filter(im, filter_function, filter_size):
    # For images in rgba use only rgb values
    if im.mode == "RGBA":
        im.load()
        rgb_im = Image.new("RGB", im.size, (255, 255, 255))
        rgb_im.paste(im, mask=im.split()[3])
        im_arr = np.array(rgb_im)
    else:
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


def reduce_im(img, level, filter_function):
    """
    Reduce an Image to a given mip map level. This will only work for order 2
    square images.
    :param Image img: A pillow Image
    :param int level: the level wanted
    :param filter_function: The filter to be used
    :return: The imaged reduced to the given level
    """
    width = img.size[0]
    current_level = int(math.log2(width))
    filter_size = 2 ** (current_level - level)
    filtered_im_arr = apply_filter(img, filter_function, filter_size)
    rgb_im_arr = (filtered_im_arr * MAX_RGB).astype(np.uint8)
    filtered_im = Image.fromarray(rgb_im_arr)
    return filtered_im


def create_all_levels(img_filename, filter_function):
    img = Image.open(img_filename)
    width = img.size[0]
    current_level = int(math.log2(width))
    img_name = img_filename.split('/')[-1].split('.')[0]
    filter_name = filter_function.__name__
    # Iterate the levels in reversed order until zero
    for level in range(current_level - 1, -1, -1):
        log_msg = "Filtering {} with {} at level {}...".format(
            img_filename, filter_name, level
        )
        print(log_msg)
        reduced_img = reduce_im(img, level, filter_function)
        output_filename = f"{OUTPUT_DIR}/{img_name}_{filter_name}_{level}.jpg"
        reduced_img.save(output_filename, quality=95)


# MAIN FUNCTION ---------------------------------------------------------------
def main():
    pass


if __name__ == '__main__':
    main()
