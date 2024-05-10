import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from parflow.tools.io import read_pfb
from parflow import Run


def read_pressure():
    nt = 8760
    pressures = []
    for time in range(nt+1):
        pressure = np.load('./Outputs/Dynamic_Spinup.out.press.'+str(time).zfill(5)+'.npy')
        pressures.append(pressure/100)
    return pressures

def read_saturation():
    nt = 8760
    saturations = []
    for time in range(nt+1):
        saturation = np.load('./Outputs/Dynamic_Spinup.out.satur.'+str(time).zfill(5)+'.npy')
        saturations.append(saturation/10000)
    return saturations

def read_clm_output():
    # run = Run.from_definition('./Outputs/Dynamic_Spinup.pfidb')
    # data = run.data_accessor
    nt = 8760
    clm_data = []
    for time in range(1,nt+1):
        clm_data.append(np.flip(read_pfb('./Outputs/Dynamic_Spinup.out.clm_output.'+str(time).zfill(5)+'.C.pfb'), axis = 1))
    return clm_data

def read_one_pressure(dt):
    return np.load('./Outputs/Dynamic_Spinup.out.press.'+str(dt).zfill(5)+'.npy')/100

def read_one_saturation(dt):
    return np.load('./Outputs/Dynamic_Spinup.out.satur.'+str(dt).zfill(5)+'.npy')/10000

def read_one_clm_output(dt):
    return np.flip(read_pfb('./Outputs/Dynamic_Spinup.out.clm_output.'+str(dt).zfill(5)+'.C.pfb'), axis = 1)

def read_others():
    run = Run.from_definition('./Outputs/Dynamic_Spinup.pfidb')
    data = run.data_accessor
    dx = data.dx
    dy = data.dy
    dz = np.array([125, 70, 20, 8.0, 1.0, 0.7, 0.15, 0.1, 0.05])

    nx = data.shape[2]
    ny = data.shape[1]
    nz = data.shape[0]

    porosity = data.computed_porosity
    specific_storage = data.specific_storage
    mask = data.mask
    slopex = data.slope_x               # shape (ny, nx)
    slopey = data.slope_y               # shape (ny, nx)
    mannings = data.mannings            # scalar value

    return dx, dy, dz, nx, ny, nz, porosity, specific_storage, mask, slopex, slopey, mannings
