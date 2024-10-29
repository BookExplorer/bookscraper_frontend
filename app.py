from dash import Dash, html, dcc, callback, Output, Input, State
import requests
import pandas as pd
from graphs import generate_graph
from plotly.graph_objs import Figure
from logger import logger



# TODO: The message needs to disappear after you submit something, otherwise it's very confusing!
app = Dash(__name__)
application = app.server
app.layout = html.Div(
    [
        dcc.Input(
            id="profile-url-input",
            type="text",
            placeholder="Enter Goodreads profile URL",
            style={"width": "300px", "height": "40px", "fontSize": "18px"},
        ),
        html.Button(
            "Submit", 
            id="submit-button", 
            n_clicks=0, 
            style={"width": "120px", "height": "40px", "fontSize": "16px", "margin": "10px"},
        ),
        html.Div(id="message-output", style={"color": "red", "fontSize": "16px", "marginTop": "10px"}),
        dcc.Loading(
            id="loading",
            type="default",
            children=dcc.Graph(
                id="visualization-output",
                style={
                    "display": "none",
                    "width": "80%",
                    "height": "500px",
                    "marginTop": "20px",
                },
            ),
        ),
        dcc.Store(id="previous-input-store", data = "")
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center",
        "height": "100vh",
        "textAlign": "center",
    },
)


@callback(
    Output("message-output", "children"),
    Input("previous-input-store", "data"),
)
def display_message(msg: str):
    return msg


@callback(
    Output("visualization-output", "style"),
    Output("visualization-output", "figure"),
    Output("previous-input-store", "data"),
    Input("submit-button", "n_clicks"),
    State("profile-url-input", "value"),
)
def update_graph(n_clicks: int, profile_url: str):
    url = "http://app:8000/process-profile/"
    data = {"profile_url": profile_url}
    if n_clicks > 0 and profile_url:
        response = requests.post(url, json=data)
        logger.debug(f"Response status code was {response.status_code}")
        if response.ok:
            country_count = response.json()["data"]
            logger.debug(country_count)
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
                "",
            )  # Return style that makes the graph visible
        else:

            detail = response.json()["detail"]
            if isinstance(detail, str):
                message = detail
            elif isinstance(detail, list):
                message = detail[0]["msg"]
            return (
                {"display": "none"},
                Figure(),
                f"Status code: {response.status_code}, Error: {message}",
            )
    return ({"display": "none"}, Figure(), "")  # Keeps the graph hidden


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050, use_reloader=True)
