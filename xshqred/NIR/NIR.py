# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
#Martin Sparre, DARK, 2nd November 2011
#version 5.9.0

from PipelineManager import *
import glob
from astropy.io import fits
import numpy as np
import os.path
script_path = os.path.abspath(os.path.dirname(__file__))

NIR = PipelineManager()
NIR.SetOutputDir(script_path+"/Output")


############################################################
###  XSH_SCIRED_SLIT_NOD
############################################################

EsorexName="xsh_scired_slit_nod"

NIR.DeclareNewRecipe(EsorexName)
NIR.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_NOD_NIR", "1..n", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "MASTER_DARK_NIR", "?", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_NIR", "?", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "DISP_TAB_NIR", "?", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName,"FLUX_STD_CATALOG_NIR", "?", "-" ,"-")
NIR.DeclareRecipeInputTag(EsorexName,"ATMOS_EXT_NIR", "?", "-" , "-")
NIR.DeclareRecipeInputTag(EsorexName,"RESPONSE_MERGE1D_SLIT_NIR", "?", "-" , "-")
NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_TAB_NIR", "1", "-", "-")

############################################################
###  XSH_SCIRED_SLIT_STARE
############################################################

EsorexName="xsh_scired_slit_stare"

NIR.DeclareNewRecipe(EsorexName)
NIR.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_STARE_NIR", "1..n", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_NIR", "1", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "MASTER_DARK_NIR", "?", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_NIR", "?", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName, "DISP_TAB_NIR", "?", "-", "-")
NIR.DeclareRecipeInputTag(EsorexName,"FLUX_STD_CATALOG_NIR", "?", "-" ,"-")
NIR.DeclareRecipeInputTag(EsorexName,"ATMOS_EXT_NIR", "?", "-" , "-")
NIR.DeclareRecipeInputTag(EsorexName,"RESPONSE_MERGE1D_SLIT_NIR", "?", "-" , "-")
NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_TAB_NIR", "1", "-", "-")

#NIR.SetRecipeOptions(SOFFileName, "--sky-method=MEDIAN")#MEDIAN is more stable than bspline
#NIR.SetRecipeOptions(SOFFileName, "--sky-bspline-order=4")
#NIR.SetRecipeOptions(SOFFileName, "--sky-subtract=FALSE")

#options from Stefan and Sune (these options might give better sky-subtraction):
#NIR.SetRecipeOptions(SOFFileName, "--background-nb-y=50 --background-radius-y=40 --background-method=median --rectify-bin-lambda=.05 --rectify-bin-slit=.2 --removecrhsingle-niter=3 --extract-method=FULL --compute-map=TRUE --rectify-conserve-flux=FALSE --sky-subtract=TRUE --sky-bspline-nbkpts-first=500 --sky-bspline-nbkpts-second=500 --sky-method=MEDIAN  --rectify-radius=1 --mergeord-method=0")

############################################################
###  INPUT-FILES: TO BE MODIFIED
############################################################

## FOLDER WITH IMAGES
# files = glob.glob(script_path+"/target/*") # /target

files = glob.glob(script_path+"/archive/*") #
files = [ii for ii in files if ii.endswith(".fits")]


##
## NODDING MODE
##
NIR.EnableRecipe("xsh_scired_slit_nod")
NIR.SetFiles("OBJECT_SLIT_NOD_NIR", files)

##
## STARING MODE
##
# NIR.EnableRecipe("xsh_scired_slit_stare")
# NIR.SetFiles("OBJECT_SLIT_STARE_NIR", files)

############################################################

# Get exptime:
exptime = [0]*len(files)
for ii in range(len(files)):
    exptime[ii] = fits.open(files[ii])[0].header["EXPTIME"]

if not exptime.count(exptime[0]) == len(exptime):
    raise TypeError("Input image list does not have the same exposure times.")

exptime = int(exptime[0])

# Get slit
slit = [0]*len(files)
for ii in range(len(files)):
    slit[ii] = fits.open(files[ii])[0].header["HIERARCH ESO INS OPTI5 NAME"]

if not slit.count(slit[0]) == len(slit):
    raise TypeError("Input image list does not use the same slit.")

JH = slit[0].endswith("JH")

# Static CALIBs
try:
    NIR.SetFiles("MASTER_DARK_NIR",[script_path+"/static_calibs/MASTER_DARK_NIR_%s.fits"%exptime])
except:
    raise InputError("NIR DARK does not exist with the correct exposure time. Get it.")

if JH:
    static_path = script_path+"/static_calibs/JH/"
else:
    static_path = script_path+"/static_calibs/"

NIR.SetFiles("MASTER_FLAT_SLIT_NIR",["%sMASTER_FLAT_SLIT_NIR.fits"%static_path])
NIR.SetFiles("ORDER_TAB_EDGES_SLIT_NIR",["%sORDER_TAB_EDGES_SLIT_NIR.fits"%static_path])
NIR.SetFiles("XSH_MOD_CFG_OPT_2D_NIR",["%sXSH_MOD_CFG_OPT_2D_NIR.fits"%static_path])
NIR.SetFiles("RESPONSE_MERGE1D_SLIT_NIR",["%sRESPONSE_MERGE1D_SLIT_NIR.fits"%static_path])
NIR.SetFiles("DISP_TAB_NIR",["%sDISP_TAB_NIR.fits"%static_path])

#REF-files:
if JH:
    NIR.SetFiles("SPECTRAL_FORMAT_TAB_NIR",["%sSPECTRAL_FORMAT_TAB_%s_NIR.fits"%(static_path, "JH")])
else:
    NIR.SetFiles("SPECTRAL_FORMAT_TAB_NIR",["%sSPECTRAL_FORMAT_TAB_NIR.fits"%static_path])

NIR.SetFiles("ARC_LINE_LIST_NIR",["%sARC_LINE_LIST_AFC_NIR.fits"%static_path])
NIR.SetFiles("XSH_MOD_CFG_TAB_NIR",["%sXS_GMCT_110710A_NIR.fits"%static_path])
NIR.SetFiles("FLUX_STD_CATALOG_NIR",["%sxsh_star_catalog_nir.fits"%static_path])
NIR.SetFiles("ATMOS_EXT_NIR",["%sxsh_paranal_extinct_model_nir.fits"%static_path])
NIR.SetFiles("SKY_LINE_LIST_NIR",["%sSKY_LINE_LIST_NIR.fits"%static_path])
NIR.SetFiles("MASTER_BP_MAP_NIR",["%sBP_MAP_RP_NIR.fits"%static_path])

#Run
NIR.RunPipeline()

# Convert 1D file to ASCII
out1d = glob.glob(script_path+"/Output/*FLUX_MERGE1D_NIR*.fits")
fitsfile = fits.open(out1d[0])
wave = 10.*(np.arange((np.shape(fitsfile[0].data)[0]))*fitsfile[0].header["CDELT1"]+fitsfile[0].header["CRVAL1"])
np.savetxt(script_path+"/Output/NIR_ASCII1D_spectrum.dat", list(zip(wave, fitsfile[0].data, fitsfile[1].data)), fmt="%1.4e %1.4e %1.4e")


