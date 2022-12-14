######### IMPORTING PACKAGES ###########
from openrouteservice.directions import directions
from openrouteservice import convert
import openrouteservice
import networkx as nx
import pandas as pd
import numpy as np
import osmnx as ox
import itertools
import folium
########################################



############# FUNCTIONS ################
# Function that removes NaN-valued items from list.
def removeNaN(List):
    
    New_list = []

    for item in list:
        if str(item) != 'nan':
            New_list.append(item)

    return(New_list) 


# Function that finds cargo points given load point's ID.
def FindCargoUnits(CargoUnits, IDs):
    
    res = []
    for i in range(len(IDs)):
        res.append(CargoUnits[IDs[i]-1])

    return res


# Function that finds all possible routes for the maximum cargo availability.
def FindRoutes(IDs, CargoUnits):

    # Target is the maximum acceptable cargo load.
    # In the case where the sum of a route's cargo load can't occur from any combination,
    # the 'Target' variable decreases until a cargo load can be collected from a route.

    Target = 50
    while Target > 0:
        # Here, all the possible routes that correspond to an overal 'Target' load are calculated.
        Routes = [list(seq) for i in range(len(IDs), 0, -1)
                    for seq in itertools.combinations(IDs,i)
                    if sum(FindCargoUnits(CargoUnits, seq)) == Target]

        # If routes have been found for a given overal cargo load, the loop breeaks
        # and the function returns these routes.
        if len(Routes) != 0:
            break
        Target -= 1
    
    return Routes


# Function that finds the shortest path.
def FindShortestPath(Distances, Routes, RemainRoutes, TotalRoutes):

    # In MinRoute the shortest in terms of length original route will be eventually stored.
    # Respctively, is used for the storation of shortest returning route. 
    MinRoute = []
    MinRetRoute = []
    # TempRoute will be used as a list in which routes will be stored to be examined.
    TempRoute = []
    # RouteLength corresponds to the calculated distance of a route. It is initialized as 0.
    RouteLength = 0
    # InitialLength is a variable used for the initialization of MinRouteLength and MinPathLength.
    InitialLength = 10000.0
    # MinRouteLength is used for the storation of shortest route's length.
    MinRouteLength = InitialLength

    # The iteration of all routes included in 'Routes' list begins.
    for Route in Routes:

        # Each route is copied to the temporary variable RouteCpy,
        # so the initial set of routes stays unnafected.
        RouteCpy = Route.copy()

        # In the case of the very first route calculated, depot (with a hypothetical ID = 16) is set as route's start.
        if RemainRoutes == TotalRoutes: 
            Start = 16
        else:
            # In any other case, as start is set the last node of the previous route.
            Start = RouteCpy[len(RouteCpy)-1]
            # This node is also removed from 'RouteCpy' becasue its position in the path has been determined.
            RouteCpy.remove(Start)
        
        # For the same reason, it is added in 'TempRoute' list.
        TempRoute.append(Start)

        # Every time a node's position in path is found, it is removed from 'RouteCpy'
        # and it is added in 'TempRoute'. So, if 'RouteCpy' is empty, the shortest path
        # for a given rset of nodes has been found.
        while len(RouteCpy) != 0:
            # In MinPathLength, the length of shortest path is stored.
            MinPathLength = InitialLength
            # Here, the next node is found in every step. The criteria that must fulfills
            # is having the shortest distance with the previously found node.
            for i in range(len(RouteCpy)):
                # Distances is a 2D array which has stored all the driving distances between nodes.
                if Distances[Start-1][RouteCpy[i]-1] < MinPathLength:
                    # If a distance between nodes is shorter than the so far minimum distance found,
                    # it is set as the new minimum distance. 
                    MinPathLength = Distances[Start-1][RouteCpy[i]-1]
                    # The second node of the shortest path, is saved as possible next node ('End'stands
                    # for path's end).
                    End = RouteCpy[i]

            # After the next node has been found, the distance between it and the previous node is added
            # in route's overall length.
            RouteLength += float(Distances[Start-1][End-1])
            # It is also appended in 'TempRoute',
            TempRoute.append(End)
            # and removed from 'RouteCpy' as it wasmentioned before.
            RouteCpy.remove(End)
            # Finally, most recent path's end-node becomes the start-node for the next path etc.
            Start = End
        
        # After the shortest versions for all routes have been found,
        # the shortest route must be retrieved.
        # The criteria of course it to have the shortest minimum path length so far.
        if RouteLength < MinRouteLength:
            MinRouteLength = RouteLength
            MinRoute = TempRoute
        
        # 'TempRoute' and 'RouteLength' are reset for the next iteration.
        TempRoute = []
        RouteLength = 0

    # When the shortest path is found, path's last node is appended in 'MinRetRoute',
    # as all the cargo selected during this route is gathered at it.
    # Depot is additionally included in the same list, by the time all gathered cargo
    # will eventually end up at it.
    MinRetRoute.append(16)
    MinRetRoute.append(MinRoute[len(MinRoute)-1])

    return MinRoute, MinRetRoute 


