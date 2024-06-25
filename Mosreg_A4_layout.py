from fpdf import FPDF
import math
from feed import Feed
def HexToRGB(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
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
pdf.add_font('MoscowSans', '', r"D:\fonts\Moscow Sans\MoscowSans-Regular.otf", uni=True)
pdf.add_font('MoscowSans-Bold', 'B', r"D:\fonts\Moscow Sans\MoscowSans-Bold.otf", uni=True)

def print_route(pdf, route, stop_name):
    pdf.add_page()
    pdf.set_font('MoscowSans', '', 50)
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
    pdf.set_font('MoscowSans', '', 36)
    pdf.cell(297-60-5, 25,  str(route['headsign'].replace(r'\n', '- ')), 0, 0, 'C')
    
    tt=route['timetable']
    if len(tt)==2:
        if 'wd' in list(tt.keys()) and 'we' in list(tt.keys()):
            pdf.set_font('MoscowSans', '', 20)
            pdf.set_xy(15, 95+40)
            with pdf.rotation(angle=90, x=15):
                pdf.cell(40, 12, 'Будни', 1, 0, 'C')
            
            pdf.set_xy(15, 95+40*2)
            with pdf.rotation(angle=90, x=15):
                pdf.cell(40, 12, 'Выходные', 1, 0, 'C')
            start_pos_h=[27, 80]
            start_pos_m=[27, 80]
            hs=['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '01']
            for i in range(len(hs)):
                h=hs[i]
                cx, cy = start_pos_h
                pdf.set_xy(cx, cy)
                pdf.cell(12, 15, str(h), 1, 0, 'C')
                
                if h in tt['wd'].keys():
                    print(tt['wd'][h])
                    ms='\n'.join(tt['wd'][h])
                    pdf.set_xy(cx, cy+15)
                    pdf.cell(12, 40, ms, 1, 1, 'C')
                else:
                    ms=''
                start_pos_h=[27+12*(i+1), 80]

            
    pdf.output('old_layout.pdf')

print_route(pdf, A3['bus_23'], 'Станция МЦД Лобня')