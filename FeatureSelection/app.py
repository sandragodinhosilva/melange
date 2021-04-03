# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# --------------------------------------------------------------------
# IMPORTS
import plotly.express as px
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# --------------------------------------------------------------------
# STLESHEET
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# --------------------------------------------------------------------
# DATA
auc_df = pd.read_csv("Evaluation_dfs/auc_df.csv")
mcc_df= pd.read_csv("Evaluation_dfs/mcc_df.csv")
precision_df= pd.read_csv("Evaluation_dfs/precision_df.csv")
recall_df= pd.read_csv("Evaluation_dfs/recall_df.csv")
f1_df= pd.read_csv("Evaluation_dfs/f1_df.csv")




auc = px.box(pd.melt(auc_df.transpose()), x="variable", y="value", 
            color="variable",
            title="Box plot of AUC",
            labels={"value": "AUC",
                     "variable": "Model"})

mcc = px.box(pd.melt(mcc_df.transpose()), x="variable", y="value", 
            color="variable",
            title="Box plot of MMC",
            labels={"value": "MMC",
                     "variable": "Model"})

precision = px.box(pd.melt(precision_df.transpose()), x="variable", y="value", 
            color="variable",
            title="Box plot of Precision measure",
            labels={"value": "Precision",
                     "variable": "Model"})

recall = px.box(pd.melt(recall_df.transpose()), x="variable", y="value", 
             color="variable",
             title="Box plot of Recall measure",
             labels={"value": "Recall",
                     "variable": "Model"})
    
f1 = px.box(pd.melt(f1_df.transpose()), x="variable", y="value", 
             color="variable",
             title="Box plot of F1",
             labels={"value": "F1",
                     "variable": "Model"})

# --------------------------------------------------------------------
# APP LAYOUT
app.layout = html.Div(children=[
    html.H1(children='Model evaluation'),

    dcc.Dropdown(id="selectCV",
                 options=[
                     {"label": "Run_0_CV_0", "value": "Run_0_CV_0"},
                     {"label": "Run_0_CV_1", "value": "Run_0_CV_1"},
                     {"label": "Run_0_CV_2", "value": "Run_0_CV_2"}],
                 multi=False,
                 value="Run_0_CV_0"
                 ),
    
    html.Div(id="output_container", children=[]),
    html.Br(), # makes space
    
    dcc.Graph(
        id='auc-graph',
        figure={})
])

# --------------------------------------------------------------------
# APP LAYOUT
@app.callback(
    [ Output(component_id="output_container", component_property="children"),
    Output(component_id='auc-graph', component_property='figure')],
    [Input(component_id='selectCV', component_property='value')])

def update_graph(option_selctd):
    print(option_selctd)
    print(type(option_selctd))
    
    container="The run chosen was: {}".format(option_selctd)
    
    df = recall_df.T.reset_index()
    df = df[df["index"]== option_selctd]
    
    fig = px.line(df)
    
    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)

