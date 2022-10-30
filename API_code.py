#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:43:42 2021

@author: floramainguet
"""

import requests
import json
import pandas as pd
import bokeh 
from bokeh.plotting import figure
from bokeh.io import output_file, show
import numpy as np
from bokeh.io import curdoc
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

# In order to get the data I used an API from NASA. As NASA allows only to scrape 7 days per 7 days
#I first tried all my codes with only a few weeks and added the rest once all sliders and plots were working in JupyterNotebook

key = '3bXKAHzkSA9pyWjJ7TcXIybdnMN0lIeT3UmnKuHa'

# define date ranges to use in ther query
date_ranges = [
    {'start': '2019-01-01',
    'end': '2019-01-08'},
    {'start': '2019-01-08',
    'end': '2019-01-15'},
    {'start': '2019-01-15',
    'end': '2019-01-22'}, 
    {'start': '2019-01-22',
    'end': '2019-01-29'},
    {'start': '2019-01-29',
    'end': '2019-02-01'},
    {'start': '2019-02-01',
    'end': '2019-02-08'},
    {'start': '2019-02-08',
    'end': '2019-02-15'},
    {'start': '2019-02-15',
    'end': '2019-02-22'},
    {'start': '2019-02-22',
    'end': '2019-02-28'},
    {'start': '2019-02-28',
    'end': '2019-03-07'},
    {'start': '2019-03-07',
    'end': '2019-03-14'},
    {'start': '2019-03-14',
    'end': '2019-03-21'},
    {'start': '2019-03-21',
    'end': '2019-03-28'},
    {'start': '2019-03-28',
    'end': '2019-03-31'},
     {'start': '2019-03-31',
    'end': '2019-04-07'},
    {'start': '2019-04-07',
    'end': '2019-04-14'},
     {'start': '2019-04-14',
    'end': '2019-04-21'},
     {'start': '2019-04-21',
    'end': '2019-04-28'},
     {'start': '2019-04-28',
    'end': '2019-05-05'},
     {'start': '2019-05-05',
    'end': '2019-05-12'},
    {'start': '2019-05-12',
    'end': '2019-05-19'},
    {'start': '2019-05-19',
    'end': '2019-05-26'},
    {'start': '2019-05-26',
    'end': '2019-06-02'},
    {'start': '2019-06-02',
    'end': '2019-06-09'},
    {'start': '2019-06-09',
    'end': '2019-06-16'},
    {'start': '2019-06-16',
    'end': '2019-06-23'},
    {'start': '2019-06-23',
    'end': '2019-06-30'}]

#
all_objects = []

# loop tthrough the date ranges and query thbe NASA api
for date_range in date_ranges:
    url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'.format(**{
    'start_date':date_range['start'], 'end_date' : date_range['end'], 'api_key' : key
})
    response = requests.get(url) #this is what I used to filter the columns and keep only the ones I needed.
    raw_data = json.loads(response.text)
    # loop through each day in the response
    for date in raw_data['near_earth_objects'].keys():
        print(date)
        objects_for_this_day = raw_data['near_earth_objects'][date]
        parsed_objects = []
        # loop through each near earth objects for this day
        for obj in objects_for_this_day:
            # parse each object for the dataframe
            parsed_objects.append({
                'estimated_diameter': obj['estimated_diameter'],
                'name': obj['name'],
                'neo_reference_id': obj['neo_reference_id'],
                'absolute_magnitude_h': obj['absolute_magnitude_h'],
                'is_sentry_object': obj['is_sentry_object'],
                'close_approach_day' : obj['close_approach_data'][0]['close_approach_date'],
                'close_approach_full' : obj['close_approach_data'][0]['close_approach_date_full'],
                'relative_velocity_kmh' : obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                'miss_distance_lunar' : obj['close_approach_data'][0]['miss_distance']['lunar'],
                'miss_distance_astro' : obj['close_approach_data'][0]['miss_distance']['astronomical'],
                'miss_distance_km' : obj['close_approach_data'][0]['miss_distance']['kilometers'],
                'estimated_diameter_min': float(obj['estimated_diameter']['meters']['estimated_diameter_min']),
                'estimated_diameter_max': float(obj['estimated_diameter']['meters']['estimated_diameter_max']),
            }) #estimated diameter_min and _max were changed to floats for creating the column average diameter
        
        # add the parsed objects to all objects5
        all_objects += parsed_objects

# add all the near earth objects to the dataframe
all_obj_dataframe = pd.DataFrame(all_objects)

#create the column average_diameter
all_obj_dataframe["average_diameter"] = all_obj_dataframe [['estimated_diameter_min', 'estimated_diameter_max']].mean(axis=1)

#changing to floats to create impact_strength column
all_obj_dataframe[['average_diameter','relative_velocity_kmh']] = all_obj_dataframe[['average_diameter','relative_velocity_kmh']].astype(float)
all_obj_dataframe['impact_strength'] = all_obj_dataframe.average_diameter * all_obj_dataframe.relative_velocity_kmh
all_obj_dataframe.to_csv("data.csv")





