# Route Optimization

## Objective
#### This project aims to find the optimum, in terms of driving distance, route for a vechicle which collects specific cargo units from different load points in the city of Heraklion, Greece.


## Parameters
#### The vechicle has a limited cargo capacity of 50 units. Having a depot as start, it is called to collect cargo units through different load points. It is only allowed to load the whole (and not a portion) point's cargo, but there is the option of transfering of units from one point to another. So, they can be gathered in specific spots and be loaded in the vechicle after it has passed through all loading points. Regarding loading points, it must be noted that they do not only provide different units between each other, but also their own cargo changes chronically.  


## Given Data
#### A set of loading points' coordinates and their cargo units in two different days is given in `.xlsx` file.


## Python Code
#### Python code has been developed to find both the minimum number of routes and the minimum length of those and plot them in Herklion's map figure. The algorithm that was used to find the optimum routes is Dijkstra's Algorithm. The packages that have been used are enlisted below:


### 1. openrouteservice
#### `openrouteservice` library provides its users with an easy access to Openrouteservice routing data via its `APIs`. The user can obtain an `API Key` through a free registration in [Openrouteservice](https://openrouteservice.org/), when helpful directions of API's usage and posibilities can be found [here](https://openrouteservice-py.readthedocs.io/en/latest/). 

Installation using `pip`:
```
pip install openrouteservice
```
**Note:**
It is possible that if an amount of requests per period of time is exceeded, `openrouteservice` will raise a warning. For more information, consult openrouteservice-client [GitHub](https://github.com/GIScience/openrouteservice-py/blob/master/openrouteservice/client.py).


### 2. osmnx
#### `osmnx` package allows the analysis and processing of real-world networks and geospatial geometries through the usage of OpenStreetMap data. The full documentation of osmnx can be found [here](https://osmnx.readthedocs.io/en/stable/).

Installation using `pip`:
```
pip install osmnx
```


### 3. itertools
#### `itertools` package is a set of tools that provides useful iteration and algebra functions such as `count()` or `map()`. There is no need of manual installation as it comes pre-installed in `Python` environment. For more information about this package, see its documentation [here](https://docs.python.org/3/library/itertools.html).


### 4. netowrkx
#### The networkx library is related to the analysis and manipulation of complex networks attributes and characteristics. For more information, follow this [link](https://pypi.org/project/networkx/).

Installation using `pip`:
```
pip install networkx
```


### 5. folium
`folium` package provides its users with the posibility of manipulating and visualizing data with the utilization of `leaflet.js` library's mapping dynamics. For package's documentation, click [here](https://python-visualization.github.io/folium/#:~:text=folium%20makes%20it%20easy%20to,as%20markers%20on%20the%20map.).

Installation using  `pip`:
```
pip install folium
```


### 6. pandas
`pandas` is a useful and flexible open source tool that is related to data analysis and manipulation. For its documentation, follow this [link](https://pandas.pydata.org/docs/).

Installation using `pip`:
```
pip install pandas
```


### 7. numpy
`numpy` library is directed to provide numerical computing posibilities through `Python`. The documentation of `numpy' can be found in NumPy's official [website](https://numpy.org/doc/stable/).

Installation using `pip`:
```
pip install numpy
```


## Results
Optimum routes for both days are plotted in `html` files in **Maps** folder. Each day corresponds to 2 different routes:
- Original route, which represents the driving course of the vechicle from depot to loading points.
- Returning route, which occurs after the vechicle has gone through all loading points and starts transfering cargo units back to depot.

For instance, the original route of the first day is displayed in the image below. Each loading point is represented by a marker, in which each point's ID and position within the route (1st, 2nd, etc.) are shown.

| ![ alt text for screen readers](C:\Users\Panagiota Mylona\Pictures\Screenshots\MapScreenshot.png "Text to show on mouseover") |
| :--: |
| *1st Day's Original Route* |

| ![ alt text for screen readers](MapScreenshot2.png "Text to show on mouseover") |
| :--: |
| *1st Day's Returning Route* |
