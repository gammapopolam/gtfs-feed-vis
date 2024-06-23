import subprocess
import json


gtfs_graph='kislovodsk_gtfs.json'
topo_graph='kislovodsk_topo.json'
topo_ed_graph='kislovodsk_topo_ed.json'
loom_graph='kislovodsk_loom.json'


print(subprocess.run(f'gtfs2graph -m bus gtfs_kislo | topo --smooth=1 --random-colors --max-aggr-dist=110 > {topo_graph}', shell=True))
loom = f'loom --optim-method=comb --ilp-num-threads=11 --ilp-solver=cbc --in-stat-sep-pen=12 --output-stats --write-stats < {topo_graph} > {loom_graph}'
print(subprocess.run(loom, stderr=subprocess.STDOUT, shell=True))
ts = f'transitmap --print-stats --outline-width=1  --tight-stations --line-width=11 --line-spacing=12 < {loom_graph} > kislovodsk_orig.svg'
print(subprocess.run(ts, stderr=subprocess.STDOUT, shell=True))
with open(topo_graph, 'r', encoding='utf-8') as f:
    topo = json.load(f)
#print(len(topo['features']))

deg_points=[]
station_points=[]
edges=[]
excluded_conns=[]

nodes=[]
for feature in topo['features']:
    if feature['geometry']['type']=='Point':
        nodes.append(feature)
        '''if 'station_id' in feature['properties'].keys():
            station_points.append(feature)
        elif 'excluded_conn' in feature['properties'].keys():
            excluded_conns.append(feature)
        else:
            deg_points.append(feature)'''
    else:
        edges.append(feature)

# находим hex_id для маршрутов
for edge in edges:
    lines=edge['properties']['lines']
    for line in lines:
        if line['label']=='10':
            hex10=line['id']
        elif line['label']=='11':
            hex11=line['id']
        elif line['label']=='29':
            hex29=line['id']
        elif line['label']=='18':
            hex18=line['id']
        elif line['label']=='9':
            hex9=line['id']
        elif line['label']=='16':
            hex16=line['id']
        elif line['label']=='4':
            hex4=line['id']
        elif line['label']=='13':
            hex13=line['id']
        elif line['label']=='14':
            hex14=line['id']
        elif line['label']=='12':
            hex12=line['id']
        elif line['label']=='25':
            hex25=line['id']
        elif line['label']=='23':
            hex23=line['id']
        elif line['label']=='22':
            hex22=line['id']
        elif line['label']=='27':
            hex27=line['id']
generalizer={
    '10': {'label': '10_11_29_18', 'id': hex(int(hex10, 16)+int(hex11, 16)+int(hex29, 16)+int(hex18, 16))},
    '11': {'label': '10_11_29_18', 'id': hex(int(hex10, 16)+int(hex11, 16)+int(hex29, 16)+int(hex18, 16))}, 
    '29': {'label': '10_11_29_18', 'id': hex(int(hex10, 16)+int(hex11, 16)+int(hex29, 16)+int(hex18, 16))}, 
    '18': {'label': '10_11_29_18', 'id': hex(int(hex10, 16)+int(hex11, 16)+int(hex29, 16)+int(hex18, 16))},
    '4': {'label': '4_13', 'id': hex(int(hex4, 16)+int(hex13, 16))},
    '13': {'label': '4_13', 'id': hex(int(hex4, 16)+int(hex13, 16))},
    '9': {'label': '9_16', 'id': hex(int(hex9, 16)+int(hex16, 16))},
    '16': {'label': '9_16', 'id': hex(int(hex9, 16)+int(hex16, 16))},
    '14': {'label': '14_12', 'id': hex(int(hex14, 16)+int(hex12, 16))},
    '12': {'label': '14_12', 'id': hex(int(hex14, 16)+int(hex12, 16))},
    '25': {'label': '25_23', 'id': hex(int(hex25, 16)+int(hex23, 16))},
    '23': {'label': '25_23', 'id': hex(int(hex25, 16)+int(hex23, 16))},
    '22': {'label': '22_27', 'id': hex(int(hex22, 16)+int(hex27, 16))},
    '27': {'label': '22_27', 'id': hex(int(hex22, 16)+int(hex27, 16))},
    }
