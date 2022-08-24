from classes.Validation import Validations
from dash import dcc, html, dash_table, Input, Output, callback
from classes.LoadData import LoadData

# Load data #
# Load footer text and logo
footer_logo = LoadData.footer_logo()

# MACEV data from 2015 till 2021
current_data, historic_data, unique_measurementobject, historic_and_current = LoadData.macev_data()

# Data validation #
# Configure the validation page
validation_page = html.Div(
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
                            className='link'
                        ),
                        dcc.Link(
                            'Validatie', 
                            href='/validatie', 
                            className='link_active'
                        ),
                        dcc.Link(
                            'Statistiek',
                            href='/statistiek', 
                            className='link'
                        )
                    ]
                )
            ],
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
                    'Validatie'
                ),
                html.Div(
                    id='dropdown_and_table',
                    children=[
                        dcc.Dropdown(
                            id='table_dropdown',
                            options=[
                                {
                                    'label':'Collectienummer Validatie',
                                    'value':'collection',
                                },
                                {
                                    'label':'Taxonstatus Validatie',
                                    'value':'taxonstatus',
                                },
                                {
                                    'label':'Oligochaeten Validatie',
                                    'value':'oligochaeta',
                                },
                                {
                                    'label':'Chironomiden Validatie',
                                    'value':'chironomidae',
                                },
                                {
                                    'label':'Taxongroep Validatie',
                                    'value':'taxongroup',
                                },
                                {
                                    'label':'Factor Validatie', 
                                    'value':'factor'
                                },
                                {
                                    'label':'Missende Taxa',
                                    'value':'missing'
                                },
                                {
                                    'label':'Nieuwe Taxa', 
                                    'value':'new'
                                },
                            ],
                            value='collection',
                            clearable=False
                        ),
                        dcc.Loading(
                            children=[
                                dash_table.DataTable(     
                                    id='table_object',
                                    columns=[
                                        {'name': i,'id': i} for i in historic_and_current
                                    ],
                                    sort_action='native',
                                    filter_action='native',
                                    css=[
                                        {
                                            'selector':'.previous-page,'
                                            '.next-page, .first-page,'
                                            '.last-page, .export, .show-hide',
                                            'rule':'color: black;',
                                        },
                                        {
                                            'selector':'.current-page',
                                            'rule':'padding-right: 5px;',
                                        },
                                    ],
                                    style_cell={
                                        'whiteSpace':'normal',
                                        'width':'100px',
                                        'textAlign':'center',
                                        'height':'15px',
                                        'padding-left':'10px',
                                        'padding-right':'10px',
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index':'odd'},
                                            'backgroundColor':'rgb(240, 240, 240)',
                                        },
                                    ],
                                    style_table={
                                        'height':'auto',
                                        'width':'auto',
                                        'overflowX':'auto',
                                        'overflowY':'auto',
                                    },
                                    cell_selectable=False,
                                    page_size=16,
                                    style_as_list_view=True,
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

# App callback for the dropdown menu in validation page
@callback(
    Output(
        'table_object', 'data'
    ),
    Input(
        'table_dropdown', 'value'
    )
)

# The table selections with validation data
def table_update(dropdown_value):
    current_data_validations = [
        'collection', 'taxonstatus', 'oligochaeta', 'chironomidae', 'taxongroup', 'factor'
    ]
    current_and_historic_data_validations = [
        'missing', 'new'
    ]
    if dropdown_value in current_data_validations:
        table_data = getattr(Validations, dropdown_value)
        return table_data(current_data).to_dict('records')
    elif dropdown_value in current_and_historic_data_validations:
        table_data = getattr(Validations, dropdown_value)
        return table_data(current_data, historic_data).to_dict('records')