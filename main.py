# import qrcode

# img = qrcode.make("Hello World")
# type(img)
# img.save("shubhang.png")

from PIL import Image
from reedsolo import RSCodec

class QRCode:
    def __init__(self):
        pass

L = 80
M = 64
Q = 48
H = 36


# https://franckybox.com/wp-content/uploads/qrcode.pdf
def get_alignment_positions(version):
    positions = []
    if version > 1:
        n_patterns = version // 7 + 2
        first_pos = 6
        positions.append(first_pos)
        matrix_width = 4 * version + 17
        last_pos = matrix_width - 1 - first_pos
        second_last_pos = (
        (first_pos + last_pos * (n_patterns - 2)
        + (n_patterns - 1) // 2)
        // (n_patterns - 1)
        ) & -2
        pos_step = last_pos - second_last_pos
        second_pos = last_pos - (n_patterns - 2) * pos_step
        positions.extend(range(second_pos, last_pos + 1, pos_step))
    return positions

# print(get_alignment_positions(2))

# 6,6 | 6,18 | 18,6 | 18,18


# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.new
im = Image.new('L',(25,25))

# This Visited gonna store which pixels have been drawn
visited = set()

def draw_alignment_area(x,y):
    for i in range(7):
        visited.add((x+0,y+i))
        visited.add((x+i,y+0))
        visited.add((x+6,y+i))
        visited.add((x+i,y+6))

        im.putpixel((x+0,y+i),0)
        im.putpixel((x+i,y+0),0)
        im.putpixel((x+6,y+i),0)
        im.putpixel((x+i,y+6),0)

    for i in range(1,6):
        visited.add((x+1,y+i))
        visited.add((x+i,y+1))
        visited.add((x+5,y+i))
        visited.add((x+i,y+5))

        im.putpixel((x+1,y+i),255)
        im.putpixel((x+i,y+1),255)
        im.putpixel((x+5,y+i),255)
        im.putpixel((x+i,y+5),255)
    
    for i in range(2,5):
        visited.add((x+2,y+i))
        visited.add((x+i,y+2))
        visited.add((x+4,y+i))
        visited.add((x+i,y+4))

        im.putpixel((x+2,y+i),0)
        im.putpixel((x+i,y+2),0)
        im.putpixel((x+4,y+i),0)
        im.putpixel((x+i,y+4),0)
    
def draw_outer_alignment_area():
    for i in range(8):
        visited.add((7,i))
        visited.add((i,7))
        visited.add((i,17))
        visited.add((7,17+i))
        visited.add((17,i))
        visited.add((17+i,7))

        im.putpixel((7,i),255)
        im.putpixel((i,7),255)
        im.putpixel((i,17),255)
        im.putpixel((7,17+i),255)
        im.putpixel((17,i),255)
        im.putpixel((17+i,7),255)

def draw_timing_strips():
    # 9 Alternating Squares is for qr code version 2  >> format strips

    # Timing Strip Middle Left
    for i in range(8,17,2):
        if (6,i) not in visited:
            im.putpixel((6,i),0)
            visited.add((6,i))
    for i in range(9,16,2):
        if (6,i) not in visited:
            im.putpixel((6,i),255)
            visited.add((6,i))
    
    # Timing Strip Middle Top
    for i in range(8,17,2):
        if (i,6) not in visited:
            im.putpixel((i,6),0)
            visited.add((i,6))
    for i in range(9,16,2):
        if (i,6) not in visited:
            im.putpixel((i,6),255)
            visited.add((i,6))
    
def draw_format_strips():
    # Format Strip Lower Left
    for i in range(18,25):
        im.putpixel((8,i),100)
        visited.add((8,i))

    # Format strips Middle Left and Middle Top
    for i in range(0,9):
        if (i,8) not in visited:
            im.putpixel((i,8),100)
            visited.add((i,8))
    for i in range(0,9):
        if (8,i) not in visited:
            im.putpixel((8,i),100)
            visited.add((8,i))
    
    for i in range(17,25):
        if (i,8) not in visited:
            im.putpixel((i,8),100)
            visited.add((i,8))
    
def draw_one_black_pixel():
    im.putpixel((8,18),0)
    visited.add((8,18))

def draw_encoding():
    x=24
    y=24
    byte = ["0","1","0","0"]
    for k in range(0,len(byte),4):
        a = k
        b = a + 1
        c = a + 2
        d = a + 3
        if byte[a] == "0":
            im.putpixel((x,y),255)
        else:
            im.putpixel((x,y),0)
        if byte[b] == "0":
            im.putpixel((x-1,y),255)
        else:
            im.putpixel((x-1,y),0)
        if byte[c] == "0":
            im.putpixel((x,y-1),255)
        else:
            im.putpixel((x,y-1),0)
        if byte[d] == "0":
            im.putpixel((x-1,y-1),255)
        else:
            im.putpixel((x-1,y-1),0)

def draw_message_length(message):
    x = 24
    y = 22
    message_length = len(message)
    # TODO: FIX if length not in 4 and add visited checks
    length_in_bytes = format(message_length,'b')
    byte = [num for num in length_in_bytes]

    for k in range(0,len(byte),4):
        a = k
        b = a + 1
        c = a + 2
        d = a + 3
        if byte[a] == "0":
            visited.add((x,y))
            im.putpixel((x,y),255)
        else:
            visited.add((x,y))
            im.putpixel((x,y),0)
        if byte[b] == "0":
            visited.add((x,y))
            im.putpixel((x-1,y),255)
        else:
            visited.add((x,y))
            im.putpixel((x-1,y),0)
        if byte[c] == "0":
            visited.add((x,y))
            im.putpixel((x,y-1),255)
        else:
            visited.add((x,y))
            im.putpixel((x,y-1),0)
        if byte[d] == "0":
            visited.add((x,y))
            im.putpixel((x-1,y-1),255)
        else:
            visited.add((x,y))
            im.putpixel((x-1,y-1),0)
        x = x - 0
        y = y - 2
    return x ,y 


def draw(x,y,color):
    if (x,y) not in visited or x > 24 or x < 0 or y > 24 or y < 0:
        visited.add((x,y))
        im.putpixel((x,y),color)
        return True
    else:
        print("Already Visited (x,y)",x,y)
        return False


def draw_data(data_string,x,y):
    converted_bytes = [format(ord(char),'b') for char in data_string]
    reverse = False
    for byte in converted_bytes:
        zeroes_to_append = (8 - len(byte))  * [str(0)]
        pp = zeroes_to_append + [c for c in byte]
        print(pp)
        # 0->7  --> 8 digits
        for i in range(0,8,2):
            if pp[i] == "0":
                draw(x,y,255)
            else:
                draw(x,y,0)
            if pp[i+1] == "0":
                draw(x-1,y,255)
            else:
                draw(x-1,y,0)
            if reverse:
                next_cord = (x,y+1)
            else:
                next_cord = (x,y-1)
            
            if next_cord not in visited or next_cord[1] <= 24 or next_cord[1] >= 0:
                y = next_cord[1]
            else:
                print("THIS IS IN VISITED",next_cord)
                x = x - 2
                if reverse:
                    reverse = False
                else:
                    reverse = True
    return x,y






# Prerequisite Part 
# Upper Left Alignment Area
draw_alignment_area(0,0)
# Lower Left Alignment Area
draw_alignment_area(0,18)
# Upper Right Alignment Area
draw_alignment_area(18,0)
draw_outer_alignment_area()
draw_timing_strips()
draw_format_strips()
draw_one_black_pixel()


# Encoding Part
# 0 -> White
# 1 -> Black
# 0100 -> Binary
draw_encoding()


# Message Part
message = "shubhang"

x,y = draw_message_length(message)
x,y = draw_data(message,x,y)
# draw_readsolomo_code(x,y)

im.show()


