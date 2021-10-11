#!/usr/bin/python3

# Made by Juno
# Program to compare two MAC address dumps (such as a unique filtered hcitool scan)
# and find any addresses that appear in one and not the other. 
#
# Example for use, testing bluetooth footprint of equipment. Run a baseline scan, saved
# to a file. Turn on equipment and run another scan saved to a different file. Run both
# files through this script to see if there are any different addresses.
#
# Don't change anything below this line!
##################################################################################

# used for input flags
import sys
# used for finding text that matches a pattern
import re
# used for file paths
import os
# used for iterating
import itertools

# help text displayed when requested
def displayHelp():
    print("Usage: ./macComparer.py --baseline \"/path/to/baseline/scan\" --input \"/path/to/macAddress/list\" --input \"/path/to/macAddress/other/list\"")
    print()
    print("-b \t--baseline \tThe path to the baseline scan file that has been uniquely filtered.")
    print("-i \t--input \tThe path to the file that was uniquely filtered from hcitool.")
    print("-h \t--help \t\tDisplay this help")
    exit()

# test the path of the input file and open/read file
def loadFile(filePath, inputSet):
    readData = ""
    # try opening the file
    try: 
        with open(filePath, 'r') as file:
            readData = file.read()
    except Exception as e: 
        print("Error reading file (", filePath, "):", e)
        exit()    
    # find the mac addresses
    allMACS = re.findall(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', readData)
    # drop them into the passed in set
    for MAC in enumerate(allMACS):
        inputSet.add(MAC[1].lower())

# prints the difference between the first set in the list, and every other set
def printDifferences(listOfMACSets, filePaths):
    for i, MACSet in enumerate(listOfMACSets):
        # don't compare the baseline list to itself
        if i > 0:
            comparedMACList = MACSet.difference(listOfMACSets[0])
            printList(comparedMACList, filePaths[i])

# does the printing 
def printList(comparedList, filePath):
    print("Items in ", filePath, " and not in Baseline:")
    for item in comparedList:
        print(item)    

# Variables
# put the flags given here
flags = sys.argv

def main():
    # Variables
    # sets to hold the mac address lists
    MACAddressSets = []
    # file paths for files
    filePaths = []

    # if user has asked for help, or not given any inputs
    if len(flags) == 1 or len(flags) > 1 and flags[1] == "--help" or flags[1] == "-h":
        displayHelp()
    
    # get the info from the user's command
    # only one baseline allowed
    alreadyHadBaseline = False
    for index, token in enumerate(flags):
        # set the baseline
        if token == '--baseline' or token == '-b':
            if alreadyHadBaseline:
                print("Only one baseline file allowed. Enter compare files as -i or --input.")
                exit()
            # baseline scan is stored at the start of the filepaths list
            filePaths.insert(0, flags[index + 1])
            alreadyHadBaseline = True
        if token == '--input' or token == '-i':
            filePaths.append(flags[index + 1])
    # if no flags given, display the help
    if len(filePaths) < 2 or not alreadyHadBaseline:
        displayHelp()

    for filePath in filePaths:
        MACSet = set()
        loadFile(filePath, MACSet)
        MACAddressSets.append(MACSet)
    
    printDifferences(MACAddressSets, filePaths)
    

if __name__ == '__main__':
    main()


