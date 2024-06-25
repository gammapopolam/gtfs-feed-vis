from fpdf import FPDF
import math
from feed import Feed
def HexToRGB(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
A1_1={
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
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 21, 'description': None
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
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 41, 'description': None
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
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 48, 'description': None
    }
    }
A2={
    'bus_1': 
    {
    'timetable': {
        'ed': {
            '05': ['30', '45'],
            '06': ['00', '20', '30', '40', '50'],
            '07': ['00', '10', '20', '25', '30', '40', '50'],
            '08': ['00', '10', '20', '30', '40'],
            '09': ['00', '10', '25', '45'],
            '10': ['00', '05', '20', '40'],
            '11': ['00', '10', '20', '30', '40'],
            '12': ['00', '10', '15', '30', '40', '50'],
            '13': ['00', '20', '40', '50'],
            '14': ['00', '20', '30', '45'],
            '15': ['10', '35'],
            '16': ['10', '25', '45'],
            '17': ['00', '05', '10', '25', '35', '45', '55'],
            '18': ['00', '05', '10', '25', '35', '45', '55'],
            '19': ['05', '20', '30', '40', '50'],
            '20': ['04', '15', '30', '40', '50', '55'],
            '21': ['00', '10', '23', '35', '45', '55'],
            '22': ['05', '22', '30', '40'],
            '23': ['10'],
            '00': ['05']
            }
    },
    'headsign': r'МЦД Лобня \nКрасная Поляна',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 1, 'description': 'через мкр.Катюшки'
    },
    'bus_4': 
    {
    'timetable': {
        'ed': {
            '06': ['00', '15', '30', '45', '58'],
            '07': ['00', '15', '30', '45', '58'],
            '08': ['00', '15', '29', '50'],
            '09': ['15', '25', '35'],
            '10': ['30', '40', '50'],
            '11': ['05', '25', '40', '55'],
            '12': ['10', '45', '50'],
            '13': ['10', '20', '30', '52'],
            '14': ['15', '25', '30', '35'],
            '15': ['20', '45'],
            '16': ['00', '30', '50'],
            '17': ['00', '15', '25', '30'],
            '18': ['00', '15', '23', '40'],
            '19': ['10', '20', '33', '50'],
            '20': ['10', '34', '40', '48', '50'],
            '21': ['20', '36', '45', '50'],
            '22': ['00', '36', '45', '55'],
            '23': ['20']
            }
    },
    'headsign': r'МЦД Лобня \nКрасная Поляна',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 4, 'description': None
    },
    'bus_9': 
    {
    'timetable': {
        'ed': {
            '05': ['35'],
            '06': ['05', '25', '35', '50'],
            '07': ['05', '15', '25', '35', '45', '50'],
            '08': ['05', '15', '25', '45', '55'],
            '09': ['25', '50'],
            '10': ['10', '35', '55'],
            '11': ['03', '15', '38', '57'],
            '12': ['07', '20', '30', '48'],
            '13': ['10', '27', '47', '55'],
            '14': ['10', '27', '50'],
            '15': ['00', '15', '30', '45'],
            '16': ['00', '15', '30', '50'],
            '17': ['00', '15', '30', '49'],
            '18': ['15', '20', '30', '45'],
            '19': ['05', '14', '30', '45'],
            '20': ['00', '05', '20', '42'],
            '21': ['00', '10', '20', '35', '55'],
            '22': ['10', '20', '35', '50'],
            '23': ['15', '35', '50'],
            '00': ['10', '30']
            }
    },
    'headsign': r'МЦД Лобня \nКрасная Поляна',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 9, 'description': 'через Депо'
    },
}
A3={
    'bus_23': 
    {
    'timetable': {
        'wd': {
            '05': ['55'],
            '06': ['35', '45'],
            '07': ['20', '40'],
            '08': ['10', '30', '55'],
            '09': ['50'],
            '10': ['25'],
            '11': ['30'],
            '12': ['15', '55'],
            '13': ['35'],
            '14': ['00', '30'],
            '15': ['00', '40'],
            '16': ['20', '55'],
            '17': ['25', '35'],
            '18': ['00', '35'],
            '19': ['00', '15', '35'],
            '20': ['00', '15', '40'],
            '21': ['30'],
            '23': ['00']
            },
        'we': {
            '06': ['25', '45'],
            '07': ['08', '35', '55'],
            '08': ['10', '25', '45'],
            '09': ['10', '35'],
            '10': ['20', '50'],
            '11': ['30'],
            '12': ['10', '50'],
            '13': ['25'],
            '14': ['00', '30'],
            '15': ['00', '40'],
            '16': ['20', '40'],
            '17': ['10', '30', '50'],
            '18': ['05', '30', '55'],
            '19': ['10', '30', '50'],
            '20': ['15', '35'],
            '21': ['30'],
            '23': ['00']
            }
    },
    'headsign': r'МЦД Лобня \nКруглое озеро',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 23, 'description': None
    },
}
pdf=FPDF(orientation='L', unit='mm', format='A4') # w=297 h=210
pdf.add_font('MoscowSans-Regular', '', r"D:\fonts\Moscow Sans\MoscowSans-Regular.otf", uni=True)
pdf.add_font('MoscowSans-Bold', '', r"D:\fonts\Moscow Sans\MoscowSans-Bold.otf", uni=True)
pdf.add_font('PTSans-Regular', '', r"D:\fonts\PTSans-Regular.ttf", uni=True)
pdf.add_font('PTSans-Bold', '', r"D:\fonts\PTSans-Bold.ttf", uni=True)

