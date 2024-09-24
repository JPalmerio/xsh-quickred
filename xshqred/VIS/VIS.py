#!/usr/bin/python
# -*- coding: utf-8 -*-
#Martin Sparre, DARK, 2nd November 2011
#version 5.9.0

from PipelineManager import *
import glob
import numpy as np
import os.path
script_path = os.path.abspath(os.path.dirname(__file__))

VIS = PipelineManager()
VIS.SetOutputDir(script_path+"/Output")


############################################################
###  XSH_SCIRED_SLIT_NOD
############################################################

EsorexName="xsh_scired_slit_nod"

VIS.DeclareNewRecipe(EsorexName)
VIS.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_NOD_VIS", "1..n", "any", "100k")
VIS.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_VIS", "1", "-", "-")
VIS.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_VIS", "1", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "MASTER_BIAS_VIS", "1", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_VIS", "1", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_VIS", "1", "-", "-")
VIS.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_VIS", "?", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "DISP_TAB_VIS", "?", "1x1", "400k")
VIS.DeclareRecipeInputTag(EsorexName, "FLUX_STD_CATALOG_VIS", "?", "-" ,"-")
VIS.DeclareRecipeInputTag(EsorexName, "RESPONSE_MERGE1D_SLIT_VIS", "?", "-" , "-")
VIS.DeclareRecipeInputTag(EsorexName, "ATMOS_EXT_VIS", "?", "-" , "-")

############################################################
###  XSH_SCIRED_SLIT_STARE
############################################################

EsorexName="xsh_scired_slit_stare"

VIS.DeclareNewRecipe(EsorexName)
VIS.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_STARE_VIS", "1..n", "any", "100k")
VIS.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_VIS", "1", "-", "-")
VIS.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_VIS", "1", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "MASTER_BIAS_VIS", "1", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_VIS", "1", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_VIS", "1", "-", "-")
VIS.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_VIS", "?", "match", "match")
VIS.DeclareRecipeInputTag(EsorexName, "DISP_TAB_VIS", "?", "1x1", "400k")
VIS.DeclareRecipeInputTag(EsorexName,"FLUX_STD_CATALOG_VIS", "?", "-" ,"-")
VIS.DeclareRecipeInputTag(EsorexName,"RESPONSE_MERGE1D_SLIT_VIS", "?", "-" , "-")
VIS.DeclareRecipeInputTag(EsorexName,"ATMOS_EXT_VIS", "?", "-" , "-")

############################################################
###  INPUT-FILES: TO BE MODIFIED
############################################################

## FOLDER WITH IMAGES
# files = glob.glob(script_path+"/target/*") # /target
files = glob.glob(script_path+"/archive/*")

##
## NODDING MODE
##
VIS.EnableRecipe("xsh_scired_slit_nod")
VIS.SetFiles("OBJECT_SLIT_NOD_VIS", files)

##
## STARING MODE
##
# VIS.EnableRecipe("xsh_scired_slit_stare")
# VIS.SetFiles("OBJECT_SLIT_STARE_VIS", files)

############################################################

# Static CALIBs
VIS.SetFiles("MASTER_BIAS_VIS",[script_path+"/static_calibs/MASTER_BIAS_VIS.fits"])
VIS.SetFiles("MASTER_FLAT_SLIT_VIS",[script_path+"/static_calibs/MASTER_FLAT_SLIT_VIS.fits"])
VIS.SetFiles("ORDER_TAB_EDGES_SLIT_VIS",[script_path+"/static_calibs/ORDER_TAB_EDGES_SLIT_VIS.fits"])
VIS.SetFiles("XSH_MOD_CFG_OPT_2D_VIS",[script_path+"/static_calibs/XSH_MOD_CFG_OPT_2D_VIS.fits"])
VIS.SetFiles("RESPONSE_MERGE1D_SLIT_VIS",[script_path+"/static_calibs/RESPONSE_MERGE1D_SLIT_VIS.fits"])
VIS.SetFiles("DISP_TAB_VIS",[script_path+"/static_calibs/DISP_TAB_VIS.fits"])

#REF-files:
VIS.SetFiles("SPECTRAL_FORMAT_TAB_VIS",[script_path+"/static_calibs/SPECTRAL_FORMAT_TAB_VIS.fits"])
VIS.SetFiles("ARC_LINE_LIST_VIS",[script_path+"/static_calibs/ThAr_vis_custom.fits"])
VIS.SetFiles("XSH_MOD_CFG_TAB_VIS",[script_path+"/static_calibs/XS_GMCT_110710A_VIS.fits"])
VIS.SetFiles("FLUX_STD_CATALOG_VIS",[script_path+"/static_calibs/xsh_star_catalog_vis.fits"])
VIS.SetFiles("ATMOS_EXT_VIS",[script_path+"/static_calibs/xsh_paranal_extinct_model_vis.fits"])
VIS.SetFiles("SKY_LINE_LIST_VIS",[script_path+"/static_calibs/SKY_LINE_LIST_VIS.fits"])
VIS.SetFiles("MASTER_BP_MAP_VIS",[script_path+"/static_calibs/BP_MAP_RP_VIS_1x2.fits"])

#Run
VIS.RunPipeline()

# Convert 1D file to ASCII
out1d = glob.glob(script_path+"/Output/*FLUX_MERGE1D_VIS*.fits")
fitsfile = fits.open(out1d[0])
wave = 10.*(np.arange((np.shape(fitsfile[0].data)[0]))*fitsfile[0].header["CDELT1"]+fitsfile[0].header["CRVAL1"])
np.savetxt(script_path+"/Output/VIS_ASCII1D_spectrum.dat", list(zip(wave, fitsfile[0].data, fitsfile[1].data)), fmt="%1.4e %1.4e %1.4e")


