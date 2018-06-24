"""
Darren Hobern
Assignment 1
COMP 307
2017
"""

import sys
from enum import Enum

# Global variables
sepal_length_max = sys.maxsize
sepal_width_max = sys.maxsize
petal_length_max = sys.maxsize
petal_width_max = sys.maxsize

sepal_length_min = sys.maxsize*-1
sepal_width_min = sys.maxsize*-1
petal_length_min = sys.maxsize*-1
petal_width_min = sys.maxsize*-1

# Constants
NUM_DATA_POINTS = 5    # Number of data points per line in the dataset
# Lists
training_nodes_list = []    # List of all the training nodes
test_nodes_list = []    # List of all the test nodes

argv = sys.argv
argc = len(argv)


class DataType(Enum):

    def __str__(self):
        return self.value

    TRAINING = 1
    TEST = 2


class TrainingNode:
    """ Node class for a training iris.
        Notably iris_name is included in the data set.
    """

    def __init__(self, sepal_length,
                 sepal_width,
                 petal_length,
                 petal_width,
                 iris_name):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.iris_name = iris_name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = self.sepal_length + " " + self.sepal_width
        + " " + self.petal_length
        + " " + self.petal_width
        + " " + self.iris_name
        return string


class TestNode:
    """ Node class for a test iris.
        Notably iris_name will be compared with calibrated_name
            to test the accurracy of the classifier.
    """

    def __init__(self, sepal_length,
                 sepal_width,
                 petal_length,
                 petal_width,
                 iris_name):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.iris_name = iris_name
        self.calibrated_name = ""
        self.distances = {}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = "{0} {1} {2} {3} {4} {5}".format(self.sepal_length,
                                                  self.sepal_width,
                                                  self.petal_length,
                                                  self.petal_width,
                                                  self.iris_name,
                                                  self.calibrated_name)
        return string


def read_file(file_name, data_type):
    """ Reads a file. """
    # Global variables for test/training lists
    global training_nodes_list
    global test_nodes_list
    global sepal_length_max, sepal_length_min
    global sepal_width_max, sepal_width_min
    global petal_length_max, petal_length_min
    global petal_width_max, petal_width_min

    with open(file_name) as data:
        line_no = 0
        for line in data:
            line_no += 1
            # If the line has no data in it ignore
            if len(line) <= 1:
                continue

            # Remove whitespace and newline characters, then split into list
            ln = line.strip().split()

            if len(ln) != NUM_DATA_POINTS:
                print("Invalid number of data points were found on "
                      "line {}".format(line_no))
                continue

            # Convert values to floats so they may be processed
            sepal_length = float(ln[0])
            sepal_width = float(ln[1])
            petal_length = float(ln[2])
            petal_width = float(ln[3])

            iris_name = ln[4].lower()   # To lower for easier processing

            # Process the line into an iris object
            if data_type is DataType.TRAINING:
                training_nodes_list.append(TrainingNode(sepal_length,
                                                        sepal_width,
                                                        petal_length,
                                                        petal_width,
                                                        iris_name))
                # Update max/min for calculating ranges later
                # Sepal Length
                sepal_length_max, sepal_length_min = update_max_min(
                    sepal_length, sepal_length_max, sepal_width_max)
                # Sepal Width
                sepal_width_max, sepal_width_min = update_max_min(
                    sepal_width, sepal_width_max, sepal_width_min)
                # Petal Length
                petal_length_max, petal_length_min = update_max_min(
                    petal_length, petal_length_max, petal_length_min)
                # Petal Width
                petal_width_max, petal_width_min = update_max_min(
                    petal_width, petal_width_max, petal_width_min)

            elif data_type is DataType.TEST:
                test_nodes_list.append(TestNode(sepal_length, sepal_width,
                                                petal_length, petal_width,
                                                iris_name))
            else:
                print("Error, invalid data type from "
                      "file {}".format(file_name))


def update_max_min(data, maximum, minimum):
    """ Calculates the range  """

    return max(data, maximum), min(data, minimum)


