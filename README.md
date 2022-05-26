# Microbit File Manager

A GUI file manager for Linux based OS for the microbit with the MicroPython runtime. __Only tested with Microbit V1.__

I was unable to find a file manager to suit my needs, so I created one.

## Features

+ Select file locations on your local system for uploads and downloads.

+ View contents of files on the Microbit directly in the application - no need to download and then navigate to and open the file.

+ Edit and save files on the Mircobit - simple text editor for basic edits.

+ Delete files on the Microbit.

## Usage

Clone the repository (must have git installed)

```git clone https://github.com/4-3is4-me/Microbit-File-Manager.git```

#### Install dependencies

```pip install guizero, microfs, uflash```

or

```pip3 install guizero, microfs, uflash```

#### Run the appliction

```cd Microbit-File-Manager```

```python MicroFS.py```

or

```python3 MicroFS.py```


To use Microbit File Manager you must have the MicroPython runtime installed on the Microbit. This creates the file system for the File Manager to access. Being able to save files on the Microbit is useful for data logging.

Microbit File Manager contains the latest version of MicroPython for the Microbit V1.

>To flash the V1 MicroPython to your Microbit, plug the Microbit in to a USB port, open Microbit File Manager and select __Create__ from the menu.

Once the MicroPython runtime is flashed to the Microbit, you may use Microbit File Manager to manage the files. To get started, please refer to the MIcrobit MicroPython documentation. Essentially, to run MicroPython code on the Microbit, you must have a file called __main.py__ with the contents of your code uploaded to the Microbit file system.

   *Do not confuse the Microbit USB Mass Storage as the Microbit file system - they are separate. You will not be able to access the files in the file system from the USB Mass Storage.*

___

### Hiccups

The Microbit USB Mass Storage must be mounted to flash the MicroPython runtime.

___

### To Do

+ Test with Microbit V2.
+ Add V2 version of MicroPython and version check.
+ Package as executable.

___

###  Disclaimer

*This is not a professional application, use at your own risk. I will not be responsible for issues created by the use of this application.*

####  Advert

*If you would like some poorly drawn icons for your application, please don't contact me!*


