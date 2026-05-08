import cv2

def grayscale(img):
    """灰度滤镜"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blur(img, ksize=(5,5)):
    """模糊滤镜"""
    return cv2.GaussianBlur(img, ksize, 0)

def edge_detect(img):
    """边缘检测"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    # Canny 输出是单通道，要转成3通道显示
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)