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
    
    def ArrivalsOnStop(self, stop_id):
        st_selection=self.stop_times[self.stop_times.stop_id==stop_id]
        st_selection_merge=st_selection.merge(self.trips, on='trip_id', how='left')
        return st_selection_merge
    
    def TripsOnStop(self, stop_id):
        st_selection=self.ArrivalsOnStop(stop_id)
        trip_ids=list(set(st_selection.trip_id))
        t_selection=self.trips[self.trips.trip_id.isin(trip_ids)]
        return t_selection
    
    def RoutesOnStop(self, stop_id):
        t_selection=self.TripsOnStop(stop_id)
        route_ids=list(set(t_selection.route_id))
        r_selection=self.routes[self.routes.route_id.isin(route_ids)]
        return r_selection
    
    def ServiceTimeOfRoutes(self, stop_arrivals, stop_routes):

        route_ids=list(stop_routes.route_id)
        route_info=dict()
        for route_id in route_ids:
            route=stop_routes[stop_routes.route_id==route_id]
            route_arrivals=stop_arrivals[stop_arrivals.route_id==route_id]
            
            # Нет учета calendar и calendar.dates
            max=route_arrivals.arrival_time.max()
            min=route_arrivals.arrival_time.min()
            # Нет учета возможных укоротов/вариантов
            main_headsign=route_arrivals.trip_headsign.mode().item()
            route_info[route_id]={'start': min, 'end': max, 'headsign': main_headsign,
                                  'route_color': route['route_color'].item(), 
                                  'route_text_color': route['route_text_color'].item(), 'route_short_name': route['route_short_name'].item()}
        return {k: v for k, v in sorted(route_info.items(), key=lambda item: item[1]['route_short_name'])}

    def GetActualServiceID(self, stop_arrivals, stop_routes, service_keys):
        # Get actual service IDs by defined dates
        route_ids=list(stop_routes.route_id)
        route_info=dict()
        for route_id in route_ids:
            route=stop_routes[stop_routes.route_id==route_id]
            route_arrivals=stop_arrivals[stop_arrivals.route_id==route_id]
            unique_service_ids=list(route_arrivals.service_id.unique())
            found_service_ids=[]
            #print(f'Route {route['route_short_name'].item()} service_ids: {unique_service_ids}')
            for i in range(len(unique_service_ids)):
                for k in service_keys:
                    if k in unique_service_ids[i] and unique_service_ids[i] not in found_service_ids:
                        found_service_ids.append(unique_service_ids[i])

            route_info[route_id]=found_service_ids
        return route_info
    
    def Intervalizer(self, arrivals):
        arrivals=arrivals[0] # bug
        hours=[t.split(':')[0] for t in arrivals]
        timetable={h: [] for h in hours}
        for hour in hours:
            for arrival in arrivals:
                if arrival.split(':')[0]==hour and arrival.split(':')[1] not in timetable[hour]:
                    timetable[hour].append(arrival.split(':')[1])
        for hour in hours:
            ha=timetable[hour]
            # интервал меньше 20 минут - значит минимум 3 рейса в час 
            # интервал больше 20 минут - значит не более 3 рейса в час
            if len(ha)>3 and 'it' not in ha:
                difs=[int(ha[i+1])-int(ha[i]) for i in range(len(ha)-1)]
                #print(hour, ha, difs)
                if min(difs)!=max(difs):
                    timetable[hour]=f'it_{min(difs)}...{max(difs)}'
                else:
                    timetable[hour]=f'it_{min(difs)}'
        return timetable
    #
    #def AggrInterval(self, route_info, pattern=[(7,9),(9,16),(16,19),(19,23)]):
    #    if pattern is not None:
    #        timetable_aggr=dict()
    #         for 
    #        for section in pattern:
    #            hs=f'{section[0]}-{section[1]}'

    
    def Timetable(self, stop_arrivals, stop_routes, service_keys):
        #! ГОСТ Р 58287-2018
        #! При интервале движения подвижного состава не более 20 мин указывают почасовой
        #! интервал движения в минутах, более 20 мин - составляют расписание движения в часах и минутах.

        route_ids=list(stop_routes.route_id)
        route_info=dict()
        for route_id in route_ids:
            route=stop_routes[stop_routes.route_id==route_id]
            route_arrivals=stop_arrivals[stop_arrivals.route_id==route_id]
            route_arrivals_by_service=route_arrivals.groupby(['service_id'])['arrival_time'].apply(lambda x: ','.join(x)).reset_index()
            route_arrivals_by_service['arrival_time']=route_arrivals_by_service['arrival_time'].apply(lambda x: x.split(','))
            route_arrivals_by_service=route_arrivals_by_service[route_arrivals_by_service.service_id.isin(service_keys[route_id])]
            all_arrivals=route_arrivals_by_service.set_index('service_id').T.to_dict('list')
            all_arrivals_2={service_id: self.Intervalizer(all_arrivals[service_id]) for service_id in service_keys[route_id]}
            main_headsign=route_arrivals.trip_headsign.mode().item()
            route_info[route_id]={'timetable': all_arrivals_2, 'headsign': main_headsign,
                                  'route_color': route['route_color'].item(), 
                                  'route_text_color': route['route_text_color'].item(), 'route_short_name': route['route_short_name'].item()}
        return {k: v for k, v in sorted(route_info.items(), key=lambda item: item[1]['route_short_name'])}
    
    def DescribeForFlag(self, stop_id):
        stop_info=self.StopInfo(stop_id)
        print(f'Stop name {stop_info.stop_name.item()}')
        stop_arrivals=self.ArrivalsOnStop(stop_id)
        stop_routes=self.RoutesOnStop(stop_id)
        print(f'Serves {len(stop_routes)} routes: {list(stop_routes.route_short_name)}')
        service_times=self.ServiceTimeOfRoutes(stop_arrivals, stop_routes)
        return service_times
    
    def DescribeForLayout(self, stop_id, service_keys):
        # service_keys - это ключи для составления расписания на лето или зиму. В случае Железногорска service_id имеют или summer, или winter, или all(0)
        stop_info=self.StopInfo(stop_id)
        print(f'Stop name {stop_info.stop_name.item()}')
        stop_arrivals=self.ArrivalsOnStop(stop_id)
        stop_routes=self.RoutesOnStop(stop_id)
        print(f'Serves {len(stop_routes)} routes: {list(stop_routes.route_short_name)}')
        service_keys_found=self.GetActualServiceID(stop_arrivals, stop_routes, service_keys)
        timetable=self.Timetable(stop_arrivals, stop_routes, service_keys_found)
        return timetable

#feed=Feed('k26_static')
#stop=feed.DescribeForLayout(21, ['summer', 'all', '0'])
#print(stop)