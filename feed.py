import pandas as pd

class Feed:
    def __init__(self, folder: str) -> None:
        # Initialize feed by importing csv to df
        self.agency=pd.read_csv(folder+r'\agency.txt', sep=',')
        self.calendar=pd.read_csv(folder+r'\calendar.txt', sep=',')
        self.calendar_dates=pd.read_csv(folder+r'\calendar_dates.txt', sep=',')
        self.routes=pd.read_csv(folder+r'\routes.txt', sep=',')
        self.trips=pd.read_csv(folder+r'\trips.txt', sep=',')
        self.stops=pd.read_csv(folder+r'\stops.txt', sep=',')
        self.stop_times=pd.read_csv(folder+r'\stop_times.txt', sep=',')
        self.shapes=pd.read_csv(folder+r'\shapes.txt', sep=',')

    def StopInfo(self, stop_id):
        return self.stops[self.stops.stop_id==stop_id]
    
    def ArrivesOnStop(self, stop_id):
        st_selection=self.stop_times[self.stop_times.stop_id==stop_id]
        st_selection_merge=st_selection.merge(self.trips, on='trip_id', how='left')
        return st_selection_merge
    
    def TripsOnStop(self, stop_id):
        st_selection=self.ArrivesOnStop(stop_id)
        trip_ids=list(set(st_selection.trip_id))
        t_selection=self.trips[self.trips.trip_id.isin(trip_ids)]
        return t_selection
    
    def RoutesOnStop(self, stop_id):
        t_selection=self.TripsOnStop(stop_id)
        route_ids=list(set(t_selection.route_id))
        r_selection=self.routes[self.routes.route_id.isin(route_ids)]
        return r_selection
    
    def ServiceTimeOfRoutes(self, stop_arrives, stop_routes):
        #print(stop_routes)
        route_ids=list(stop_routes.route_id)
        route_info=dict()
        for route_id in route_ids:
            route=stop_routes[stop_routes.route_id==route_id]
            route_arrives=stop_arrives[stop_arrives.route_id==route_id]
            
            # Нет учета calendar и calendar.dates
            max=route_arrives.arrival_time.max()
            min=route_arrives.arrival_time.min()
            # Нет учета возможных укоротов/вариантов
            main_headsign=route_arrives.trip_headsign.mode().item()
            route_info[route_id]={'start': min, 'end': max, 'headsign': main_headsign,
                                  'route_color': route['route_color'].item(), 
                                  'route_text_color': route['route_text_color'].item(), 'route_short_name': route['route_short_name'].item()}
        return {k: v for k, v in sorted(route_info.items(), key=lambda item: item[1]['route_short_name'])}
            #print(route_id, min, max)

    def DescribeForFlag(self, stop_id):
        stop_info=self.StopInfo(stop_id)
        print(f'Stop name {stop_info.stop_name.item()}')
        stop_arrives=self.ArrivesOnStop(stop_id)
        stop_routes=self.RoutesOnStop(stop_id)
        print(f'Serves {len(stop_routes)} routes: {list(stop_routes.route_short_name)}')
        service_times=self.ServiceTimeOfRoutes(stop_arrives, stop_routes)
        #print(service_times)
        return service_times

