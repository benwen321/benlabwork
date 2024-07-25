import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np

# Sample data for 3D scatter plot
np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)
z = np.random.randn(100)

# Initialize the thresholds array
thresholds = np.zeros(6, np.float32)

# Initial x value and color for the draggable plane
initial_x = 0
initial_color = '#8B4513'  # Initial color is brown

# Create the 3D scatter plot
scatter = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=5))


# Function to create a plane with a specific color
def create_plane(x_value, color):
    return go.Surface(
        z=[[min(z), min(z)], [max(z), max(z)]],
        y=[[min(y), max(y)], [min(y), max(y)]],
        x=[[x_value, x_value], [x_value, x_value]],
        opacity=0.5,
        surfacecolor=[[0, 0], [0, 0]],  # Set a uniform surfacecolor
        colorscale=[[0, color], [1, color]],  # Use the specified color
        showscale=False  # Hide the color scale
    )


# Create the initial figure
fig = go.Figure(data=[scatter, create_plane(initial_x, initial_color)])

# Set initial layout
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        zaxis=dict(range=[min(z), max(z)]),
        camera=dict(
            eye=dict(x=1.25, y=1.25, z=1.25)
        )
    )
)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(style={'height': '100vh', 'margin': '0', 'display': 'flex', 'flexDirection': 'column'}, children=[
    dcc.Graph(
        id='3d-plot',
        figure=fig,
        style={'height': '70vh', 'width': '100%'}
    ),
    html.Div([
        html.Div([
            html.Label('X-Axis Position:', style={'fontSize': '18px', 'marginRight': '10px'}),
            dcc.Slider(
                id='x-slider',
                min=min(x),
                max=max(x),
                step=0.1,
                value=initial_x,
                marks={i: {'label': str(i), 'style': {'fontSize': '14px'}} for i in
                       range(int(min(x)), int(max(x)) + 1)},
                tooltip={'placement': 'bottom', 'always_visible': True},
                updatemode='drag'
            ),
        ], style={'width': '80%', 'margin': '20px auto'}),
        html.Div([
            html.Button('Save Slider Value', id='save-button', n_clicks=0,
                        style={'fontSize': '16px', 'padding': '10px', 'marginRight': '10px'}),
            html.Div(id='saved-value', style={'fontSize': '16px', 'marginLeft': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '10px 0'}),
        html.Div([
            html.Button('Light Brown', id='light-brown-button', n_clicks=0,
                        style={'fontSize': '14px', 'padding': '8px', 'margin': '5px'}),
            html.Button('Dark Brown', id='dark-brown-button', n_clicks=0,
                        style={'fontSize': '14px', 'padding': '8px', 'margin': '5px'}),
            html.Button('Light Blue', id='light-blue-button', n_clicks=0,
                        style={'fontSize': '14px', 'padding': '8px', 'margin': '5px'}),
            html.Button('Dark Blue', id='dark-blue-button', n_clicks=0,
                        style={'fontSize': '14px', 'padding': '8px', 'margin': '5px'}),
            html.Button('Light Red', id='light-red-button', n_clicks=0,
                        style={'fontSize': '14px', 'padding': '8px', 'margin': '5px'}),
            html.Button('Dark Red', id='dark-red-button', n_clicks=0,
                        style={'fontSize': '14px', 'padding': '8px', 'margin': '5px'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}),
    ], style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center',
              'alignItems': 'center', 'backgroundColor': '#f0f0f0', 'padding': '20px'}),
    dcc.Store(id='plane-color', data=initial_color),  # Store for the plane color
    dcc.Store(id='thresholds', data=thresholds.tolist())  # Store for thresholds array
])


@app.callback(
    Output('3d-plot', 'figure'),
    Input('x-slider', 'value'),
    Input('3d-plot', 'relayoutData'),
    State('plane-color', 'data')
)
def update_figure(x_value, relayout_data, plane_color):
    # Create a new plane with the updated position and color
    new_plane = create_plane(x_value, plane_color)

    # Create the updated figure with the new plane
    updated_fig = go.Figure(data=[scatter, new_plane])

    # Preserve the camera position if available
    if relayout_data and 'scene.camera' in relayout_data:
        camera = relayout_data['scene.camera']
    else:
        camera = fig.layout.scene.camera

    # Update layout with preserved camera position
    updated_fig.update_layout(
        scene=dict(
            xaxis=dict(range=[min(x), max(x)]),
            yaxis=dict(range=[min(y), max(y)]),
            zaxis=dict(range=[min(z), max(z)]),
            camera=camera
        )
    )

    return updated_fig


@app.callback(
    Output('plane-color', 'data'),
    Input('light-brown-button', 'n_clicks'),
    Input('dark-brown-button', 'n_clicks'),
    Input('light-blue-button', 'n_clicks'),
    Input('dark-blue-button', 'n_clicks'),
    Input('light-red-button', 'n_clicks'),
    Input('dark-red-button', 'n_clicks'),
    prevent_initial_call=True
)
def update_color(light_brown, dark_brown, light_blue, dark_blue, light_red, dark_red):
    ctx = dash.callback_context

    if not ctx.triggered:
        return initial_color

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    colors = {
        'light-brown-button': '#D2B48C',  # Light brown
        'dark-brown-button': '#5C4033',  # Dark brown
        'light-blue-button': '#ADD8E6',  # Light blue
        'dark-blue-button': '#00008B',  # Dark blue
        'light-red-button': '#FFA07A',  # Light red
        'dark-red-button': '#8B0000'  # Dark red
    }

    return colors.get(button_id, initial_color)


@app.callback(
    Output('saved-value', 'children'),
    Input('save-button', 'n_clicks'),
    State('x-slider', 'value'),
    State('plane-color', 'data'),
    State('thresholds', 'data')
)
def save_slider_value(n_clicks, slider_value, plane_color, thresholds_data):
    if n_clicks > 0:
        # Load the thresholds array from the stored data
        thresholds = np.array(thresholds_data)

        # Determine the index based on the color
        color_indices = {
            '#D2B48C': 0,  # Light brown
            '#5C4033': 1,  # Dark brown
            '#ADD8E6': 2,  # Light blue
            '#00008B': 3,  # Dark blue
            '#FFA07A': 4,  # Light red
            '#8B0000': 5  # Dark red
        }

        # Get the index for the current plane color
        index = color_indices.get(plane_color, -1)

        if index != -1:
            # Update the thresholds array
            thresholds[index] = slider_value

            # Save the updated array back to the store
            return f'Saved Slider Value: {slider_value} at index {index}'

        return 'Invalid color selected.'

    return 'Click the button to save the slider value.'


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
