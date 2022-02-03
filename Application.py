"""
Application.py
This file is used to test a trained network. It only works
if the computer is connected to a Leap Motion Controller.

Specifically it lets the user spell out a word in sign language.
Press a to submit a letter.
Press t to print out the finished word.

With every letter a confidence rating is printed.
"""


# imports
import pickle, keyboard, sys, os, inspect, time
import numpy as np
from Network import sigmoid


# Opening the Leap Motion Module
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
from LeapMotionPython import Leap

# connecting to the controller
controller = Leap.Controller()

# function taken from Network.py to feedforward inputs (a) through a trained network
def feedforward(a):
    for b, w in zip(biases, weights):
        a = sigmoid(np.dot(w, a)+b)
    return a

# function taken and slightly altered from Serialize_Data.py
# it converts a hand object into elements, a list of all the inputs
def Serialize():
    elements = []
    frame = controller.frame()
    hands_list = frame.hands
    fingers_list = frame.fingers
    if(len(hands_list)==1 and len(fingers_list)==5):
        elements = []
        for finger in fingers_list:
            for i in range(4):
                currentBone = finger.bone(i).basis
                for j in range(3):
                    elements.append(currentBone.x_basis[j])
                for j in range(3):
                    elements.append(currentBone.y_basis[j])
                for j in range(3):
                    elements.append(currentBone.z_basis[j])
        if(len(elements) != 180):
            print("Warning: Invalid number of vectors")
    else:
        print("Warning: Invalid number of fingers or hands")
    
    return elements



# load the trained network into biases and weights
# if no trained network exists, one can be generated with Main.py
with open("trained_network_parameters", "rb") as p:
    parameters = pickle.load(p)
biases = parameters[0]
weights = parameters[1]


# letting the user spell a word in sign language
text = ""
print("Please spell a word in sign language!")

while True:
    print("Press a to submit a letter, press t to terminate program")
    pressed = keyboard.read_key()
    if(pressed == "a"):
        
        # calling Serialize() to take a "snapshot"
        elements = Serialize()

        # converting inputs into the ndarry format
        inputs = np.ndarray((180,1))
        for i in range(180):
            inputs[i,0] = float(elements[i])
        
        # feedforward the inpus to get result, which is the list of outputs of the output neurons
        result = feedforward(inputs)

        #finding the highest output i.e. the most likely letter
        max_value = 0
        for i in range(26):
            if(result[i] > max_value):
                max_value = result[i]
                max_value_index = i
        # using ascii-values to convert a number into a letter
        letter = chr(max_value_index+97)

        # printing the letter together with a confidence rating
        #print(result)
        print("Scanned as a " + letter + ", with a certainty of " + str(round(max_value, 2)*100) + "%")
        text = text + letter
        time.sleep(1)
        

    if(pressed == "t"):
        # adding the letter to the text
        print(text)
        quit()