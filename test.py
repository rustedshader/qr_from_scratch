import qrcode
import qrcode.constants
import qrcode.image.base
import qrcode.main

# Testing Using QRCode Library

img = qrcode.make("shubhang",version=2,error_correction=qrcode.constants.ERROR_CORRECT_L,mask_pattern=0)
type(img)
img.save("shubhang.png")
