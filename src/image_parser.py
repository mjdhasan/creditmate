import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytesseract
# from pytesseract import Output
import layoutparser as lp  # https://github.com/Layout-Parser/layout-parser
# pip install fvcore==0.1.1.post20200623
# pip install pycocotools==2.0.1

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


if __name__ == '__main__':
    image = cv2.imread('./output/cropped_pdf_image.png')
    # image.shape
    cv2.imshow('original image', image)
    plt.imshow(image)

    deskew = deskew(image)
    plt.imshow(deskew)
    gray = get_grayscale(deskew)
    plt.imshow(gray)
    thresh = thresholding(gray)
    plt.imshow(thresh)
    rnoise = remove_noise(gray)
    plt.imshow(rnoise)
    dilate = dilate(gray)
    plt.imshow(dilate, cmap='gray')
    erode = erode(gray)
    plt.imshow(erode)
    opening = opening(gray)
    plt.imshow(opening)
    canny = canny(gray)
    plt.imshow(canny)

    image_str = pytesseract.image_to_string(gray, config='--psm 1', output_type=pytesseract.Output.DICT)
    image_data = pytesseract.image_to_data(gray, config='--psm 1', output_type=pytesseract.Output.DICT)
    image_data.keys()
    image_data['text']
    df = pd.DataFrame(image_data)

    df[df['text'] != '']

    # using layout parser
    dir(lp)
    lp.models
    model = lp.Detectron2LayoutModel('lp://PrimaLayout/mask_rcnn_R_50_FPN_3x/config')
    image = cv2.imread('./output/cropped_pdf_image.png')
    layout = model.detect(image)  # You need to load the image somewhere else, e.g., image = cv2.imread(...)
    lp.draw_box(image, layout, )  # With extra configurations





