import cv2
import pytesseract
from skimage.metrics import structural_similarity
from skimage.transform import resize
import numpy as np
from valorant.config import GlobalConfig


class Image:
    def __init__(self):
        self.config = GlobalConfig()

    @staticmethod
    def masking_color(img, lower, upper, erode=0, dilate=0, show=False):
        """
        making color image
        :param img: imported image from img cv2
        :param lower: set example: (0,0,0)
        :param upper: set example: (179, 225, 255)
        :param erode: int example: 3
        :param dilate: int example: 4
        :param show: bool  example: False
        :return: cv2 masked image
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_color = np.array(lower, np.uint8)
        upper_color = np.array(upper, np.uint8)
        frame_threshold = cv2.inRange(hsv, lower_color, upper_color)
        frame_threshold = cv2.erode(frame_threshold, np.ones((erode, erode), dtype=np.uint8))
        frame_threshold = cv2.dilate(frame_threshold, np.ones((dilate, dilate), dtype=np.uint8))
        frame_threshold = cv2.cvtColor(frame_threshold, cv2.COLOR_GRAY2RGB)
        if show:
            cv2.imshow('Color Detection', frame_threshold)
        return frame_threshold

    @staticmethod
    def detect_white(img, sensitivity=3):
        lower_white = np.array([0, 0, 255 - sensitivity])
        upper_white = np.array([255, sensitivity, 255])
        return cv2.inRange(img, lower_white, upper_white)

    @staticmethod
    def crop_image(img, show=False, crop_size=None):
        # default value
        x, y, h, w = 0, 0, 300, 300

        # change crop coordinate
        if crop_size is not None:
            x, y, h, w = crop_size

        crop_img = img[y:y + h, x:x + w]
        if show:
            cv2.imshow("Cropped Image", crop_img)
            cv2.waitKey(0)
        return crop_img

    def ocr(self, img, digit_only=False, config=None):
        tesseract_config = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if 'config' in config:
            tesseract_config = config['config'].tesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_config
        if digit_only:
            text = pytesseract.image_to_string(img, lang='eng',
                                               config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        else:
            text = pytesseract.image_to_string(img)
        return text

    @staticmethod
    def orb_sim(img1, img2):
        # SIFT is no longer available in cv2 so using ORB
        orb = cv2.ORB_create()

        # detect keypoints and descriptors
        kp_a, desc_a = orb.detectAndCompute(img1, None)
        kp_b, desc_b = orb.detectAndCompute(img2, None)

        # define the bruteforce matcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # perform matches.
        matches = bf.match(desc_a, desc_b)
        # Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
        similar_regions = [i for i in matches if i.distance < 50]
        if len(matches) == 0:
            return 0
        return len(similar_regions) / len(matches)

    @staticmethod
    def structural_sim(img1, img2):
        sim, diff = structural_similarity(img1, img2, full=True)
        return sim

    @staticmethod
    def check_similar(img1, img2):
        orb_similarity = orb_sim(img1, img2)  # 1.0 means identical. Lower = not similar
        print("Similarity using ORB is: ", orb_similarity)
        # Resize for SSIM
        img5 = resize(img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True)
        ssim = structural_sim(img1, img2)  # 1.0 means identical. Lower = not similar
        print("Similarity using SSIM is: ", ssim)
        return orb_similarity, ssim
