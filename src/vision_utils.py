import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

class VisionProcessor:
    @staticmethod
    def get_blur_score(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    @staticmethod
    def get_brightness_score(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return np.mean(gray)

    @staticmethod
    def compare_frames(frame_a, frame_b):
        gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
        # Redimensiona para garantir que tenham o mesmo tamanho
        gray_b = cv2.resize(gray_b, (gray_a.shape[1], gray_a.shape[0]))
        score, _ = ssim(gray_a, gray_b, full=True)
        return score
