#TODO: Create test for just graph function.
import pandas as pd
import graphs

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


def test_choropleth():
    colorscale = graphs.make_colorscale(scale_max=max(COUNTS))
    choropleth = graphs.make_choropleth(colorscale, COUNTRY_COUNTS)
    assert all(choropleth.z == COUNTS)
    assert all(choropleth.locations == COUNTRIES)
    assert choropleth.locationmode == 'country names'
    assert choropleth.colorscale == colorscale
    print(choropleth)

def test_graphing_function():
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
            "count":COUNTS ,
        }
    )
    figure = graphs.generate_graph(country_counts)
    print(figure)
