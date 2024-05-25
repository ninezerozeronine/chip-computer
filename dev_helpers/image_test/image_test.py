import sys

from PIL import Image

# 80x60           101 0000    x       11 1100     =     4,800
#    R RRRR RCCC CCCC    
# 0000 0000 0000 0000

def rgb_to_bgr(rgb_val):
    res = 0
    # Red
    res |= (rgb_val & 0b110000) >> 4

    # Green
    res |= rgb_val & 0b001100

    # Blue
    res |= (rgb_val & 0b000011) << 4
    return res 

def column_and_row_to_address(column_index, row_index):
    res = 0
    res |= column_index
    res |= row_index << 7
    return res

def to_program(image_path):
    with Image.open(image_path) as im:
        px = im.load()
        for row_index in range(im.height):
            for column_index in range(im.width):
                value = rgb_to_bgr(px[column_index, row_index])
                address = column_and_row_to_address(column_index, row_index)
                if column_index == 0:
                    print(f"@ #{address}")
                    print(f"$ROW_{row_index:<4}", end="")
                print(f"#{value:<3}", end="")
                    
            print("")

def to_commands(image_path):
    with Image.open(image_path) as im:
        px = im.load()
        for row_index in range(im.height):
            print(f"W 65532 {row_index} // Set Row")
            for column_index in range(im.width):
                print(f"W 65533 {column_index}")
                print(f"W 65534 {px[column_index, row_index]}")

if __name__ == "__main__":
    # to_program(sys.argv[1])
    to_commands(sys.argv[1])