for node in nodes:
    if 'excluded_conn' in node['properties'].keys():
        #print('exclude')
        for conn in node['properties']['excluded_conn']:
            if conn['line']==hex10:
                conn['line']=generalizer['10']['id']
            elif conn['line']==hex11:
                conn['line']=generalizer['11']['id']
            elif conn['line']==hex29:
                conn['line']=generalizer['29']['id']
            elif conn['line']==hex18:
                conn['line']=generalizer['18']['id']
            elif conn['line']==hex9:
                conn['line']=generalizer['9']['id']
            
            elif conn['line']==hex16:
                conn['line']=generalizer['16']['id']
            elif conn['line']==hex4:
                conn['line']=generalizer['4']['id']
            elif conn['line']==hex13:
                conn['line']=generalizer['13']['id']
            elif conn['line']==hex14:
                conn['line']=generalizer['14']['id']

            elif conn['line']==hex12:
                conn['line']=generalizer['12']['id']
            elif conn['line']==hex25:
                conn['line']=generalizer['25']['id']
            elif conn['line']==hex23:
                conn['line']=generalizer['23']['id']
            elif conn['line']==hex22:
                conn['line']=generalizer['22']['id']
            elif conn['line']==hex27:
                conn['line']=generalizer['27']['id']
    elif 'not_serving' in node['properties'].keys():
        for line_ns in node['properties']['not_serving']:
            if line_ns==hex10:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['10']['id']
            elif line_ns==hex11:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['11']['id']
            elif line_ns==hex29:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['29']['id']
            elif line_ns==hex18:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['18']['id']
            elif line_ns==hex9:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['9']['id']
            elif line_ns==hex16:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['16']['id']
            elif line_ns==hex4:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['4']['id']
            elif line_ns==hex13:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['13']['id']
            elif line_ns==hex14:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['14']['id']
            elif line_ns==hex12:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['12']['id']
            elif line_ns==hex25:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['25']['id']
            elif line_ns==hex13:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['13']['id']
            elif line_ns==hex22:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['22']['id']
            elif line_ns==hex27:
                line_ns_i=node['properties']['not_serving'].index(line_ns)
                node['properties']['not_serving'][line_ns_i]=generalizer['27']['id']

            node['properties']['not_serving']=list(set(node['properties']['not_serving']))
# меняем все 10, 11, 29, 18 на 10_11_29_18 с новым id
# после этого удаляем дубликаты
new_deg_points=[]
new_station_points=[]
new_edges=[]
new_excluded_conns=[]
for edge in edges:
    #print(edge)
    lines=edge['properties']['lines']
    dbg_lines=edge['properties']['dbg_lines'].split(',')
    for linenum in dbg_lines:
        if linenum in generalizer.keys():
            dbg_lines[dbg_lines.index(linenum)]=generalizer[linenum]['label']
    dbg_lines=",".join(list(set(dbg_lines)))
    edge['properties']['dbg_lines']=dbg_lines
    for i in range(len(lines)):
        if lines[i]['label'] in generalizer.keys():
            #edge обновляется
            lines[i]['id']=generalizer[lines[i]['label']]['id']
            lines[i]['label']=generalizer[lines[i]['label']]['label']
    #print(edge['properties']['lines'])
    edge['properties']['lines']=[dict(t) for t in {tuple(d.items()) for d in edge['properties']['lines']}]
    #edge['properties']['lines']=list(set(edge['properties']['lines']))

dumper={'type': 'FeatureCollection', 'features': [*nodes, *edges]}
with open(topo_ed_graph, 'w', encoding='cp1251') as f:
    json.dump(dumper, f)


loom_gen = f'loom --optim-method=comb --ilp-num-threads=4 --ilp-solver=glpk --in-stat-sep-pen=12 --output-stats --write-stats < {topo_ed_graph} > {loom_graph}'
print(subprocess.run(loom_gen, stderr=subprocess.STDOUT, shell=True))
ts = f'transitmap --print-stats --outline-width=1 --no-render-stations --render-dir-markers --tight-stations --line-width=11 --line-spacing=12 < {loom_graph} > kislovodsk_gen.svg'
print(subprocess.run(ts, stderr=subprocess.STDOUT, shell=True))
ts = f'transitmap --print-stats --outline-width=0 --labels --tight-stations --render-engine=mvt --line-width=4 --line-spacing=3 -z 16,17 --mvt-path=./net_tiles < {loom_graph}'
print(subprocess.run(ts, stderr=subprocess.STDOUT, shell=True))
