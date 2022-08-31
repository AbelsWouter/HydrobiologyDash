from classes.LoadData import LoadData
from dash import dcc, html, dash, Input, Output
from pages.IndexPage import *
from pages.AbundancePage import *
from pages.ValidationPage import *

#---------------------------------------------
# File: dash_graph.py
# Author: Wouter Abels (wouter.abels@rws.nl)
# Created: 21/02/22
# Last modified: 01/08/22
# Python ver: 3.10.6
#---------------------------------------------

# Load data#
# Load footer text and logo
footer_footer = LoadData.footer_logo()

# Build App
app = dash.Dash(
    __name__,
    title='RWS Hydrobiologie Dash'
)
app.layout = html.Div(
    id='app',
    children= [
        dcc.Location(
            id='url',
            pathname='/',
            refresh=False
        ),
        html.Div(
            id='page_content'
        )
    ]
)

# Pagination
# app callback for page selection in header
@app.callback(
    Output(
        'page_content', 
        'children'
    ),
    Input(
        'url', 
        'pathname'
    )
)

# Configure the multiple pages
def display_page(pathname):
    """Redirects webpage to selected page from navbar."""
    paths = {
        '/': index_page,
        '/abundantie': abundance_page,
        '/validatie': validation_page,
    }
    return paths.get(pathname)

#Run app
if __name__ == '__main__':
    app.run_server()