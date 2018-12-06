import metro_data
import metro_router



def main():
    router = metro_router.Router()

    start_station = metro_router.Station('Дмитровская')
    finish_station = metro_router.Station('Бутырская')
    route = router.make_shortest_route(
            start_station, finish_station, is_drawing_graph=False)
    print(route)




if __name__ == '__main__':
    main()

