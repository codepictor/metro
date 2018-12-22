import metro_data
import metro_router
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt



def make_time_histogram():
    """Make a histogram with distribution of links between stations by time."""
    times = []
    for link in metro_data.LINKS:
        times.append(link[2]['time'])

    fig = plt.figure(figsize=(18, 12))
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.hist(times, bins='auto')
    plt.title('time distribution', fontsize=42)
    plt.ylabel('number of stations', fontsize=30)
    plt.xlabel('time (in seconds)', fontsize=30)

    try:
        plt.savefig('../img/time_histogram.pdf', dpi=180, format='pdf')
    except FileNotFoundError:
        print("WARNING! To get a time histogram you should run "
              + "the script 'main.py' inside metro/src/ directory")



def main():
    router = metro_router.Router()
    router.draw_route()
    make_time_histogram()

    start_station = metro_router.Station('Дмитровская')
    finish_station = metro_router.Station('Бутырская')
    route1 = router.make_shortest_route(
            start_station, finish_station,
            is_drawing_graph=True)
    print(route1)

    start_station = metro_router.Station('Парк культуры', line=1)
    finish_station = metro_router.Station('Бунинская аллея')
    route2 = router.make_shortest_route(
            start_station, finish_station,
            is_drawing_graph=True)
    print(route2)

    start_station = metro_router.Station('Окружная', line=10)
    finish_station = metro_router.Station('Ясенево')
    intermediate_station1 = metro_router.Station('Соколиная гора')
    intermediate_station2 = metro_router.Station('Фили')
    route_with_intermediates = router.make_shortest_route(
            start_station,
            finish_station,
            intermediate_stations=[
                intermediate_station1,
                intermediate_station2
            ],
            is_drawing_graph=True)
    print(route_with_intermediates)



if __name__ == '__main__':
    main()

