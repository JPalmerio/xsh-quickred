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


def run_UVB_pipeline(input_dir, output_dir, mode='nodding', convert_ascii=False):

    # Make sure paths are Path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Main object
    UVB = PipelineManager()

    UVB.SetOutputDir(str(output_dir))

    # FOLDER WITH IMAGES
    files = [str(f) for f in input_dir.iterdir() if f.suffix.lower() == '.fits']

    if mode == 'nodding':
        EsorexName = "xsh_scired_slit_nod"

        UVB.DeclareNewRecipe(EsorexName)
        UVB.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_NOD_UVB", "1..n", "any", "100k")
        UVB.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_UVB", "1", "-", "-")
        UVB.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_UVB", "1", "match", "match")
        UVB.DeclareRecipeInputTag(EsorexName, "MASTER_BIAS_UVB", "1", "match", "match")
        UVB.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_UVB", "1", "-", "-")
        UVB.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_UVB", "1", "-", "-")
        UVB.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_UVB", "?", "match", "match")
        UVB.DeclareRecipeInputTag(EsorexName, "DISP_TAB_UVB", "?", "1x1", "400k")
        UVB.DeclareRecipeInputTag(EsorexName, "FLUX_STD_CATALOG_UVB", "?", "-" ,"-")
        UVB.DeclareRecipeInputTag(EsorexName, "ATMOS_EXT_UVB", "?", "-" , "-")
        UVB.DeclareRecipeInputTag(EsorexName, "RESPONSE_MERGE1D_SLIT_UVB", "?", "-" , "-")

        UVB.EnableRecipe(EsorexName)
        UVB.SetFiles("OBJECT_SLIT_NOD_UVB", files)
    elif mode == "stare":
        EsorexName = "xsh_scired_slit_stare"

        UVB.DeclareNewRecipe(EsorexName)
        UVB.DeclareRecipeInputTag(EsorexName, "OBJECT_SLIT_STARE_UVB", "1", "any", "any")
        UVB.DeclareRecipeInputTag(EsorexName, "SPECTRAL_FORMAT_TAB_UVB", "1", "-", "-")
        UVB.DeclareRecipeInputTag(EsorexName, "MASTER_FLAT_SLIT_UVB", "1", "match", "match")
        UVB.DeclareRecipeInputTag(EsorexName, "MASTER_BIAS_UVB", "1", "match", "match")
        UVB.DeclareRecipeInputTag(EsorexName, "ORDER_TAB_EDGES_SLIT_UVB", "1", "match", "match")
        UVB.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_OPT_2D_UVB", "1", "-", "-")
        UVB.DeclareRecipeInputTag(EsorexName, "MASTER_BP_MAP_UVB", "?", "match", "match")
        UVB.DeclareRecipeInputTag(EsorexName, "DISP_TAB_UVB", "?", "1x1", "400k")
        UVB.DeclareRecipeInputTag(EsorexName, "FLUX_STD_CATALOG_UVB", "?", "-" ,"-")
        UVB.DeclareRecipeInputTag(EsorexName, "ATMOS_EXT_UVB", "?", "-" , "-")
        UVB.DeclareRecipeInputTag(EsorexName, "RESPONSE_MERGE1D_SLIT_UVB", "?", "-" , "-")
        UVB.DeclareRecipeInputTag(EsorexName, "XSH_MOD_CFG_TAB_UVB", "1", "-", "-")

        UVB.EnableRecipe(EsorexName)
        UVB.SetFiles("OBJECT_SLIT_STARE_UVB", files)
    else:
        raise ValueError("mode must be 'nodding' or 'stare'.")

    # Static CALIBs
    UVB.SetFiles("MASTER_BIAS_UVB",[script_path+"/static_calibs/MASTER_BIAS_UVB.fits"])
    UVB.SetFiles("MASTER_FLAT_SLIT_UVB",[script_path+"/static_calibs/MASTER_FLAT_SLIT_UVB.fits"])
    UVB.SetFiles("ORDER_TAB_EDGES_SLIT_UVB",[script_path+"/static_calibs/ORDER_TAB_EDGES_SLIT_UVB.fits"])
    UVB.SetFiles("XSH_MOD_CFG_OPT_2D_UVB",[script_path+"/static_calibs/XSH_MOD_CFG_OPT_2D_UVB.fits"])
    UVB.SetFiles("RESPONSE_MERGE1D_SLIT_UVB",[script_path+"/static_calibs/RESPONSE_MERGE1D_SLIT_UVB.fits"])
    UVB.SetFiles("DISP_TAB_UVB",[script_path+"/static_calibs/DISP_TAB_UVB.fits"])

    # REF-files:
    UVB.SetFiles("SPECTRAL_FORMAT_TAB_UVB",[script_path+"/static_calibs/SPECTRAL_FORMAT_TAB_UVB.fits"])
    UVB.SetFiles("ARC_LINE_LIST_UVB",[script_path+"/static_calibs/ThAr_uvb_2012PBR.fits"])
    UVB.SetFiles("XSH_MOD_CFG_TAB_UVB",[script_path+"/static_calibs/XS_GMCT_110710A_UVB.fits"])
    UVB.SetFiles("FLUX_STD_CATALOG_UVB",[script_path+"/static_calibs/xsh_star_catalog_uvb.fits"])
    UVB.SetFiles("ATMOS_EXT_UVB",[script_path+"/static_calibs/xsh_paranal_extinct_model_uvb.fits"])
    UVB.SetFiles("SKY_LINE_LIST_UVB",[script_path+"/static_calibs/SKY_LINE_LIST_UVB.fits"])
    UVB.SetFiles("MASTER_BP_MAP_UVB",[script_path+"/static_calibs/BP_MAP_RP_UVB_1x2.fits"])

    # Run
    UVB.RunPipeline()

    # Convert 1D file to ASCII
    if convert_ascii:
        out1d = glob.glob(str(output_dir)+"/*FLUX_MERGE1D_UVB*.fits")
        fitsfile = fits.open(out1d[0])
        wave = 10.*(np.arange((np.shape(fitsfile[0].data)[0]))*fitsfile[0].header["CDELT1"]+fitsfile[0].header["CRVAL1"])
        np.savetxt(output_dir/"UVB_ASCII1D_spectrum.dat", list(zip(wave, fitsfile[0].data, fitsfile[1].data)), fmt="%1.4e %1.4e %1.4e")
