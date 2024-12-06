import funcnodes as fn
import funcnodes_pandas as fnpd
import funcnodes_plotly as fnplotly
from .weatherapi import NODE_SHELF as WAPI_NODE_SHELF


NODE_SHELF = fn.Shelf(
    name="Weather",
    description="weather functionalities",
    nodes=[],
    subshelves=[WAPI_NODE_SHELF],
)
