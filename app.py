import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from parflow.tools.io import read_pfb
from parflow import Run
import os

st.title('Dynamic Spinup Outputs 💧')

folder = './Outputs/'
runname = 'Dynamic_Spinup'
print(os.system('pwd'))
# log = np.loadtxt(folder+'log_file.txt')
# run = Run.from_definition(folder+runname+'.pfidb')
# data = run.data_accessor

# dx = data.dx
# dy = data.dy
# dz = data.dz

# nx = data.shape[2]
# ny = data.shape[1]
# nz = data.shape[0]

# porosity = data.computed_porosity
# specific_storage = data.specific_storage
# mask = data.mask
# slopex = data.slope_x               # shape (ny, nx)
# slopey = data.slope_y               # shape (ny, nx)
# mannings = data.mannings            # scalar value

# nt = 10

# subsurface_storage = np.zeros(nt)
# surface_storage = np.zeros(nt)
# wtd = np.zeros((nt, ny, nx))
# et = np.zeros(nt)
# overland_flow = np.zeros((nt, ny, nx))
# mannings = data.mannings

# pressures = []
# saturations = []
# clm_data = []

# for time in range(nt+1):
#     pressure = read_pfb(folder+runname+'.out.press.'+str(time).zfill(5)+'.pfb')
#     pressure[pressure < -10000000] = np.nan
#     pressures.append(pressure)

#     saturation = read_pfb(folder+runname+'.out.satur.'+str(time).zfill(5)+'.pfb')
#     saturation[saturation < -4000] = np.nan
#     saturations.append(saturation)

# for time in range(1,nt+1):
#     clm_data.append(read_pfb(folder+runname+'.out.clm_output.'+str(time).zfill(5)+'.C.pfb'))

