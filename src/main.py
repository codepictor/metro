import metro_data
import metro_router



def main():
    router = metro_router.Router()
    router.draw_route()

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

    # intermediate_station1 = metro_router.Station('Марьина Роща')
    # route_with_intermediates = router.make_shortest_route(
    #         start_station, finish_station,
    #         intermediate_stations=[
    #             intermediate_station1,
    #         ],
    #         is_drawing_graph=True)
    # print(route_with_intermediates)

    start_station = metro_router.Station('Окружная', line=10)
    finish_station = metro_router.Station('Братиславская')
    intermediate_station1 = metro_router.Station('Борисово')
    intermediate_station2 = metro_router.Station('Орехово')
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

