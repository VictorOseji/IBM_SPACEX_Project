import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Assuming `spacex_df` is your DataFrame and it has a column 'Launch Site' that contains the launch site names.
# Assuming `app.layout` is where you set up your Dash layout, integrate the dropdown
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard'),

    html.Label('Select Launch Site:'),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    html.Label('Select Payload Range (Kg):'),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min(spacex_df['Payload Mass (kg)']), max(spacex_df['Payload Mass (kg)'])], # Use min and max from the dataframe
        marks={i: f'{i} Kg' for i in range(0, 10001, 1000)}
    ),
    html.Br(),
    html.Br(),

    #dcc.Graph(id='success-pie-chart'),
    #dcc.Graph(id='success-payload-scatter-chart')
    html.Div([
    html.Div(id = "output-container", 
             className = 'chart-grid', 
             children = [html.Div(children = dcc.Graph(id = 'success-pie-chart')), html.Div(children = dcc.Graph(id = 'success-payload-scatter-chart'))], 
             style = {'display':'flex'}),])

])

# Assuming 'app.layout' is already set with the dropdown component from Task 1
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(site_selected):
    if site_selected == 'ALL':
        filtered_df = spacex_df
        title = 'Total Success Launches for All Sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_selected]
        title = f'Total Success Launches for {site_selected}'
    
    pie_chart = px.pie(
        filtered_df,
        names='class',
        title=title
    )
    return pie_chart

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(site_selected, payload_range):
    if site_selected == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_selected]
        
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    scatter_plot = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Payload vs. Outcome Scatter Plot for {site_selected}'
    )
    return scatter_plot

if __name__ == '__main__':
    app.run_server(debug=True)