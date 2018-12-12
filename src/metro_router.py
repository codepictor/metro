import scipy
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import metro_data
import singleton



class Station:
    """Convenient wrapper around a metro's station."""

    def __init__(self, station, line=None):
        """Inits station.

        This method can init a station based on whether station's id
        or station's name. Some stations have same names but different
        line numbers. That is why, you need specify a line number explicitly
        to avoid ambiguity.
        
        Args:
            station (int or str): station's id or name
            line (int): line number of the given station

        Raises:
            ValueError: trying to init a station with incorrect data
                (given station's id doesn't exist,
                ambiguity in choosing line number, etc.)
        """
        if isinstance(station, int):
            if station not in metro_data.STATIONS:
                raise ValueError('Station with id = {0}'.format(station)
                                 + ' not found')
            self._id = station
        elif isinstance(station, str):
            stations_count = 0
            found_line = None
            for station_id, station_info in metro_data.STATIONS.items():
                if station_info['name'] == station:
                    stations_count += 1
                    if line is None or station_info['line'] == line:
                        self._id = station_id
                        found_line = station_info['line']
            if stations_count == 0:
                raise ValueError("Station '{0}' ".format(station)
                                 + "doesn't exist")
            if stations_count >= 2 and line is None:
                raise ValueError("You have to specify a line "
                                 + "for the station '{0}'".format(station))
            if found_line is None:
                raise ValueError("Incorrect line {0} ".format(line)
                                 + "for station '{0}'".format(station))
        else:
            raise ValueError("Wrong station's type: {0}".format(type(station)))


    def __repr__(self):
        return "Station: '{0}' (line: {1})".format(
                metro_data.STATIONS[self._id]['name'],
                metro_data.STATIONS[self._id]['line'])



class Route:
    """Convenient wrapper around a metro's route.

    Attributes:
        path (list of dicts): each dict in this list contains:
            'from': Station - beginning if the route
            'to': Station - end of the route
            'time': int - time (in seconds) needed to move between from and to
    """

    def __init__(self):
        """Inits empty route (with no stations)."""
        self.path = []


    def _append_edge(self, station_from_id, station_to_id, time):
        self.path.append({
                'from': Station(station_from_id),
                'to':   Station(station_to_id),
                'time': time})


    def __repr__(self):
        representation = "Route: from '{0}' to '{1}':\n".format(
                self.path[0]['from'], self.path[-1]['to'])
        total_time = 0
        for edge in self.path:
            total_time += edge['time']
            representation += '  {0} -> {1}: {2}s\n'.format(
                    edge['from'], edge['to'], edge['time'])
        representation += 'Total time: {0}s'.format(str(total_time))
        return representation



class Router(metaclass=singleton.Singleton):
    """A singleton for making different routes in metro.

    This class provides convenient interface for getting routes
    between two metro's stations. A route can have intermediate stations
    (see the 'make_shortest_path' method).
    """

    def __init__(self):
        """Constructs a metro's graph."""
        self._graph = nx.Graph()
        self._graph.add_nodes_from(metro_data.STATIONS.keys())
        self._graph.add_edges_from(metro_data.LINKS)


    def _make_shortest_simple_path(self, start_station, finish_station):
        # Just performs Dijkstra's algorithm
        shortest_path = [start_station,]
        if (start_station != finish_station):
            shortest_path = nx.dijkstra_path(
                    self._graph, start_station._id,
                    finish_station._id, weight='time')
        return shortest_path


    def draw_route(self, route=None):
        """Draws the graph with the highlighted route.
        
        If route is not provided, this method will draw self._graph
        without highlighting any route. The figure will be saved
        into a file.

        Args:
            route (Route): a route for highlighting
        """
        plt.gcf().clear()
        # layout
        pos = nx.kamada_kawai_layout(self._graph, weight='time')

        # nodes
        colors = [metro_data.COLORS[station['line']]
                  for station in metro_data.STATIONS.values()]
        nx.draw_networkx_nodes(self._graph, pos, node_size=80,
                               node_color=colors)

        # edges
        nx.draw_networkx_edges(self._graph, pos, width=1)
        if route is not None:
            highlighted_stations = []
            for edge in route.path:
                highlighted_stations.append((edge['from']._id, edge['to']._id))
            nx.draw_networkx_edges(self._graph, pos,
                                   edgelist=highlighted_stations,
                                   width=4, edge_color='r')

        # labels
        nx.draw_networkx_labels(self._graph, pos,
                                font_size=4, font_family='sans-serif')

        plt.gcf().set_size_inches(18, 12)
        plt.axis('off')
        filename = 'metro.pdf'
        if route is not None:
            start_station_id = route.path[0]['from']._id
            start_station_name = metro_data.STATIONS[start_station_id]['name']
            finish_station_id = route.path[-1]['to']._id
            finish_station_name = metro_data.STATIONS[finish_station_id]['name']
            filename = 'from_' + start_station_name + '_to_'\
                       + finish_station_name + '.pdf'
        try:
            plt.savefig('../img/' + filename, dpi=180, format='pdf')
        except FileNotFoundError:
            print("WARNING! To get an image of the graph you should run "
                  + "the script 'main.py' inside metro/src/ directory")


    def _make_route_from_path(self, path):
        # Converts given path to a route
        edges = nx.get_edge_attributes(self._graph, 'time')
        route = Route()
        for i in range(1, len(path)):
            station_from_id = path[i - 1]
            station_to_id = path[i]
            if station_from_id != station_to_id:
                if (station_from_id, station_to_id) in edges:
                    time = edges[(station_from_id, station_to_id)]
                else:
                    time = edges[(station_to_id, station_from_id)]
                route._append_edge(station_from_id, station_to_id, time)
        return route


    def make_shortest_route(self, start_station, finish_station,
                            intermediate_stations=None,
                            is_drawing_graph=False):
        """Constructs the shortest route between two given stations.
        
        Args:
            start_station (Station): station which is the beginning
                of the shortest route
            finish_station (Station): station which is the end
                of the shortest route
            intermediate_stations (iterable object): intermediate stations
                which you want to visit (in given order)
            is_drawing_graph (bool): whether the self._graph shoul be drawn

        Returns:
            A route (instance of the class Route) which is the shortest between
            start_station and finish_station.
        """
        if intermediate_stations is None or not intermediate_stations:
            shortest_path = self._make_shortest_simple_path(
                    start_station, finish_station)
        else:
            shortest_path = []
            intermediate_stations.append(finish_station)
            curr_station = start_station
            for next_station in intermediate_stations:
                shortest_path.extend(self._make_shortest_simple_path(
                        curr_station, next_station))
                # if next_station != finish_station
                curr_station = next_station

        shortest_route = self._make_route_from_path(shortest_path)
        if is_drawing_graph:
            self.draw_route(shortest_route)
        return shortest_route


