import cv2 as cv
import numpy as np
import pyautogui as gui
import keyboard
import time
import random
import itertools
import threading
import os
from winotify import Notification


# Initialize all constant variables
MIN_THRESHOLD = 0.51
COMPLETE_IMG = cv.imread('complete.PNG', cv.IMREAD_COLOR)
QUEST_PROGRESS_IMG = cv.imread('quest_progress.PNG', cv.IMREAD_COLOR)
TURN_IN_IMG = cv.imread('turn_in.PNG', cv.IMREAD_COLOR)
ACCEPT_IMG = cv.imread('accept.PNG', cv.IMREAD_COLOR)


def match_img(needle_img):
    # save a .PNG image of the entire display and read it in with OpenCV
    screenshot = gui.screenshot()
    screenshot.save(r"PASTE THE DIRECTORY THAT THIS SCRIPT FILE IS IN HERE!")
    haystack_img = cv.imread('screenshot.PNG', cv.IMREAD_COLOR)

    # compare the haystack and needle images to each other
    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

    # store the (x,y) coordinate locations of the lowest and highest confidence regions where an image match was found
    min_confidence, max_confidence, min_location, max_location = cv.minMaxLoc(result)
    outline_img_match(confidence=max_confidence, location=max_location, h_img=haystack_img, n_img=needle_img)


"""
Helper method which was used to test for working image matching while writing this script.
"""
def outline_img_match(confidence, location, h_img, n_img):
    print(str(confidence))
    if confidence >= MIN_THRESHOLD:

        # get dimensions of needle image
        needle_width = n_img.shape[1]
        needle_height = n_img.shape[0]

        top_left = location
        bottom_right = (top_left[0] + needle_width, top_left[1] + needle_height)

        # use the calculated coordinates draw a rectangle around the highest confidence image match that OpenCV finds
        cv.rectangle(h_img, top_left, bottom_right,
                     color=(255, 0, 255), thickness=2, lineType=cv.LINE_4)
        cv.imshow('Outlined Match', h_img)
        cv.waitKey()


match_img(COMPLETE_IMG)