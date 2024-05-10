import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from app_common import *

st.set_page_config(page_title="Visualize Climate Maps", page_icon="🌦️", layout="wide", initial_sidebar_state="auto")

variables = pd.DataFrame(columns=['variable', 'index', 'label', 'cmap'], data=[
            ['Latent Heat Flux', 0, 'Latent Heat [W/m<sup>2</sup>]', 'plasma'],
            ['Outgoing Long-wave Radiation', 1, 'Outgoing LW Radiation [W/m<sup>2</sup>]', 'plasma'],
            ['Sensible Heat Flux', 2, 'Sensible Heat [W/m<sup>2</sup>]', 'plasma'],
            ['Ground Heat Flux', 3, 'Ground Heat [W/m<sup>2</sup>]', 'plasma'],
            ['Total Evaporation', 4, 'Total EV. [mm/h]', 'earth_r'],
            ['Ground Evaporation without condensation', 5, 'Ground EV. (no condensation) [mm/s]', 'earth_r'],
            ['Soil Evaporation', 6, 'Soil EV. [mm/s]', 'earth_r'],
            ['Vegetation Evaporation', 7, 'Vegetation EV. [mm/s]', 'earth_r'],
            ['Vegetation Transpiration', 8, 'Vegetation TR. [mm/s]', 'viridis'],
            ['Soil Infiltration', 9, 'Infiltration [mm/s]', 'viridis'],
            ['Snow Water Equivalent', 10, 'SWE [m]', 'Blues_r'],
            ['Ground Surface Temperature', 11, 'Ground Temp. [K]', 'thermal'],
            ['Temperature Layer 1', 13, 'T 1 [K]', 'thermal'],
            ['Temperature Layer 2', 14, 'T 2 [K]', 'thermal'],
            ['Temperature Layer 3', 15, 'T 3 [K]', 'thermal'],
            ['Temperature Layer 4', 16, 'T 4 [K]', 'thermal'],
            ['Temperature Layer 5', 17, 'T 5 [K]', 'thermal']]).set_index('variable')

def plot():
    if Mask_name == 'Lombardy Valley': Mask = np.loadtxt('masks/Mask_Valley.txt', delimiter = ' ')
    elif Mask_name == 'Lombardy': Mask = np.loadtxt('masks/Mask_Lombardy.txt', delimiter = ' ')
    else: Mask = np.loadtxt('masks/Mask.txt', delimiter = ' ')
    Mask[Mask==0] = np.nan

    fig = px.imshow(read_one_clm_output(time)[variables.loc[Variable][0]]*Mask, color_continuous_scale=variables.loc[Variable][2], 
                        labels = dict(x = 'X Coordinate', y = 'Y Coordinate', color = variables.loc[Variable][1]))

    fig.update_layout(margin_t = 30, coloraxis_colorbar=dict(title=None), title = variables.loc[Variable][1])
    if Mask_name == 'Lombardy': fig.update_layout(xaxis = dict(range = [70, 200]))
    if Mask_name == 'Lombardy Valley': fig.update_layout(xaxis = dict(range = [70, 200]))
    return fig

col1,col2 = st.columns([1,3])

with col1:
    Variable = st.selectbox('Variable', variables.index, index=0)
    time = st.number_input('Time', min_value=1, max_value=8760, value=1, step=1)
    Mask_name = st.selectbox('What do you want to focus?', ['Po basin', 'Lombardy', 'Lombardy Valley'], index=0)

with col2:
    st.plotly_chart(plot(), use_container_width=True)