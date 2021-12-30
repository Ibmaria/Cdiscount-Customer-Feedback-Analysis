from types import new_class
from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import pickle
import plotly.express as px

#import config
from wordcloud import WordCloud
from nltk.corpus import stopwords
from matplotlib import pyplot as plt
stop_words = list(stopwords.words('french'))+['ctre','tcdicount']
import numpy as np
tab_style = { "padding": "1.3vh","color": '#AEAEAE',"fontSize": '30px',"backgroundColor": 'fuchsia','border-bottom': '1px white solid',}
tab_selected_style = {"fontSize": '30px',"color": '#F4F4F4',"padding": "1.3vh",'fontWeight': 'bold',"backgroundColor": 'pink','border-top': '1px white solid','border-left': '1px white solid','border-right': '1px white solid','border-radius': '0px 0px 0px 0px',}

tabs_styles = {
    'height': '18px'
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app7=DjangoDash('WorlCloud', external_stylesheets=external_stylesheets)
a_file = open("data/data.pkl", "rb")
output = pickle.load(a_file)
pos=output['positive']
neg=output['negative']
all_postives= " ".join(p for p in pos)
all_negatives=" ".join(n for n in neg)

app7.layout = html.Div([
    html.H3('Worcloud',style={'textAlign': 'center'}),
    dcc.Tabs(id="tabs-example-graph", value='tab1', children=[
        dcc.Tab(label='Tendances Positives', value='tab1',style=tab_style,selected_style = tab_selected_style),
        dcc.Tab(label='Tendances Negatives', value='tab2',style=tab_style,selected_style = tab_selected_style),
       
    ]),
    html.Div(id='tabs-content-example-graph')
])
@app7.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab1':
        my_wordcloud = WordCloud(
        stopwords=stop_words,
        background_color='white',
        height=300).generate(all_postives)
        fig = px.imshow(my_wordcloud, template='ggplot2')
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        return html.Div([
            html.H4('Tendances Positives'),
            dcc.Graph(figure=fig, config={"displayModeBar":False}),
            html.Button('Resume', id='btn-nclicks-1', n_clicks=0),
            html.P( id='resumep')])
    else:
        my_wordcloud = WordCloud(
        stopwords=stop_words,
        background_color='white',
        height=275).generate(all_negatives)
        fig = px.imshow(my_wordcloud, template='ggplot2')
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        return html.Div([
            html.H4('Tendances Negatives'),
            dcc.Graph(figure=fig, config={"displayModeBar":False}),
            html.Button('Resume', id='btn-nclicks-2', n_clicks=0),
            html.P( id='resumen')
            ])
@app7.callback(Output('resumep', 'children'),
              Input('btn-nclicks-1', 'n_clicks'))
def render_n(n):
    if n>0:
        return "les clients ont l'air d'aimer le site car ils le trouvent ergonomique ,Les commandes sont au rdv.Ce qui leur pousse à recommander. "
@app7.callback(Output('resumen', 'children'),
              Input('btn-nclicks-2', 'n_clicks'))
def render_n(n):
    if n>0:
        return "les clients ont l'impression que les produits sont surtaxés, voire des contrefaçons.Les commandes ne sont au rdv.Ils croient se faire arnaquer par les vendeurs , comportement qu'ils trouvent honteux, ce qui leur pousse à désapprouver le site  voire se desinscrire. "

