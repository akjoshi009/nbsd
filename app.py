# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 20:18:43 2019

@author: HP
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

import pandas as pd

import numpy as np

import dash

import dash_html_components as html

import dash_core_components as dcc
import dash_bootstrap_components as dbc


from dash.dependencies import Input, Output

from plotly import graph_objs as go

N = 100





app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True



server = app.server



#US_STATES_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'



#US_AG_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv'

c= ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]
data=pd.read_excel(open(r'data.xlsx','rb'),sheetname ='Master',encoding = 'unicode_escape')
datax=data.head(411)
datax.columns
datax['flat_cnt']=1
datax['Agreement_Value']=datax['Agreement Value']
datax['Sale_Area']=datax['Sale Area']
datax['AV_for_Brokerage']=datax['AV for Brokerage']
datax['Brokearge_Amt']=datax['Brokearge Amt']

random_x = np.random.randn(N)
random_y = np.random.randn(N)

projets=datax.Project.unique()
def loaddata(text):
    d_work=datax[data['Project']==text]
    return d_work


data_park=loaddata('Parkwest')
data_vici=loaddata('Vicinia')
data_mumbai=loaddata('Mumbai Dreams')
data_sp=loaddata('SP Residency')

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

grp_by_prj= datax.groupby(['Project'])[['flat_cnt','Sale_Area','Agreement_Value','AV_for_Brokerage','Brokearge_Amt']].sum()

grp_by_prj.Sale_Area=grp_by_prj.Sale_Area.apply(lambda x: round(x/1000000,2))
grp_by_prj.Agreement_Value=grp_by_prj.Agreement_Value.apply(lambda x: round(x/10000000,2))
grp_by_prj.AV_for_Brokerage=grp_by_prj.AV_for_Brokerage.apply(lambda x: round(x/10000000,2))
grp_by_prj.Brokearge_Amt=grp_by_prj.Brokearge_Amt.apply(lambda x: round(x/10000000,2))

grp_by_prj=grp_by_prj.reset_index()


grp_by_src= datax.groupby(['Source','Project'])[['flat_cnt','Sale_Area','Agreement_Value','AV_for_Brokerage','Brokearge_Amt']].sum()

labels = list(grp_by_prj.Project)
values =list(grp_by_prj.flat_cnt)
trace = go.Pie(labels=labels, values=values)

labels_av = list(grp_by_prj.Project)
values_av =list(grp_by_prj.Agreement_Value)
trace1 = go.Pie(labels=labels_av,values=values_av)


labels_avb = list(grp_by_prj.Project)
values_avb =list(grp_by_prj.AV_for_Brokerage)
trace2 = go.Pie(labels=labels_avb, values=values_avb)

labels_ava = list(grp_by_prj.Project)
values_ava =list(grp_by_prj.Brokearge_Amt)
trace3 = go.Pie(labels=labels_ava, values=values_ava)

labels_sa = list(grp_by_prj.Project)
values_sa =list(grp_by_prj.Sale_Area)
trace4 = go.Pie(labels=labels_sa, values=values_sa)
new_data = grp_by_prj.rename(columns = {"flat_cnt": "Apartment Count", 
                              "Sale_Area":"Sale Area", 
                              "Agreement_Value":"Agreement Value",
                              "AV_for_Brokerage": "AV for Brokerage",
                             "Brokearge_Amt": "Brokerage Amount" }) 


def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        
        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ])
def df_to_table2(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col,style={'padding':'10px'}) for col in df.columns])] +
        
        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col],style={'font-size':'50px','font-family': "Bookman",'font-weight': 'bold','padding':'10px'})
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ])            
    
