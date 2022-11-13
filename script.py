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


"""
This method acts as the entry point to our program. It will create two different threads to run
our processes concurrently if needed.
"""
def main(quests):
    if quests:
        skills_thread = threading.Thread(target=use_skills, daemon=False)
        skills_thread.start()

        # change the number passed into args as you see fit
        quests_thread = threading.Thread(target=turn_in_quest, args=(1,), daemon=True)
        quests_thread.start()

        skills_thread.join()
        quests_thread.join()
    else:
        use_skills()


"""
This method automatically uses our characters skills for us
"""
def use_skills():
    # continuously make key presses to use the skills in our sequence
    for skill in itertools.cycle(skill_sequence):
        gui.typewrite(skill)
        # delay between each key press (change the numbers as you see fit)
        time.sleep(random.uniform(0.23, 0.36))

        # check if the stop hotkey has been pressed to end the program
        if keyboard.is_pressed("p"):
            notify(round(time.time() - start_time), end=True)
            print("PROGRAM EXITED.")
            os._exit(0)


"""
This method automatically clicks on the game screen and turns in quests for us
"""
def turn_in_quest(interval):
    while True:
        # listen for the quest being completed every 'x' seconds defined by the interval variable
        # for quick quests this interval should be short, for long quests this interval should be longer
        time.sleep(interval)
        if match_img(COMPLETE_IMG, get_location=False) >= MIN_THRESHOLD:
            # click on the quest name
            quest_location = match_img(QUEST_PROGRESS_IMG, get_location=True)
            gui.moveTo(quest_location, duration=random.uniform(0.1, 0.2)) # change these numbers as you see fit
            gui.leftClick()

            time.sleep(random.uniform(0.5, 0.75)) # change these numbers as you see fit

            # click on the turn in button
            turn_in_location = match_img(TURN_IN_IMG, get_location=True)
            gui.moveTo(turn_in_location, duration=random.uniform(0.1, 0.2))
            gui.leftClick()

            time.sleep(random.uniform(2, 2.25))

            # click back onto the quest after turning it in
            gui.moveTo(quest_location, duration=random.uniform(0.1, 0.2))
            gui.leftClick()

            time.sleep(random.uniform(0.5, 0.75))

            # reaccept the quest
            accept_location = match_img(ACCEPT_IMG, get_location=True)
            gui.moveTo(accept_location, duration=random.uniform(0.1, 0.2))
            gui.leftClick()


"""
This helper method screenshots what is currently displayed on screen, compares it to a repository image (needle_img),
and returns the location, (x,y coordinates) of where the repository image is located within the screen.
"""
def match_img(needle_img):
    # save a .PNG image of the entire display and read it in with OpenCV
    screenshot = gui.screenshot()
    screenshot.save(r"PASTE THE DIRECTORY THAT THIS SCRIPT FILE IS IN HERE!")
    haystack_img = cv.imread('screenshot.PNG', cv.IMREAD_COLOR)

    # compare the haystack and needle images to each other
    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

    # store the (x,y) coordinate locations of the lowest and highest confidence regions where an image match was found
    min_confidence, max_confidence, min_location, max_location = cv.minMaxLoc(result)

    if get_location:
        return offset(max_location, 15, 15) # change the numbers as you see fit
    else:
        return max_confidence

    # test code
    # outline_img_match(confidence=max_confidence, location=max_location, h_img=haystack_img, n_img=needle_img)


"""
This method draws a rectangle around a region within the haystack image where the recognition algorithm detected
the highest confidence match between the haystack and needle image. This was used to test that the image/object
detection was working while writing this script.
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


"""
This method sends a desktop notification to the user whenever the program starts or ends
"""
def notify(end_time, end):
    # check if program is ending or starting
    if end:
        end_notification = Notification(app_id="Automation Script",
                                        title="Program Exited.",
                                        msg=f"Program ran for:  {end_time // 60} minute(s) and {end_time % 60} seconds.",
                                        duration="short",
                                        icon="")
        end_notification.show()
    else:
        start_notification = Notification(app_id="Automation Script",
                                        title="Program Started! Spam press the 'p' key to end.",
                                        msg="You have 3 seconds to switch tabs.",
                                        duration="short",
                                        icon="")
        start_notification.show()


"""
This helper method slightly adjusts the coordinates returned by match_img(). This is done so that we ensure
that we are clicking on the object since the coordinates returned by default represent the very top left corner
"""
def offset(location, x, y):
    offset_location = (location[0] + x, location[1] + y)
    return offset_location


# Initialize all constant variables
MIN_THRESHOLD = 0.51
COMPLETE_IMG = cv.imread('complete.PNG', cv.IMREAD_COLOR)
QUEST_PROGRESS_IMG = cv.imread('quest_progress.PNG', cv.IMREAD_COLOR)
TURN_IN_IMG = cv.imread('turn_in.PNG', cv.IMREAD_COLOR)
ACCEPT_IMG = cv.imread('accept.PNG', cv.IMREAD_COLOR)

# Read in the skill sequence as a .txt file and convert it to a list so we can repeatedly iterate over it
text = open("skillSequenceExample.txt")
skill_sequence = [skill for skill in text.read().split()[0]]

# Notify user that the program has started
notify(None, end=False)
print("PROGRAM STARTED. Spam press the 'p' key to end.")
start_time = time.time()
time.sleep(3)

# Pass in quests=True if you want to automate turning in quests, otherwise quests=False
main(quests=True)