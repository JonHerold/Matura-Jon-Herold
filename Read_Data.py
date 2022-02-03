"""
Read_Data.py
This module is responsible for extracting the letter data
from the letter_files (which should be found in a sub-folder
of that name). After extraction, the data is converted into
a format Network.py can work with and split up into both
training_data and test_data. Naturally, traing_data is for
training the network, test_data is for testing its performance.

This is how training_data is structured:

training_data (type: list) contains:
    training examples (type: tuple) which contain 2 elements:
        -inputs (type: 180-dimensional numpy.ndarry*) where each element is:
            a 1x1 array that contains:
                a single input (type: float)

        -outputs (type: 26-dimensional numpy.ndarry*) where each element is:
            a 1x1 array that contains:
                the desired output for the respective output neuron (type: int)

*In this case a ndarray is basically a list. Network.py uses this format however,
as it is easy to make calculations with. The exact format is explained in greater
detail in the paper.

test_data is structured mostly the same, except that the second element in the
tuple is simply a number, rather than an ndarray. This number represents which output
neuron is the correct one, e.g. "0" for an "a" (the first output neuron), or "3" for a
"d" (the fourth output neuron)
"""

#imports
import random
import numpy as np



# Main function, called by Main.py
def load_data():

    training_data = []
    test_data = []

    # This for-loop goes through every letter_file and adds all training examples to letter_data
    for h in range(26):
        currentLetterNumber = h
        # the current letter is found by converting h into the ascii-value (by adding 97)
        currentLetter = chr(h+97)
        # letter_data holds all the extracted data until it is divided into traing_data and test_data
        letter_data = []

        try:
            # reading all the content from 1 file
            currentFile = "./letter_files/" + currentLetter + "_file.txt"
            file = open(currentFile, "r")
            content = file.read()
            file.close()

            # raw_data is a list where each element contains one training example.
            # The training are still unprocessed though
            raw_data = content.split("\n")
            # filtering out the line break at the end of raw_data
            if(raw_data[-1] == ""):
                raw_data = raw_data[:-1]

            # for each training example in raw_data a inputs and outputs ndarray is generated
            for i in range(len(raw_data)):
                # making the inputs ndarray
                inputs = np.ndarray((180,1))
                vector_list = raw_data[i].split(" ")
                for j in range(180):
                    inputs[j,0] = float(vector_list[j])

                # filling the outputs ndarray with 0's
                outputs = np.ndarray((26,1))
                for j in range(26):
                    outputs[j,0] = 0
                # substituting one 0 for a 1 at the correct position, as given by currenLetterNumber
                outputs[currentLetterNumber,0] = 1

                trainingExample = (inputs, outputs)
                letter_data.append(trainingExample)
        
        # filtering out errors in case no file is found
        except:
            print(currentLetter + "_file does not exist")


        # randomly distributing letter_data into training_data and test_data
        # roughly 80% goes into training_data, the rest into test_data
        random.shuffle(letter_data)
        dataLength = len(letter_data)
        boundary = int(round(dataLength*0.8))
        for i in range(boundary):
            training_data.append(letter_data[i])
        for i in range(boundary, dataLength):
            test_data.append(letter_data[i])


    random.shuffle(training_data)
    random.shuffle(test_data)


    # like explained above, the outputs in test_data need a different format than the
    # outputs in traing_data. This converts every test example into the right format
    # the indexing is a bit confusing here, consult the paper for the details
    for i in range(len(test_data)):
        for neuron in range(26):
            # here: i = current test example / 1 = outputs / neuron = current output neuron
            # 0 = first and only element in the neuron
            if(test_data[i][1][neuron][0] == 1):
                location = neuron
        test_data[i] = [test_data[i][0]]
        test_data[i].append(location)
        test_data[i] = tuple(test_data[i])

    

    return(training_data, test_data)