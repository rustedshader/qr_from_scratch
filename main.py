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


visited = set()
def draw_alignment_area(x,y):
    for i in range(7):
        for k in range(7):
            visited.add((x+i,y+k))
            im.putpixel((x+i,y+k),255)
    for i in range(2,5):
        for k in range(2,5):
            visited.add((x+i,y+k))
            im.putpixel((x+i,y+k),0)

draw_alignment_area(0,0)
draw_alignment_area(0,18)
draw_alignment_area(18,0)


# Reed Solomon Code Woah 
def percentage_error_code_draw():
    pass

def draw_encoding(x,y):
    byte = [0,1,0,0]
    for k in range(0,len(byte),4):
        a = k
        b = a + 1
        c = a + 2
        d = a + 3
        if byte[a] == 0:
            im.putpixel((x,y),255)
        else:
            im.putpixel((x,y),0)
        if byte[b] == 0:
            im.putpixel((x-1,y),255)
        else:
            im.putpixel((x-1,y),0)
        if byte[c] == 0:
            im.putpixel((x,y-1),255)
        else:
            im.putpixel((x,y-1),0)
        if byte[d] == 0:
            im.putpixel((x-1,y-1),255)
        else:
            im.putpixel((x-1,y-1),0) 
        y -= 2
    return x,y


message_length = format(len("shubhang"),'b')
print(message_length)

def draw_message_length(x,y):
    byte = [int(num) for num in message_length]
    print(byte)
    for k in range(0,len(byte),4):
        a = k
        b = a + 1
        c = a + 2
        d = a + 3
        if byte[a] == 0:
            im.putpixel((x,y),255)
        else:
            im.putpixel((x,y),0)
        if byte[b] == 0:
            im.putpixel((x-1,y),255)
        else:
            im.putpixel((x-1,y),0)
        if byte[c] == 0:
            im.putpixel((x,y-1),255)
        else:
            im.putpixel((x,y-1),0)
        if byte[d] == 0:
            im.putpixel((x-1,y-1),255)
        else:
            im.putpixel((x-1,y-1),0)
        x = x - 0
        y = y - 2
    return x ,y 



def draw_data(data_string,x,y):
    converted_bytes = [format(ord(char),'b') for char in data_string]
    rev_zag = False
    for byte in converted_bytes:
        if len(byte) < 8:
            zeroes_to_append = (8 - len(byte))  * [str(0)]
            pp = zeroes_to_append + [c for c in byte]
            for k in range(0,len(pp),4):
                a = k
                if a+1 <= len(pp) - 1:
                    b = a + 1
                else:
                    b = None
                if a+2 <= len(pp) - 1:
                    c = a + 2
                else:
                    c = None
                if a+3 <= len(pp) - 1:
                    d = a + 3
                else:
                    d = None
                
                if not rev_zag:
                    if a:
                        if pp[a] == "0":
                            im.putpixel((x,y),255)
                        else:
                            im.putpixel((x,y),0)
                    if b:
                        if pp[b] == "0":
                            im.putpixel((x-1,y),255)
                        else:
                            im.putpixel((x-1,y),0)
                    if c:
                        if pp[c] == "0":
                            im.putpixel((x,y-1),255)
                        else:
                            im.putpixel((x,y-1),0)
                    if d:
                        if pp[d] == "0":
                            im.putpixel((x-1,y-1),255)
                        else:
                            im.putpixel((x-1,y-1),0)
                    if (x,y-2) in visited or x+1 <= 24 or x+1 >= 0 or y +1 >= 24 or y + 1  >= 0:
                        rev_zag = True
                        x = x-2
                        y = y - 1
                    else:
                        rev_zag = False
                        x = x - 0
                        y = y - 2
                else:
                    if a:
                        if pp[a] == "0":
                            im.putpixel((x,y),255)
                        else:
                            im.putpixel((x,y),0)
                    if b:
                        if pp[b] == "0":
                            im.putpixel((x-1,y),255)
                        else:
                            im.putpixel((x-1,y),0)
                    if c:
                        if pp[c] == "0":
                            im.putpixel((x,y+1),255)
                        else:
                            im.putpixel((x,y+1),0)
                    if d:
                        if pp[d] == "0":
                            im.putpixel((x-1,y-1),255)
                        else:
                            im.putpixel((x-1,y-1),0)
                    if (x+1,y+2) in visited or x+1 <= 24 or x+1 >= 0 or y +1 >= 24 or y + 1  >= 0: 
                        rev_zag = True
                        x = x - 2
                        y = y - 1
                    else:
                        rev_zag = False
                        x = x - 2
                        y = y + 1
    return x,y


