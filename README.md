# Route Optimizations

## Objective
#### This project aims to find the optimum, in terms of driving distance, route for a vechicle which collects specific cargo units from different load points in the city of Heraklion, Greece.

## Parameters
#### The vechicle has a limited cargo capacity of 50 cargo units. Having a depot as a start, it is called to collect cargo units through different load points. It is not allowed to load cargo from a point to another but only to temporarily leave it in the load point, so it can be loaded after vechicle's capacity has reached its fullines and it returns back to depot to empty its storage. Cargo units do not only provide different cargo quantity with between each other, but their own cargo points differ between two days.  

## Given Data
#### A set of loading points' coordinates and their cargo units in two different days is given in .xlsx file.

## Python Code
#### Python code has been developed to find both the minimum number of routes and the minimum length of those and plot them in Herklion's map figure. The algorithm that was used to find the optimum routes is Dijkstra's Algorithm. The packages that have been used are enlisted below,

### 1. openrouteservice
### 2. openstreetmap
### 3. itertools
### 4. netowrkx
### 5. folium
### 6. pandas
### 7. numpy
