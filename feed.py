import pandas as pd
import math
import geopandas as gpd
import warnings
from pandas.errors import SettingWithCopyWarning
import subprocess
import os
import mapbox_vector_tile
import json

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
class Loom:
    # Init with Feed to get selection by stop
    def __init__(self, folder: str, stop_id):
        self.stop_id=stop_id
        self.folder=folder
        feed=Feed(folder)
        selection_folder=feed.SaveSelectionOfStop(stop_id, folder)
        gtfs_folder=selection_folder+'/gtfs_edited'
        self.agency=pd.read_csv(gtfs_folder+'/agency.txt', sep=',')
        self.calendar=pd.read_csv(gtfs_folder+'/calendar.txt', sep=',')
        self.calendar_dates=pd.read_csv(gtfs_folder+'/calendar_dates.txt', sep=',')
        self.routes=pd.read_csv(gtfs_folder+'/routes.txt', sep=',')
        self.trips=pd.read_csv(gtfs_folder+'/trips.txt', sep=',')
        stops=pd.read_csv(gtfs_folder+'/stops.txt', sep=',')
        self.stops=gpd.GeoDataFrame(stops, geometry=gpd.points_from_xy(stops.stop_lon, stops.stop_lat), crs="EPSG:4326")
        #self.stops=pd.read_csv(folder+'/stops.txt', sep=',')
        self.stop_times=pd.read_csv(gtfs_folder+'/stop_times.txt', sep=',')
        shapes=pd.read_csv(gtfs_folder+'/shapes.txt', sep=',')
        self.shapes=gpd.GeoDataFrame(shapes, geometry=gpd.points_from_xy(shapes.shape_pt_lon, shapes.shape_pt_lat))
        self.selection_folder=selection_folder
    def gtfs2graph(self, mots=['all']):
        try:
            gtf2graph_subp=subprocess.check_output(f'gtfs2graph {self.selection_folder}/gtfs_edited --mots {",".join(mots)} > {self.selection_folder}/gtfs2graph.json', shell=True)                       
        except subprocess.CalledProcessError as exc:                                                                                                   
            print("error code", exc.returncode, exc.output)
    def topo(self, max_aggr_dist=50, no_infer_restr=False, infer_restr_max_dist=50, max_comp_dist=10000, smooth=0):
        if no_infer_restr==False:
            try:
                #print(f'topo --max-aggr-dist={max_aggr_dist} --max-comp-dist={max_comp_dist} --smooth={smooth} < {self.selection_folder}/gtfs2graph.json > {self.selection_folder}/topo.json')
                #print(subprocess.run(f'topo --max-aggr-dist={max_aggr_dist} --max-comp-dist={max_comp_dist} --smooth={smooth} < {self.selection_folder}/gtfs2graph.json > {self.selection_folder}/topo.json', shell=True))
                topo_subp=subprocess.check_output(f'topo --max-aggr-dist={max_aggr_dist} --max-comp-dist={max_comp_dist} --smooth={smooth} < {self.selection_folder}/gtfs2graph.json > {self.selection_folder}/topo.json', shell=True)                       
            except subprocess.CalledProcessError as exc:                                                                                                   
                print("error code", exc.returncode, exc.output)
        else:
            try:
                topo_subp=subprocess.check_output(f'topo --max-aggr-dist={max_aggr_dist} --no-infer-restr --infer-restr-max-dist={infer_restr_max_dist} --max-comp-dist={max_comp_dist} --smooth={smooth} < {self.selection_folder}/gtfs2graph.json > {self.selection_folder}/topo.json', shell=True)                       
            except subprocess.CalledProcessError as exc:                                                                                                   
                print("error code", exc.returncode, exc.output)
    def loom(self, optim_method='hillc', no_prune=False, no_untangle=False, same_seg_cross_pen=4, diff_seg_cross_pen=1, in_stat_cross_pen_same_seg=12, in_stat_cross_pen_diff_seg=3, sep_pen=3, in_stat_sep_pen=9, ilp=False, ilp_solver='cbc', ilp_num_threads=4):
        loom_cfg=f'loom --optim-method'
        if ilp==True:
            loom_cfg+=f' ilp --ilp-solver={ilp_solver} --ilp-num-threads={ilp_num_threads}'
        if no_prune==True:
            loom_cfg+=f' --no-prune'
        if no_untangle==True:
            loom_cfg+=f' --no-untangle'
        loom_cfg+=f' --same-seg-cross-pen={same_seg_cross_pen} --diff-seg-cross-pen={diff_seg_cross_pen} --in-stat-cross-pen-same-seg={in_stat_cross_pen_same_seg} --in-stat-cross-pen-diff-seg={in_stat_cross_pen_diff_seg} --in-stat-sep-pen={in_stat_sep_pen} --sep-pen={sep_pen}'
        loom_cfg+=f' < {self.selection_folder}/topo.json> {self.selection_folder}/loom.json'
        try:
            loom_subp=subprocess.check_output(loom_cfg, shell=True)
        except subprocess.CalledProcessError as exc:                                                                                                   
            print("error code", exc.returncode, exc.output)
    def transitmap(self, render_engine='svg', line_width=20, line_spacing=10, outline_width=1, render_dir_markers=False, no_render_stations=False, tight_stations=False, no_render_node_connections=False, labels=False, z=[14,15,16,17]):
        self.zls=z
        transitmap_cfg=f'transitmap --line-width={line_width} --line-spacing={line_spacing} --outline-width={outline_width}'
        if render_dir_markers==True:
            transitmap_cfg+=f' --render-dir-markers'
        if no_render_stations==True:
            transitmap_cfg+=f' --no-render-stations'
        if tight_stations==True:
            transitmap_cfg+=f' --tight-stations'
        if no_render_node_connections==True:
            transitmap_cfg+=f' --no-render-node-connections'
        if labels==True:
            transitmap_cfg+=f' --labels'
        if render_engine=='svg':
            transitmap_cfg+=f' --render-engine=svg > {self.selection_folder}/stop_{self.stop_id}.svg'
        elif render_engine=='mvt':
            transitmap_cfg+=f' --render-engine=mvt -z {",".join(map(str, z))} --mvt-path={self.selection_folder}'
        transitmap_cfg+=f' < {self.selection_folder}/loom.json'
        try:
            transitmap_subp=subprocess.check_output(transitmap_cfg, shell=True)
        except subprocess.CalledProcessError as exc:                                                                                                   
            print("error code", exc.returncode, exc.output)
    def decode_mvt(self, zl=14):
        def pixel2deg(xtile, ytile, zoom, xpixel, ypixel, extent = 1024):
            # from https://gis.stackexchange.com/a/460173/44746
            n = 2.0 ** zoom
            xtile = xtile + (xpixel / extent)
            ytile = ytile + ((extent - ypixel) / extent)
            lon_deg = (xtile / n) * 360.0 - 180.0
            lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
            lat_deg = math.degrees(lat_rad)
            return (lon_deg, lat_deg)

        inner_connections=[]
        lines=[]
        stations=[]
        zoomfolder=f'/{self.selection_folder}/{zl}'
        for subdir, dirs, files in os.walk(zoomfolder):
            for file in files:
                #print(os.path.join(subdir, file))
                tile=os.path.join(subdir, file)
                with open(tile, 'rb') as f:
                    data=f.read()
                tile_zoom=int(tile.split('/')[-3])
                tile_x=int(tile.split('/')[-2])
                tile_y=int(tile.split('/')[-1][:-4])
                decoded_data = mapbox_vector_tile.decode(data, transformer = lambda x, y: pixel2deg(tile_x, tile_y, tile_zoom, x, y))
                #print(decoded_data)
                inner_connections.append(decoded_data['inner-connections']['features'])
                lines.append(decoded_data['lines']['features'])
                stations.append(decoded_data['stations']['features'])
        lines=[fe for fes in lines for fe in fes]
        stations=[fe for fes in stations for fe in fes]
        inner_connections=[fe for fes in inner_connections for fe in fes]
        #print('ic', len(inner_connections))
        return lines, stations, inner_connections
    
    def net2gpkg(self):
        #zls = [ f.path for f in os.scandir(f'/{self.selection_folder}') if f.is_dir() and 'gtfs_edited' not in f ]
        for zl in self.zls:
            lines, stations, inner_connections = self.decode_mvt(zl)

            gdf_lines=gpd.GeoDataFrame.from_features(lines)
            gdf_stations=gpd.GeoDataFrame.from_features(stations)
            gdf_inner_connections=gpd.GeoDataFrame.from_features(inner_connections)
            if len(gdf_lines)>0:
                gdf_lines.to_file(f'{self.selection_folder}/stop_{self.stop_id}.gpkg', driver='GPKG', layer=f'stop_{self.stop_id}_z{zl}_lines')
            if len(gdf_stations)>0:
                gdf_stations.to_file(f'{self.selection_folder}/stop_{self.stop_id}.gpkg', driver='GPKG', layer=f'stop_{self.stop_id}_z{zl}_stations')
            if len(gdf_inner_connections)>0:
                gdf_inner_connections.to_file(f'{self.selection_folder}/stop_{self.stop_id}.gpkg', driver='GPKG', layer=f'stop_{self.stop_id}_z{zl}_ic')

            subprocess.run(f'rm -rf {self.selection_folder}/{zl}', shell=True)
        #dumping={'type': 'FeatureCollection', 'features': [*lines[0]['features'], *stations[0]['features'], *inner_connections[0]['features']]}
        #with open(f'{self.selection_folder}/stop_{self.stop_id}_zl{zl}.json', 'w', encoding='utf-8') as net:
        #    json.dump(dumping, net)
        print(f'{self.selection_folder}/stop_{self.stop_id}.gpkg')