def draw_readsolomo_code(x,y):
    rsc = RSCodec(10)
    rs_code = rsc.encode(b'shubhang')
    converted_bytes = [format(char,'b') for char in rs_code]
    rev_zag = False
    for byte in converted_bytes:
        if len(byte) < 8:
            zeroes_to_append = (8 - len(byte))  * [str(0)]
            pp = zeroes_to_append + [c for c in byte]
            for k in range(0,len(pp),4):
                print(k,pp)
                if k <= len(pp) - 1:
                    a = k
                else:
                    a = None
                if a+1 <= len(pp) - 1:
                    b = a + 1
                else:
                    b = None
                if a+2 <= len(pp) - 1:
                    c = a + 2
                else:
                    c = None
                if a+3 <= len(pp) - 1:
                    d = a + 3
                else:
                    d = None
                
                if not rev_zag:
                    if x+1 <= 24 or x+1 >= 0 or y +1 >= 24 or y + 1  >= 0:
                        if a:
                            if pp[a] == "0":
                                im.putpixel((x,y),255)
                            else:
                                im.putpixel((x,y),0)
                        if b:
                            if pp[b] == "0":
                                im.putpixel((x-1,y),255)
                            else:
                                im.putpixel((x-1,y),0)
                        if c:
                            if pp[c] == "0":
                                im.putpixel((x,y-1),255)
                            else:
                                im.putpixel((x,y-1),0)
                        if d:
                            if pp[d] == "0":
                                im.putpixel((x-1,y-1),255)
                            else:
                                im.putpixel((x-1,y-1),0)
                        if (x,y-2) in visited or x+1 <= 24 or x+1 >= 0 or y +1 >= 24 or y + 1  >= 0:
                            rev_zag = True
                            x = x-2
                            y = y - 1
                        else:
                            rev_zag = False
                            x = x - 0
                            y = y - 2
                else:
                    if x+1 <= 24 and x+1 >= 0 and y +1 >= 24 and y + 1  >= 0:
                        if a:
                            if pp[a] == "0":
                                im.putpixel((x,y),255)
                            else:
                                print(x,y)
                                im.putpixel((x,y),0)
                        if b:
                            if pp[b] == "0" :
                                im.putpixel((x-1,y),255)
                            else:
                                im.putpixel((x-1,y),0)
                        if c:
                            if pp[c] == "0":
                                im.putpixel((x,y+1),255)
                            else:
                                im.putpixel((x,y+1),0)
                        if d:
                            if pp[d] == "0":
                                im.putpixel((x-1,y-1),255)
                            else:
                                im.putpixel((x-1,y-1),0)
                        if (x+1,y+2) in visited or x+1 <= 24 or x+1 >= 0 or y +1 >= 24 or y + 1  >= 0: 
                            rev_zag = True
                            x = x - 2
                            y = y - 1
                        else:
                            rev_zag = False
                            x = x - 2
                            y = y + 1


def masking():
    pass
x,y = draw_encoding(24,24)
x,y = draw_message_length(x,y)
x,y = draw_data("shubhang",x,y)
draw_readsolomo_code(x,y)

im.show()


