from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import config
import numpy as np
tab_style = { "padding": "1.3vh","color": '#AEAEAE',"fontSize": '30px',"backgroundColor": 'fuchsia','border-bottom': '1px white solid',}
tab_selected_style = {"fontSize": '30px',"color": '#F4F4F4',"padding": "1.3vh",'fontWeight': 'bold',"backgroundColor": 'pink','border-top': '1px white solid','border-left': '1px white solid','border-right': '1px white solid','border-radius': '0px 0px 0px 0px',}

tabs_styles = {
    'height': '18px'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df1 =pd.read_csv('data/fre_bigram_detracteur.csv')
df2=pd.read_csv('data/fre_trigrams_detracteur.csv')
df3=pd.read_csv('data/fre_unigrams_detracteur.csv')
app4=DjangoDash('Detracteur', external_stylesheets=external_stylesheets)
app4.css.append_css({ "external_url" : "/static/model/css/s2.css" })
app4.layout = html.Div([
    html.H3('Detracteurs',style={'textAlign': 'center'}),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Unigrams', value='tab3',style=tab_style,selected_style = tab_selected_style),
        dcc.Tab(label='Bigrams', value='tab-1-example-graph',style=tab_style,selected_style = tab_selected_style),
        dcc.Tab(label='Trigrams', value='tab-2-example-graph',style=tab_style,selected_style = tab_selected_style),
        
    ]),
    html.Div(id='tabs-content-example-graph')
])

@app4.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.H4('Bigram'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': df1.bigrams,
                        'y': df1.frequence,
                        'type': 'bar'
                    }],
                     "layout": go.Layout(
                    title = "Detracteurs",
                    xaxis = dict(title = "Bigram"),
                    yaxis = dict(title = "Frequence")
                    )
                }
            )
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H4('Trigram'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': df2.trigrams,
                        'y': df2.frequence,
                        'type': 'bar'
                    }],
                     "layout": go.Layout(
                    title = "Detracteurs",
                    xaxis = dict(title = "Trigram"),
                    yaxis = dict(title = "Frequence")
                    )
                    
                
                }
            )
        ])
    elif tab == 'tab3':
        return html.Div([html.H4('Unigram'),dcc.Graph(id='graph-2-tabs',figure={
                    'data': [{
                        'x': df3.unigrams,
                        'y': df3.Detracteur,
                        'type': 'bar'
                    }],
                     "layout": go.Layout(
                    title = "Detracteurs",
                    xaxis = dict(title = "Unigram"),
                    yaxis = dict(title = "Frequence")
                    )
                    
                
                }
            )
        ])
