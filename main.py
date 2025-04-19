from PIL import Image
from reedsolo import RSCodec

# Create image with quiet zone (25x25 QR + 4-module border on each side)
im = Image.new("L", (33, 33), 255)  # White background
visited = set()

# Offset to center the 25x25 QR code in the 33x33 image
offset = 4


def draw_alignment_area(x, y):
    x, y = x + offset, y + offset
    for i in range(7):
        visited.add((x, y + i))
        visited.add((x + i, y))
        visited.add((x + 6, y + i))
        visited.add((x + i, y + 6))
        im.putpixel((x, y + i), 0)
        im.putpixel((x + i, y), 0)
        im.putpixel((x + 6, y + i), 0)
        im.putpixel((x + i, y + 6), 0)
    for i in range(1, 6):
        im.putpixel((x + 1, y + i), 255)
        im.putpixel((x + i, y + 1), 255)
        im.putpixel((x + 5, y + i), 255)
        im.putpixel((x + i, y + 5), 255)
        visited.add((x + 1, y + i))
        visited.add((x + i, y + 1))
        visited.add((x + 5, y + i))
        visited.add((x + i, y + 5))
    for i in range(2, 5):
        im.putpixel((x + 2, y + i), 0)
        im.putpixel((x + i, y + 2), 0)
        im.putpixel((x + 4, y + i), 0)
        im.putpixel((x + i, y + 4), 0)
        visited.add((x + 2, y + i))
        visited.add((x + i, y + 2))
        visited.add((x + 4, y + i))
        visited.add((x + i, y + 4))


def draw_outer_alignment_area():
    for i in range(8):
        coords = [(7, i), (i, 7), (i, 17), (7, 17 + i), (17, i), (17 + i, 7)]
        for dx, dy in coords:
            x, y = dx + offset, dy + offset
            im.putpixel((x, y), 255)
            visited.add((x, y))


def draw_alignment_pattern(cx, cy):
    cx, cy = cx + offset, cy + offset
    for i in range(5):
        for j in range(5):
            x, y = cx - 2 + i, cy - 2 + j
            im.putpixel((x, y), 0)
            visited.add((x, y))
    for i in range(3):
        for j in range(3):
            x, y = cx - 1 + i, cy - 1 + j
            im.putpixel((x, y), 255)
            visited.add((x, y))
    im.putpixel((cx, cy), 0)
    visited.add((cx, cy))


def draw_timing_strips():
    for i in range(8, 17, 2):
        im.putpixel((6 + offset, i + offset), 0)
        im.putpixel((i + offset, 6 + offset), 0)
        visited.add((6 + offset, i + offset))
        visited.add((i + offset, 6 + offset))
    for i in range(9, 16, 2):
        im.putpixel((6 + offset, i + offset), 255)
        im.putpixel((i + offset, 6 + offset), 255)
        visited.add((6 + offset, i + offset))
        visited.add((i + offset, 6 + offset))


def draw_format_strips(format_info):
    # Top-left horizontal
    positions = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (7, 8), (8, 8)]
    bits = [14, 13, 12, 11, 10, 9, 8, 7]
    for (dx, dy), bit_idx in zip(positions, bits):
        x, y = dx + offset, dy + offset
        color = 0 if format_info[bit_idx] == "1" else 255
        im.putpixel((x, y), color)
        visited.add((x, y))
    # Top-left vertical
    positions = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8)]
    bits = [7, 6, 5, 4, 3, 2, 1, 0]
    for (dx, dy), bit_idx in zip(positions, bits):
        x, y = dx + offset, dy + offset
        color = 0 if format_info[bit_idx] == "1" else 255
        im.putpixel((x, y), color)
        visited.add((x, y))
    # Bottom-left vertical
    positions = [(8, 24), (8, 23), (8, 22), (8, 21), (8, 20), (8, 19), (8, 18), (8, 17)]
    bits = [7, 6, 5, 4, 3, 2, 1, 0]
    for (dx, dy), bit_idx in zip(positions, bits):
        x, y = dx + offset, dy + offset
        color = 0 if format_info[bit_idx] == "1" else 255
        im.putpixel((x, y), color)
        visited.add((x, y))
    # Top-right horizontal
    positions = [(24, 8), (23, 8), (22, 8), (21, 8), (20, 8), (19, 8), (18, 8), (17, 8)]
    bits = [14, 13, 12, 11, 10, 9, 8, 7]
    for (dx, dy), bit_idx in zip(positions, bits):
        x, y = dx + offset, dy + offset
        color = 0 if format_info[bit_idx] == "1" else 255
        im.putpixel((x, y), color)
        visited.add((x, y))


def draw_one_black_pixel():
    im.putpixel((8 + offset, 17 + offset), 0)
    visited.add((8 + offset, 17 + offset))


def mask_condition(x, y, mask_number):
    if mask_number == 0:
        return (x + y) % 2 == 0
    return False  # Add other mask patterns if needed


def apply_mask(im, visited, mask_number):
    for y in range(33):
        for x in range(33):
            if (
                (x, y) not in visited
                and offset <= x < 25 + offset
                and offset <= y < 25 + offset
            ):
                if mask_condition(x - offset, y - offset, mask_number):
                    current_value = im.getpixel((x, y))
                    new_value = 255 if current_value == 0 else 0
                    im.putpixel((x, y), new_value)


def place_data(bit_stream):
    x, y = 24 + offset, 24 + offset  # Bottom-right corner
    reverse = False
    bit_idx = 0
    while bit_idx < len(bit_stream) and x >= offset:
        for col in [x, x - 1]:
            if col < offset:
                continue
            while offset <= y < 25 + offset:
                if (col, y) not in visited:  # Skip functional patterns
                    color = 0 if bit_stream[bit_idx] == "1" else 255
                    im.putpixel((col, y), color)
                    # Do NOT add to visited
                    bit_idx += 1
                    if bit_idx >= len(bit_stream):
                        return
                y += -1 if reverse else 1
            y = 24 + offset if reverse else offset
            reverse = not reverse
        x -= 2


# Draw structural patterns
draw_alignment_area(0, 0)
draw_alignment_area(0, 18)
draw_alignment_area(18, 0)
draw_alignment_pattern(18, 18)
draw_outer_alignment_area()
draw_timing_strips()
format_info = "111010110100100"  # Level L, Mask 0
draw_format_strips(format_info)
draw_one_black_pixel()

# Encode data
message = "shubhang"
mode_bits = "0100"  # Byte mode
count_bits = format(len(message), "08b")
data_bits = "".join(format(ord(char), "08b") for char in message)
bit_stream = mode_bits + count_bits + data_bits
remainder = 8 - (len(bit_stream) % 8) if len(bit_stream) % 8 != 0 else 0
bit_stream += "0" * remainder
padding_codewords = ["11101100", "00010001"]
while len(bit_stream) < 272:
    bit_stream += padding_codewords[len(bit_stream) // 8 % 2]
bit_stream = bit_stream[:272]

# Error correction
rsc = RSCodec(10)
data_bytes = [int(bit_stream[i : i + 8], 2) for i in range(0, 272, 8)]
encoded = rsc.encode(bytes(data_bytes))
all_bits = "".join(format(byte, "08b") for byte in encoded)

# Place data and apply mask
place_data(all_bits)
mask_number = 0
# apply_mask(im, visited, mask_number)

# Save and display
im.save("shubhang_qr.png")
im.show()
