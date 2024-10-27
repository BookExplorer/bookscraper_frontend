#TODO: Create test for just graph function.
import pandas as pd
import graphs
from plotly.graph_objs import Figure

COUNTS = [20, 15, 10, 8, 5, 3, 2]
COUNTRIES = [
                "United States",
                "United Kingdom",
                "France",
                "Germany",
                "Canada",
                "Australia",
                "Brazil",
            ]
COUNTRY_COUNTS = pd.DataFrame(
    {"country":COUNTRIES,
     "count": COUNTS}
)
def test_colorscale_regular():
    scale_max = max(COUNTS)
    colorscale = graphs.make_colorscale(scale_max=scale_max)
    grey = [0, "rgba(217, 217, 217, 1)"]
    maximum = [1, "#ff4500"]
    scale = [1/scale_max, "#ffeda0"]
    expected = [grey, scale, maximum] 
    assert expected == colorscale


def test_colorscale_zeros():
    scale_max = 0
    colorscale = graphs.make_colorscale(scale_max=scale_max)
    grey = [0, "rgba(217, 217, 217, 1)"]
    maximum = [1, "#ff4500"]
    scale = [1, "#ffeda0"]
    expected = [grey, scale, maximum] 
    assert expected == colorscale


def test_choropleth_regular():
    colorscale = graphs.make_colorscale(scale_max=max(COUNTS))
    choropleth = graphs.make_choropleth(colorscale, COUNTRY_COUNTS)
    assert all(choropleth.z == COUNTS)
    assert all(choropleth.locations == COUNTRIES)
    assert choropleth.locationmode == 'country names'


def test_choropleth_zeros():
    cc = pd.DataFrame(
       { "country": COUNTRIES,
        "count": [0] * len(COUNTRIES)}
    )
    colorscale = graphs.make_colorscale(scale_max=0)
    choropleth = graphs.make_choropleth(colorscale, cc)
    assert all(choropleth.z == [0] * len(COUNTRIES))
    assert all(choropleth.locations == COUNTRIES)
    assert choropleth.locationmode == 'country names'
    

def test_graphing_function():
    figure = graphs.generate_graph(COUNTRY_COUNTS)
    
    # Ensure the output is a Figure object
    assert isinstance(figure, Figure), "The output should be a Plotly Figure"
    
    # Extract the Choropleth trace
    choropleth = figure.data[0]
    
    # Validate Choropleth data
    expected_choropleth = graphs.make_choropleth(
        color_scale=graphs.make_colorscale(max(COUNTS)),
        complete_data=COUNTRY_COUNTS
    )
    
    # Compare essential attributes
    assert (choropleth.z == expected_choropleth.z).all(), "Z values should match"
    assert list(choropleth.locations) == list(expected_choropleth.locations), "Locations should match"
    assert choropleth.colorscale == expected_choropleth.colorscale, "Colorscales should match"
    assert choropleth.locationmode == expected_choropleth.locationmode, "Location modes should match"
    
    # Validate layout properties
    assert figure.layout.title.text == "Number of Authors by Country", "Title should be set correctly"
    assert figure.layout.geo.projection.type == "equirectangular", "Projection type should be 'equirectangular'"
    assert figure.layout.geo.showcoastlines is False, "Coastlines should not be shown"
    assert figure.layout.geo.showframe is False, "Frame should not be shown"
