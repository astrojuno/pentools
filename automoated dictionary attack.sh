#!/bin/bash

hashcat -m 16800 -a 0 -w 3 -o big1CrackedPassword '/home/juno/Documents/22WilliamSt/22WilliamsHashOutput.txt' '/home/juno/ESA/Wordlists/ESA Top/Next Batch/BIG-WPA-LIST-1' 

touch /home/juno/big1Done
cp /home/juno/.hashcat/hashcat.potfile /home/juno/.hashcat/hashcat.potfile.big1
rm /home/juno/.hashcat/hashcat.potfile

hashcat -m 16800 -a 0 -w 3 -o big2CrackedPassword '/home/juno/Documents/22WilliamSt/22WilliamsHashOutput.txt' '/home/juno/ESA/Wordlists/ESA Top/Next Batch/BIG-WPA-LIST-2' 

touch /home/juno/big2Done
cp /home/juno/.hashcat/hashcat.potfile /home/juno/.hashcat/hashcat.potfile.big2
rm /home/juno/.hashcat/hashcat.potfile


hashcat -m 16800 -a 0 -w 3 -o big3CrackedPassword '/home/juno/Documents/22WilliamSt/22WilliamsHashOutput.txt' '/home/juno/ESA/Wordlists/ESA Top/Next Batch/BIG-WPA-LIST-3' 

touch /home/juno/big3Done
cp /home/juno/.hashcat/hashcat.potfile /home/juno/.hashcat/hashcat.potfile.big3
rm /home/juno/.hashcat/hashcat.potfile


hashcat -m 16800 -a 0 -w 3 -o top2BillionCrackedPassword '/home/juno/Documents/22WilliamSt/22WilliamsHashOutput.txt' '/home/juno/ESA/Wordlists/ESA Top/Next Batch/Top2Billion-probable-v2.txt' 

touch /home/juno/top2BillionDone
cp /home/juno/.hashcat/hashcat.potfile /home/juno/.hashcat/hashcat.potfile.1billion
rm /home/juno/.hashcat/hashcat.potfile

