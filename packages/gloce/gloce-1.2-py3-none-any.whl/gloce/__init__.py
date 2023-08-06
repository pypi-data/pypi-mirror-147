import sys
import os
path = os.getcwd()
sys.path.append(path)
import gloce.func
import gloce.area
import gloce.interpolation
import gloce.resample
#----func----
running_mean = gloce.func.running_mean
nanravel = gloce.func.nanravel
listdir = gloce.func.listdir
nanaverage = gloce.func.nanaverage
arrayinfo = gloce.func.arrayinfo
fslice = gloce.func.fslice
exclude_outlier = gloce.func.exclude_outlier
#------------

#----resample----
downscaling = gloce.resample.downscaling
upscaling = gloce.resample.upscaling
#----------------

#----area----
globalarea = gloce.area.globalarea
gridarea = gloce.area.gridarea
#------------

#----interpolation----
interpolation_map = gloce.interpolation.interpolation_map
interpolation_time = gloce.interpolation.interpolation_time
#---------------------