import streamlit as st
import numpy as np
import plotly.express as px
from app_common import *
from parflow.tools.hydrology import calculate_water_table_depth
from parflow.tools.hydrology import calculate_subsurface_storage
from parflow.tools.hydrology import calculate_surface_storage

st.set_page_config(page_title="Visualize Hydrology Maps", page_icon="🌎", layout="wide", initial_sidebar_state="auto")

def plot_map():
    if Mask_name == 'Lombardy Valley': Mask = np.loadtxt('masks/Mask_Valley.txt', delimiter = ' ')
    elif Mask_name == 'Lombardy': Mask = np.loadtxt('masks/Mask_Lombardy.txt', delimiter = ' ')
    else: Mask = np.loadtxt('masks/Mask.txt', delimiter = ' ')
    Mask[Mask==0] = np.nan

    if Variable == 'Pressure':
        pressure_data = np.flip(read_one_pressure(time)[layer], axis = 0)*Mask
        fig = px.imshow(pressure_data, color_continuous_scale='viridis', 
                        labels = dict(x = 'X Coordinate', y = 'Y Coordinate', color = 'Press. Head [m]'))
        fig.update_layout(margin_t = 30, coloraxis_colorbar=dict(title=None), title = 'Pressure Head [m]')
    elif Variable == 'Saturation':
        saturation_data = np.flip(read_one_saturation(time)[layer], axis  = 0)*Mask
        fig = px.imshow(saturation_data, color_continuous_scale='viridis', 
                        labels = dict(x = 'X Coordinate', y = 'Y Coordinate', color = 'Satur [-]'), 
                        contrast_rescaling = 'infer')
        fig.update_layout(margin_t = 30, coloraxis_colorbar=dict(title=None), title = 'Saturation [-]')
    elif Variable == 'WTD':
        pressure_data = read_one_pressure(time)
        saturation_data = read_one_saturation(time)
        wtd_data = np.flip(calculate_water_table_depth(pressure_data, saturation_data, dz), axis = 0)*Mask
        fig = px.imshow(wtd_data, color_continuous_scale='viridis', 
                        labels = dict(x = 'X Coordinate', y = 'Y Coordinate', color = 'WTD [m]'), 
                        contrast_rescaling = 'infer')
        fig.update_layout(margin_t = 30, coloraxis_colorbar=dict(title=None), title = 'Water Table Depth [m]')
    elif Variable == 'Subsurface Storage':
        pressure_data = read_one_pressure(time)
        saturation_data = read_one_saturation(time)
        subsurface_storage_data = np.flip(np.sum(calculate_subsurface_storage(porosity, pressure_data, saturation_data, specific_storage, dx, dy, dz, mask=mask), axis = 0), axis = 0)*Mask
        fig = px.imshow(subsurface_storage_data, color_continuous_scale='viridis', 
                        labels = dict(x = 'X Coordinate', y = 'Y Coordinate', color = 'Sub. Storage [m^3]'))
        fig.update_layout(margin_t = 30, coloraxis_colorbar=dict(title=None), title = 'Subsurface Storage [m^3]')
    elif Variable == 'Surface Storage':
        pressure_data = read_one_pressure(time)
        surface_storage_data = np.flip(calculate_surface_storage(pressure_data, dx, dy, mask=mask), axis = 0)*Mask
        fig = px.imshow(surface_storage_data, color_continuous_scale='viridis', 
                        labels = dict(x = 'X Coordinate', y = 'Y Coordinate', color = 'Surf. Storage [m^3]'))
        fig.update_layout(margin_t = 30, coloraxis_colorbar=dict(title=None), title = 'Surface Storage [m^3]')
    return fig

dx, dy, dz, nx, ny, nz, porosity, specific_storage, mask, slopex, slopey, mannings = read_others()

col1,col2 = st.columns([1,3])

with col1:
    Variable = st.selectbox('Variable', ['Pressure', 'Saturation', 'WTD', 'Subsurface Storage', 'Surface Storage'], index=0)
    time = st.number_input('Time', min_value=0, max_value=8760, value=1, step=1)
    Mask_name = st.selectbox('What do you want to focus?', ['Po basin', 'Lombardy', 'Lombardy Valley'], index=0)
    if Variable == 'Pressure' or Variable == 'Saturation':
        layer = st.number_input('Layer (8 is top, 0 is bottom)', min_value=0, max_value=8, value=0, step=1)

with col2:
    st.plotly_chart(plot_map(), use_container_width=True)