a_x = html.Div(children=[
    html.H2(children='''Projects Sales Comparision''',style={'margin':'25px'}),
       dbc.Card(
            [
                
                dbc.CardBody(
                    [
                          html.Div([df_to_table(new_data)], style={'text-align':'center','width': '50%','display': 'inline-block'}),

                    ]
                ),
            ],color="dark",inverse=True,style={'margin':'2%'}
        ),
  dbc.Card(
            [
                
                dbc.CardBody(
                    [
                        html.Div([ 
      html.Div([
    dcc.Graph(
        id='col1',
        figure={
            'data': [trace,],
            'layout':go.Layout(title='Units Sold',legend=dict(x=-0.3,y=-0.9,font=dict(size=9)),width=400,height=300)  #, barmode='stack'
        })], style={'width': '20%','display': 'inline-block'}),
      html.Div([
    dcc.Graph(
        id='col2',
        figure={
            'data': [trace1],
            'layout':go.Layout(title='Agreement Value',legend=dict(x=-0.3,y=-0.9,font=dict(size=9)),width=400,height=300) #, barmode='stack'
        })
    ], style={'width': '20%','display': 'inline-block'}),
 html.Div([
    dcc.Graph(  
        id='col3',
        figure={
            'data': [trace2],
            'layout':go.Layout(title='AV for Brokerage',legend=dict(x=-0.3,y=-0.9,font=dict(size=9)),width=400,height=300)  #, barmode='stack'
        })], style={'width': '20%','display': 'inline-block'}),
     
                    
], style={'backgroundColor':'white','width': '100%','display': 'inline-block'})  ,

                    ]
                ),
            ],style={'margin':'2%'}
        )              
  
])
# Create a Dash layout
app.layout = html.Div([
    html.Div(
        html.H1('NBSD Intelligent Reporting',style={'textAlign':'center','color':'#7FDBFF','margin':'2%'})
        ),
        dbc.Tabs([
        dbc.Tab(label='Sales Report', tab_id='tab1'),
        dbc.Tab(label='Projects Collation', tab_id='tab2'),
        dbc.Tab(label='Summary Report', tab_id='tab3'),
        dbc.Tab(label='Pivot Report', tab_id='tab4'),
        ],id='tabs', active_tab='tab1'),
        html.Div(id='tabs-content')

])
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'active_tab')])
def render_content(tab):
    if tab == 'tab1':
        
        return html.Div(
                [html.H2('Sales Report',style={'margin':'1.8%','color':'#7FDBFF'}),
            dcc.Dropdown(
                id="prgt",
                options=[{
                    'label': i,
                    'value': i
                } for i in projets],
                value='Parkwest',
                style={'width': '50%',
               'display': 'inline-block','padding-left':'1.8%'}
                ),
           html.Div(id='update')
               
             ])
    elif tab == 'tab2':
        return a_x
    
    elif tab == 'tab3':
        return html.Div([
            dcc.Dropdown(
                id="sumry",
                options=[{
                    'label': i,
                    'value': i
                } for i in projets],
                value='Parkwest',
                style={'width': '50%','display': 'inline-block','margin-left':'1.6%','margin-top':'10px'}
                ),
    dbc.Card(
            [
                
                dbc.CardBody(
                    [
                         html.Div(id='update2')
                    ]
                ),
            ],style={'margin':'2%'}
        )       
   
    
        ])
    elif tab == 'tab4':
        return html.Div([
            html.H3('Configuration Wise sales',style={'padding':'20px','font-weight': 'bold','color':'#7FDBFF'}),
            dcc.Graph(
                id='graph-3-tabs',
                figure={
                    'data': [{
                        'x': data_sp['Configuration'],
                        'y': data_sp['Agreement Value'],
                        'type': 'bar'
                    }]
                }
            ),
           html.H3('Next Graph Dreams')
    
        ])
    

    

@app.callback(
  dash.dependencies.Output('update', 'children'),
  [dash.dependencies.Input('prgt', 'value')])