# Function that plots routes in map.
def PlotRoutes(Route, Longitude, Latitude, MapName):
    
    # Configuring connection ot OpenRouteService API Client.
    api_key = '5b3ce3597851110001cf624859d0296996b54a9aa059c47d64e73da8'
    client = openrouteservice.Client(key=api_key)
    
    # Initialization of map figure.
    m = folium.Map(location=[35.3387, 25.1442], zoom_start=15, control_scale=True, tiles='OpenStreetMap')

    # 'LoadPoint' displays the position of each load point in a route (1st, 2nd etc.).
    LoadPoint = 1
    # Access in route's nodes.
    for i in range(len(Route)-1):

        # The coordinates of the first and the second point are stored in 'Coords' as tuples.
        Coords = ((Longitude[Route[i]-1], Latitude[Route[i]-1]), (Longitude[Route[i+1]-1], Latitude[Route[i+1]-1]))
        # Requesting data related to this path.
        res = directions(client=client, coordinates=Coords)
        # In 'Geometry', the interval path postions are included.
        Geometry = res['routes'][0]['geometry']
        # Decoding 'Geometry'
        Geometry_dec = convert.decode_polyline(Geometry)
        # and inserting to map in GeoJson format.
        folium.GeoJson(Geometry_dec).add_to(m)

        # Adding markers in route's nodes. Each marker will display load point's ID and its position in route.
        # This if-else condition exists because the last point is not accessed through i iterator in previous
        # loop (see ln. 151 where i iterates 'Routes' until the pre-last node).
        # So, when i reaches the prelast node,
        if i == len(Route)-2:

            # sets the marker in it.
            folium.Marker((Latitude[Route[i]-1], Longitude[Route[i]-1]),
                           tooltip = 'ID: ' + str(Route[i]) + ' | Load Point #' + str(LoadPoint)).add_to(m)
            LoadPoint += 1

            # Next, checks if the last node is either a load point (original route) or depot (returning route)
            if Route[i+1] == 16:
                # and sets the proper markers.
                folium.Marker((Latitude[15],Longitude[15]), tooltip='Depot').add_to(m)
            else:
                folium.Marker((Latitude[Route[i+1]-1], Longitude[Route[i+1]-1]), 
                               tooltip = 'ID: ' + str(Route[i+1]) + ' | Load Point #' + str(LoadPoint)).add_to(m)    
                LoadPoint += 1
        
        # A similar check is also done during the accessing of the previous nodes and especially the first one.
        # In an original route depot is the origin, when in returning route the origin can be any of the load points.
        else:

            if Route[i] == 16:
                folium.Marker((Latitude[15],Longitude[15]), tooltip='Depot').add_to(m)
            else:
                folium.Marker((Latitude[Route[i]-1], Longitude[Route[i]-1]),
                               tooltip = 'ID: ' + str(Route[i]) + ' | Load Point #' + str(LoadPoint)).add_to(m)
                LoadPoint += 1

    # Finally, the map is saved as an .html archive.
    m.save(MapName)
########################################



############# LOADING DATA #############
excel = pd.read_excel('OptimumRouting/Coordinates&Cargo.xlsx')
IDs = excel['ID'].tolist()
Latitude = excel['Latitude'].tolist()
Longitude = excel['Longitude'].tolist()
Load_318 = excel['Load 31/8'].tolist()
Load_79 = excel['Load 7/9'].tolist()
########################################



############ CLEARING DATA #############
# Removing NaN-valued elements from lists.
IDs = removeNaN(IDs)
Latitude = removeNaN(Latitude)
Longitude = removeNaN(Longitude)
Load_318 = removeNaN(Load_318)
Load_79 = removeNaN(Load_79)
########################################



########## DISTANCES ARRAY ############
# Initialization of distances array.
DistAr = [[0 for rows in range(len(IDs))] for columns in range(len(IDs))]

# Bbox set graph's geographical frame.
Bbox = [35.319478, 25.12237, 35.327829, 25.141145]
# Initialization of graph. As network type, drive mode has been selected.
Graph = ox.graph_from_bbox(north=Bbox[2], south=Bbox[0], west=Bbox[1], east=Bbox[3], network_type='drive')

# Accesing of matrx's cell blocks.
for rows in range(len(IDs)):
    for columns in range(len(IDs)):

        # Cordinates of two interfering load points (e.g. Load points with IDs 3 (Lon3, Lat3) and 4 (Lon4, Lat4))
        Coord_1 = (Longitude[rows], Latitude[rows])
        Coord_2 = (Longitude[columns], Latitude[columns])

        # Placing the two points inside the graph as origin and destination.
        Orig_node = ox.nearest_nodes(Graph, Longitude[rows], Latitude[rows])
        Dest_node = ox.nearest_nodes(Graph, Longitude[columns], Latitude[columns])

        # Calculation of shortest path's length and its storation in the proper array block cell.
        DistAr[rows][columns] = "{:.2f}".format(float(nx.shortest_path_length(Graph, Orig_node, Dest_node, weight = 'length')))

