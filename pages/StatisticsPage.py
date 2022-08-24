import pandas as pd
import plotly.express as px
from classes.Statistics import Statistics
from dash import dcc, html, Input, Output, callback
from classes.LoadData import LoadData

# Load data #
# Load footer text and logo
footer_logo = LoadData.footer_logo()

# MACEV data from 2015 till 2021
current_data, historic_data, unique_measurementobject, historic_and_current = LoadData.macev_data()

# Statistics page #
# Load Statistics page
statistics_page = html.Div(
    id='statistics_page',
    children=[
        html.Div(
            id='navbar',
            children=[
                html.Header(
                    children=[
                        dcc.Link(
                            'Home', 
                            href='/', 
                            className='link'
                        ),
                        dcc.Link('Abundantie', 
                            href='/abundantie', 
                            className='link'
                        ),
                        dcc.Link(   
                            'Validatie', 
                            href='/validatie', 
                            className='link'
                        ),
                        dcc.Link(
                            'Statistiek', 
                            href='/statistiek', 
                            className='link_active'
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id='page',
            children=[ 
                html.H1(
                    'Macroevertebraten'
                ),
                html.H2(
                    '2015-2021'
                ),
                html.H2(
                    'Statistiek'
                ),
                html.Div(
                    id='dropdown_and_heatmap', 
                    children=[
                        html.Div(
                            id='selection_statistics', children=[
                                html.P(
                                    'Soort statistische test'
                                ),
                                dcc.Dropdown(
                                    id='statistical_test_dropdown',
                                    options=[
                                        {
                                            'label': 'Similariteit',
                                            'value': 'similarity'
                                        },
                                        {
                                            'label': 'Test',
                                            'value': 'test'
                                        }
                                    ],
                                    value='similarity',
                                ),
                            ]
                        ),
                        html.Div(
                            id='statistics'
                        ),
                    ]
                ),
            ]
        ),
        footer_logo
    ]
) 

@callback(
    Output('statistics', 'children'),
    Input('statistical_test_dropdown', 'value')
)

#Create heatmap
def statistics(statistical_value):
    if statistical_value == 'similarity':
        return html.Div(
            id='similarity', 
            children=[
                html.Div(
                    id='div_data_selection_heatmap',
                    children=[
                        html.P(
                        'Data selectie'
                        ),
                        dcc.RadioItems(
                            id='heatmap_radio',
                            options=[
                                {
                                    'label': 'Jaar',
                                        'value': 'year'
                                },
                                {
                                    'label': 'Locatie',
                                    'value': 'measurement_object'

                                }
                            ],
                        value='year',
                        ),
                        html.P(
                            'Methode'
                        ),
                        dcc.Dropdown(
                            id='heatmap_dropdown', 
                            options=[
                                {
                                    'label': 'Bray Curtis',
                                    'value': 'bray_curtis'
                                },
                                {
                                    'label': 'Chao',
                                    'value': 'chao'
                                }
                            ],
                            value='bray_curtis',
                            clearable=False
                        ),
                    ]
                ),
                html.Div(
                    id='div_heatmap', 
                    children=[
                        dcc.Loading(
                            children=[
                                dcc.Graph(
                                    id='heatmap'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    elif statistical_value == 'test':
        return html.Div(
            children=[
                html.P(
                    'test'
                )
            ]
        )
    else:
        return html.Div(
            children=[
                html.H2(
                    'Geen statistische test gekozen'
                )
            ]
        )

@callback(
    Output('heatmap', 'figure'),
    Input('statistical_test_dropdown', 'value'), 
    Input('heatmap_radio', 'value',),
    Input('heatmap_dropdown', 'value')
)

#Create heatmap
def heatmap(statistical_value, radio_value, dropdown_value):
    if statistical_value == 'similarity':
        label = 'Similariteit'
        if dropdown_value == 'bray_curtis':
            methode = 'Bray Curtis'
        elif dropdown_value == 'chao':
            methode = 'Chao'
        if radio_value == 'year':
            statistic_func = getattr(Statistics, dropdown_value)
            fig = px.imshow(statistic_func(pd.read_csv('data/bray_testdata.csv', index_col=[0])),title= methode, aspect='auto', labels=dict(x='Locatie', y='Locatie',color=label), text_auto=True)
            return fig
        elif radio_value == 'location':
            pass
    else:
        pass