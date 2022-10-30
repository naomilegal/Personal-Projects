#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:40:19 2021

@author: floramainguet
"""

import requests
import json
import pandas as pd
import bokeh 
import copy
from bokeh.plotting import figure
from bokeh.io import output_file, show
import numpy as np
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import row, widgetbox
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.layouts import column
from bokeh.models import Select
from numpy.random import random, normal, lognormal
import numpy as np
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, Slider, CustomJS, Div
from bokeh.plotting import Figure, show
from bokeh.models import Button, CustomJS, Slider
from bokeh.layouts import row
from bokeh.io import output_file, show
from bokeh.models.widgets import DateRangeSlider
from bokeh.models.widgets import Panel, Tabs




datasteroids = pd.read_csv('data.csv')

#plot1
source= ColumnDataSource(data={"x": datasteroids['average_diameter'],
                               "y": datasteroids['relative_velocity_kmh'],
                               "x_available":datasteroids['average_diameter'],
                               "y_available":datasteroids['relative_velocity_kmh']  })

p = Figure(title = "Diameter and Velocity of Asteroids", x_axis_label='Average Diameter, in meters',
           y_axis_label='Velocity, in Km/h',  plot_width=1000, plot_height=900)

p.circle('x', 'y', source=source, fill_alpha=0.9, size=10 )
# here max_diameter was used because I first tried my code only with a few weeks, while I wanted to make the dashboard for 6months. 

max_diameter = datasteroids['average_diameter'].max()
diameter_slider = Slider(start=0, end=max_diameter, value=max_diameter, step=100, width= 500, title="Diameter Slider")

# I had troubles trying to figure out how to make the callback with python it did not work in Jupyter Notebook 
#I found how to do it in JScript

callback = CustomJS(args=dict(source=source, slider=diameter_slider), code="""
    //declaring variables
    const data = source.data;
    const selected_diameter = slider.value;  
    const x_available = data['x_available']
    const y_available = data['y_available']
    // creating empty lists to bee filled later
    const filtered_x = []
    const filtered_y = []
    for (var i = 0; i < x_available.length; i++) {
        var current_asteroid_diameter = x_available[i]
        // filter each asteroid, removes the ones larger than selected value
        if (current_asteroid_diameter<=selected_diameter) {
            filtered_x.push(data['x_available'][i])
            filtered_y.push(data['y_available'][i])
        }
    }
    data['x'] = filtered_x
    data['y'] = filtered_y
    source.change.emit();
""")
#adding the callback function to the slider
diameter_slider.js_on_change('value', callback)

#Second slider velocity
max_velocity = datasteroids['relative_velocity_kmh'].max()


velocity_slider = Slider(start=0, end=max_velocity, value=max_velocity, step=1000, width=500, title="Velocity Slider")
#callback using CJS
callback = CustomJS(args=dict(source=source, slider=velocity_slider), code="""
    //declaring variables
    const data = source.data;
    const selected_velocity = slider.value;  
    const x_available = data['x_available']
    const y_available = data['y_available']
    //creating empty lists to be filled later
    const filtered_x = []
    const filtered_y = []
    for (var i = 0; i < y_available.length; i++) {
        var current_asteroid_velocity = y_available[i]
        // filter each asteroid, remove the ones different than selected value
        if (current_asteroid_velocity<=selected_velocity) {
            filtered_x.push(data['x_available'][i])
            filtered_y.push(data['y_available'][i])
        }
    }
    data['x'] = filtered_x
    data['y'] = filtered_y
    source.change.emit();
