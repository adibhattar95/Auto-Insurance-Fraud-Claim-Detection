#Import Libraries
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np


#Load Dataset
df = pd.read_csv('cat_columns.csv')

#Setup Dash server
app = dash.Dash(__name__)
server = app.server

#Take out features for plotting
features = df.drop(['fraud_reported', 'incident_location'], 1)
features_list = list(features)
target = df['fraud_reported']

#Set range for y_axis
range_y = list(np.arange(0, 1000, 50))

#Layout of HTML page
app.layout = html.Div([
    html.Div([dcc.Dropdown(id='feature-select', options=[{'label': i, 'value': i} for i in features_list],
                           value='witnesses', style={'width': '500px'})]),
    dcc.Graph('countplot-graph')])

#Figure to display on page
@app.callback(
    Output('countplot-graph', 'figure'),
    [Input('feature-select', 'value')]
)


#Function to make graphs for the categorical features
def update_graph(column):
    import plotly.graph_objects as go
    fig = go.Figure(data=[
        go.Bar(name = 'No', x = features[column], y = target.values == 'N',
               marker_color = 'darkgreen'),
        go.Bar(name = "Yes", x = features[column], y = target.values == 'Y',
               marker_color = 'crimson')])
    fig.update_layout(title = 'Distribution of Fraud Reported', xaxis_type = 'category',
                      xaxis_title = column,
                      font = dict(family = 'Courier New, monospace',
                                  size = 20,
                                  color = 'Black'))
    fig.update_yaxes(ticktext = range_y, tickvals = range_y)
    fig.update_xaxes(tickangle=315, tickfont=dict(family='Rockwell', color='blue', size=14))
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)



