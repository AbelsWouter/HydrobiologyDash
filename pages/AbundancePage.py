import plotly.express as px
from classes.Graph import Graphs
from dash import dcc, html, Input, Output, callback
from classes.LoadData import LoadData


# Load data #
# Load footer text and logo
footer_logo = LoadData.footer_logo()

# MACEV data from 2015 till 2021
current_data, historic_data, unique_measurementobject, historic_and_current = LoadData.macev_data()

# Data for abundance plot
total_plot_data = Graphs.value_per_year(historic_and_current)

# Abbundance graphs page #
# Configure the page with the graphs
abundance_page = html.Div(
    id='abundance_page',
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
                        dcc.Link(
                            'Abundantie',
                             href='/abundantie', 
                             className='link_active'
                        ),
                        dcc.Link(
                         'Validatie', 
                            href='/validatie', 
                            className='link'
                        ),
                        dcc.Link(
                            'Statistiek', 
                            href='/statistiek', 
                            className='link'
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id='page',
            children=[
                html.Div(
                    id='graph_total',
                    children=[
                        html.H1(
                            'Macroevertebraten'
                        ),
                        html.H2(
                            '2015-2021'
                        )
                    ]
                ),
                html.H2(
                    'Abundantie'
                ),
                html.Div(
                    id='abundance_radio',
                    children=[
                        dcc.RadioItems(
                            id='abundance_radio',
                            options=[
                                {
                                    'label':'Totale Abundantie',
                                    'value':'Totale Abundantie',
                                },
                                {
                                    'label':'Relatieve Abundantie',
                                    'value':'Relatieve Abundantie',
                                }
                            ],
                            value='Totale Abundantie',
                            labelStyle={'display':'inline-block'},
                            style={
                                'display':'flex','justifyContent':'center'
                            }
                        )
                    ]
                ),
                dcc.Loading(
                    children=[
                        dcc.Graph(
                            id='abundance_graph'
                        )
                    ]
                ),
                html.H2(
                    'Abundantie per meetobject'
                ),
                html.Div(
                    id='graph_dropdown_objects',
                    children=[
                        html.Div(
                            id='dropdown_objects',
                            children=[
                                dcc.Dropdown(
                                    id='object_dropdown',
                                    options=[
                                        {
                                        'label': i,'value': i
                                        }
                                        for i in unique_measurementobject
                                    ],
                                    value=unique_measurementobject[0],
                                    clearable=False,
                                    optionHeight=40,
                                    maxHeight=360
                                )
                            ]
                        ),
                        
                        html.Div(
                            id='graph_objects', 
                            children=[
                                dcc.Loading(
                                    children=[
                                        dcc.Graph(
                                            id='object_graph'
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            ]
        ),
        footer_logo
    ]
)

# App callback for the total or relative abundance graph
@callback(
    Output(
        'abundance_graph','figure'
    ),
    Input(
        'abundance_radio', 'value'
    ),
)

# Total abundace graph with its properties
def graph_total_update(dropdown_value):
    fig0 = px.bar(
        total_plot_data,
        color_discrete_map=Graphs.macev_taxongroup_colours,
        title='Totale Abundantie', template='simple_white',
        orientation='h',
        labels={
            'value':'Totale Abundantie (n)', 
            'index':'Jaar', 
            'Taxongroup':'Taxongroep'
            }
    )
    fig1 = px.bar(
        total_plot_data.apply(lambda x: x*100/sum(x),axis=1),
        color_discrete_map=Graphs.macev_taxongroup_colours,
        title='Relatieve Abundantie',
        template='simple_white',
        orientation='h',
        labels={
            'value':'Relatieve Abundantie (%)', 
            'index':'Jaar', 
            'Taxongroup':'Taxongroep'
            }
    )
    if dropdown_value =='Totale Abundantie':
        return fig0
    elif dropdown_value =='Relatieve Abundantie':
        return fig1

# App callback for the graphs dropdown and radio buttons
@callback(
    Output('object_graph','figure'),
    Input('object_dropdown','value'),
    Input('abundance_radio','value'),
)

# The properties of the graph per measurement object with abundance data
def graph_object_update(object_value, radio_value):
    for object in unique_measurementobject:
        if radio_value =='Totale Abundantie':
            if object == object_value:
                object_plot_data = Graphs.relative_data_location_per_year(
                    historic_and_current, object_value)
                fig2 = px.bar(
                    object_plot_data,
                    color_discrete_map=Graphs.macev_taxongroup_colours,
                    title='Totale Abundantie meetobject:'+ str(object_value),
                    template='simple_white',
                    orientation='h',
                    labels={
                        'value':'Totale Abundantie (n)', 
                        'index':'Jaar', 
                        'Taxongroup':'Taxongroep'
                        }
                )
                return fig2
        elif radio_value =='Relatieve Abundantie':
            if object == object_value:
                object_plot_data = Graphs.relative_data_location_per_year(
                    historic_and_current, object_value)
                fig3 = px.bar(
                    object_plot_data.apply(lambda x: x*100/sum(x),axis=1),
                    color_discrete_map=Graphs.macev_taxongroup_colours,
                    title='Relatieve Abundantie meetobject:'+ str(object_value),
                    template='simple_white',
                    orientation='h',
                    labels={
                        'value':'Relatieve Abundantie (%)', 
                        'index':'Jaar', 
                        'Taxongroup':'Taxongroep'
                        }
                )
                return fig3
