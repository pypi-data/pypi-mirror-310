import cv2
import numpy as np
from modules.pyautogui import pyautogui
# from PIL import Image
from modules.screeninfo import get_monitors

# import random
# import math


class ImageMatcher:
    def __init__(self, template_path):
        self.template_path = template_path
        self.template_image = self.load_image(template_path)
        self.screenshot_image = None
        self.matches = None
        self.good_matches = None
        self.object_location = None
        self.object_center = None
    
    def load_image(self, path, grayscale=True):
        if grayscale:
            return cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        else:
            return cv2.imread(path)
    
    def capture_screen(self):
        monitors = get_monitors()
        if len(monitors) > 1:
            monitor = monitors[1]
        else:
            monitor = monitors[0]
        
        screenshot = pyautogui.screenshot(region=(monitor.x, monitor.y, monitor.width, monitor.height))
        screenshot_image = np.array(screenshot)
        self.screenshot_image = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)
    
    def find_features(self):
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(self.template_image, None)
        kp2, des2 = sift.detectAndCompute(self.screenshot_image, None)
        return kp1, des1, kp2, des2
    
    def match_features(self, des1, des2):
        index_params = dict(algorithm=1, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        return matches
    
    def filter_good_matches(self, matches, ratio=0.7):
        good_matches = [m for m, n in matches if m.distance < ratio * n.distance]
        return good_matches
    
    def find_object_location(self, kp1, kp2, good_matches, min_match_count=10):
        if len(good_matches) > min_match_count:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            h, w = self.template_image.shape[:2]
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            self.object_location = np.int32(dst)
            self.object_center = int((dst[0][0][0] + dst[2][0][0]) / 2), int((dst[0][0][1] + dst[2][0][1]) / 2)
        else:
            print("Not enough matches are found - {}/{}".format(len(good_matches), min_match_count))
            self.object_location = None
        
        return self.object_center
    



    
    def draw_object_location(self, color=(0, 255, 0), thickness=3):
        if self.object_location is not None:
            input_image2_bgr = cv2.cvtColor(self.screenshot_image, cv2.COLOR_GRAY2BGR)
            input_image2_bgr = cv2.polylines(input_image2_bgr, [self.object_location], True, color, thickness, cv2.LINE_AA)
            cv2.imshow("image1", self.template_image)
            cv2.imshow("Detected Object", input_image2_bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    def run(self):
        self.capture_screen()
        kp1, des1, kp2, des2 = self.find_features()
        self.matches = self.match_features(des1, des2)
        self.good_matches = self.filter_good_matches(self.matches)
        object_location_center = self.find_object_location(kp1, kp2, self.good_matches)
        print(object_location_center)
        self.draw_object_location()

if __name__ == "__main__":
    template_path = r'..\python-automation\tests\images\youtube.JPG'
    matcher = ImageMatcher(template_path)
    matcher.run()