class Feed:
    def __init__(self, folder: str) -> None:
        # Initialize feed by importing csv to df
        self.agency=pd.read_csv(folder+'/agency.txt', sep=',')
        self.calendar=pd.read_csv(folder+'/calendar.txt', sep=',')
        self.calendar_dates=pd.read_csv(folder+'/calendar_dates.txt', sep=',')
        self.routes=pd.read_csv(folder+'/routes.txt', sep=',')
        self.trips=pd.read_csv(folder+'/trips.txt', sep=',')
        stops=pd.read_csv(folder+'/stops.txt', sep=',')
        self.stops=gpd.GeoDataFrame(stops, geometry=gpd.points_from_xy(stops.stop_lon, stops.stop_lat), crs="EPSG:4326")
        #self.stops=pd.read_csv(folder+'/stops.txt', sep=',')
        self.stop_times=pd.read_csv(folder+'/stop_times.txt', sep=',')
        shapes=pd.read_csv(folder+'/shapes.txt', sep=',')
        self.shapes=gpd.GeoDataFrame(shapes, geometry=gpd.points_from_xy(shapes.shape_pt_lon, shapes.shape_pt_lat))
    def RTSelection(self, trip_ids, t, r):
        # Выборка маршрутов, соответствующих выбранным поездкам

        # На вход: 
        # trip_ids - список идентификаторов поездок
        # t - dataframe всех поездок маршрутов
        # r - dataframe всех маршрутов 

        # Все поездки, соответствующие выборке
        t_selection=t[t.trip_id.isin(trip_ids)]
        # Список уникальных идентификаторов маршрутов
        route_ids=list(set(t_selection.route_id))
        # Выборка маршрутов по идентификаторам
        r_selection=r[r.route_id.isin(route_ids)]
        return t_selection, r_selection
    def SSelection(self, st_selection):
        stop_ids=list(set(st_selection.stop_id))
        s_selection=self.stops[self.stops.stop_id.isin(stop_ids)]
        return s_selection
    def STSelection(self, stop_id, st):
        # Выборка поездок маршрутов, проходящих через остановку

        # На вход: 
        # stop_id - идентификатор остановки
        # st - dataframe всех поездок маршрутов

        # Все поездки, проходящие через остановку
        st_selection=st[st.stop_id==stop_id]

        # Пустой dataframe, в который будет внесены выборки поездок маршрутов
        st_empty=pd.DataFrame(columns=st.columns)
        for _, trip in st_selection.iterrows():
            # Выборка поездок от момента прибытия на остановку stop_id до конца поездки
            #print(st)
            st_serving=st.loc[(trip.trip_id==st.trip_id)]
            #print(st_serving.iloc[0], '\n', st_serving.iloc[len(st_serving)-1])
            #Если маршрут круговой (ID остановок в начале и конце совпадают), то выбрать всю последовательность
            if st_serving.iloc[len(st_serving)-1]['stop_id']==st_serving.iloc[0]['stop_id']:
                #print(st_serving)
                #st_serving=st_serving.drop_duplicates(subset=['trip_id', 'stop_sequence', 'stop_id'], keep='first')
                print(st_serving.value_counts())
            else:
                st_serving=st.loc[(trip.trip_id==st.trip_id) & (trip.stop_sequence<=st.stop_sequence)]
                # Обновление порядка остановок
                st_serving['stop_sequence']=st_serving['stop_sequence']-trip.stop_sequence+1
            # Конкатенация пустого dataframe с выборкой
            st_empty=pd.concat([st_empty, st_serving])
            st_empty.drop_duplicates(subset=['trip_id', 'stop_sequence', 'stop_id'], keep='first', inplace=True)
        return st_empty
    def ShapeSelection(self, stop, shape_ids, shp):
        # Выборка геометрии маршрутов
        # 
        # На вход: 
        # stop - остановка с геометрией типа точка, 
        # shape_ids - выборка идентификаторов геометрии маршрутов,
        # shp - выборка геометрии маршрутов
        dist=math.inf
        seq=None
        stop_geom=stop.iloc[0].geometry
        # Пустой dataframe, в который будет внесены выборки геометри маршрутов
        shp_empty=gpd.GeoDataFrame(columns=shp.columns)
        for shape_id in shape_ids:
            # Выборка геометрии маршрута по shape_id
            shp_selection=shp[shp.shape_id==shape_id]
            #Если маршрут круговой (геометрия остановок в начале и конце совпадают), то выбрать всю последовательность
            if shp_selection.iloc[0]['shape_pt_lat']!=shp_selection.iloc[len(shp_selection)-1]['shape_pt_lat']:
                # Нахождение точки маршрута, расстояние от которой до остановки наименьшее
                for  _, shape_point in shp_selection.iterrows():
                    meas=stop_geom.distance(shape_point.geometry)
                    if meas<=dist:
                        dist=meas
                        seq=shape_point.shape_pt_sequence
                # Найдена точка маршрута, расстояние от которой до остановки наименьшее.
                # Выборка из dataframe геометрии маршрута: seq - порядок прохождения точки маршрута.
                # Необходимо в пустой dataframe добавить все точки маршрута, которые по порядку будут не ниже, чем seq
                shp_serving=shp_selection[shp_selection.shape_pt_sequence>=seq]
            # Обновление порядка прохождения точек маршрута
                shp_serving['shape_pt_sequence']=shp_serving['shape_pt_sequence']-seq+1
            else:
                shp_serving=shp_selection
            # Конкатенация пустого dataframe с выборкой
            shp_empty=pd.concat([shp_empty, shp_serving])
        return shp_empty
    
    def GetGeomOfStop(self, stop_id):
        stop_geom=self.stops[self.stops.stop_id==stop_id]
        stop_times_selection=self.STSelection(stop_id, self.stop_times)
        stops_selection=self.SSelection(stop_times_selection)
        stop_times_selection_merge=stop_times_selection.merge(self.trips, on='trip_id', how='left')
        trip_ids=list(set(stop_times_selection_merge.trip_id))
        trips_selection, routes_selection=self.RTSelection(trip_ids, self.trips, self.routes)
        shape_ids=list(set(stop_times_selection_merge.shape_id))
        shape_selection=self.ShapeSelection(stop_geom, shape_ids, self.shapes)
        return [stops_selection, stop_times_selection, trips_selection, shape_selection, routes_selection]
    
    def SaveSelectionOfStop(self, stop_id, folder):
        stop_geom=self.stops[self.stops.stop_id==stop_id]
        stop_times_selection=self.STSelection(stop_id, self.stop_times)
        stops_selection=self.SSelection(stop_times_selection)
        stop_times_selection_merge=stop_times_selection.merge(self.trips, on='trip_id', how='left')
        trip_ids=list(set(stop_times_selection_merge.trip_id))
        trips_selection, routes_selection=self.RTSelection(trip_ids, self.trips, self.routes)
        shape_ids=list(set(stop_times_selection_merge.shape_id))
        shape_selection=self.ShapeSelection(stop_geom, shape_ids, self.shapes)

        subprocess.run(f'rm -rf {folder}/stop_{stop_id}/*', stderr=subprocess.STDOUT, shell=True)
        subprocess.run(f'mkdir -p {folder}/stop_{stop_id}', stderr=subprocess.STDOUT, shell=True)
        subprocess.run(f'mkdir -p {folder}/stop_{stop_id}/gtfs_edited', stderr=subprocess.STDOUT, shell=True)

        stops_selection.drop('geometry', axis=1).to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/stops.txt', index=False, sep=',', header=True)
        stop_times_selection.to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/stop_times.txt', index=False, sep=',', header=True)
        trips_selection.to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/trips.txt', index=False, sep=',', header=True)
        routes_selection.to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/routes.txt', index=False, sep=',', header=True)
        self.agency.to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/agency.txt', index=False, sep=',', header=True)
        self.calendar.to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/calendar.txt', index=False, sep=',', header=True)
        self.calendar_dates.to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/calendar_dates.txt', index=False, sep=',', header=True)
        shape_selection.drop('geometry', axis=1).to_csv(f'{folder}/stop_{stop_id}/gtfs_edited/shapes.txt', index=False, sep=',', header=True)
        return f'{folder}/stop_{stop_id}'
    
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
            main_headsign=route_arrivals.trip_headsign.mode()
            route_info[route_id]={'start': min, 'end': max, 'headsign': main_headsign,
                                  'route_color': route['route_color'].item(), 
                                  'route_text_color': route['route_text_color'], 'route_short_name': route['route_short_name'].item()}
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