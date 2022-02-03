"""
Main.py
This is the main module of this project, where the training of the network happens
There is not much code here, as it mostly connects the other modules and executes their functions
Written in Python 2.7.16

Structure of the full project (purpose of each module at the top of the respective file):

Python:
-Main.py
-Network.py
-Read_Data.py
-Serialize_Data.py
-Application.py

Folders:
-LeapMotionPython
    contains the Leap Motion software
-keyboard
    module used in Serialize_Data.py and Application.py for better user control
-letter_files
    -a_file
    -b_file
    ...
    -z_file
    contains the raw data generated with Serialize_Data.py
"""


# imports
import pickle
from Network import Network
from Read_Data import load_data


# parameters for the network (100, 10, 2.1 respectively seems to work best)
epochs = 100
mini_batch_size = 10
learning_rate = 2.1
# if this is set to true the trained weights and biases are saved for later use
saveTrainedNetwork = False

# loading training_data and test_data from the Read_Data module
training_data, test_data = load_data()


# initializing network with number of neurons in each layer
# 180 input neurons and 26 output neurons shouldn't be changed
# hidden layers can be changed, but [30, 30] seems to work best
net = Network([180,30,30,26])


# training the network and saving it if so requested
if(saveTrainedNetwork):
    biases, weights = net.SGD(training_data, epochs, mini_batch_size, learning_rate, test_data=test_data)
    parameters = [biases, weights]
    with open("trained_network_parameters", "wb") as p:
        pickle.dump(parameters, p)
else:
    net.SGD(training_data, epochs, mini_batch_size, learning_rate, test_data=test_data)