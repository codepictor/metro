import networkx as nx
import matplotlib.pyplot as plt
import metro_data


class Station:
    def __init__(self, station):
        """"""
        if isinstance(station, int):
            if station not in metro_data.STATIONS.keys():
                raise ValueError('Station with id = {0} '
                                 + ' not found'.format(station))
            self._id = station
        elif isinstance(station, str):
            stations_count = 0
            for station_id, station_info in metro_data.STATIONS.items():
                if station_info['name'] == station:
                    self._id = station_id
                    stations_count += 1
            if stations_count == 0:
                raise ValueError("Station '{0}' doesn't exist".format(station))
            if stations_count >= 2:
                raise ValueError("You have to specify a line "
                                 + " for the station '{0}'".format(station))
        else:
            raise ValueError("Wrong station's type: {0}".format(type(station)))

    def __repr__(self):
        return "Station: '{0}' (line: {1})".format(
                metro_data.STATIONS[self._id]['name'],
                metro_data.STATIONS[self._id]['line'])


class Route:
    def __init__(self):
        self.path = []

    def _append_edge(self, station_from_id, station_to_id, time):
        """"""
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


class Router:
    def __init__(self):
        self._graph = nx.Graph()
        self._graph.add_nodes_from(metro_data.STATIONS.keys())
        self._graph.add_edges_from(metro_data.LINKS)

    def make_shortest_route(self, start_station, finish_station,
                            is_drawing_graph=False):
        """"""
        shortest_path = [start_station,]
        shortest_path_time = 0.0
        if (start_station != finish_station):
            shortest_path = nx.dijkstra_path(
                    self._graph, start_station._id,
                    finish_station._id, weight='time')

        if is_drawing_graph:
            nx.draw_networkx(self._graph, with_labels=True, font_weight='bold')
            start_station_name = metro_data.STATIONS[start_station._id]['name']
            finish_station_name = metro_data.STATIONS[finish_station._id]['name']
            plt.savefig('from_' + start_station_name + '_to_'
                        + finish_station_name + '.png')

        edges = nx.get_edge_attributes(self._graph, 'time')
        shortest_route = Route()
        for i in range(1, len(shortest_path)):
            station_from_id = shortest_path[i - 1]
            station_to_id = shortest_path[i]
            if (station_from_id, station_to_id) in edges:
                time = edges[(station_from_id, station_to_id)]
            else:
                time = edges[(station_to_id, station_from_id)]
            shortest_route._append_edge(station_from_id, station_to_id, time)
        return shortest_route



    def __repr__(self):
        return 'A singletone for constructing routes'




