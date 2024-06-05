from fpdf import FPDF

from feed import Feed

A1={
    'bus_21': 
    {
    'timetable': {
        'ed': {
            '05': ['35', '45', '55'],
            '06': ['05', '25', '35', '45', '55', '59'],
            '07': ['05', '14', '20', '25', '35', '45', '55'],
            '08': ['05', '10', '15', '25', '30', '35', '55'],
            '09': ['05', '15', '20', '25', '35', '40', '45', '55'],
            '10': ['05', '15', '25', '35', '45', '55'],
            '11': ['05', '15', '25', '35', '45', '50', '55'],
            '12': ['05', '15', '20', '25', '35', '45', '55', '59'],
            '13': ['05', '15', '25', '30', '35', '45', '55'],
            '14': ['05', '10', '15', '25', '35', '40', '45', '55'],
            '15': ['05', '15', '25', '35', '45', '55'],
            '16': ['05', '15', '20', '25', '35', '45', '50', '55'],
            '17': ['05', '15', '25', '30', '35', '45', '55', '59'],
            '18': ['05', '15', '25', '35', '40', '45', '55'],
            '19': ['05', '10', '15', '25', '35', '40', '45', '55'],
            '20': ['05', '25', '40', '55'],
            '21': ['05', '20', '35', '50'],
            '22': ['05', '20', '35', '55'],
            '23': ['20']
            }
    },
    'headsign': r'Лобня (м/р) Южный \nШереметьево – Терминал В',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 21
    }, 
    'bus_41': 
    {
        'timetable': {
        'ed': {
            '06': ['45'],
            '07': ['35'],
            '10': ['10'],
            '11': ['15'],
            '13': ['45'],
            '16': ['07'],
            '17': ['55'],
            '18': ['55']
            }
    },
    'headsign': r'МЦД Лобня \nМЦД Химки',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 41
    }, 'bus_48': {
        'timetable': {
        'wd': {
            '06': ['25', '45'],
            '07': ['10', '30', '50'],
            '08': ['10', '40'],
            '09': ['10', '35'],
            '10': ['00'],
            '11': ['00','30'],
            '12': ['05','30'],
            '13': ['20', '35'],
            '14': ['00','47'],
            '15': ['20'],
            '16': ['00', '32'],
            '17': ['00', '30'],
            '18': ['00', '30'],
            '19': ['02', '30'],
            '20': ['12']
            },
        'we': {
            '06': ['15'],
            '07': ['00', '30', '50'],
            '08': ['40'],
            '09': ['10'],
            '10': ['00'],
            '11': ['00','30'],
            '12': ['05','30'],
            '13': ['35'],
            '14': ['00'],
            '15': ['20'],
            '16': ['00'],
            '17': ['00', '30'],
            '18': ['00'],
            '19': ['00', '30'],
            '20': ['12']
            }
    },
    'headsign': r'МЦД Лобня \nДубровки',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 48
    }
    }

# Макет по авторской концепции
def HexToRGB(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
class Route:
    def __init__(self, route_timetable):
        self.service_cols=len(route_timetable['timetable'].keys())
        self.tt_rows={s: route_timetable['timetable'][s] for s in route_timetable['timetable'].keys()}
        self.x=0
        self.y=0
        
        self.w=0
        self.h=0
class Timetable:
    def __init__(self, timetable):
        pass


#stop_id=18
#feed=Feed('k26_static')
#stop=feed.DescribeForLayout(21, ['summer', 'all', '0'])
#stop_name=feed.StopInfo(stop_id).stop_name.item()
stop=A1
stop_id=1
stop_name='Станция МЦД Лобня'

pdf = FPDF(format=(475, 675))
pdf.add_font('MoscowSans', '', r"D:\fonts\Moscow Sans\MoscowSans-Regular.otf", uni=True)
pdf.alias_nb_pages()
pdf.add_page()
page=1
pdf.set_font('MoscowSans', '', 108)
#pdf.image("stop-01.png", x=10, y=10, w = 50, h = 50)
pdf.set_xy(20, 20)
pdf.cell(475-20-20, 40, stop_name, 0, 0, 'L')

def DefineBoxes(pdf, routes, available_canvas):
    route_ids=list(routes.keys())
    num_routes=len(route_ids)
    x, y, w, h = available_canvas
    for route_id in route_ids:
        tt=routes[route_id]['timetable']
        max_h_trips=0
        for tt_p in tt.keys():
            max_cols=len(tt.keys())
            max_h=len(tt[tt_p])
            
            for tt_m in tt[tt_p]:
                if max_h_trips<len(tt[tt_p][tt_m]):
                    max_h_trips=len(tt[tt_p][tt_m])
        min_h_size=(20, 20)
        min_m_size=(15*max_h_trips, 15)
        print(route_id, max_cols, max_h, max_h_trips)
        print(min_h_size, min_m_size)
        
    
        #global_cols_rows={s: tt[s] for s in tt.keys()} # недельные варианты: будни, выходные
        #print(global_cols_rows)
         
        
def DrawRoute(pdf, route, x, y, w, h):
    # RouteRect w, h
    rect=(70, 40)
    pdf.set_font('MoscowSans', '', 72)
    pdf.set_xy(x, y)
    pdf.set_fill_color(*HexToRGB(route['route_color']))
    pdf.set_text_color(*HexToRGB(route['route_text_color']))
    pdf.cell(*rect, str(route['route_short_name']), 0, 0, 'C', True)
    #RouteHeadsign x, y, w, h
    pdf.set_text_color(r=0)
    pdf.set_font('MoscowSans', '', 60)
    part_1, part_2 = route['headsign'].split(r'\n')
    rect_hs_align=10
    hs=(x+rect[0]+rect_hs_align, y, w-rect[0]-rect_hs_align, rect[1])
    hs1=(hs[0], hs[1], hs[2], hs[3]/2)
    hs2=(hs[0], hs[1]+hs[3]/2, hs[2], hs[3]/2)
    pdf.set_xy(hs1[0], hs1[1])
    pdf.cell(hs1[2], hs1[3], part_1, 0, 0, 'L')
    pdf.set_xy(hs2[0], hs2[1])
    pdf.cell(hs2[2], hs2[3], part_2, 0, 0, 'L')

# available_canvas: x, y, w, h
# в эту канву нужно вместить как можно большее число маршрутов
available_canvas=(20, 80, 435, 615)
DefineBoxes(pdf, stop, available_canvas)
#DrawRoute(pdf, page, stop['bus_21'], *available_canvas)
#pdf.output(f'stop_{stop_id}_mrg.pdf')