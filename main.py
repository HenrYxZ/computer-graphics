import filters
import mipmapping


TEXTURES_DIR = "textures"
OUTPUT_DIR = "output"
CHECKERBOARD_FILENAME = f"{TEXTURES_DIR}/checkerboard.png"
MICKEY_FILENAME = f"{TEXTURES_DIR}/mickey.jpg"
SEATTLE_FILENAME = f"{TEXTURES_DIR}/Seattle-1024x1024.jpg"


def get_filter_function(filter_opt, footprint_opt):
    if filter_opt == '1':
        if footprint_opt == '1':
            return filters.box_square
        else:
            return filters.box_circular
    elif filter_opt == '2':
        if footprint_opt == '1':
            return filters.tent_square
        else:
            return filters.tent_circular
    else:
        return filters.gaussian


# MAIN FUNCTION ---------------------------------------------------------------
def main():
    select_img = (
        "Please choose an option:\n"
        "[1] to use a pattern\n"
        "[2] to use a mickey\n"
        "[3] to use a real world image\n"
        "[0] to quit\n"
    )
    select_filter = (
        "Please choose a filter:\n"
        "[1] to use box\n"
        "[2] to use tent\n"
        "[3] to use gaussian\n"
    )
    select_footprint = (
        "Please choose a footprint:\n"
        "[1] to use square\n"
        "[2] to use circular\n"
    )
    while True:
        opt = input(select_img)
        if opt == '0':
            break
        filter_opt = input(select_filter)
        if filter_opt != '3':
            footprint_opt = input(select_footprint)
        else:
            footprint_opt = 0
        filter_function = get_filter_function(filter_opt, footprint_opt)
        if opt == '1':
            mipmapping.create_all_levels(CHECKERBOARD_FILENAME, filter_function)
        elif opt == '2':
            mipmapping.create_all_levels(MICKEY_FILENAME, filter_function)
        elif opt == '3':
            mipmapping.create_all_levels(SEATTLE_FILENAME, filter_function)
        else:
            print("Wrong option")


if __name__ == '__main__':
    main()
