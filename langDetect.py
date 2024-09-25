# run that at the beginning: 
# export PATH="/opt/homebrew/bin:$PATH"
#

import cv2
import pytesseract
from langdetect import detect
from langdetect import detect_langs
import pypdfium2 as pdfium
from PIL import Image
import numpy as np

pdf = pdfium.PdfDocument("Biography.pdf")
n_pages = len(pdf)

for pageNum in range(n_pages):
    page = pdf[pageNum]
    bitmap = page.render(
        scale = 3,
        rotation = 0,
    )
    pil_image = bitmap.to_pil()
    pil_image.save(f'images/page{pageNum+1}.png')

def is_blank_pixels_check(image_path):
    with Image.open(image_path) as image:
        croppedImage = image.crop((200, 300, 1200, 1600))
        gray = croppedImage.convert("L")
        img_array = np.array(gray)

        average_intensity = np.mean(img_array)
        dark_pixel_count = np.sum(img_array < 155)
        dark_pixel_ratio = dark_pixel_count / img_array.size

        return dark_pixel_ratio < 0.01

def detect_language_with_langdetect(image_path): 
    engFlag = False
    arFlag = False
    image = cv2.imread(image_path)
    custom_config = r'--oem 1 --psm 12'
    custom_config2 = r'--oem 1 --psm 11'
    text = pytesseract.image_to_string(image, lang='ara+eng', config=custom_config)


    if len(text) < 90 or is_blank_pixels_check(image_path):
        return "blank"

    try: 
        langs = detect_langs(text)
        # print(langs) 
        for item in langs: 
            if item.lang == "ar" and item.prob > 0.12:
                arFlag = True
            elif item.lang == "en" or item.lang == "so" or item.lang == "nl" and item.prob > 0.12:
                engFlag = True

        if engFlag and arFlag:
            return "EN/AR"
        elif arFlag:
            return "AR"
        else:
            return "EN"
    except: return "error"

for pageNum in range(n_pages):
    image_path = f'images/page{pageNum+1}.png'

    print(detect_language_with_langdetect(image_path))