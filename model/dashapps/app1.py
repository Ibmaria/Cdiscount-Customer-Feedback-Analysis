from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import config
import numpy as np

##css load
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app1=DjangoDash('Entete', external_stylesheets=external_stylesheets)
##append css
app1.css.append_css({ "external_url" : "/static/model/css/s1.css" })
df =pd.read_csv('data/cdiscount_reviews.csv')
number_of_review= df.shape[0]
average_rating= df.rating.mean()
column=['Unnamed: 0']
df = df.drop(column, axis=1)
df['detracteurs'] = np.where(df['rating'] < 4, 1, 0)
df['passifs'] = np.where(df['rating'] == 4, 1, 0)
df['promoteurs'] = np.where(df['rating'] == 5, 1, 0)
detracteurs=int(df.detracteurs[df['detracteurs']==1].count())
passifs=int(df.passifs[df['passifs']==1].count())
promoteurs=int(df.promoteurs[df['promoteurs']==1].count())
nps_score=((promoteurs * 100) / number_of_review) - ((detracteurs * 100) / number_of_review)

#####Layout
app1.layout=html.Div((

    html.Div(
        html.Div([
                    html.P('Total reviews', className='text-primary-p1', style={'textAlign': 'center'}),
                    html.Span('{0:,.0f}'.format(number_of_review), className='font-bold text-title',
                              style={'textAlign': 'center', 'margin-top': '-15px'}),

                ], className="card_inner"),className="create_container two columns"),

    html.Div(
         html.Div([
                    html.P('Average Rating', className='text-primary-p1', style={'textAlign': 'center'}),
                    html.Span('{0:,.0f}'.format(average_rating), className='font-bold text-title',
                              style={'textAlign': 'center', 'margin-top': '-15px'}),

                ], className="card_inner"),className="create_container two columns"),

    html.Div(
         html.Div([
                    html.P('NPS', className='text-primary-p1', style={'textAlign': 'center'}),
                    html.Span('{0:,.0f}'.format(nps_score), className='font-bold text-title',
                              style={'textAlign': 'center'}),

                ], className="card_inner"),className="create_container two columns"),
        html.Div(
         html.Div([
                    html.P('Promoteurs', className='text-primary-p1', style={'textAlign': 'center'}),
                    html.Span('{0:,.0f}'.format(promoteurs), className='font-bold text-title',
                              style={'textAlign': 'center'}),

                ], className="card_inner"),className="create_container two columns"),
        html.Div(
         html.Div([
                    html.P('Passifs', className='text-primary-p1', style={'textAlign': 'center'}),
                    html.Span('{0:,.0f}'.format(passifs), className='font-bold text-title',
                              style={'textAlign': 'center'}),

                ], className="card_inner"),className="create_container two columns"),
    



     html.Div(
         html.Div([
                    html.P('Detracteurs', className='text-primary-p1', style={'textAlign': 'center'}),
                    html.Span('{0:,.0f}'.format(detracteurs), className='font-bold text-title',
                              style={'textAlign': 'center'}),

                ], className="card_inner"),className="create_container two columns")),
                className="row flex-display")













