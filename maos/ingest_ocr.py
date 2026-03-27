import pytesseract
import cv2
from maos.chunker import chunk_text

def read_image(path):

    img=cv2.imread(path)

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    text=pytesseract.image_to_string(gray)

    return chunk_text(text)
