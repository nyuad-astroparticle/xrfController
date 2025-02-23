import sys
import os
import time
from termcolor import colored

PROGRAMDIR   = '/home/xrf/maxrf/xrfController/'
DATADIR     = '/home/xrf/maxrf/data/' 


#PROGRAMDIR   = '/home/danish/Documents/xrfController/'
#DATADIR     = '/home/danish/Documents/testData/' 

CELLSIZEDEFAULT     = '0.5'
RASTERSPEEDDEFAULT  = '5'
HELIUMDEFAULT       = 'false'

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
    if scanType != 'point' and scanType!= 'raster':
        print(colored("Sorry, I don't understand that scan type", 'red'))
        return()
    if scanType == 'raster':
        bottomRightX = input(colored('Bottom right X coordinate: ', 'blue'))
        bottomRightY = input(colored('Bottom right Y coordinate: ', 'blue'))
        TopLeftX     = input(colored('Top left X coordinate: ', 'blue'))
        TopLeftY     = input(colored('Top left Y coordinate: ', 'blue'))
        cellSize     = input(colored(f'Cell size (default {CELLSIZEDEFAULT}): ', 'blue'))
        rasterSpeed  = input(colored(f'Raster Speed (default {RASTERSPEEDDEFAULT}): ', 'blue'))
    if scanType == 'point':
        time         = input(colored("Please enter scan duration in seconds: ", 'blue'))
    helium      = input(colored(f"Should Helium be turned on? (y/n) (default {HELIUMDEFAULT}): ", 'blue'))
    
    #Setting defaults
    
    if scanType == 'raster':
        if cellSize == '':
            cellSize = CELLSIZEDEFAULT
        if rasterSpeed == '':
            rasterSpeed = RASTERSPEEDDEFAULT
    if helium == 'y':
        helium = 'true'
    else:
        helium = HELIUMDEFAULT

    #Setting input parameters

    with open(f"{PROGRAMDIR}template.json", 'r') as file:
        filedata = file.read()


    filedata = filedata.replace("BASEFILENAME", filename)

    if scanType == 'point':
        filedata = filedata.replace("BASETIME", time)
        filedata = filedata.replace("BASESCANTYPE", "Point Spectrum")
        filedata = filedata.replace("BASEBOTTOMRIGHTX", '100.0') # All of these are to make sure the out.json file is corrctly formatted
        filedata = filedata.replace("BASEBOTTOMRIGHTY", '100.0')
        filedata = filedata.replace("BASETOPLEFTX", '0.0')
        filedata = filedata.replace("BASETOPLEFTY", '0.0')
        filedata = filedata.replace("BASECELLSIZE", CELLSIZEDEFAULT)
        filedata = filedata.replace("BASERASTERSPEED", RASTERSPEEDDEFAULT)
    if scanType == 'raster':
        filedata = filedata.replace("BASESCANTYPE", "Raster Spectrum")
        filedata = filedata.replace("BASEBOTTOMRIGHTX", bottomRightX)
        filedata = filedata.replace("BASEBOTTOMRIGHTY", bottomRightY)
        filedata = filedata.replace("BASETOPLEFTX", TopLeftX)
        filedata = filedata.replace("BASETOPLEFTY", TopLeftY)
        filedata = filedata.replace("BASECELLSIZE", cellSize)
        filedata = filedata.replace("BASERASTERSPEED", rasterSpeed)
        filedata = filedata.replace("BASETIME", '1')    #This it to make sure that the output json file is formatted correctly. 
                                                        #I don't know if it makes a difference 
    filedata = filedata.replace("BASEHELIUM", helium)

    with open(f'{PROGRAMDIR}out.json', 'w') as file:
        file.write(filedata)
    
    os.system("clear")
    printBanner()

    # Sanity checks

    if scanType == 'raster':
        if float(bottomRightX) < float(TopLeftX):
            print(colored('WARNING: BOTTOM RIGHT X COORDINATE IS SMALLER THAN TOP LEFT X COORDINATE', 'yellow'))
        if float(bottomRightY) < float(TopLeftY):
            print(colored('WARNING: BOTTOM RIGHT Y COORDINATE IS SMALLER THAN TOP LEFT Y COORDINATE', 'yellow'))
        if ((float(bottomRightY) - float(TopLeftY)) % float(cellSize) != 0) or ((float(bottomRightX) - float(TopLeftX)) % float(cellSize) != 0):
            print(colored("WARNING: IMAGE SIZE IS NOT DIVISIBLE BY CELL SIZE", 'yellow'))
    #Confirming input parameters

    print(colored('Name:                      ', 'blue'), colored(f'{filename}', 'red'))
    print(colored('Scan type:                 ', 'blue'), colored(f'{scanType}', 'red'))
    if scanType == 'point':
        print(colored('Time:                      ', 'blue'), colored(f'{time}', 'red'))
    elif scanType == 'raster':
        print(colored("Bottom Right X Coordinate: ", 'blue'), colored(f'{bottomRightX}', 'red'))
        print(colored("Bottom Right Y Coordinate: ", 'blue'), colored(f'{bottomRightY}', 'red'))
        print(colored("Top Left X Coordinate    : ", 'blue'), colored(f'{TopLeftX}', 'red'))
        print(colored("Top Left Y Coordinate    : ", 'blue'), colored(f'{TopLeftY}', 'red'))
        print(colored("Cell Size                : ", 'blue'), colored(cellSize, 'red'))
        print(colored("Raster Speed             : ", 'blue'), colored(rasterSpeed, 'red'))
    print(colored('Helium:                    ', 'blue'), colored(helium, 'red'))




    response = input(colored('Continue (y/n)?: ', 'blue'))

    if response == 'y':
        os.system(f'source /home/xrf/maxrf/this-iba-imaging.sh && daq_daemon {PROGRAMDIR}out.json') # Running daq_daeon with new json file
        print(colored("Scan done!", 'green'))

        # Adding image info tag to the output files
        if scanType == 'point':    
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
                filedata.insert(9,  "<Image_Info> \n")
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