""")
#adding the slider
velocity_slider.js_on_change('value', callback)
#little HTML text
text = Div(text="<h1> This graphic shows all 2710 asteroids that came close to Earth within a 6 months period. Here the graphic gives the diameter of the asteroids in meters and their velocity in Km/h. </h1>", width=300, height=300)
#Only solution I found to have the visual match what I had in mind
row1 = row(p, text)
# add the first row created to the final layout
layout_all = column(row1, diameter_slider, velocity_slider)
#displays plot and its corresponding sliders
#show(layout_all)

tab1 = Panel(child= layout_all, title=" Diameter and Velocity")


output_file("Diameter_Velocity.html")

#plot 2
source= ColumnDataSource(data={"x": datasteroids['impact_strength'],
                               "y": datasteroids['miss_distance_lunar'],
                               "x_available":datasteroids['impact_strength'],
                               "y_available":datasteroids['miss_distance_lunar'],
                             'approach_date':datasteroids['close_approach_day'] })


p = figure(title = "Hazard of Asteroids", x_axis_label= 'Possible Impact Strength', y_axis_label = 'Missed Distance in Lunars, (1Lunar = 384,400 km)', plot_width=900, plot_height=800)
p.circle('x', 'y', source=source, fill_alpha=0.8, size=10 )


#setting variables to maximum in prevision of adding more weeks and months and creating the first slider for this plot

max_miss = datasteroids['miss_distance_lunar'].max()
miss_slider = Slider(start=0, end=max_miss, value=max_miss, step=10, width=500, title="Missed Distance Slider")

#callback function in CJS
callback = CustomJS(args=dict(source=source, slider=miss_slider), code="""
    //declaring vzriabls
    const data = source.data;
    const selected_distance = slider.value;  
    const x_available = data['x_available']
    const y_available = data['y_available']
    //creating empty lists to be filled later
    const filtered_x = []
    const filtered_y = []
    for (var i = 0; i < y_available.length; i++) {
        var current_miss_distance = y_available[i]
        // filter each asteroid, remove the ones different from selected value
        if (current_miss_distance <=selected_distance) {
            filtered_x.push(data['x_available'][i])
            filtered_y.push(data['y_available'][i])
        }
    }
    data['x'] = filtered_x
    data['y'] = filtered_y
    source.change.emit();
""")
#adding the slider miss distance to the plot
miss_slider.js_on_change('value', callback)

dates_column = datasteroids['close_approach_day']

#creating the range slider for date selection

date_range_slider = DateRangeSlider(
    title=" Select Date", start=dates_column[0], end=dates_column[len(dates_column)-1],
    value=(dates_column[0], dates_column[len(dates_column)-1]), step=1, width= 500)

callback = CustomJS(args=dict(source=source, slider=date_range_slider), code="""
    // declaring variables
    const data = source.data;
    const selected_start_date = slider.value[0];  
    const selected_end_date = slider.value[1]; 
    // creating X and Y axes to be filled
    const x_available = data['x_available']
    const y_available = data['y_available']
    const list_of_dates = data['approach_date']
    //
    const filtered_x = []
    const filtered_y = []
    for (var i = 0; i < list_of_dates.length; i++) {
        var current_date = Date.parse(list_of_dates[i])
        // filter each asteroid, remove the ones that are within selected value
        if (selected_start_date <= current_date && selected_end_date >= current_date ) {
            filtered_x.push(data['x_available'][i])
            filtered_y.push(data['y_available'][i])
        }
    }
    data['x'] = filtered_x
    data['y'] = filtered_y
    source.change.emit();
""")
#adding the range slider to the plot
date_range_slider.js_on_change('value', callback)

#adding some explanation text

text = Div(text="<h1> This graphic shows all 2710 asteroids that came close to Earth within a 6 months period. Here the graphic gives the missed distance of the asteroids in Lunar (1L = 384,000 km), as well as an idea of the strength the impact could have created on the ground (Asteroid's diameter*Velocity in Km/h). </h1>", width=300, height=300)


#Organizing the sliders and the plot 
row2 = row(p, text)

layout_all_2 = column(row2, miss_slider, date_range_slider)
output_file("Ouch.html")
#show(layout_all_2)

tab2 = Panel(child=layout_all_2, title="Asteroids' Hazard")
tabs = Tabs(tabs=[ tab1, tab2 ])
show(tabs)