def print_route(pdf, route, stop_name):
    pdf.add_page()
    pdf.set_font('MoscowSans-Bold', '', 50)
    pdf.set_xy(5,5)
    pdf.set_fill_color(r=255, g=213, b=1)
    pdf.cell(57, 40, '', 0, 0, 'C', fill=True)
    pdf.image("mt.png", x=7.5, y=7.5, w = (57.25-2.5)*0.9, h = (40-2.5)*0.9)
    pdf.set_xy(60,5)
    pdf.cell(287-57, 40, stop_name, 0, 0, 'C', fill=True)

    pdf.set_xy(10, 50)
    pdf.set_fill_color(*HexToRGB(route['route_color']))
    pdf.set_text_color(*HexToRGB(route['route_text_color']))
    pdf.cell(45, 25, str(route['route_short_name']), 0, 0, 'C', True)

    pdf.set_xy(60, 50)
    pdf.set_fill_color(r=255)
    pdf.set_text_color(r=1)
    pdf.set_font('MoscowSans-Bold', '', 24)
    pdf.cell(297-60-5, 10,  route['headsign'].split(r'\n')[0], 0, 0, 'C')

    pdf.set_xy(60, 50+10)
    pdf.set_font('MoscowSans-Bold', '', 30)
    pdf.cell(297-60-5, 15, route['headsign'].split(r'\n')[1], 0, 0, 'C')
    
    tt=route['timetable']
    if len(tt)==2:
        if 'wd' in list(tt.keys()) and 'we' in list(tt.keys()):
            pdf.set_font('MoscowSans-Bold', '', 20)
            pdf.set_xy(15, 95+40)
            with pdf.rotation(angle=90, x=15):
                pdf.cell(40, 12, 'Будни', 0, 0, 'C')
            
            pdf.set_xy(15, 95+40*2)
            with pdf.rotation(angle=90, x=15):
                pdf.cell(40, 12, 'Выходные', 0, 0, 'C')
            start_pos_h=[27, 80]
            start_pos_m=[27, 80]
            hs=['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '01']
            
            for i in range(len(hs)):
                h=hs[i]
                cx, cy = start_pos_h
                pdf.set_font('MoscowSans-Bold', '', 20)
                pdf.set_xy(cx, cy)
                pdf.cell(12, 15, str(h), 1, 0, 'C')
                #TODO: multi_cell minutes is terrible, should use minute stacking

                # Hmin=10 -> 4 рейса в час
                if h in tt['wd'].keys():
                    print(tt['wd'][h])
                    ms=tt['wd'][h]
                    #ms='\r\n'.join(tt['wd'][h])
                    pdf.set_font('MoscowSans-Regular', '', 18)
                    for m in range(4):
                        pdf.set_xy(cx, cy+15+10*(m))
                        if m+1<=len(ms):
                            pdf.cell(12, 10, ms[m], 'LR', 0, 'C')
                        else:
                            pdf.cell(12, 10, '', 'LR', 0, 'C')
                    #pdf.set_xy(cx, cy+15)
                    #pdf.multi_cell(12, 40/len(tt['wd'][h]), ms, 1, 'J', print_sh=False)
                else:
                    ms=''
                    pdf.set_font('MoscowSans-Regular', '', 18)
                    pdf.set_xy(cx, cy+15)
                    pdf.cell(12, 40, ms, 1, 1, 'C')
                if h in tt['we'].keys():
                    print(tt['we'][h])
                    ms=tt['we'][h]
                    #ms='\r\n'.join(tt['we'][h])
                    pdf.set_font('MoscowSans-Regular', '', 18)
                    borders=None
                    for m in range(4):
                        pdf.set_xy(cx, cy+15+10*(m)+40)
                        
                        if m==0:
                            borders='LTR'
                        elif m+1==4:
                            borders='LBR'
                        else:
                            borders='LR'
                        print(len(ms), m, borders)
                        if m+1<=len(ms):
                            pdf.cell(12, 10, ms[m], borders, 0, 'C')
                        else:
                            pdf.cell(12, 10, '', borders, 0, 'C')
                    #pdf.set_xy(cx, cy+15+40)
                    #pdf.multi_cell(12, 40/len(tt['we'][h]), ms, 1, 'J', print_sh=False)
                else:
                    ms=''
                    pdf.set_font('MoscowSans-Regular', '', 18)
                    pdf.set_xy(cx, cy+15+40)
                    pdf.cell(12, 40, ms, 1, 1, 'C')
                start_pos_h=[27+12*(i+1), 80]
    elif len(tt)==1:
        if 'ed' in list(tt.keys()):
            pdf.set_font('MoscowSans-Bold', '', 20)
            pdf.set_xy(15, 95+40*2)
            with pdf.rotation(angle=90, x=15):
                pdf.cell(40*2, 12, 'Ежедневно', 0, 0, 'C')
            start_pos_h=[27, 80]
            start_pos_m=[27, 80]
            hs=['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '01']
            for i in range(len(hs)):
                h=hs[i]
                cx, cy = start_pos_h
                pdf.set_font('MoscowSans-Bold', '', 20)
                pdf.set_xy(cx, cy)
                pdf.cell(12, 15, str(h), 1, 0, 'C')
                
                if h in tt['ed'].keys():
                    #print(80/len(tt['ed'][h]), cx, cy+15)
                    ms='\r\n'.join(tt['ed'][h])
                    ms=tt['ed'][h]
                    pdf.set_font('MoscowSans-Regular', '', 18)
                    borders=None
                    for m in range(8):
                        pdf.set_xy(cx, cy+15+10*(m))
                        if m==0:
                            borders='LTR'
                        elif m+1==8:
                            borders='LBR'
                        else:
                            borders='LR'
                        if m+1<=len(ms):
                            pdf.cell(12, 10, ms[m], borders, 0, 'C')
                        else:
                            pdf.cell(12, 10, '', borders, 0, 'C')
                    pdf.set_xy(cx, cy+15)
                    #pdf.multi_cell(12, 80/len(tt['ed'][h]), ms, 1, 'J', print_sh=False)
                else:
                    ms=''
                    pdf.set_font('MoscowSans-Regular', '', 18)
                    pdf.set_xy(cx, cy+15)
                    pdf.cell(12, 80, ms, 1, 1, 'C')
                start_pos_h=[27+12*(i+1), 80]
            
    return pdf

pdf=print_route(pdf, A3['bus_23'], 'Станция МЦД Лобня')
pdf=print_route(pdf, A2['bus_1'], 'Станция МЦД Лобня')
pdf=print_route(pdf, A1_1['bus_21'], 'Станция МЦД Лобня')
pdf.output('old_layout.pdf')