#!/bin/python2
"""Runs the program."""

from lsstbroker.binary_classifier import *
from lsstbroker.classifier import *
from lsstbroker.classifier_box import *
from lsstbroker.handler import *
from lsstbroker.observation import *

import getpass
import sys

from period04 import get_period


def main():
    if len(sys.argv) < 2:
        print "Need input file names."
        sys.exit(1)

    input_files = sys.argv[1:]
    handler = create_handler()

    process_files(input_files, handler)

def process_files(input_files, handler):
    for input_file in input_files:
        process_input_file(input_file, handler)

def process_input_file(input_file, handler):
    print input_file
    observations = get_observations(input_file)
    for observation in observations:
        handler.run(observation)

def get_observations(input_file):
    lines = [line.rstrip('\n').split(" ") for line in open(input_file)]

    observations = []
    for line in lines:
        time = float(line[0])
        light = float(line[1])
        error = float(line[2])
        obs = Observation(input_file, time, light, error)
        observations.append(obs)

    return observations

def create_handler():
    # Create BinaryClassifier
    name = "Period"
    function = get_period
    binary_classifier = BinaryClassifier(name, function)

    # Create Classifier
    classifier = Classifier()
    classifier.add_binary_classifier(binary_classifier)

    # Create ClassifierBox
    classifier_box = ClassifierBox()
    classifier_box.add_classifier(classifier)

    # Create handler
    host = "localhost"
    database = raw_input("Database: ")
    username = raw_input("Username: ")
    password = getpass.getpass()
    handler = MySqlDatabaseHandler(host, database, username, password)
    handler.set_classifier_box(classifier_box)

    return handler

# Run main function
if __name__ == "__main__":
    main()
