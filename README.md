# xrfController
Python scripts to control the XRF

![Demo GIF Showing the basic usage of the tool](https://github.com/nyuad-astroparticle/xrfController/blob/main/demo.gif)

## Dependencies
- termcolor: Needed for colour output

## Usage 
To run the utility, run the following command in a terminal on the XRF computer:
```
xrfController
```
No need to source anything!

The first screen prompts the user for fields to populate the .json file which will be given to ```daq_daemon```.
Here is a list of fields and their expected values

|Field          | Expected input                                            |
|---------------|-----------------------------------------------------------|
|filename       | string                                                    |
|scanType       | either ```point``` or ```raster```                        |
|time           | Int. Time in seconds (only for point scan). Defaults to 10|
|bottomRightX   | Float. (only for raster). Defaults to 100.0               |
|bottomRightY   | Float. (only for raster). Defaults to 100.0               |
|topLeftX       | Float. (only for raster). Defaults to 0.0                 |
|topLeftY       | Float. (only for raster). Defaults to 0.0                 |
|cellSize       | Float. (only for raster). Defaults to 0.5                 |
|rasterSpeed    | Float. (only for raster). Defaults to 5                   |
|helium         | y/n. Defults to n                                         |

After all prompts are given to the program, it replaces the placeholders in the ```template.json``` file with the given values or their defaults and creates an ```out.json``` file.

## Warning system
The next screen shows all the values supplied by the user to let them double check if everything is ok.
The program runs a sanity check when doing raster scans if anything looks off. The warnings currently trigger if:

- ```BottomRightX``` is smaller than ```TopLeftX``` or ```BottomRightY``` is smaller than ```TopLeftY```
- If any of the coordinate fields, cell size, or raster speed are not numbers
- ```cellSize``` does not neatly divide either the image width or height. I don't know if the ```daq_daemon``` would be fine if the division was not neat, but I don't know for sure, and I don't think you'd want to run the program if the division was not neat, so the program lets you know anyway

The program then prompts the user if they want to continue. if the user says yes, then the program calls ```daq_daemon``` with ```out.json``` and prints the output of ```daq_daemon``` as it runs.

## Post Scan Stuff

After the scan is done, the program prompts the user wants it to modify the output files if the scan was a point scan. This is because the current version of ```daq_daemon``` does not add image size information to the output file if it does a point scan. If the user says yes, the program adds the following to the output files:
```
<Image_Info>
<Width>1</Width>
<Height>1</Height>
<Pixels>1</Pixels>
</Image_Info>
```

Then the program asks the user if they want to open ```maxrf-spectra```, and does so if the user desires. This allows the user to immediately see the spectrum acquired if it was a point spectrum without opening a new terminal. If the user wants to continue using the tool, they need to close ```maxrf-spectra```

Finally the tool asks the user if they want to take another spectra. If the user says yes, the screen clears and the program starts over again.

## Tips

If you want to save a specific configuration, you can copy the ```out.json``` file to a safe location and use that directly with ```daq_daemon``` to repeat a scan without entering all the fields again.
