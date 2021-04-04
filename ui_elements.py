import dash_core_components as dcc
import dash_html_components as html
# import dash_bootstrap_components as dbc
import dash_table

tabs_styles = {
    'height': '44px'
}
top_tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold'
}
top_tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    # 'borderTop': '1px solid #d6d6d6',
    # 'borderBottom': '1px solid #d6d6d6',
    # 'backgroundColor': '#119DFF',
    # 'color': 'white',
    'padding': '6px'
}


def create_app_layout(app):
    return html.Div(
        children=[
            # # Error Message
            # html.Div(id="error-message"),
            # Top Banner
            html.Div(
                className="study-browser-banner row",
                children=[
                    html.H2(className="h2-title", children="ESGnomist"),
                    # html.Div(
                    #     className="div-logo",
                    #     children=html.Img(
                    #         className="logo", src=app.get_asset_url("dash-logo-new.png")
                    #     ),
                    # ),
                    html.H2(className="h2-title-mobile", children="ESGnomist"),
                ],
            ),
            # Body of the App
            html.Div(
                className="row app-body",
                children=[
                    # search box
                    html.Div(
                        # className="padding-top-bot",
                        children=[dcc.Input(id='search-box',
                                            type='text',
                                            placeholder='Enter search query',
                                            style={'width': '75%', 'height': '100%'}),
                                  html.Button('Search', id='search-go', n_clicks=0,
                                              style={'height': '100%'})
                                  ],
                        style={'display': 'flex',
                               'justifyContent': 'center',
                               'width': '100%',
                               'height': '50px',
                               'margin-top': '15px',
                               'verticalAlign': 'middle'}
                    ),
                    # Main panel
                    html.Div(
                        className="twelve columns card-left",
                        children=[
                            dcc.Tabs(
                                id='top-tabs',
                                value='output-tab',
                                # vertical=True,
                                children=[
                                    dcc.Tab(
                                        label='Inputs',
                                        id='input-tab',
                                        value='input-tab',
                                        style=top_tab_style,
                                        selected_style=top_tab_selected_style,
                                        children=[
                                            dcc.Tabs(
                                                id='tabs',
                                                value='upload',
                                                children=[
                                                    dcc.Tab(
                                                        label='Upload',
                                                        value='upload',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style,
                                                        children=[html.Div(
                                                            className="padding-top-bot",
                                                            children=[
                                                                # html.H6("File"),
                                                                dcc.Upload(
                                                                    id="upload-data",
                                                                    className="upload",
                                                                    children=html.Div(
                                                                        children=[
                                                                            html.P("Drag and Drop or Select Files")
                                                                            # html.A("Select Files"),
                                                                        ]
                                                                    ),
                                                                    # accept=[".csv", ".pdf", ".xlsx"],
                                                                    multiple=True
                                                                ),
                                                            ],
                                                        ),
                                                            # html.Ul(id="file-list"),
                                                            html.H6("Uploaded Files"),
                                                            dcc.Dropdown(id='file-dropdown', multi=True),
                                                            html.H6("Extracted Tables"),
                                                            dcc.Dropdown(id='table-dropdown', multi=True),
                                                            html.Div(
                                                                className="padding-top-bot",
                                                                children=[
                                                                    html.H6("Available Fields"),
                                                                    # dcc.Dropdown(id="study-dropdown"),
                                                                    dcc.Dropdown(
                                                                        id='column-dropdown',
                                                                        multi=True
                                                                    )
                                                                ],
                                                            )
                                                        ]
                                                    ),
                                                    dcc.Tab(
                                                        label='Scrape',
                                                        value='scrape',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style,
                                                        children=[
                                                            # search keywords
                                                            html.Div(
                                                                className="padding-top-bot",
                                                                children=[dcc.Input(id='web-search',
                                                                                    type='text',
                                                                                    placeholder='Enter search keywords',
                                                                                    style={'width': '50%',
                                                                                           'height': '100%'}),
                                                                          dcc.Input(id='web-search-sources',
                                                                                    type='text',
                                                                                    placeholder='Enter sources to search',
                                                                                    style={'width': '50%',
                                                                                           'height': '100%'})
                                                                          ],
                                                                style={'display': 'flex',
                                                                       'justifyContent': 'center',
                                                                       'width': '100%',
                                                                       'height': '50px',
                                                                       # 'margin-top': '15px',
                                                                       'verticalAlign': 'middle'}
                                                            ),
                                                            html.Div(
                                                                html.Button('Search', id='web_search_button', n_clicks=0,
                                                                            style={'height': '100%'}),
                                                                style={'display': 'flex',
                                                                       'justifyContent': 'center',
                                                                       'width': '100%',
                                                                       'height': '50px',
                                                                       # 'margin-top': '15px',
                                                                       'verticalAlign': 'middle'}
                                                            ),
                                                            # # sources to search
                                                            # dcc.Dropdown(
                                                            #     id='source-dropdown',
                                                            #     options=[{'label': 'google', 'value': 'https://www.google.com'},
                                                            #              {'label': 'linkedin', 'value': 'https://www.linkedin.com'},
                                                            #              {'label': 'sgx', 'value': 'sgx.com'}],
                                                            #     value='https://www.google.com',
                                                            #     multi=True
                                                            # )
                                                        ]
                                                    ),  # / end of scrape tab
                                                    dcc.Tab(
                                                        id='tab_onedrive',
                                                        label='OneDrive',
                                                        value='tab_onedrive',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style,
                                                        children=[
                                                            html.H6("Query Files"),
                                                            dcc.Dropdown(
                                                                id='onedrive-dropdown',
                                                                multi=False
                                                            ),
                                                            html.H6("Source Files"),
                                                            dcc.Dropdown(
                                                                id='onedrive-source-dropdown',
                                                                multi=True
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),  # end of dcc.Tabs()
                                        ]
                                    ),  # / end of inputs tab
                                    # outputs tab
                                    dcc.Tab(
                                        label='Outputs',
                                        id='output-tab',
                                        value='output-tab',
                                        style=top_tab_style,
                                        selected_style=top_tab_selected_style,
                                        children=[
                                            dcc.Tabs(
                                                id='output-subtabs',
                                                value='iframe-tab',
                                                children=[
                                                    dcc.Tab(
                                                        label='Graph',
                                                        value='graph',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style,
                                                        children=html.Div(
                                                            className="bg-white",
                                                            children=[
                                                                # html.H5("Animal data plot"),
                                                                dcc.Graph(id='table-editing-simple-output'),
                                                                # dcc.Graph(id="plot"),
                                                            ],
                                                        )
                                                    ),  # / plot tab
                                                    dcc.Tab(
                                                        id='tables-tab',
                                                        label='Tables',
                                                        value='tables-tab',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style,
                                                    ),
                                                    dcc.Tab(
                                                        id='text-tab',
                                                        label='Text',
                                                        value='text-tab',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style
                                                    ),
                                                    dcc.Tab(
                                                        id='images-tab',
                                                        label='Images',
                                                        value='images-tab',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style
                                                    ),
                                                    dcc.Tab(
                                                        id='iframe-tab',
                                                        label='Iframe',
                                                        value='iframe-tab',
                                                        style=tab_style,
                                                        selected_style=tab_selected_style,
                                                        children=[
                                                            html.Iframe(
                                                                src="https://onedrive.live.com/embed?resid=6CB02B0C51E92B1C%213460&authkey=%21AKTzxzLmfARAfy4&em=2&wdAllowInteractivity=False&wdHideGridlines=True&wdHideHeaders=True&wdDownloadButton=True&wdInConfigurator=True",
                                                                style={"height": "346px", "width": "100%", "scrolling": "no"})
                                                        ]
                                                    )
                                                ]
                                            ),  # end of dcc.Tabs()
                                        ]
                                    )  # / end of outputs tab
                                ]
                            )  # end of top tabs
                        ]
                    ),
                    # dcc.Store(id="error", storage_type="memory"),
                ],
            ),
        ]
    )
