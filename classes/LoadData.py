import json
import numpy as np
import pandas as pd
from dash import html
from HydrobiologyDash import app

class LoadData:

    def footer_logo():
        footer = 'Wouter Abels (wouterabels@rws.nl) 22 Augustus 2022 Python 3.10.6'
        logo = ('assets/IW_RW_Logo_online_pos_nl.png')
        footer_logo = html.Div(
            children=[
                html.Footer(
                    footer
                ),
                html.Img(
                    id='logo',
                    src=app.get_asset_url(logo)
                )
            ]
        )
        return footer_logo

    def geo_data():
        with open ('data/measurementobjects_rws.json', 'r') as f:
            geo_data = json.load(f)
        return geo_data
    
    def macev_data():
        all_data = pd.read_csv(
            'data/macev_2015_2021.csv',
            dtype={'externalreference': str})
        all_data = all_data.drop(
            [
                'name',
                'taxongroup_twn',
                'synonymname',
                'maintypecode',
                'code'
            ],
            axis= 1
        )
        current_data = all_data.loc[all_data['measurementdate'] >= '2021']
        historic_data = all_data.loc[all_data['measurementdate'] <= '2021']
        unique_measurementobject = np.sort(
            pd.unique(
                current_data['measurementobjectname']
            )
        )
        historic_location= []
        historic_and_current = []
        for object in unique_measurementobject:
            historic_per_location = historic_data.loc[historic_data['measurementobjectname'] == object]
            all_per_location = all_data.loc[all_data['measurementobjectname'] == object]
            historic_and_current = pd.concat(
                [
                    all_per_location,
                    pd.DataFrame(
                        historic_and_current
                    )
                ]
            )
            historic_location = pd.concat(
                [
                    historic_per_location,
                    pd.DataFrame(
                        historic_location
                    )
                ]
            )
        return current_data, historic_data, unique_measurementobject, historic_and_current



