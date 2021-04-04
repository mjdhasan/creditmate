
# https://stackoverflow.com/questions/53817270/html-structure-into-network-graph
# def _traverse_html(_d: soup, _graph: nx.Graph, _counter, _parent=None) -> None:
#     for i in _d.contents:
#         if i.name is not None:
#             try:
#                 _name_count = _counter.get(i.name)
#                 if _parent is not None:
#                     _graph.add_node(_parent)
#                     _graph.add_edge(_parent, i)
#                 _counter[i.name] += 1
#                 _traverse_html(i, _graph, _counter, i)
#             except AttributeError:
#                 pass


# # User Controls
# html.Div(
#     className="four columns card",
#     children=[
#         html.Div(
#             className="bg-white user-control",
#             children=
#             dcc.Tabs(
#                 id='sidebar-tabs',
#                 value='upload',
#                 children=[
#                     dcc.Tab(
#                         label='Upload',
#                         value='upload',
#                         children=[html.Div(
#                             className="padding-top-bot",
#                             children=[
#                                 # html.H6("File"),
#                                 dcc.Upload(
#                                     id="upload-data",
#                                     className="upload",
#                                     children=html.Div(
#                                         children=[
#                                             html.P("Drag and Drop or Select Files")
#                                             # html.A("Select Files"),
#                                         ]
#                                     ),
#                                     # accept=[".csv", ".pdf", ".xlsx"],
#                                     multiple=True
#                                 ),
#                             ],
#                         ),
#                             # html.Ul(id="file-list"),
#                             html.H6("Uploaded Files"),
#                             dcc.Dropdown(id='file-dropdown', multi=True),
#                             html.H6("Extracted Tables"),
#                             dcc.Dropdown(id='table-dropdown', multi=True),
#                             html.Div(
#                                 className="padding-top-bot",
#                                 children=[
#                                     html.H6("Available Fields"),
#                                     # dcc.Dropdown(id="study-dropdown"),
#                                     dcc.Dropdown(
#                                         id='column-dropdown',
#                                         multi=True
#                                     )
#                                 ],
#                             )
#                             # html.Div(
#                             #     className="padding-top-bot",
#                             #     children=[
#                             #         html.H6("Choose the type of plot"),
#                             #         dcc.RadioItems(
#                             #             id="chart-type",
#                             #             options=[
#                             #                 {"label": "Box Plot", "value": "box"},
#                             #                 {
#                             #                     "label": "Violin Plot",
#                             #                     "value": "violin",
#                             #                 },
#                             #             ],
#                             #             value="violin",
#                             #             labelStyle={
#                             #                 "display": "inline-block",
#                             #                 "padding": "12px 12px 12px 0px",
#                             #             },
#                             #         ),
#                             #     ],
#                             # )
#
#                         ]
#                     ),
#                     dcc.Tab(
#                         label='Scrape',
#                         value='scrape'
#                     )
#                 ]
#             )
#         )
#     ],
# ),



# # Callback to generate error message
# # Also sets the data to be used
# # If there is an error use default data else use uploaded data
# @app.callback(
#     [
#         Output("error", "data"),
#         Output("error-message", "children"),
#         Output("study-dropdown", "options"),
#         Output("study-dropdown", "value"),
#     ],
#     [Input("upload-data", "filename"),
#      Input("upload-data", "contents")],
# )
# def update_error(filenames, contents):
#
#     if filenames is not None and contents is not None:
#         for name, data in zip(filenames, contents):
#             save_file(name, data)
#
#     error_status = False
#     error_message = None
#     study_data = default_study_data
#
#     # Check if there is uploaded content
#     if filenames:
#         file_path = os.path.join(UPLOAD_DIRECTORY, filenames[0])
#         # Try reading uploaded file
#         try:
#             study_data = load_workbook(file_path)
#             print('successfully loaded study_data')
#         except Exception as e:  # Data is invalid
#             error_message = html.Div(
#                 className="alert",
#                 children=["That doesn't seem to be a valid csv file!"],
#             )
#             error_status = True
#             study_data = default_study_data
#     else:
#         print('no content')
#
#     # Update Dropdown
#     options = []
#     mapping = {}
#     for sheet_name in study_data.sheetnames:
#         ws = study_data[sheet_name]
#         for entry, data_boundary in ws.tables.items():
#             options.append({"label": f"{sheet_name}_{entry}", "value": f"{sheet_name}_{entry}"})
#             mapping[entry] = parse_excel_table(ws, data_boundary)
#
#     options.sort(key=lambda item: item["label"])
#     value = options[0]["value"] if options else None
#
#     return error_status, error_message, options, value


# @app.callback(
#     Output('table-editing-simple-output', 'figure'),
#     Input('table-editing-simple', 'data'),
#     Input('table-editing-simple', 'columns'))
# def display_output(rows, columns):
#     df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#     return {
#         'data': [{
#             'type': 'parcoords',
#             'dimensions': [{
#                 'label': col['name'],
#                 'values': df[col['id']]
#             } for col in columns]
#         }]
#     }
# # Callback to generate study data
# @app.callback(
#     [Output('tables', 'data'), Output('tables', 'columns')],
#     [Input("study-dropdown", "value")],
#     [State("upload-data", "contents"), State("error", "data")],
# )
# def updateTable(study, contents, error):
#     # df = pd.DataFrame({'a': [1, 2, 3], 'b': ['a', 'b', 'c']})
#     df = pd.DataFrame({'Symbol': ['RSG'], 'Company': ['Republic Services  Inc.'], 'Market Cap': [31604176866]})
#     # columns = [{'name': str(i), 'id': str(i)} for i in df.columns]
#
#     return df.to_dict('records'), [{'name': 'Symbol', 'id': 'sym'}, {'name': 'Company', 'id': 'company'}]
#     # return np.array({'Symbol': ['aapl'], 'Company': ['Apple Inc']})
#
#     # dash_table.DataTable(data=df.to_dict(), columns=[{"name": i, "id": i} for i in df.columns])
#     # return [
#     #     dash_table.DataTable(
#     #         rows=df.to_dict('rows'),
#     #         columns=df.columns,
#     #         row_selectable=True,
#     #         filterable=True,
#     #         sortable=True,
#     #         selected_row_indices=list(df.index),  # all rows selected by default
#     #         id='3'
#     #     )
#     # ]


# def update_output(chart_type, study, contents, error):
#     if study is None:
#         return {}
#
#     if error or not contents:
#         study_data = default_study_data
#     else:
#         content_type, content_string = contents.split(",")
#         decoded = base64.b64decode(content_string)
#         # study_data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
#         study_data = load_workbook(io.StringIO(decoded.decode("utf-8")))
#
#     figure = None
#     df = pd.DataFrame({'a': [1, 2, 3], 'b': ['a', 'b', 'c']})
#
#     return df.values, columns[0:2]

