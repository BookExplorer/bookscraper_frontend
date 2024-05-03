from dash import Dash, html, dcc, callback, Output, Input, State
import requests
import pandas as pd
from graphs import generate_graph
from plotly.graph_objs import Figure
import pdb

app = Dash(__name__)
application = app.server
app.layout = html.Div(
    [
        dcc.Input(
            id="profile-url-input",
            type="text",
            placeholder="Enter Goodreads profile URL",
        ),
        html.Button("Submit", id="submit-button", n_clicks=0),
        html.Div(id="message-output", style={"color": "red"}),
        dcc.Graph(
            id="visualization-output",
            style={"display": "none"},
        ),  # This will hide the graph in the start.
    ]
)


@callback(
    Output("visualization-output", "style"),
    Output("visualization-output", "figure"),
    Input("submit-button", "n_clicks"),
    State("profile-url-input", "value"),
)
def update_graph(n_clicks, profile_url: str):
    url = "http://app:8000/process-profile/"
    data = {"profile_url": profile_url}
    if n_clicks > 0 and profile_url:
        response = requests.post(url, json=data)
        if response.ok:
            country_count = response.json()["data"]
            print(country_count)
            df = pd.DataFrame(
                [
                    {"country": country, "count": count}
                    for country, count in country_count.items()
                ]
            )
            figure = generate_graph(df)
            # Logic to update the graph or process the input data
            return (
                {
                    "display": "block",
                    "height": "90vh",
                    "width": "90vw",
                },
                figure,
            )  # Return style that makes the graph visible
        else:
            return {"display": "none"}, Figure()
    return (
        {"display": "none"},
        Figure(),
    )  # Keeps the graph hidden


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
