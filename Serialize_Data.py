"""
Serialize_Data.py
This module is responsible for generating the training data
the network uses to learn. It only works if the computer is
connected to a Leap Motion Controller.
The data about the hand position is extracted from the Con-
troller and then written to a file. There are 26 files con-
taining training data (one for each letter), found in the
folder letter_files. Each file contains 50 training examples.

A training example consists of 180 numbers which are compo-
nents of the vectors assigned to each bone of the finger.
"""


# imports
import os, sys, inspect, time, keyboard

# Opening the Leap Motion Module
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
from LeapMotionPython import Leap


# Connecting to the Leap Motion Controller
controller = Leap.Controller()


print("Starting Serialization")
time.sleep(1)


# This function generates a letter_file (if it does
# not already exist) and adds one training example to
# the file. As an argument it takes one letter, so that
# it knows which file to append to. 
def AppendFile(currentLetter):
    # telling the user what type of file is being made
    print("making " + currentLetter + "-File. Press a when ready")

    # using the keyboard module to wait until the user is ready
    keyboard.wait(hotkey="a")
    
    # taking the current frame and making a list of visible hands and fingers
    frame = controller.frame()
    hands_list = frame.hands
    fingers_list = frame.fingers

    # filtering out cases where none or both hands are visible
    if(len(hands_list)==1 and len(fingers_list)==5):
        # elements contains all 180 vector components
        elements = []

        # a hand has five fingers, each with 4 bones, each with
        # a x_basis, a y_basis, z_basis, which are vectors with
        # 3 values each
        # this writes all these values to elements
        for finger in fingers_list:
            for i in range(4):
                currentBone = finger.bone(i).basis
                for j in range(3):
                    elements.append(currentBone.x_basis[j])
                for j in range(3):
                    elements.append(currentBone.y_basis[j])
                for j in range(3):
                    elements.append(currentBone.z_basis[j])
        # filtering out errors
        if(len(elements) != 180):
            print("Warning: Invalid number of vectors")


        # appending elements to a file of the appropriate name
        currentFile = currentLetter + "_file.txt"
        textfile = open(currentFile, "a")
        for element in elements:
            textfile.write(str(element) + " ")
        textfile.write("\n")
        textfile.close()

        # confirming a file has been made
        print("made/appended " + currentLetter + "-File")

    else:
        print("Warning: Invalid number of fingers or hands")


# This is where the user can input which letter file to
# write to and how many training examples of that letter
# should be made
for i in range(20):
    AppendFile("x")