def updategraphs(prgt):
    datax=data[data['Project']==prgt]
    return [ 
            dbc.Card(
            [
                
                dbc.CardBody(
                    [
                         dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': datax['Configuration'],
                        'y': datax['Agreement Value'],
                        'type': 'bar'
                       
                    }],
                  'layout': {
                'title': 'Configuration Wise Sales'
            }
                }
            )
                    ]
                ),
            ],style={'margin':'2%','width':'44%','display': 'inline-block'}
        ),
    dbc.Card(
            [
                
                dbc.CardBody(
                    [
                         dcc.Graph(
                id='graph-10-tabs',
                figure={
                    'data': [
                            go.Scattergl(
                                    x = datax['Tower'],
                                    y = datax['Agreement Value'],
                                    mode = 'markers',
                                    marker = dict(
        color = '#FFBAD2',
        line = dict(width = 1)
    )
                                    )],
                'layout':go.Layout(title='Tower Wise Sale',legend=dict(x=-0.3,y=-0.9,font=dict(size=9))),
                }
                
            )
                    ]
                ),
            ],style={'margin':'2%','width':'44%','display': 'inline-block'}
        )
    ,
         dbc.Card(
            [
                
                dbc.CardBody(
                    [
                         dcc.Graph(
                id='graph-11-tabs',
                figure={
                    'data': [
                            go.Scatter(
                                    x = datax['Source'],
                                    y = datax['Agreement Value'],
                                    mode = 'markers',
                                    marker = dict(color = '#FFBAD2',line = dict(width = 1))
    )],
                                'layout': {
                                'title': 'Source Wise Sales'
                                    }
    
                }
            )
                    ]
                ),
            ],style={'margin':'2%','width':'44%','display': 'inline-block'}
        ),
           dbc.Card(
            [
                
                dbc.CardBody(
                    [
                      dcc.Graph(
                id='graph-12-tabs',
                figure={
                    'data': [{
                        'x': datax['Source'],
                        'y': datax['Agreement Value'],
                        'type': 'bar'
                    }],
                'layout': {
                'title': 'Configuration Wise Sales'
                }
                }
            )   
                    ]
                ),
            ],style={'margin':'2%','width':'44%','display': 'inline-block'}
        )
            ]
    

    
@app.callback(
  dash.dependencies.Output('update2', 'children'),
  [dash.dependencies.Input('sumry', 'value')])
def updatesumry(sumry):
    datax=new_data[new_data['Project']==sumry]
    datax.drop('Project', axis=1, inplace=True)
    
    return [
            
            dbc.Card(
            [
                
                dbc.CardBody(
                    [
                         html.Div([df_to_table2(datax)], style={'text-align':'center','width': '100%','display': 'inline-block','padding-left':'25%'}),

                    ]
                ),
            ],color="dark",inverse=True,style={'margin':'2%'}
        ), dbc.Card(
            [
                
                dbc.CardBody(
                    [
                         html.Div([
    dcc.Graph(
        id='col1',
        figure={
            'data': [trace,],
            'layout':go.Layout(title='Units Sold',legend=dict(x=-0.3,y=-0.9,font=dict(size=9)),width=600,height=400)  #, barmode='stack'
        })], style={'width': '40%'})
                    ]
                ),
            ],style={'margin':'2%','display': 'inline-block'}
        ),
     html.Div([
            dcc.Graph(
                id='graph-12-tabs',
                figure={
                    'data': [{
                        'x': data['Source'],
                        'y': data['Agreement Value'],
                        'type': 'bar'
                        }],
                     'layout': {
                'title': 'Dash Data Visualization'
            }
                }
            )],style={'width': '40%','display': 'inline-block'}),
    dbc.Card(
            [
                
                dbc.CardBody(
                    [
                         html.Div([
    dcc.Graph(
        id='colx1',
        figure={
            'data': [
                    go.Scatter(
                            x = random_x,
                            y = random_y,
                            mode = 'markers',
                            marker=dict(
        size=16,
        color = np.random.randn(100), #set color equal to a variable
        colorscale='Viridis',
        showscale=True
    )
                            )],
            'layout':go.Layout(title='Units Sold',legend=dict(x=-0.3,y=-0.9,font=dict(size=9)),width=600,height=400)  #, barmode='stack'
        })], style={'width': '40%'})
                    ]
                ),
            ],style={'margin':'2%','display': 'inline-block'}
        ),
   
    html.Div([
            dcc.Graph(
                id='graph-13-tabs',
                figure={
                    'data': [{
                        'x': data['Configuration'],
                        'y': data['Agreement Value'],
                        'type': 'bar'
                        }],
                     'layout': {
                'title': 'Dash Data Visualization'
            }
                }
            )],style={'width': '40%','display': 'inline-block'})

   ]
    
    
  

if __name__ == '__main__':

    app.run_server(debug=True)
