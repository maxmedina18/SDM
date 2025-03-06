import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

app = dash.Dash(__name__)
 
# Define system parameters (default values)
m = 300   # kg (quarter car mass)
k = 15000  # N/m (spring stiffness)
c = 1000   # Ns/m (damping coefficient)

def suspension_system(t, y, k, c, m):
    x, v = y  # Position & velocity
    F_road = np.sin(2 * np.pi * t) * 500  # Simulating a road bump
    dxdt = v
    dvdt = (F_road - c * v - k * x) / m
    return [dxdt, dvdt]

def solve_suspension(k, c):
    t_span = (0, 5)
    t_eval = np.linspace(0, 5, 500)
    y0 = [0, 0]
    sol = solve_ivp(suspension_system, t_span, y0, t_eval=t_eval, args=(k, c, m))
    return sol.t, sol.y[0]

# Layout for the UI
app.layout = html.Div([
    html.H1("Interactive Suspension Model"),
    dcc.Graph(id='suspension-graph'),
    html.Label("Spring Stiffness (k)"),
    dcc.Slider(
        id='k-slider',
        min=5000, max=30000, step=250,
        value=15000, marks={i: str(i) for i in range(5000, 30001, 5000)}
    ),
    html.Label("Damping Coefficient (c)"),
    dcc.Slider(
        id='c-slider',
        min=500, max=5000, step=50,
        value=1000, marks={i: str(i) for i in range(500, 5001, 1000)}
    )
])

@app.callback(
    Output('suspension-graph', 'figure'),
    [Input('k-slider', 'value'),
     Input('c-slider', 'value')]
)
def update_graph(k, c):
    t, x = solve_suspension(k, c)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=x, mode='lines', name='Displacement'))
    fig.update_layout(title='Suspension Response Over a Bump',
                      xaxis_title='Time (s)',
                      yaxis_title='Displacement (m)',
                      template='plotly_dark')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

