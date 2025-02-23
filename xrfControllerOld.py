import sys
import os
os.system('clear')
with open("template.json", 'r') as file:
    filedata = file.read()
filedata = filedata.replace("BASEFILENAME", sys.argv[1])
filedata = filedata.replace("BASETIME", sys.argv[2])
with open('out.json', 'w') as file:
    file.write(filedata)

print(f'Name: {sys.argv[1]}' )
print(f'Time: {sys.argv[2]}' )
print(f'Scan type: {sys.argv[3]}')
response = input('Continue (y/n)?: ')
if sys.argv[3] != 'point':
    print("Sorry, raster scans are not supported right now")
else:
    if response == 'y':
        os.system('daq_daemon out.json')
        print("Scan done!")
        response2 = input("Would you like to modify the output files? (y/n): ")
        if response2 == 'y':
            with open(f"../data/{sys.argv[1]}_detector1.xhyperc", 'r') as file:
                filedata = file.readlines()
            filedata.insert(9, "<Image_Info> \n")
            filedata.insert(10, "<Width>1</Width> \n")
            filedata.insert(11, "<Height>1</Height> \n")
            filedata.insert(12, "<Pixels>1</Pixels> \n")
            filedata.insert(13, "</Image_Info> \n")
            with open(f"../data/{sys.argv[1]}_detector1.xhyperc", 'w') as file:
                filedata = "".join(filedata)
                file.write(filedata)
            with open(f"../data/{sys.argv[1]}_detector0.xhyperc", 'r') as file:
                filedata = file.readlines()
            filedata.insert(9, "<Image_Info> \n")
            filedata.insert(10, "<Width>1</Width> \n")
            filedata.insert(11, "<Height>1</Height> \n")
            filedata.insert(12, "<Pixels>1</Pixels> \n")
            filedata.insert(13, "</Image_Info> \n")
            with open(f"../data/{sys.argv[1]}_detector0.xhyperc", 'w') as file:
                filedata = "".join(filedata)
                file.write(filedata)
            response3 = input("Open maxrf-spectra? (y/n): ")
            if response3 == 'y':
                os.system('maxrf-spectra')
        
print("Bye!")


