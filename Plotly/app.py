from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('diamonds.csv')


app = Dash(__name__)

app.layout = html.Div([
    html.H1(className='superHeading', children='Fabrication of Diamonds'),
    html.Hr(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    html.H4('Select...'),
    dcc.Dropdown(['all', 'natural', 'lab'],'natural', id='controls-and-dropdown-item', className='dropdowns'),
    dcc.Graph(figure={}, id='controls-and-graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-dropdown-item', component_property='value')
)
def update_graph(col_chosen):
    clarity_order = ['SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']
    if not col_chosen == 'all':
        data = df[df['type'] == col_chosen]
    else:
        data = df
    heatmap_data = data.pivot_table(index='colour', columns='clarity', values='carat', aggfunc='mean')
    heatmap_data = heatmap_data[clarity_order]
    fig = px.imshow(heatmap_data, color_continuous_scale="mint", labels=dict(color="Pureness"))
    return fig

if __name__ == '__main__':
    app.run(debug=True)
