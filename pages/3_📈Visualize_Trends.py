import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from app_common import read_others

st.set_page_config(page_title="Visualize Trends", page_icon="📈", layout="wide", initial_sidebar_state="auto")

variables = pd.DataFrame(columns = ['Variable', 'Index', 'Description', 'Type'], data = [
            ['Mean WTD', 0, 'Mean Water Table Depth [m]', 'Parflow'],
            ['Subsurface Storage', 1, 'Subsurface Storage [m<sup>3</sup>]', 'Parflow'],
            ['Surface_Storage', 2, 'Surface Storage [m<sup>3</sup>]', 'Parflow'],
            ['Overland_Flow', 3, 'Overland Flow [m<sup>3</sup>/s]', 'Parflow'],
            ['Latent Heat Flux', 4, 'Latent Heat Flux [W/m<sup>2</sup>]', 'CLM'],
            ['Outgoing Long-wave Radiation', 5, 'Outgoing Long-wave Radiation [W/m<sup>2</sup>]', 'CLM'],
            ['Sensible Heat Flux', 6, 'Sensible Heat Flux [W/m<sup>2</sup>]', 'CLM'],
            ['Ground Heat Flux', 7, 'Ground Heat Flux [W/m<sup>2</sup>]', 'CLM'],
            ['Total Evaporation', 8, 'Total Evaporation [mm/h]', 'CLM'],
            ['Ground Evaporation without condensation', 9, 'Ground Evaporation without condensation [mm/s]', 'CLM'],
            ['Soil Evaporation', 10, 'Soil Evaporation [mm/s]', 'CLM'],
            ['Vegetation Evaporation', 11, 'Vegetation Evaporation [mm/s]', 'CLM'],
            ['Vegetation Transpiration', 12, 'Vegetation Transpiration [mm/s]', 'CLM'],
            ['Soil Infiltration', 13, 'Soil Infiltration [mm/s]', 'CLM'],
            ['Snow Water Equivalent', 14, 'Snow Water Equivalent [m]', 'CLM'],
            ['Ground Surface Temperature', 15, 'Ground Surface Temperature [K]', 'CLM'],
            ['Temperature Layer 1', 16, 'Temperature Layer 1 [K]', 'CLM'],
            ['Temperature Layer 2', 17, 'Temperature Layer 2 [K]', 'CLM'],
            ['Temperature Layer 3', 18, 'Temperature Layer 3 [K]', 'CLM'],
            ['Temperature Layer 4', 19, 'Temperature Layer 4 [K]', 'CLM'],
            ['Temperature Layer 5', 20, 'Temperature Layer 5 [K]', 'CLM']]
            ).set_index('Variable')

def plot_series():

    if Mask_name == 'Po basin': series = np.loadtxt('series_data_all.txt')
    elif Mask_name == 'Lombardy': series = np.loadtxt('series_data_Lombardy.txt')
    elif Mask_name == 'Lombardy Valley': series = np.loadtxt('series_data_valley.txt')
    series = series[:, variables.loc[Variable][0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.array(range(time[0], time[1])), y=series[time[0]: time[1]], mode='lines', name=Variable, line=dict(color='blue')))
    first = 0
    if variables.loc[Variable][2] == 'CLM': first = 1
    if initial: fig.add_trace(go.Scatter(x=[time[0], time[1]], y=[series[first], series[first]], mode='lines', name='Initial Value', line=dict(color='red', dash='dash')))
    if mean: fig.add_trace(go.Scatter(x=[time[0], time[1]], y=[np.mean(series[first:]), np.mean(series[first:])], mode='lines', name='Mean Value', line=dict(color='green', dash='dash')))

    fig.update_layout(
        margin_t = 0,
        xaxis_title = 'Time [hours]',
        yaxis_title = variables.loc[Variable][1],
        xaxis = dict(range = [time[0], time[1]]),
        legend = dict(x = 0.7, y = 0.9, traceorder = "normal", font = dict(family = "sans-serif", size = 12, color = "black"), 
                      bgcolor = "lightblue", bordercolor = "Black", borderwidth = 1),
        showlegend = True,
        )
    return fig


dx, dy, dz, nx, ny, nz, porosity, specific_storage, mask, slopex, slopey, mannings = read_others()

col1,col2 = st.columns([2,3])

with col1:
    Variable = st.selectbox('Variable', variables.index, index=0)
    Mask_name = st.selectbox('What do you want to focus?', ['Po basin', 'Lombardy', 'Lombardy Valley'], index=0)
    time = st.slider('Time', min_value=1, max_value=8760, value=(1, 8760), step=1)
    initial = st.checkbox('Show Initial Value', value=True)
    mean = st.checkbox('Show Mean Value', value=True)

with col2:
    st.plotly_chart(plot_series(), use_container_width=True)

