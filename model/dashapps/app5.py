from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import config
import numpy as np
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df =pd.read_csv('data/df_preprocess.csv')
df1=df.copy()
fig1=px.pie(df, values='sentiment_value',names='sentiment', title='Distribution des Sentiments')
df_pos=df1[df1['sentiment_value']==1].groupby('month')['sentiment_value','sentiment'].sum()
df_neg=df1[df1['sentiment_value']==3].groupby('month')['sentiment_value','sentiment'].sum()
df_neu=df1[df1['sentiment_value']==2].groupby('month')['sentiment_value','sentiment'].sum()
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=list(df_pos.index), y=df_pos['sentiment_value'],mode='lines+markers',name='Positif',line=dict(color='rgb(0,245,153)', width=1)))
fig2.add_trace(go.Scatter(x=list(df_neg.index), y=df_neg['sentiment_value'],mode='lines+markers',name='Negatif',line=dict(color='rgb(255, 102, 102)', width=1)))
fig2.add_trace(go.Scatter(x=list(df_neu.index), y=df_neu['sentiment_value'],mode='lines+markers',name='Neutre',line=dict(color='rgb(102, 102, 255)', width=1)))
fig2.update_layout(autosize=False,title='Sentiments au cours des Mois',xaxis_title='Mois',yaxis_title='Sentiments')



app5=DjangoDash('Sentiments', external_stylesheets=external_stylesheets)
app5.css.append_css({ "external_url" : "/static/model/css/s5.css" })
app5.layout = html.Div([html.H3('Sentiments',style={'textAlign': 'center'}),
    html.Div([
        
                html.Div([

                    html.Div([
                        html.Label(id='title_bar'),
                        dcc.Graph(figure=fig1,config={'displayModeBar':False,}),

                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '40%'}),

                html.Div([
                    html.Div([
                        # html.Label(id='title_bar1'),
                        dcc.Graph(figure=fig2,config={'displayModeBar':False,}),

                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '60%'}),

            ], className='row'),
])

