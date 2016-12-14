#!/usr/bin/python

# Copyright 2015-2016 Arogi Inc
# Copyright 2010-2014 Google
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Antonio Medrano

"""A Vehicle Routing Problem example that imports a JSON file problem definition and
   solves using the Google OR-Tools solver using constraint progrmming. Note
   that our test files include other data used to solve both the MCLP and
   p-Median problems.
"""

import cgi
import json
import GISOps
import numpy as np
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def main():
    objective = RunVRP()
    generateGEOJSON(objective)
    
def RunVRP():
    #TSP using Google OR-Tools Constraint Programming model example
    read_problem(receivedMarkerData)
    PreComputeDistances() #compute the distances between points
    objective = SolveModel()
    return objective

def PreComputeDistances():
    #declare a couple variables
    global d
    global xyPointArray
    # Get the Distance Coordinates in CONUS EqD Projection
    xyPointArray = GISOps.GetCONUSeqDprojCoords(js)
    d = cdist(xyPointArray, xyPointArray,'euclidean')
    return 1

def Distance(i,j):
    return d[i,j]

# Demand callback
class CreateDemandCallback(object):
    """Create callback to get demands at each location."""

    def __init__(self, demands):
        self.matrix = demands

    def Demand(self, from_node, to_node):
        return self.matrix[from_node]


def SolveModel():
    """Solve the problem and print the solution."""
    global routeCoord
    depot = 0

    demands = [1]*numFeatures
    demands[depot] = 0
    num_locations = numFeatures
    num_vehicles = 5
    time_limit = 10
  
    # Ensure that the data is valid for making at TSP route
    if numFeatures > 1:

        # The number of nodes of the VRP is num_locations.
        # Nodes are indexed from 0 to num_locations - 1. By default the start of
        # a route is node 0.
        routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

        # Setting first solution heuristic: the
        # method for finding a first solution to the problem.
        # If no feasible solution exists, program will timeout
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Improve opon the initial solution
        # search_parameters.local_search_metaheuristic = (
        #     routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit_ms = time_limit*1000

        # The 'PATH_CHEAPEST_ARC' method does the following:
        # Starting from a route "start" node, connect it to the node which produces the
        # cheapest route segment, then extend the route by iterating on the last
        # node added to the route.

        # Put a callback to the distance function here. The callback takes two
        # arguments (the from and to node indices) and returns the distance between
        # these nodes.
        routing.SetArcCostEvaluatorOfAllVehicles(Distance)

        # Put a callback to the demands.
        demands_at_locations = CreateDemandCallback(demands)
        demands_callback = demands_at_locations.Demand

        # Adding capacity dimension constraints.
        vehicle_capacity = (numFeatures / num_vehicles) + 1
        null_capacity_slack = 0
        fix_start_cumul_to_zero = True
        capacity = "Capacity"
        routing.AddDimension(demands_callback, null_capacity_slack, vehicle_capacity,
                             fix_start_cumul_to_zero, capacity)

        # Solve displays a solution, if any.
        assignment = routing.SolveWithParameters(search_parameters)
        if assignment:
            # Display solution.
            i = 0
            routeCoord = [None]*(numFeatures+num_vehicles-1)

            for vehicle_nbr in range(num_vehicles):
                index = routing.Start(vehicle_nbr)
                index_next = assignment.Value(routing.NextVar(index))
                route_dist = 0
                route_demand = 0

                while not routing.IsEnd(index_next):
                    node_index = routing.IndexToNode(index)
                    node_index_next = routing.IndexToNode(index_next)
                    routeCoord[i] = [node_index, node_index_next, vehicle_nbr]
                    # Add the distance to the next node.
                    route_dist += Distance(node_index, node_index_next)
                    # Add demand.
                    route_demand += demands[node_index_next]
                    index = index_next
                    index_next = assignment.Value(routing.NextVar(index))
                    i += 1

                node_index = routing.IndexToNode(index)
                node_index_next = routing.IndexToNode(index_next)
                routeCoord[i] = [node_index, node_index_next, vehicle_nbr]
                route_dist += Distance(node_index, node_index_next)
            # NOTE: The ObjectiveValue() returns a different distance than the calculated accumulated distance route_dist
            # return assignment.ObjectiveValue()/1000.0
            return route_dist/1000.0
  
        else:
            print 'No feasible solution found after %d seconds.' % time_limit
    else:
        print 'Specify an instance greater than 0.'
    return 0


# Read a problem instance from a file
def read_problem(file):
    global numFeatures
    global js
    try:
        js = json.loads(file)
    except IOError:
        print 'Error reading file'
        raise
    # count the number of point features to connect
    numFeatures = len(js['features'])
    return 1


### This function will return a geojson formatted string to send back to the web
### Since it is based on the p-Median/MCLP data files we can use some of those
### atributes to send back. In this case facilityLocated represents the 'from
### node' and assignedTo represents the 'to node' for the TSP.
def generateGEOJSON(objective):
    for i in range(numFeatures):
        node = routeCoord[i][0]
        nextNode = routeCoord[i][1]
        vehicle = routeCoord[i][2]
        js['features'][node]['properties']['thisNode'] = node
        js['features'][node]['properties']['nextNode'] = nextNode
        js['features'][node]['properties']['vehicle'] = vehicle

    # if properties does not exist in the geojson, then create
    if 'properties' not in js:
        js['properties'] = {}

    # write the objective value into the geojson
    js['properties']['objective'] = objective

    return 1

###########################################################
##################### The main controller code starts here.
###########################################################

# Create instance of FieldStorage and get data
form = cgi.FieldStorage()
receivedMarkerData = form.getvalue('useTheseMarkers')

# the magic happens here...
main()

# prepare for output... the GeoJSON should be returned as a string
transformedMarkerData = json.dumps(js)
print "Content-type:text/html\r\n\r\n"
print transformedMarkerData
