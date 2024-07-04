# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import math
import numpy as np

def round_up(val):
    out = val
    while out >= 10:
        out /= 10
    out = math.ceil(out)
    while out < val:
        out *= 10
    return out        

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
min_payload = 0
max_payload = round_up(spacex_df['Payload Mass (kg)'].max())
marks = {pt:f"{int(pt) if float(pt).is_integer() else pt}" for pt in np.linspace(min_payload, max_payload, 21)}
options=[{'label': 'All Sites', 'value': 'ALL'}]
sites = spacex_df['Launch Site'].unique()
for site in sites:
    options.append({'label': site, 'value': site})

# Create a dash application
app = dash.Dash(__name__) 
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=options,
                                                value='ALL',
                                                placeholder="place holder here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload, max=max_payload, step=0.1,
                                                marks=marks,
                                                value=[min_payload, max_payload]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br()
                                ], style={'font-family': 'Segoe UI'})

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').count().reset_index()
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Success Rate')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class').count().reset_index()
        fig = px.pie(data, values='Launch Site', 
        names='class', 
        title='Success Rate')
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site,payload_range):
    payload_diff = payload_range[1]-payload_range[0]
    if entered_site == 'ALL':
        data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    else:
        data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1]) & (spacex_df['Launch Site'] == entered_site)]
    fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', range_x=[payload_range[0]-payload_diff*0.005, payload_range[1]+payload_diff*0.005], range_y=[-0.25, 1.25])
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# data = spacex_df[spacex_df['Payload Mass (kg)'] >= payload_range[0]] & spacex_df[spacex_df['Payload Mass (kg)'] <= payload_range[1]]