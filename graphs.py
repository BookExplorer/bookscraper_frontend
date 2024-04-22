import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objs import Figure, Choropleth


def generate_graph(complete_data: pd.DataFrame) -> Figure:

    # Custom colorscale
    custom_colorscale = [
        [0, "rgba(217, 217, 217, 1)"],  # grey for 0 count
        [1.0 / complete_data["count"].max(), "#ffeda0"],  # light orange for min count
        [1, "#ff4500"],  # dark orange for max count
    ]
    # Create a base map to show all country borders
    fig = Figure(
        data=Choropleth(
            locations=complete_data["country"],
            z=complete_data["count"],
            locationmode="country names",
            colorscale=custom_colorscale,
            marker_line_color="black",  # Lines between countries
            marker_line_width=0.5,
            colorbar_title="Number of Authors",
        )
    )
    fig.update_geos(
        projection_type="orthographic",
        showcountries=True,  # show country boundaries
    )
    # Update the layout to add the title and adjust geo settings
    fig.update_layout(
        title_text="Number of Authors by Country",
        coloraxis_colorbar=dict(
            title="Number of Authors",
            tickvals=[
                0,
                complete_data["count"].max(),
            ],  # ensures that 0 is labeled on the colorbar
            ticktext=["0", "Max"],
        ),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type="equirectangular",
            landcolor="rgba(217, 217, 217, 1)",  # Light grey land color
            lakecolor="rgba(127,205,255,1)",  # Light blue lake color
            oceancolor="rgba(127,205,255,0.5)",  # Slightly transparent ocean color
        ),
    )

    return fig


if __name__ == "__main__":
    # Sample data
    country_counts = pd.DataFrame(
        {
            "country": [
                "United States",
                "United Kingdom",
                "France",
                "Germany",
                "Canada",
                "Australia",
                "Brazil",
            ],
            "count": [20, 15, 10, 8, 5, 3, 2],
        }
    )

    generate_graph(country_counts).show()