def calculate_distance_vector(node1, node2):
    """ Calculates the distance between two nodes using their data values """

    global sepal_length_max, sepal_length_min
    global sepal_width_max, sepal_width_min
    global petal_length_max, petal_length_min
    global petal_width_max, petal_width_min

    # Inner class to get the normalised difference squared
    def difference_squared_normalised(val1, val2, val3):
        return (val1 - val2)**2 / val3**2

    sepal_length_range = sepal_length_max - sepal_length_min
    sepal_width_range = sepal_width_max - sepal_width_min
    petal_length_range = petal_length_max - petal_length_min
    petal_width_range = petal_width_max - petal_width_min

    # sqrt( (a1 - b1)^2 / R^2
    sepal_length = difference_squared_normalised(node1.sepal_length,
                                                 node2.sepal_length,
                                                 sepal_length_range)

    sepal_width = difference_squared_normalised(node1.sepal_width,
                                                node2.sepal_width,
                                                sepal_width_range)

    petal_length = difference_squared_normalised(node1.petal_length,
                                                 node2.petal_length,
                                                 petal_length_range)

    petal_width = difference_squared_normalised(node1.petal_width,
                                                node2.petal_width,
                                                petal_width_range)

    # Sum and square root attribute differences
    return (sepal_length + sepal_width + petal_length + petal_width)**0.5


def calculate_nearest_neighbour(distances):
    """ Calculates the nearest neighbours  """

    global number_of_neighbours     # How many neighbours to look for
    nearest_neighbours = []
    for count in range(number_of_neighbours):
        """ Sets 'nearest' to the training node by getting the
            minimum distance from the dict and using that as a key
            to access the node value
        """
        nearest = min(distances)
        # Add training node to nearest_neighbours list
        nearest_neighbours.append(distances[nearest])
        # Remove training_node from distances dict
        # so we can find the next nearest neighbour
        del distances[nearest]

    return nearest_neighbours


def classify(test_node, nearest_neighbours):
    """ Classifies the node as the most frequent class of its neighbours """

    names_dict = {}
    # Count the freqency of class names from nearest neighbours
    for node in nearest_neighbours:
        name = node.iris_name
        if node.iris_name not in names_dict:
            names_dict[name] = 0
        else:
            names_dict[name] += 1

    test_node.calibrated_name = max(names_dict)


def test_classifier():
    """ Tests the calibrated_name against the actual name
        for all of the test nodes and calculates how many
        were correct, printing a percentage score.
    """

    global test_nodes_list
    global number_of_neighbours

    score = 0   # Number of test cases correct
    count = 0   # Total number of test cases
    print("Calibrated:\t\tActual:\t\t\tCorrect:")
    for test_node in test_nodes_list:
        count += 1
        output = "{0}\t\t{1}\t\t".format(test_node.calibrated_name,
                                         test_node.iris_name)
        if test_node.calibrated_name == test_node.iris_name:
            score += 1
            output += "Hit"
        else:
            output += "Miss"

        print(output)
    percent = int(score/count*100)
    print("With a K value of {0}, the classifier successfully got "
          "{1} percent correct".format(number_of_neighbours, percent))


# Main code body
if __name__ == "__main__":
    if argc != 4:
        print("ERROR: requires arguments <training> <test> <k>")
        exit(1)

    training_path = argv[1]
    test_path = argv[2]
    number_of_neighbours = int(argv[3])

    read_file(training_path, DataType.TRAINING)     # Read the training file
    read_file(test_path, DataType.TEST)             # Read the test file

    """ For each test node iterate over each training node
    and calculate the distance vector beween the two nodes.
    Select the smallest k distances and classify as the most commonly
    occuring class.
    """

    for test_node in test_nodes_list:
        for training_node in training_nodes_list:
            distance = calculate_distance_vector(training_node, test_node)
            test_node.distances[distance] = training_node
        nearest_neighbours = calculate_nearest_neighbour(test_node.distances)
        classify(test_node, nearest_neighbours)

    test_classifier()
