#!/usr/bin/python3

# Made by Juno
# Program to display the vendors when scanning using Aircrack
# Run this after starting Aircrack, any found MAC addresses will be listed
# Add any vendors you want to be coloured here. The program will just use partial 
# matches, so "ring" will also flag "engineering". This list is case agnostic.
vendorsToShowInRed = ["arlo", "ring"]
vendorsToShowInBlue = []
vendorsToShowInGreen = []

# Don't change anything below this line!
##################################################################################

# used for input flags
import sys
# used for finding text that matches a pattern
import re
# used for file paths
import os
# used for sleep
import time
# used for concurrent threads
import threading
# used for iterating
import itertools
# used for coloured terminal output
import colorama

# help text displayed when requested
def displayHelp():
    print("Usage: ./macAddressFinder.py --database \"/path/to/macAddress/database.csv\" --captureFile \"/path/to/aircrack/output.csv\"")
    print()
    print("Run this script AFTER starting your Aircrack capture.")
    print("CTRL-C to exit the program")
    print()
    print("-c \t--captureFile \tThe path to the Aircrack csv capture file.")
    print("-d \t--database \tThe path to the database of MAC address prefixes.")
    print("\t\tMust be in the format XX:XX:XX, Vendor Name")
    print("-i \t--ignore \tDo not print (ignore) MAC addresses that return 'No Vendor Found'")
    print("-h \t--help \tDisplay this help")
    exit()

# displays a nice spinner to show we haven't frozen
def displaySpinner():
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while True:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)

# test the path of the database and open/read file
def loadDatabase(databasePath, macPrefixes):
    # characters we don't want in our vendor string
    charToOmit = ",\t\n\f\r\""
    # try opening the file
    try: 
        with open(databasePath, 'r') as databaseFile:
            # put the data into our dictionary
            for line in databaseFile:
                (key, value) = line.split(",", 1)
                # clean the string
                for c in charToOmit: 
                    value = value.replace(c, "")
                macPrefixes[key.lower()] = value
    except Exception as e: 
        print("Error reading database:", e)
        exit()

# test the path of the capture and open/read file
def loadCapture(capturePath, foundMacs):
    read_data = ""
    # try opening the file
    try: 
        with open(capturePath, 'r') as captureFile:
            read_data = captureFile.read()
    except Exception as e: 
        print("Error reading capture file:", e)
        print("Make sure Aircrack has already started...")
        exit()    
    allMatches = re.findall(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', read_data)
    for match in enumerate(allMatches):
        foundMacs.add(match[1].lower())

# print the found mac address and their vendors
def printFoundMacs(foundMacs, printedMacs, macPrefixes, hideNoVendorFound):
    for mac in foundMacs:
        if mac not in printedMacs:
            # to keep track of when it has been printed in a colour
            needsPrinting = True
            # add it to the list of printed macs
            printedMacs.append(mac.lower())
            # get the prefix for the vendor
            macPrefix = mac[:8]

            # assign the vendor from the database. if it's not in the database give it
            # no vendor found
            vendor = macPrefixes.get(macPrefix.lower(), "No vendor found")

            # exit out if do not print no vendor flag has been set
            if hideNoVendorFound and vendor == "No vendor found":
                pass

            else:
                for name in vendorsToShowInRed: 
                    if name.lower() in vendor.lower():
                        print(f"{colorama.Fore.RED}", mac, "\t", vendor, f"{colorama.Style.RESET_ALL}")
                        needsPrinting = False
                        break
                for name in vendorsToShowInBlue:
                    if name.lower() in vendor.lower(): 
                        print(f"{colorama.Fore.BLUE}", mac, "\t", vendor, f"{colorama.Style.RESET_ALL}")
                        needsPrinting = False
                        break
                for name in vendorsToShowInGreen: 
                    if name.lower() in vendor.lower():
                        print(f"{colorama.Fore.GREEN}", mac, "\t", vendor, f"{colorama.Style.RESET_ALL}")
                        needsPrinting = False
                        break
                if needsPrinting:
                    print("", mac, "\t", vendor)

# Variables
# put the flags given here
flags = sys.argv

def main():
    # Variables    
    # inputs
    database = ""
    capture = ""
    # dictionary to hold our prefixes
    macPrefixes = {}
    # set of found mac addresses
    foundMacs = set()
    # list of printed mac addresses
    printedMacs = []
    # flag for hiding no vendor found macs
    hideNoVendorFound = False

    # if user has asked for help, or not given any inputs
    if len(flags) == 1 or len(flags) > 1 and flags[1] == "--help" or flags[1] == "-h":
        displayHelp()

    # tokenize the relevant inputs
    for index, token in enumerate(flags):
        # set the database
        if token == '--database' or token == '-d':
            database = flags[index + 1]
        # set the capture file
        if token == '--captureFile' or token == '-c':
            capture = flags[index + 1]
        if token == '--ignore' or token == '-i':
            hideNoVendorFound = True
        if token == '--help' or token == '-h':
            displayHelp()
    # if no database or capture found, display help
    if database == "" or capture == "" :
        displayHelp()

    # load the database file
    loadDatabase(database, macPrefixes)

    # load the capture file
    loadCapture(capture, foundMacs)

    # block of code for keyboard intuerrupt
    try: 
        # start some visual feedback to the user knows we haven't frozen
        spinnerProcess = threading.Thread(target=displaySpinner)
        spinnerProcess.daemon = True
        spinnerProcess.start()
        # exit direction for user
        print("ctrl-c to exit")
        # heading
        print("Found MAC Addresses \tVendor")
        print("----------------------------------")

        # infinite loop to print results
        while True:
            loadCapture(capture, foundMacs)
            printFoundMacs(foundMacs, printedMacs, macPrefixes, hideNoVendorFound)
            time.sleep(3)

    except KeyboardInterrupt:
        print("Quitting...")
        exit()

if __name__ == '__main__':
    main()
