import pytest
import src.utils as utils
import pandas as pd
import matplotlib.pyplot as plt


@pytest.mark.filterwarnings()
def test_extract_keywords():
    # Test extract_keywords function
    word = "https://www.example.com"
    pattern = r'https?://(?:www\.)?([^/]+)'
    assert utils.extract_keywords(word, pattern) == "example.com"
    word = "https://www.example.co.uk"
    pattern = r'https?://(?:www\.)?([^/]+)'
    assert utils.extract_keywords(word, pattern) == "example.co.uk"
    word = "https://www.example.com/path"
    pattern = r'https?://(?:www\.)?([^/]+)'
    assert utils.extract_keywords(word, pattern) == "example.com"
    word = "not a url"
    pattern = r'https?://(?:www\.)?([^/]+)'
    assert utils.extract_keywords(word, pattern) is None
    
@pytest.mark.filterwarnings()
def test_barchart():
    # Test barchart function
    x_axis = [1, 2, 3]
    y_axis = [10, 20, 30]
    x_label = "X Axis"
    y_label = "Y Axis"
    title = "Bar Chart"
    figsize = (18, 6)
    orientation = "horizontal"
    utils.barchart(x_axis, y_axis, x_label, y_label, title, figsize, orientation)
    # Check if the plot is created successfully
    assert plt.gca().has_data()
    
@pytest.mark.filterwarnings()
def test_barchart_with_grouping():
    # Test barchart_with_grouping function
    df = pd.DataFrame({"A": [1, 2, 3, 1, 2, 3], "B": [10, 20, 30, 40, 50, 60]})
    x_axis = "A"
    y_axis = "B"
    title = "Bar Chart with Grouping"
    x_label = "X Axis"
    y_label = "Y Axis"
    top = 2
    ascending = True
    grouping = ""
    figsize = (18, 6)
    orientation = "horizontal"
    utils.barchart_with_grouping(df, x_axis, y_axis, title, x_label, y_label,orientation, top, ascending, grouping, figsize, )
    # Check if the plot is created successfully
    assert plt.gca().has_data()