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
from dash.dependencies import Input, Output
from plotly import graph_objs as go
N = 100000


app = dash.Dash()
app.config['suppress_callback_exceptions']=True

#US_STATES_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'

#US_AG_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv'
data=pd.read_excel(open(r'data.xlsx','rb'),sheetname ='Master',encoding = 'unicode_escape')
datax=data.head(411)
datax.columns
datax['flat_cnt']=1
datax['Agreement_Value']=datax['Agreement Value']
datax['Sale_Area']=datax['Sale Area']
datax['AV_for_Brokerage']=datax['AV for Brokerage']
datax['Brokearge_Amt']=datax['Brokearge Amt']

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
    html.H2(children='''Projects Sales comparision''',style={'padding-left':'20px'}),       
            html.Div([df_to_table(new_data)], style={'text-align':'center','width': '50%','display': 'inline-block'}),
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
     html.Div([
    dcc.Graph(
        id='col4',
        figure={
            'data': [trace3],
            'layout':go.Layout(title='Brokerage Amount',legend=dict(x=-0.5,y=-0.9,font=dict(size=9)),width=380,height=300)  #, barmode='stack'
        })], style={'width': '20%','display':'inline-block'}),
     html.Div([
    dcc.Graph(
        id='col5',
        figure={
            'data': [trace4],
            'layout':go.Layout(title='Sale Area by Project',legend=dict(x=-0.5,y=-0.9,font=dict(size=9)),width=380,height=300)  #, barmode='stack'
        })], style={'width': '20%','display': 'inline-block'}),                 
], style={'backgroundColor':'white','width': '100%','display': 'inline-block'})
])
# Create a Dash layout
app.layout = html.Div([
    html.Div(
        html.H1('NBSD Intelligent Reporting',style={'textAlign':'center','color':'#7FDBFF'})
        ),
        dcc.Tabs(id='tabs', value='Tab1', children=[
        dcc.Tab(label='Sales Report', id='tab1',style={'textAlign':'center','fontWeight': 'bold','color':'#7FDBFF'},value='Tab1'),
        dcc.Tab(label='Projects Collation', id='tab2', value='Tab2',style={'textAlign':'center','fontWeight': 'bold','color':'#7FDBFF'}),
        dcc.Tab(label='Summary Report', id='tab3', value='Tab3',style={'textAlign':'center','fontWeight': 'bold','color':'#7FDBFF'}),
        dcc.Tab(label='Pivot Report', id='tab4', value='Tab4',style={'textAlign':'center','fontWeight': 'bold','color':'#7FDBFF'})
        ]),
        html.Div(id='tabs-content')

])
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'Tab1':
        
        return html.Div(
                [html.H2('Sales Report',style={'padding':'20px','color':'#7FDBFF'}),
            dcc.Dropdown(
                id="prgt",
                options=[{
                    'label': i,
                    'value': i
                } for i in projets],
                value='Parkwest',
                style={'width': '50%',
               'display': 'inline-block','padding-left':'10px'}
                ),
           html.Div(id='update')
               
             ])
    elif tab == 'Tab2':
        return a_x
    
    elif tab == 'Tab3':
        return html.Div([
            
            dcc.Dropdown(
                id="sumry",
                options=[{
                    'label': i,
                    'value': i
                } for i in projets],
                value='Parkwest',
                style={'width': '55%',
               'display': 'inline-block','padding-left':'25%','padding-top':'10px','position':'relative'}
                ),
           html.Div(id='update2')
    
        ])
    elif tab == 'Tab4':
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
    return [html.H2('Configuration Wise sales',style={'padding':'20px','color':'#7FDBFF'}),                                          
             dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': datax['Configuration'],
                        'y': datax['Agreement Value'],
                        'type': 'bar'
                    }]
                }
            ),
            html.H2('Tower Wise sales',style={'padding':'20px','color':'#7FDBFF'}),
            dcc.Graph(
                id='graph-10-tabs',
                figure={
                    'data': [{
                        'x': datax['Tower'],
                        'y': datax['Agreement Value'],
                        'type': 'bar'
                    }]
                }
            ),
            html.H2('Source Wise sales',style={'padding':'20px','color':'#7FDBFF'}),
            dcc.Graph(
                id='graph-11-tabs',
                figure={
                    'data': [{
                        'x': datax['Source'],
                        'y': datax['Agreement Value'],
                        'type': 'bar'
                    }]
                }
            ),
            html.H2('Tower Wise sales',style={'padding':'20px','color':'#7FDBFF'}),
            dcc.Graph(
                id='graph-12-tabs',
                figure={
                    'data': [{
                        'x': datax['CP Name'],
                        'y': datax['Agreement Value'],
                        'type': 'bar'
                    }]
                }
            )]
    

    
@app.callback(
  dash.dependencies.Output('update2', 'children'),
  [dash.dependencies.Input('sumry', 'value')])
def updatesumry(sumry):
    datax=new_data[new_data['Project']==sumry]
    datax.drop('Project', axis=1, inplace=True)
    return [html.Div([df_to_table2(datax)], style={'text-align':'center','width': '100%','display': 'inline-block','padding-left':'25%'}
            ),
    dcc.Graph(
                id='scatter',
                figure={
                    'data': [go.Scatter(
    y = np.random.randn(500),
    mode='markers',
    marker=dict(
        size=16,
        color = np.random.randn(500), #set color equal to a variable
        colorscale='Viridis',
        showscale=True
    ))],
    'layout': go.Layout(
            title ='Scatter Plot',
            xaxis={'title':'Value X '},
            yaxis={'title':'Value Y '}
            
                  
                  )
                }
            )            
                    
            
            ]
    
    





if __name__ == '__main__':
    app.run_server()
