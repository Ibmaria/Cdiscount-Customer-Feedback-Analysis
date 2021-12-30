from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import config
import numpy as np
import plotly.express as px
import dash_table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df =pd.read_csv('data/df_preprocess.csv')
df=df.sort_values(by=['date'],ascending=False)[:15]
df=df[['author','sentiment','body']]

app6=DjangoDash('Recentsreviews', external_stylesheets=external_stylesheets)
app6.layout = html.Div([
    html.H3('Commentaires Recents',style={'textAlign': 'center'}),
    dash_table.DataTable(
    id='table',
    style_cell={'textAlign': 'left'},
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)])