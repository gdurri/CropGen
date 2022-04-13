# CropGen

The goal of CropGen is to optimise crop design through the connection of an optimisation algorithm with APSIM-Sorghum

## APSIM Wrapper

CropGen can run apsim by using the apsim wrapper, which is implemented in
apsim.py. There are two classes - `ApsimOptions` and `ApsimRunner`.
`ApsimOptions` contains the path to the Models executable and the path to the
.apsimx file to be run. In the future it might be a good idea to expand this
class to contain other optional settings which may be passed to the apsim CLI
(such as max # of CPUs to use).

In order to use the apsim wrapper, the user will first need to install apsim on
their computer (or compile it). Apsim instalers are available
[here](https://registration.apsim.info/). Once installed, open the apsim
installation path and locate Models.exe (or Models on Linux/mac). The path to
this file must be passed as the `exe` argument to the `ApsimOptions`
constructor. The other required option is the path to the .apsimx file to be
run. There is a sample .apsimx file included in this repository, located at
`apsim-inputs/sorghum-simple/sorg.apsimx`.
