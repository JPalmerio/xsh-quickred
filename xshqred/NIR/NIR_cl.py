#!/usr/bin/python
# -*- coding: utf-8 -*-
# Martin Sparre, DARK, 2nd November 2011
# version 5.9.0
# modified by Jesse Palmerio Feb 2024

from .PipelineManager import PipelineManager
import glob
from astropy.io import fits
import numpy as np
from pathlib import Path
import logging

log = logging.getLogger(__name__)

# script_path = os.path.abspath(os.path.dirname(__file__))
script_path = str(Path(__file__).parent)


def run_NIR_pipeline(input_dir, output_dir, mode='nodding', convert_ascii=False):

    # Make sure paths are Path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Main object
    NIR = PipelineManager()

    NIR.SetOutputDir(str(output_dir))

    # FOLDER WITH IMAGES
    files = [str(f) for f in input_dir.iterdir() if f.suffix.lower() == '.fits']

    if mode == 'nodding':
        EsorexName = "xsh_scired_slit_nod"

        NIR.DeclareNewRecipe(EsorexName)
        NIR.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_NOD_NIR", "1..n", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "MASTER_DARK_NIR", "?", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_NIR", "?", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "DISP_TAB_NIR", "?", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "FLUX_STD_CATALOG_NIR", "?", "-" ,"-")
        NIR.DeclareRecipeInputTag(EsorexName, "ATMOS_EXT_NIR", "?", "-" , "-")
        NIR.DeclareRecipeInputTag(EsorexName, "RESPONSE_MERGE1D_SLIT_NIR", "?", "-" , "-")
        NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_TAB_NIR", "1", "-", "-")

        NIR.EnableRecipe(EsorexName)
        NIR.SetFiles("OBJECT_SLIT_NOD_NIR", files)
    elif mode == "stare":
        EsorexName = "xsh_scired_slit_stare"

        NIR.DeclareNewRecipe(EsorexName)
        NIR.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_STARE_NIR", "1..n", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_NIR", "1", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "MASTER_DARK_NIR", "?", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_NIR", "?", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "DISP_TAB_NIR", "?", "-", "-")
        NIR.DeclareRecipeInputTag(EsorexName, "FLUX_STD_CATALOG_NIR", "?", "-" ,"-")
        NIR.DeclareRecipeInputTag(EsorexName, "ATMOS_EXT_NIR", "?", "-" , "-")
        NIR.DeclareRecipeInputTag(EsorexName, "RESPONSE_MERGE1D_SLIT_NIR", "?", "-" , "-")
        NIR.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_TAB_NIR", "1", "-", "-")

        NIR.EnableRecipe(EsorexName)
        NIR.SetFiles("OBJECT_SLIT_STARE_NIR", files)
    else:
        raise ValueError("mode must be 'nodding' or 'stare'.")

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
        raise ValueError("NIR DARK does not exist with the correct exposure time. Get it.")

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

    # Run
    NIR.RunPipeline()

    # Convert 1D file to ASCII
    if convert_ascii:
        out1d = glob.glob(str(output_dir)+"/*FLUX_MERGE1D_NIR*.fits")
        fitsfile = fits.open(out1d[0])
        wave = 10.*(np.arange((np.shape(fitsfile[0].data)[0]))*fitsfile[0].header["CDELT1"]+fitsfile[0].header["CRVAL1"])
        np.savetxt(output_dir/"NIR_ASCII1D_spectrum.dat", list(zip(wave, fitsfile[0].data, fitsfile[1].data)), fmt="%1.4e %1.4e %1.4e")
