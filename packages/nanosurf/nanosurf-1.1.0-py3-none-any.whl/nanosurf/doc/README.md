# Python API for Nanosurf controllers

Package for data acquisition and control of Nanosurf atomic force microscopes.

![Nanosurf Python](https://www.nanosurf.com/images/logos/nsf_python.png)

### Prerequisites

* Python >=3.9 installation on Windows OS.
* A Nanosurf controller software running and a controller connected to the PC.
* Nanosurf Scripting Interface option activated

### Installation

Assuming that a Python interpreter is already installed in the system,
open Windows Command Prompt, or Windows PowerShell and run:
```
pip install nanosurf
```

If for some reason pip does not work, unzip the content of the package
into a folder and in this folder run:
```
python setup.py install
```

### Usage Example
```
import nanosurf

spm = nanosurf.SPM()  # or .C3000() or .CX(), or .CoreAFM()
application = spm.application

scan = application.Scan
opmode = application.OperatingMode
approach = application.Approach
zcontrol = application.ZController
head = application.ScanHead

# Set file mask
mask = "TestSample-"
application.SetGalleryHistoryFilenameMask(mask)

# Choose cantilever
head.CantileverByGUID = spm.CantileverGUID.Dyn190Al

# Operating mode
opmode.OperatingMode = spm.OperatingMode.DynamicAFM
opmode.VibratingAmpl = 0.5 # [V] 

# Set scan parameters
scan.ImageWidth = 5e-6 # [m]
scan.ImageHeight = 5e-6 # [m]
scan.Scantime = 0.55 # s
scan.Points = 256 # points per line
scan.Lines = 256 # lines
scan.CenterPosX = 10e-6 # [m]
scan.CenterPosY = 10e-6 # [m]
scan.SlopeX = 0.0 # degree
scan.SlopeY = 0.0 # degree
scan.Overscan = 5 #%

# Set Z controller parameters
zcontrol.SetPoint = 70 # [%]
zcontrol.PGain = 3100
zcontrol.IGain = 3500

# Start scan
scan.StartFrameUp()

# Check if scanning
scanning = scan.IsScanning
print(scanning)

# Stop scan
scan.Stop()

# Get image
scan.StartCapture()

del spm

```

### Scripting Manual

Full list of objects and methods can be found in the Scripting Manual
in Nanosurf controller software under Help tab:
Help -> Manuals -> Script Programmers Manual, or [here](https://www.nanosurf.com/downloads/programmers-manual.pdf).


### License
[MIT License](https://en.wikipedia.org/wiki/MIT_License)
