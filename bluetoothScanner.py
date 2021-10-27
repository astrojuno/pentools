#!/usr/bin/python3

#########################################################
#   Script to scan bluetooth, and then scan again.      #
#   Use case is for testing if equipment is broadcasting#
#   a bluetooth signature.                              #
#                                                       #
#   Do the initial baseline scan, plug in your equipment#
#   do your second scan. Any differences are displayed. #
#########################################################

# used for flags
import sys
# used to capture bash output
import subprocess
# used for matching patterns in strings
import re
# used for sleeping
import time
# used for multiple threads
import threading
# used for coloured terminal text
import colorama
# used for iterating
import itertools
# used to get a password
import getpass

# help for the user
def displayHelp():
    print("Usage: ./blutoothScanner.py")
    print("Follow the prompts to do a baseline scan.")
    print("Plug in your equipment to test, and follow the")
    print("prompts to do your second scan.")
    print("Differences will be displayed.")
    print()
    exit()

# tokenises the user input and acts on the flags
def tokeniseCommand():
    # tokenize the relevant inputs
    for index, token in enumerate(flags):
       if token == '--help' or token == '-h':
           displayHelp()

# gets and returns which bluetooth adapter to use as a string
def getAdapter(blueDevices, firstBlueDevice):
    # if there's a difference, use the new one. If not, default to the highest number (hci1 over hci0...)
    deviceToUse = ""
    newDevices = re.findall(r'hci+.', blueDevices.stdout.decode('utf-8'))
    # close out if no bluetooth adapters found
    if newDevices.count == 0:
        print("No bluetooth adapters found.")
        print("Quitting...")
        exit()
    if firstBlueDevice.stdout != blueDevices.stdout:
        oldDevices = re.findall(r'hci+.', firstBlueDevice.stdout.decode('utf-8'))
        # this array shouldn't be more than a few elements, so using a slow search here
        for device in newDevices:
            if device not in oldDevices:
                deviceToUse = device
    else:
        deviceToUse = newDevices[0]
        for device in newDevices:
            if device > deviceToUse:
                deviceToUse = device
    return deviceToUse

# displays a nice spinner to pass the time
# time passed should be an int representing seconds
def displaySpinner():
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    counter = 0.0
    while counter < scanTime:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        counter += 0.1
        time.sleep(0.1)

# kicks off the spinner
def startSpinner():
    spinnerProcess = threading.Thread(target=displaySpinner)
    spinnerProcess.daemon = True
    spinnerProcess.start()

# takes a scan file from subprocess and returns a set of MACs
def cleanScanFile(scanFile):
    scanString = scanFile.decode('utf-8')
    allMACs = re.findall(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', scanString)
    MACsToReturn = set()
    for mac in enumerate(allMACs):
        MACsToReturn.add(mac[1].lower())
    
    return MACsToReturn

# takes two sets and nicely prints the elements in the second that are not in the first
def printDifference(firstSet, secondSet):
    # elements present in second that are not in first
    diff = secondSet - firstSet
    # if there are no entries
    if len(diff) == 0:
        print("No new bluetooth devices found in second scan")
    else:
        print("Anomalies found:")
        print("-----------------")
        for mac in diff:
            print(mac)

# submits an array of commands to the system
# cmd should conform to: ['command', 'option', 'more']
# returns a tuple in the form of (success, process)
def runBashCommand(cmd, sudoPassword=None):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, _ = process.communicate("{}\n".format(sudoPassword).encode('utf-8'))
    # return the result
    return (process.returncode, output)

# runs a bluetooth scan
def runBluetoothScan(sudoPass):
    startSpinner()
    scanRunTime = str(scanTime) + 's'
    scanCommand = ['sudo', 'timeout', scanRunTime, 'hcitool', 'lescan']
    return runBashCommand(scanCommand, sudoPass)

# brings the specified adapter up
def bringAdapterUp(adapter, sudoPass):
    hciConfigCommandUp = ['sudo', 'hciconfig', adapter, 'up']
    configResult = runBashCommand(hciConfigCommandUp, sudoPass)
    # if we failed to bring the adapter up
    if configResult[0] != 0:
        print("Unable to start bluetooth adapter. Not all adapters can be used.")
        print("Quitting...")
        exit()
    else: 
        return True

# brings the specified adapter down
def bringAdapterDown(adapter, sudoPass):
    hciConfigCommandDown = ['sudo', 'hciconfig', adapter, 'down']
    configResult = runBashCommand(hciConfigCommandDown, sudoPass)
    # if we failed to bring the adapter down
    if configResult[0] != 0:
        print("Trouble bringing the bluetooth adapter down. Try reconnecting and starting again.")
        print("Quitting...")
        exit()
    else: 
        return True


# Variables
# put the flags given here
flags = sys.argv
# how long to perform a scan for in seconds
scanTime = 5

# main entry point
def main():
    # deal with any user flags
    tokeniseCommand()

    # run a quick scan of the computer for bluetooth dongles
    firstBlueDevice = subprocess.run(['hciconfig'], stdout=subprocess.PIPE)
    
    print("About to run baseline scan. You will be asked for your sudo password. This app does not access your password, and it is only used to run the hci commands.")
    print("Make sure the equipment you want to test for a bluetooth signature is OFF.")
    input("Plug in your bluetooth dongle and press enter when ready.")

    # run a second scan of the computer. 
    blueDevices = subprocess.run(['hciconfig'], stdout=subprocess.PIPE)

    # get which adapter to use
    bluetoothAdapter = getAdapter(blueDevices, firstBlueDevice)
    
    passwordRequest = "[sudo] password for " + getpass.getuser() + ": "
    sudoPass = getpass.getpass(passwordRequest)
    
    # bring the adapter up
    if bringAdapterUp(bluetoothAdapter, sudoPass):
        print("Using adpater", bluetoothAdapter)

    # run the bluetooth baseline scan
    scanResult = runBluetoothScan(sudoPass)
  
    # get a clean set of macs from the scans
    baselineMACs = cleanScanFile(scanResult[1])

    # turns out, this leaves the adapter up and running. so we need to reset it to just 'up'
    bringAdapterDown(bluetoothAdapter, sudoPass)
    bringAdapterUp(bluetoothAdapter, sudoPass)
    # run the scan to see if the equipment is broadcasting
    input("Start the equipment you want to scan and press enter")
    print("Running detector scan...")
    scanResult = runBluetoothScan(sudoPass)

    # bring the adapter back down
    bringAdapterDown(bluetoothAdapter, sudoPass)

    # get a clean copy of the new scan
    targetScanMACs = cleanScanFile(scanResult[1])

    # print the difference between the two scans
    printDifference(baselineMACs, targetScanMACs)

if __name__ == '__main__':
    main()
