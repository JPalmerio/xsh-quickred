This repository contains a python wrapper around the ESO pipeline, meant for quick-and-dirty reductions of VLT/X-shooter data.
It is largely based on the work of [Jonatan Selsing](https://github.com/jselsing/XSH_QuickReduction) and [Martin Sparre](https://github.com/martinsparre/XSHPipelineManager).
All credit for the original scripts goes to Martin Sparre.

# Prerequisites
This package relies on the ESO X-shooter pipeline and static calibration files.
Information on the ESO pipelines can found at https://www.eso.org/sci/software/pipelines/, as well as instructions on how to install.
This quick-reduction pipeline relies specifically on Esorex - the ESO recipe excecution framework.
Make sure these are installed and functional before installing this package.

# Installation
First clone the project, then create a Python virtual environment and activate it by running:
```
conda create -n xshqred python=3.10
conda activate xshqred
```
Then move to the root of the project and run (with your environment active):
```
pip install -e .
```
That's it!

# Usage
Assuming you have downloaded some data from the ESO archive, move to the directory containing the unzipped downloaded folder from the ESO archive, with the environment active, run:
```
xshqred
```
This should launch the script that will reorganize the files and use old calibrations for a quick reduction.
For now, only `NOD` mode is available but `STARE` should be available soon.
Wavelengths are in air. No extinction correction is applied to the final products.

