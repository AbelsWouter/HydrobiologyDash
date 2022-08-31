import dash_leaflet as dl
from dash import dcc, html, callback
from classes.LoadData import LoadData

# Load data #
# JSON geodata of measurementobjects RWS
geo_data = LoadData.geo_data()

# Index Page #
# Configure Index page and map with measurement locations
index_page = html.Div(
    id='index',
    children=[
        html.Div(
            id='navbar',
            children=[
                html.Header(
                    children=[
                        dcc.Link(
                            'Home',
                            href='/',
                            className='link_active'
                        ),
                        dcc.Link(
                            'Abundantie',
                            href='/abundantie',
                            className='link'
                        ),
                        dcc.Link(
                            'Validatie',
                            href='/validatie',
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
                    id='index_text_map',
                    children=[
                        html.Div(
                            id='index_text',
                            children=[
                                html.H1(
                                    'Geautomatiseerde validatie en analyse van Macro-Evertebraten data'
                                ),
                                html.P(
                                    'Dit rapport'
                                    ' betreft de geautomatiseerde'
                                    ' datavalidatie en analyse methode'
                                    ' voor het controleren van de'
                                    ' data oplevering van'
                                    ' perceel A, B'
                                    ' (Randmeren en Trintelzand) en C (Maas).'
                                ),
                                html.P(
                                    'In dit rapport zijn de volgende'
                                    ' validatie stappen uitgevoerd:'
                                ),
                                html.Ul(
                                    children=[
                                        html.Li(
                                            'Collectienummers zijn gevalideerd op'
                                            ' notatie van het juiste jaartal.'
                                        ),
                                        html.Li(
                                            'Taxon statuscode van de gedetermineerde'
                                            ' soorten worden gecontroleerd met de TWN lijst.'
                                        ),
                                        html.Li(
                                            'Voor de taxongroepen Oligochaeta en'
                                            ' Chironomiden is er gevalideer'
                                            ' of er wel minimaal 100 zijn gedetermineerd'
                                            ' wanneer de berekende waarde 100 of hoger is.'
                                        ),
                                        html.Li(
                                            'Voor de resterende taxongroepen is een'
                                            ' soortgelijke validatie uitgevoerd'
                                            ' maar dan met minimaal 50 gedetermineerde'
                                            ' individuen.'
                                        ),
                                        html.Li(
                                            'Er is gevalideerd wanneer er getallen met'
                                            ' een factor worden doorgerekend'
                                            ' of dit ook genoteerd is met een limietsymbool.'
                                        ),
                                        html.Li(
                                            'De nieuwe data wordt vergeleken met'
                                            ' historische data van de afgelopen 6 jaar'
                                            ' om te kijken of er soorten niet zijn'
                                            ' gevonden bij deze metingen'
                                            ' die wel in het verleden op de locaties'
                                            ' zijn aangetroffen.'
                                        ),
                                        html.Li(
                                            'Ook wordt er gecontroleerd of er soorten'
                                            ' zijn gevonden'
                                            ' die nooit eerder op de meetlocaties zijn'
                                            ' waargenomen.'
                                        )
                                    ]
                                ),
                                html.P(
                                    'Verder is de data geplot,'
                                    ' alle meetdata worden opgedeeld per taxongroep,'
                                    ' meetjaar en op basis van meetlocatie.'
                                    ' De verwerkte waarde worden omgerekend naar'
                                    ' relatieve waarden'
                                    ' om dit vervolgens tegen jaren uit te zetten in grafieken.'
                                    ' Er wordt een overzichtsgrafiek geplot waar alle'
                                    ' locatie bij elkaar worden genomen.'
                                    ' Ook wordt alle data per meetlocatie geplot. In het'
                                    ' totaal gaat het om 122 plots.'
                                ),
                                html.P(
                                    'Wat er nog toegevoegd gaat worden:'
                                    ),
                                html.Ul(
                                    children=[
                                        html.Li(
                                            'Controleren of de coördinaten van de'
                                            ' meeting dichtbij genoeg zijn van het meetpunt.'
                                        ),
                                        html.Li(
                                            'Validatie van de sample volumes en oppervlaktes.'
                                        ),
                                        html.Li(
                                            'Statistische tests op de data uitvoeren,'
                                            ' om mogelijk wat te kunnen zeggen over'
                                            ' correlaties door de jaren heen.'
                                        ),
                                        html.Li(
                                            'Opmaak en leesbaarheid verbeteren.'
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            id='index_map',
                            children=[
                                dl.Map(
                                    center=[
                                        53, 5
                                    ],
                                    zoom=7,
                                    children=[
                                        dl.TileLayer(),
                                        dl.GestureHandling(),
                                        dl.GeoJSON(
                                            data=geo_data,
                                            cluster=True,
                                            zoomToBoundsOnClick=True,
                                            superClusterOptions={
                                            'radius': 120,
                                            'extent': 250
                                            }
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)