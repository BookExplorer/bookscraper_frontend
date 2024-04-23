from dash import Dash, html, dcc, callback, Output, Input, State
import requests

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Input(
            id="profile-url-input",
            type="text",
            placeholder="Enter Goodreads profile URL",
        ),
        html.Button("Submit", id="submit-button", n_clicks=0),
        dcc.Graph(
            id="visualization-output", style={"display": "none"}
        ),  # This will hide the graph in the start.
    ]
)


@callback(Output("visualization-output", "style"), Input("submit-button", "n_clicks"))
def update_test(n_clicks):
    if n_clicks > 0:
        # Logic to update the graph or process the input data
        return {"display": "block"}  # Return style that makes the graph visible
    else:
        return {"display": "none"}  # Keeps the graph hidden


if __name__ == "__main__":
    app.run(debug=True)
