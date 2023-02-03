# CropGen

The goal of CropGen is to optimise crop design through the connection of an
optimisation algorithm with APSIM-Sorghum

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

## APSIM Server Wrapper

The apsim server wrapper uses the
[apsim server](https://apsimnextgeneration.netlify.app/usage/server) feature to
run simulations. This should be faster than using the "standard" apsim wrapper,
although the differences will be more significant for shorter simulations. The
caveat is that the apsim server wrapper cannot be run on windows. The workaround
is to use visual studio code for
[remote debugging](https://code.visualstudio.com/docs/remote/remote-overview) on
a remote (Linux) VM.

1. Connect to the remote VM from inside vscode
   - See above link for vscode instructions. You need to install the remote
     debugging extension.
   - See Drew/Jason for login details (ssh keypair)
2. Upload your .apsimx/.met files [here](https://cropgen.cgmwgp.com)
   - Ensure that your .apsimx file uses relative paths for the .met files. This
     is the default behaviour in the GUI, as long as the .met files are in the
     same directory as the .apsimx file
3. Do development as normal in vscode

test
test2

To test the Websocket API you can use off the shelve tools such as PostMan or Chrome
extensions. The following address can be used:

Docker:
  ws://127.0.0.1:8000/cropgen/run

Visual Code (Debug):
  ws://127.0.0.1:<port>/cropgen/run
  Where Port is whatever is configured in the CropGen\config\config.json file for the socketServerPort.

Using the following Payload:
{
    "jobType": "multiyear",
    "body": {
        "jobId": 2222,
        "individuals": 10,
        "inputs": [
            "[Sorghum].Phenology.TTEndJuvToInit.FixedValue", 
            "[Sow on a fixed date].Script.Tillering"
        ],
        "outputs": [
            "Total Crop Water Use (mm)", 
            "Yield (t/ha)"
        ]
    }
}

Where jobType can be any of the following (Case insensitive):
singleyear
multiyear