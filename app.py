import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

df = pd.read_csv('data/country_wise_latest.csv')

day_wise = pd.read_csv('data/day_wise.csv')

full_grouped = pd.read_csv('data/full_grouped.csv')
full_grouped['Date'] = pd.to_datetime(full_grouped['Date'])

fig = px.line(day_wise, x='Date', y='Confirmed', title='Time Series with Rangeslider')
fig.update_xaxes(rangeslider_visible=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Covid DashBoard || Group #06'
url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


############################################################
#######          All key Function Day Wise        ##########
############################################################

def plot_hbar(df, col, n, hover_data=[]):
    fig = px.bar(df.sort_values(col).tail(n),
                 x=col, y="Country/Region", color='WHO Region',
                 text=col, orientation='h', width=700, hover_data=hover_data,
                 color_discrete_sequence=px.colors.qualitative.Dark2)
    fig.update_layout(title=col, xaxis_title="", yaxis_title="",
                      yaxis_categoryorder='total ascending',
                      uniformtext_minsize=8, uniformtext_mode='hide')
    return fig


def plot_daywise(col, hue='#2874A6'):
    fig = px.bar(day_wise, x="Date", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    return fig


def plot_daywise_line(col, hue='#2874A6'):
    fig = px.line(day_wise, x="Date", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    return fig


######################################################################################
# country wise
####################################################################################
def plot_stacked(col):
    fig = px.bar(full_grouped, x="Date", y=col, color='Country/Region',
                 height=600, title=col,
                 color_discrete_sequence=px.colors.cyclical.mygbm)
    fig.update_layout(showlegend=True)
    return fig


def plot_line(col):
    fig = px.line(full_grouped, x="Date", y=col, color='Country/Region',
                  height=600, title=col,
                  color_discrete_sequence=px.colors.cyclical.mygbm)
    fig.update_layout(showlegend=True)
    return fig


###############################################################################
# world_map
############################################################################

def plot_map(col, df=df, pal='matter'):
    df = df[df[col] > 0]
    fig = px.choropleth(df, locations="Country/Region", locationmode='country names',
                        color=col, hover_name="Country/Region",
                        title=col, hover_data=[col], color_continuous_scale=pal)
    #     fig.update_layout(coloraxis_showscale=False)
    return fig


############################################################################
# weekly and monthly report
###########################################################################

full_grouped['Week No.'] = full_grouped['Date'].dt.strftime('%U')
week_wise = full_grouped.groupby('Week No.')[
    'Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered'].sum().reset_index()


def plot_weekwise(col, hue='#2874D6'):
    fig = px.bar(week_wise, x="Week No.", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    return fig


full_grouped['Month'] = pd.DatetimeIndex(full_grouped['Date']).month
month_wise = full_grouped.groupby('Month')[
    'Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered'].sum().reset_index()


def plot_monthwise(col, hue='#2874D6'):
    fig = px.bar(month_wise, x="Month", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    return fig


###########################################################################
day_wise_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Covid-19 Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Project by Group #06", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.A(
                                    html.Button("Day-Wise", id="day-w"),
                                    href="/day_wise",
                                ),
                                html.A(
                                    html.Button("Country-Wise", id="country-w"),
                                    href="/country_wise",
                                ),
                                html.A(
                                    html.Button("World-Map", id="world-m"),
                                    href="/world_map",
                                ),
                                html.A(
                                    html.Button("World-report", id="world_r"),
                                    href="/world_report",
                                ),
                            ]
                        ),
                    ],
                    className="one-third column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        # html.Div(
        #     [
        #         html.Div(
        #             [
        #                 html.P("Select Country:", className="control_label"),
        #                 dcc.Dropdown(
        #                     id="country_name",
        #
        #                     options=[{'label': i, 'value': i} for i in df['Country/Region'].tolist()],
        #                     value=f"{df['Country/Region'].tolist()[79]}",
        #                     className="dcc_control",
        #                 ),
        #             ],
        #             className="pretty_container four columns",
        #             id="cross-filter-options",
        #         ),
        #         html.Div(
        #             [
        #                 html.Div(
        #                     [
        #                         html.Div(
        #                             [html.H6(id="confirmed_cases"), html.P("No. of Confirmed Cases")],
        #                             id="confirmed",
        #                             className="pretty_container three columns",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="death_cases"), html.P("No. of Deaths")],
        #                             id="death",
        #                             className="pretty_container three columns",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="recovered_cases"), html.P("Recovered cases")],
        #                             id="recovered",
        #                             className="pretty_container three columns",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="active_cases"), html.P("Active cases")],
        #                             id="active",
        #                             className="pretty_container three columns",
        #                         ),
        #                     ],
        #                     id="info-container",
        #                     className="container-display",
        #                 ),
        #             ],
        #             id="right-column",
        #             className="eight columns",
        #         ),
        #     ],
        #     className="row flex-display",
        # ),
        html.Div(
            [
                html.P("Select Cotegory:", className="control_label"),
                dcc.Dropdown(
                    id="category",

                    options=[{'label': i, 'value': i} for i in day_wise.columns.tolist()[1:]],
                    value=f"{day_wise.columns.tolist()[1:][0]}",
                    className="dcc_control",
                ),
            ],
            className="pretty_container",
            id="cross-filter-options2",
            style={'width': '75%', 'margin': 25, 'textAlign': 'center'}
        ),
        html.Div(
            [dcc.Graph(id="category_plot")],
            className="pretty_container",
        ),
        html.Div(
            [dcc.Graph(id="plot_daywise")],
            className="pretty_container",
        ),
        html.Div(
            [dcc.Graph(id="plot_daywise_line")],
            className="pretty_container",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
country_wise_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Covid-19 Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Project by Group #06", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.A(
                                    html.Button("Day-Wise", id="day-w"),
                                    href="/day_wise",
                                ),
                                html.A(
                                    html.Button("Country-Wise", id="country-w"),
                                    href="/country_wise",
                                ),
                                html.A(
                                    html.Button("World-Map", id="world-m"),
                                    href="/world_map",
                                ),
                                html.A(
                                    html.Button("World-report", id="world_r"),
                                    href="/world_report",
                                ),
                            ]
                        ),
                    ],
                    className="one-third column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("Select Country:", className="control_label"),
                        dcc.Dropdown(
                            id="country_name",

                            options=[{'label': i, 'value': i} for i in df['Country/Region'].tolist()],
                            value=f"{df['Country/Region'].tolist()[79]}",
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="confirmed_cases"), html.P("No. of Confirmed Cases")],
                                    id="confirmed",
                                    className="pretty_container three columns",
                                ),
                                html.Div(
                                    [html.H6(id="death_cases"), html.P("No. of Deaths")],
                                    id="death",
                                    className="pretty_container three columns",
                                ),
                                html.Div(
                                    [html.H6(id="recovered_cases"), html.P("Recovered cases")],
                                    id="recovered",
                                    className="pretty_container three columns",
                                ),
                                html.Div(
                                    [html.H6(id="active_cases"), html.P("Active cases")],
                                    id="active",
                                    className="pretty_container three columns",
                                ),
                            ],
                            id="info-container",
                            className="container-display",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.P("Select Cotegory:", className="control_label"),
                dcc.Dropdown(
                    id="category_country",

                    options=[{'label': i, 'value': i} for i in full_grouped.columns.tolist()[2:-1]],
                    value=f"{full_grouped.columns.tolist()[2:-1][0]}",
                    className="dcc_control",
                ),
            ],
            className="pretty_container",
            id="cross-filter-options2",
            style={'width': '75%', 'margin': 25, 'textAlign': 'center'}
        ),
        html.Div(
            [dcc.Graph(id="plot_daywise_country")],
            className="pretty_container"
        ),
        html.Div(
            [dcc.Graph(id="plot_daywise_line_country")],
            className="pretty_container",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
world_map_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Covid-19 Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Project by Group #06", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.A(
                                    html.Button("Day-Wise", id="day-w"),
                                    href="/day_wise",
                                ),
                                html.A(
                                    html.Button("Country-Wise", id="country-w"),
                                    href="/country_wise",
                                ),
                                html.A(
                                    html.Button("World-Map", id="world-m"),
                                    href="/world_map",
                                ),
                                html.A(
                                    html.Button("World-report", id="world_r"),
                                    href="/world_report",
                                ),
                            ]
                        ),
                    ],
                    className="one-third column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.P("Select Cotegory:", className="control_label"),
                dcc.Dropdown(
                    id="category_col",

                    options=[{'label': i, 'value': i} for i in df.columns.tolist()[1:-1]],
                    value=f"{df.columns.tolist()[1:-1][0]}",
                    className="dcc_control",
                ),
            ],
            className="pretty_container",
            id="cross-filter-options2",
            style={'width': '75%', 'margin': 25, 'textAlign': 'center'}
        ),
        html.Div(
            [dcc.Graph(id="plot_world_map")],
            className="pretty_container"
        ),
        html.Div(
            [dcc.Graph(id="world_map_slider")],
            className="pretty_container",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
world_report = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Covid-19 Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Project by Group #06", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.A(
                                    html.Button("Day-Wise", id="day-w"),
                                    href="/day_wise",
                                ),
                                html.A(
                                    html.Button("Country-Wise", id="country-w"),
                                    href="/country_wise",
                                ),
                                html.A(
                                    html.Button("World-Map", id="world-m"),
                                    href="/world_map",
                                ),
                                html.A(
                                    html.Button("World-report", id="world_r"),
                                    href="/world_report",
                                ),
                            ]
                        ),
                    ],
                    className="one-third column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.P("Select Cotegory:", className="control_label"),
                dcc.Dropdown(
                    id="category_report",

                    options=[{'label': i, 'value': i} for i in week_wise.columns.tolist()[1:]],
                    value=f"{week_wise.columns.tolist()[1:][0]}",
                    className="dcc_control",
                ),
            ],
            className="pretty_container",
            id="cross-filter-options2",
            style={'width': '75%', 'margin': 25, 'textAlign': 'center'}
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="plot_weekly_report")],
                    className="pretty_container six column"
                ),
                html.Div(
                    [dcc.Graph(id="plot_monthly_report")],
                    className="pretty_container six column",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
layout_index = html.Div([
    dcc.Link('Navigate to "/day_wise"', href='/day_wise'),
    html.Br(),
    dcc.Link('Navigate to "/country_wise"', href='/country_wise'),
    html.Br(),
    dcc.Link('Navigate to "/world_map"', href='/world_map'),
    html.Br(),
    dcc.Link('Navigate to "/world_report"', href='/world_report'),

])


# Selectors -> Confirmed Cases
@app.callback(
    Output("confirmed_cases", "children"),
    [
        Input("country_name", "value"),
    ],
)
def update_well_text(country_name):
    dff = df[df['Country/Region'] == f"{country_name}"]['Confirmed']
    return dff


# Selectors -> Death Cases
@app.callback(
    Output("death_cases", "children"),
    [
        Input("country_name", "value"),
    ],
)
def update_well_text(country_name):
    dff = df[df['Country/Region'] == f"{country_name}"]['Deaths']
    return dff


# Selectors -> Recovered Cases
@app.callback(
    Output("recovered_cases", "children"),
    [
        Input("country_name", "value"),
    ],
)
def update_well_text(country_name):
    dff = df[df['Country/Region'] == f"{country_name}"]['Recovered']
    return dff


# Selectors -> Active Cases
@app.callback(
    Output("active_cases", "children"),
    [
        Input("country_name", "value"),
    ],
)
def update_well_text(country_name):
    dff = df[df['Country/Region'] == f"{country_name}"]['Active']
    return dff


# day_wise data plot ->
@app.callback(
    Output("category_plot", "figure"),
    [
        Input("category", "value"),
    ],
)
def update_well_text(category):
    dff = plot_hbar(df, f'{category}', 15)
    return dff


# day_wise data plot ->
@app.callback(
    Output("plot_daywise", "figure"),
    [
        Input("category", "value"),
    ],
)
def update_well_text(category):
    dff = plot_daywise(f'{category}')
    return dff


# day_wise data plot ->
@app.callback(
    Output("plot_daywise_line", "figure"),
    [
        Input("category", "value"),
    ],
)
def update_well_text(category):
    dff = plot_daywise_line(f'{category}')
    return dff


# day_wise data plot ->
@app.callback(
    Output("plot_daywise_country", "figure"),
    [
        Input("category_country", "value"),
    ],
)
def update_well_text(category):
    dff = plot_stacked(f'{category}')
    return dff


# day_wise data plot ->
@app.callback(
    Output("plot_world_map", "figure"),
    [
        Input("category_col", "value"),
    ],
)
def update_well_text(category):
    dff = plot_map(f'{category}')
    return dff


# day_wise data plot ->
@app.callback(
    Output("world_map_slider", "figure"),
    [
        Input("category_col", "value"),
    ],
)
def update_well_text(category):
    fig = px.choropleth(full_grouped, locations="Country/Region",
                        color=np.log(full_grouped["Confirmed"]),
                        locationmode='country names', hover_name="Country/Region",
                        animation_frame=full_grouped["Date"].dt.strftime('%Y-%m-%d'),
                        title='Cases over time', color_continuous_scale=px.colors.sequential.matter)
    fig.update(layout_coloraxis_showscale=False)
    return fig


# day_wise data plot ->
@app.callback(
    Output("plot_daywise_line_country", "figure"),
    [
        Input("category_country", "value"),
    ],
)
def update_well_text(category):
    dff = plot_line(f'{category}')
    return dff


# day_wise data plot ->
@app.callback(
    Output("plot_weekly_report", "figure"),
    [
        Input("category_report", "value"),
    ],
)
def update_well_text(category):
    dff = plot_weekwise(f'{category}')
    return dff


@app.callback(
    Output("plot_monthly_report", "figure"),
    [
        Input("category_report", "value"),
    ],
)
def update_well_text(category):
    dff = plot_monthwise(f'{category}')
    return dff


app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    day_wise_layout,
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/day_wise":
        return day_wise_layout
    elif pathname == "/country_wise":
        return country_wise_layout
    elif pathname == "/world_map":
        return world_map_layout
    elif pathname == "/world_report":
        return world_report
    else:
        return day_wise_layout


if __name__ == '__main__':
    app.run_server(debug=False)