# Converting data type of array's content from 'str' to 'float64'.
DistAr = np.array(DistAr).astype('float64')
########################################



############### DAY 31/8 ###############
# Gathering all load points IDs (the last element is the depot, so it is excluded).
LoadPointsIDs = IDs[0:len(IDs)-1]

# The minimum number of routes is the ceil of total cargo divided by vechicle's maximum capacity.
TotalCargo = sum(Load_318)
MaxCapacity = 50
TotRoutes = int(np.ceil(TotalCargo/MaxCapacity))

# Initialization of 'RemainingRoutes' variable.
RemRoutes = TotRoutes

# 'OrigRoute' will store the original route during which cargo units are gathered in specific points.
# 'RetRoute' will store the nodes includedin returning route, during cargo loading proccess.
# Both of 'TempOrigRoute' and 'TempRetRoute' are used temporarily during the formation of 'OrigRoute' and 'RetRoute'.
OrigRoute = []
RetRoute = []
TempOrigRoute = []
TempRetRoute = []

# The loop is repeated untill there are no remaining routes.
while RemRoutes != 0:

    # Calculation of all possible routes which result in maximum cargo collection.
    Routes = FindRoutes(IDs = LoadPointsIDs, CargoUnits = Load_318)
    # Finding the shortest of these paths.
    TempOrigRoute, TempRetRoute = FindShortestPath(Distances = DistAr, Routes = Routes,
                                                   RemainRoutes = RemRoutes, TotalRoutes = TotRoutes)

    # New path's nodes, for both original and returning routes, are included in 
    # the corresponding overall set of nodes calculated so far. 
    OrigRoute += TempOrigRoute
    RetRoute += TempRetRoute

    # The IDs of nodes that have been added insets above are now excluded from 'LoadPointsIDs',
    # as their position in route has been found. 
    for item in OrigRoute:
        try:
            LoadPointsIDs.remove(item)
        except:
            continue

    RemRoutes -= 1

# Reversing returning route, as it was calculated from the end to the start.
RetRoute = RetRoute[::-1]

# Plotting routes.
PlotRoutes(Route = OrigRoute, Longitude = Longitude, Latitude = Latitude, MapName = 'OptimumRouting/Maps/OrigRoute(31-8).html')
PlotRoutes(Route = RetRoute, Longitude = Longitude, Latitude = Latitude, MapName = 'OptimumRouting/Maps/RetRoute(31-8).html')
# ########### END OF DAY 31/8 ###########



############### DAY 7/9 ###############
# Similarly with day 31/8.

# Loadpoints IDs.
LoadPointsIDs = IDs[0:len(IDs)-1]

# Minimum number of routes.
TotalCargo = sum(Load_79)
MaxCapacity = 50
TotRoutes = int(np.ceil(TotalCargo/MaxCapacity))

# Remaining routes.
RemRoutes = TotRoutes

# Original and returning routes.
OrigRoute = []
RetRoute = []
TempOrigRoute = []
TempRetRoute = []

# The loop is repeated untill there are no remaining routes.
while RemRoutes != 0:

    # Calculation of all possible routes which result in maximum cargo collection.
    Routes = FindRoutes(IDs = LoadPointsIDs, CargoUnits = Load_79)
    # Finding the shortest of these paths.
    TempOrigRoute, TempRetRoute = FindShortestPath(Distances = DistAr, Routes = Routes,
                                                   RemainRoutes = RemRoutes, TotalRoutes = TotRoutes)

    # New path's nodes, for both original and returning routes, are included in 
    # the corresponding overall set of nodes calculated so far. 
    OrigRoute += TempOrigRoute
    RetRoute += TempRetRoute

    # The IDs of nodes that have been added insets above are now excluded from 'LoadPointsIDs',
    # as their position in route has been found. 
    for item in OrigRoute:
        try:
            LoadPointsIDs.remove(item)
        except:
            continue

    RemRoutes -= 1

# Reversing returning route, as it was calculated from the end to the start.
RetRoute = RetRoute[::-1]

# Plotting routes.
PlotRoutes(Route = OrigRoute, Longitude = Longitude, Latitude = Latitude, MapName = 'OptimumRouting/Maps/OrigRoute(7-9).html')
PlotRoutes(Route = RetRoute, Longitude = Longitude, Latitude = Latitude, MapName = 'OptimumRouting/Maps/RetRoute(7-9).html')
########### END OF DAY 7/9 ###########
########### END OF SCRIPT ############