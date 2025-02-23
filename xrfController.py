import sys
import os
import time
from termcolor import colored

PROGRAMDIR   = '/home/xrf/maxrf/xrfController/'
DATADIR     = '/home/xrf/maxrf/data/' 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printBanner():
    print(colored( '''
=============================================================================================
               __                           __              ___   ___                  
             /'___                         /\ \__          /\_ \ /\_ \                 
 __  _ _ __ /\ \__/       ___    ___    ___\ \ ,_\ _ __  __\//\ \\\\//\ \      __  _ __  
/\ \/'/\`'__\ \ ,__\     /'___\ / __`\/' _ `\ \ \//\`'__/ __`\ \ \ \ \ \   /'__`/\`'_\\
\/>  <\ \ \/ \ \ \_/    /\ \__//\ \L\ /\ \/\ \ \ \\\\ \ \/\ \L\ \_\ \_\_\ \_/\  __\ \ \/ 
 /\_/\_\ \_\  \ \_\     \ \____\ \____\ \_\ \_\ \__\ \_\ \____/\____/\____\ \____\ \_\ 
 \//\/_/\/_/   \/_/      \/____/\/___/ \/_/\/_/\/__/\/_/\/___/\/____\/____/\/____/\/_/ 
=============================================================================================
          ''', 'green'))

def runner():
    # Prety printing
    os.system('clear')
    printBanner()
    
    # Getting input parameters
    print(colored("Welcome to the XRF Contorl Interface \n", 'green'))
    filename    = input(colored("Please enter filename: ", 'blue')).strip()
    scanType    = input(colored("Please enter scantype: ", 'blue')).lower().strip()
    if scanType != 'point' and scantype!= 'raster':
        print(colored("Sorry, I don't understand that scan type", 'red'))
        return()
    if scanType == 'raster':
        bottomRightX = input(colored('Bottom right X coordinate: ', 'blue'))
        bottomRightY = input(colored('Bottom right Y coordinate: ', 'blue'))
        TopLeftX     = input(colored('Top left X coordinate: ', 'blue'))
        TopLeftY     = input(colored('Top left Y coordinate: ', 'blue'))
        cellSize     = input(colored('Cell size (default 0.5): '), 'blue')
        rasterSpeed  = input(colored('Raster Speed (default 5)'), 'blue')
    if scanType == 'point':
        time         = input(colored("Please enter scan duration in seconds: ", 'blue'))
    helium      = input(colored("Should Helium be turned on? (y/n) (default n): ", 'blue'))

    #Setting input parameters

    with open(f"{PROGRAMDIR}template.json", 'r') as file:
        filedata = file.read()


    filedata = filedata.replace("BASEFILENAME", filename)

    if scanType == 'point':
        filedata = filedata.replace("BASESCANTYPE", "Point Spectrum")
    if scanType == 'raster':
        filedata = filedata.replace("BAESCANTYPE", "Raster Spectrum")
        filedata = filedata.replace("BASEBOTTOMRIGHTX", bottomRightX)
        filedata = filedata.replace("BASEBOTTOMRIGHTY", bottomRightY)
        filedata = filedata.replace("BASETOPLEFTX", TopLeftX)
        filedata = filedata.replace("BASETOPLEFTY", TopLeftY)
        filedata = filedata.replace("BASECELLSIZE", cellSize)
        filedata = filedata.replace("BASERASTERSPEED", rasterSpeed)



    filedata = filedata.replace("BASETIME", time)

    if helium == 'y':
        filedata = filedata.replace("BASEHELIUM", 'true')
    else:
        filedata = filedata.replace("BASEHELIUM", 'false')

    with open(f'{PROGRAMDIR}out.json', 'w') as file:
        file.write(filedata)
    
    os.system("clear")
    printBanner()
    
    #Confirming input parameters

    print(colored('Name:      ', 'blue'), colored(f'{filename}', 'red'))
    print(colored('Time:      ', 'blue'), colored(f'{time}', 'red'))
    print(colored('Scan type: ', 'blue'), colored(f'{scanType}', 'red'))
    print(colored('Helium:    ', 'blue'), colored(f'{"True" if helium == "y" else "False"}', 'red'))




    response = input(colored('Continue (y/n)?: ', 'blue'))
    if response == 'y':
        os.system(f'source /home/xrf/maxrf/this-iba-imaging.sh && daq_daemon {PROGRAMDIR}out.json') # Running daq_daeon with new json file
        print(colored("Scan done!", 'green'))

        # Adding image info tag to the output files

        response2 = input(colored("Would you like to modify the output files? (y/n): ", 'blue'))
        if response2 == 'y':
            with open(f"{DATADIR}{filename}_detector1.xhyperc", 'r') as file:
                filedata = file.readlines()
            filedata.insert(9, "<Image_Info> \n")
            filedata.insert(10, "<Width>1</Width> \n")
            filedata.insert(11, "<Height>1</Height> \n")
            filedata.insert(12, "<Pixels>1</Pixels> \n")
            filedata.insert(13, "</Image_Info> \n")
            with open(f"{DATADIR}{filename}_detector1.xhyperc", 'w') as file:
                filedata = "".join(filedata)
                file.write(filedata)
            with open(f"{DATADIR}{filename}_detector0.xhyperc", 'r') as file:
                filedata = file.readlines()
            filedata.insert(9, "<Image_Info> \n")
            filedata.insert(10, "<Width>1</Width> \n")
            filedata.insert(11, "<Height>1</Height> \n")
            filedata.insert(12, "<Pixels>1</Pixels> \n")
            filedata.insert(13, "</Image_Info> \n")
            with open(f"{DATADIR}{filename}_detector0.xhyperc", 'w') as file:
                filedata = "".join(filedata)
                file.write(filedata)
            response3 = input(colored("Open maxrf-spectra? (y/n): ", 'blue'))
            if response3 == 'y':
                os.system('source /home/xrf/maxrf/this-iba-imaging.sh && maxrf-spectra')

def main():
    repTest = 0
    runner()
    while repTest == 0:
        response = input(colored("Would you like to run another scan? (y/n): ", 'blue'))
        if response == 'y':
            runner()
        else:
            return()
main()
print(colored("Bye!", 'green'))
time.sleep(1)
os.system("clear")


