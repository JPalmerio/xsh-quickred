# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
#Martin Sparre, DARK, 2nd November 2011
#version 5.9.0

from PipelineManager import *
import glob
import numpy as np

NIR = PipelineManager()
NIR.SetOutputDir('Output')

############################################################
###   XSH_MDARK
############################################################

EsorexName='xsh_mdark'
SOFFileName = EsorexName

NIR.DeclareNewRecipe(EsorexName)

NIR.DeclareRecipeInputTag(SOFFileName, "DARK_NIR", "3", "-", "-")#recipe_name, InputTag, Nfiles, binning, readout
NIR.DeclareRecipeInputTag(SOFFileName, "MASTER_BP_MAP_NIR", "?", "-", "-")

NIR.EnableRecipe(SOFFileName)


############################################################
###  INPUT-FILES: TO BE MODIFIED
############################################################

## FOLDER WITH DARK IMAGES
files = glob.glob('darks/*') # /target


############################################################
NIR.SetFiles('DARK_NIR', files)
static_path = "static_calibs/"
NIR.SetFiles('MASTER_BP_MAP_NIR',['%sBP_MAP_RP_NIR.fits'%static_path])

#Run
NIR.RunPipeline()
