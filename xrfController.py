import sys
import os
import time
def printBanner():
    print('''
=============================================================================================
               __                           __              ___   ___                  
             /'___                         /\ \__          /\_ \ /\_ \                 
 __  _ _ __ /\ \__/       ___    ___    ___\ \ ,_\ _ __  __\//\ \\\\//\ \      __  _ __  
/\ \/'/\`'__\ \ ,__\     /'___\ / __`\/' _ `\ \ \//\`'__/ __`\ \ \ \ \ \   /'__`/\`'_\\
\/>  <\ \ \/ \ \ \_/    /\ \__//\ \L\ /\ \/\ \ \ \\\\ \ \/\ \L\ \_\ \_\_\ \_/\  __\ \ \/ 
 /\_/\_\ \_\  \ \_\     \ \____\ \____\ \_\ \_\ \__\ \_\ \____/\____/\____\ \____\ \_\ 
 \//\/_/\/_/   \/_/      \/____/\/___/ \/_/\/_/\/__/\/_/\/___/\/____\/____/\/____/\/_/ 
=============================================================================================
          ''')
PROGRAMDIR   = '/home/xrf/maxrf/xrfController/'
DATADIR     = '/home/xrf/maxrf/data/' 

def runner():
    # Prety printing
    os.system('clear')
    printBanner()
    
    # Getting input parameters
    print("Welcome to the XRF Contorl Interface \n")
    filename    = input("Please enter filename: ")
    scanType    = input("Please enter scantype: ").lower()
    if scanType != 'point':
        print("Sorry, raster scans are not supported right now")
        return()
    time        = input("Please enter scan duration in seconds: ")
    helium      = input("Should Helium be turned on? (y/n) (default n): ")

    #Setting input parameters

    with open(f"{PROGRAMDIR}template.json", 'r') as file:
        filedata = file.read()


    filedata = filedata.replace("BASEFILENAME", filename)

    if scanType == 'point':
        filedata = filedata.replace("BASESCANTYPE", "Point Spectrum")

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

    print(f'Name: {filename}' )
    print(f'Time: {time}' )
    print(f'Scan type: {scanType}')
    response = input('Continue (y/n)?: ')
    if response == 'y':
        os.system(f'daq_daemon {PROGRAMDIR}out.json') # Running daq_daeon with new json file
        print("Scan done!")

        # Adding image info tag to the output files

        response2 = input("Would you like to modify the output files? (y/n): ")
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
            response3 = input("Open maxrf-spectra? (y/n): ")
            if response3 == 'y':
                os.system('maxrf-spectra')

def main():
    repTest = 0
    runner()
    while repTest == 0:
        response = input("Would you like to run another scan? (y/n): ")
        if response == 'y':
            runner()
        else:
            return()
main()
print("Bye!")
time.sleep(1)
os.system("clear")


