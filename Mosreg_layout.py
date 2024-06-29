from fpdf import FPDF
import math
from feed import Feed

A1_1={
    'bus_21': 
    {
    'timetable': {
        'ed': {
            '05': ['35', '45', '55'],
            '06': ['05', '25', '35', '45', '55'],
            '07': ['00', '05', '15', '20', '25', '35', '45', '55'],
            '08': ['05', '10', '15', '25', '30', '35', '55'],
            '09': ['05', '15', '20', '25', '35', '40', '45', '55'],
            '10': ['05', '15', '25', '35', '45', '55'],
            '11': ['05', '15', '25', '35', '45', '55'],
            '12': ['05', '15', '20', '25', '35', '45', '55'],
            '13': ['00', '05', '15', '25', '30', '35', '45', '55'],
            '14': ['05', '10', '15', '25', '35', '40', '45', '55'],
            '15': ['05', '15', '25', '35', '45', '55'],
            '16': ['05', '15', '20', '25', '35', '45', '50', '55'],
            '17': ['05', '15', '25', '30', '35', '45', '55'],
            '18': ['00', '05', '15', '25', '35', '40', '45', '55'],
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
            '07': ['10'],
            '08': ['30'],
            '12': ['10'],
            '14': ['00'],
            '16': ['30'],
            '18': ['30']
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
A1_2={
    'bus_5': 
    {
    'timetable': {
        'ed': {
            '07': ['10'],
            '08': ['10'],
            '09': ['10'],
            '11': ['10'],
            '12': ['10'],
            '14': ['10'],
            '16': ['40'],
            '17': ['40'],
            '18': ['40'],
            '19': ['40']
            }
    },
    'headsign': r'МЦД Лобня \nплатф. Луговая',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 5, 'description': None
    },
    'bus_38': 
    {
    'timetable': {
        'ed': {
            '07': ['10'],
            '08': ['15'],
            '11': ['30'],
            '12': ['45'],
            '13': ['55'],
            '15': ['40'],
            '17': ['15'],
            '19': ['00']
            }
    },
    'headsign': r'МЦД Лобня \nМЦД Долгопрудная',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 38, 'description': None
    },
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
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 4, 'description': 'без заезда в мкр.Катюшки'
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
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 9, 'description': 'через мкр.Депо'
    },
}
A3={
    'bus_23': 
    {
    'timetable': {
        'wd': {
            '05': ['55'],
            '06': ['25', '45'],
            '07': ['20', '40'],
            '08': ['10', '30', '55а'],
            '09': ['50'],
            '10': ['25'],
            '11': ['30'],
            '12': ['15', '55'],
            '13': ['35'],
            '14': ['00', '30'],
            '15': ['00', '40'],
            '16': ['20', '55'],
            '17': ['15', '35'],
            '18': ['00', '35', '55'],
            '19': ['15', '35'],
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
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 23, 'description': 'а - через мкр. Красная Поляна'
    },
    'bus_50': 
    {
    'timetable': {
        'ed': {
            '07': ['10'],
            '08': ['00а'],
            '10': ['10в'],
            '12': ['00'],
            '13': ['10', '50б'],
            '14': ['40'],
            '15': ['40а'],
            '16': ['35в'],
            '18': ['00д'],
            '19': ['10г'],
            '20': ['20'],
            '21': ['40']
            }
    },
    'headsign': r'МЦД Лобня \nРогачёво',
    'route_color': '#79A859', 'route_text_color': '#ffffff', 'route_short_name': 50, 'description': 'а - через Турбичево, б - до Рождествено, в - до Фёдоровки, \nг - через Турбичево и Телешово, д - через Телешово'
    },
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

#stop_id=18
#feed=Feed('k26_static')
#stop=feed.DescribeForLayout(21, ['summer', 'all', '0'])
#stop_name=feed.StopInfo(stop_id).stop_name.item()
def print_platform(platform, stop_id):
    stop=platform
    stop_id=stop_id
    stop_name='Станция МЦД Лобня'

    pdf = FPDF(format=(475, 675))
    pdf.add_font('MoscowSans', '', r"D:\fonts\Moscow Sans\MoscowSans-Regular.otf", uni=True)
    pdf.add_font('MoscowSans-Bold', 'B', r"D:\fonts\Moscow Sans\MoscowSans-Bold.otf", uni=True)
    pdf.alias_nb_pages()
    pdf.add_page()
    page=1
    pdf.set_font('MoscowSans', '', 108)
    #pdf.image("stop-01.png", x=10, y=10, w = 50, h = 50)
    pdf.set_xy(20, 20)
    pdf.cell(475-20-20, 40, stop_name, 0, 0, 'L')
    available_canvas=(20, 80, 435, 585)
    print(available_canvas)
    #DefineBoxes(pdf, stop, available_canvas)
    for r in stop.keys():
        print(r, available_canvas)
        if available_canvas[1]+available_canvas[3]<270:
            pdf.add_page(same=True)
            #print(pdf.get_x(), pdf.get_y())
            available_canvas=(20, 20, 435, 595)
        available_canvas = DrawRoute(pdf, stop[r], *available_canvas)
        
        if stop[r]['description'] is not None:
            available_canvas=[available_canvas[0], available_canvas[1]+20, available_canvas[2], available_canvas[3]-20]
            pdf.set_xy(available_canvas[0], available_canvas[1]-20)
            pdf.cell(580, 10, f'Примечание:')
            text=[]
            if '\n' in stop[r]['description']:
                text=stop[r]['description'].split('\n')
                for i in range(len(text)):
                    line=text[i]
                    print(line)
                    pdf.set_xy(available_canvas[0], available_canvas[1]-10)
                    available_canvas=[available_canvas[0], available_canvas[1]+10, available_canvas[2], available_canvas[3]-10]
                    pdf.cell(580, 20, f'{line}')
            else:
                line=stop[r]['description']
                pdf.set_xy(available_canvas[0], available_canvas[1]-10)
                pdf.cell(580, 20, f'{line}')
        available_canvas=[available_canvas[0], available_canvas[1]+20, available_canvas[2], available_canvas[3]-20]
    pdf.output(f'stop_{stop_id}_mrg.pdf')

def DrawRoute(pdf, route, x, y, w, h):
    # RouteRect w, h
    rect=(70, 40)
    pdf.set_font('MoscowSans', '', 72)
    pdf.set_xy(x, y)
    pdf.set_fill_color(*HexToRGB(route['route_color']))
    pdf.set_text_color(*HexToRGB(route['route_text_color']))
    pdf.cell(*rect, str(route['route_short_name']), 0, 0, 'C', True)
    pdf.set_fill_color(r=255)
    #RouteHeadsign x, y, w, h
    pdf.set_text_color(r=0)
    pdf.set_font('MoscowSans', '', 48)
    part_1, part_2 = route['headsign'].split(r'\n')
    rect_hs_align=10
    hs=(x+rect[0]+rect_hs_align, y, w-rect[0]-rect_hs_align, rect[1])
    hs1=(hs[0], hs[1], hs[2], hs[3]/2)
    hs2=(hs[0], hs[1]+hs[3]/2, hs[2], hs[3]/2)
    pdf.set_xy(hs1[0], hs1[1])
    pdf.cell(hs1[2], hs1[3], part_1, 0, 0, 'L')
    pdf.set_font('MoscowSans', '', 60)
    pdf.set_xy(hs2[0], hs2[1])
    pdf.cell(hs2[2], hs2[3], part_2, 0, 0, 'L')
    #x, y, w, h = available_canvas
    pdf.set_xy(x, hs2[1]+hs2[3]+20)

    tt=route['timetable']
    #print(route, len(tt))
    if len(tt)==1 and list(tt.keys())[0]=='ed':
        pdf.set_xy(x, y+rect[1]+10)
        pdf.set_font('MoscowSans', '', 32)
        pdf.cell(w, 10, 'Ежедневно', 0, 0, 'L')
        max_h_trips=0
        for tt_p in tt.keys():
            max_cols=len(tt.keys())
            max_h=len(tt[tt_p])
            for tt_m in tt[tt_p]:
                if max_h_trips<len(tt[tt_p][tt_m]):
                    max_h_trips=len(tt[tt_p][tt_m])
        print(max_h_trips)
        table_box=[x, y, w, h]
        sample_row_box=[None, None, 15*(max_h_trips+1)+5, 10+5]
        #print(sample_row_box)
        # количество колонок
        cols=math.floor(table_box[2]/sample_row_box[2])
        rows=math.ceil(max_h/cols)
        #print('cols, rows', cols, rows)
        pdf.set_xy(x, y+rect[1]+30)
        #pdf.set_draw_color(255)
        #pdf.set_line_width(0)
        col_widths=[]
        text_aligns=[]
        for i in range(cols):
            col_widths.append(20)
            text_aligns.append('RIGHT')
            col_widths.append(5*(max_h_trips+3))
            text_aligns.append('LEFT')
        #print(col_widths)
        pdf.set_draw_color(195)
        with pdf.table(width=w, col_widths=col_widths, borders_layout='HORIZONTAL_LINES', line_height=17, align='L', gutter_width=0, gutter_height=0, first_row_as_headings=False, v_align='T', text_align=text_aligns) as table:
            pdf.set_font('MoscowSans-Bold', 'B', 24)
            hs = list(tt['ed'].keys())
            #print(hs)
            #print(len(hs))
            for hh in range(0, len(hs), cols):
                #print(hh)
                row = table.row()
                for j in range(cols):
                    #print(hh+j)
                    if hh+j!=len(hs):
                        #print(j, hs[hh+j], ' '.join(tt['ed'][hs[hh+j]]))
                        pdf.set_font('MoscowSans-Bold', 'B', 36)
                        row.cell(hs[hh+j])
                        pdf.set_font('MoscowSans-Bold', 'B', 24)
                        row.cell(' '.join(tt['ed'][hs[hh+j]]))
                    else:
                        y=y+rect[1]+sample_row_box[3]*rows+50
                        #y+=(5+12+sample_row_box[3])*rows
                        return (x, y, w, h-((rect[1]+sample_row_box[3])*rows+50))
    elif len(tt)==2 and list(tt.keys())[0]=='wd' and list(tt.keys())[1]=='we':
        pdf.set_xy(x, y+rect[1]+10)
        pdf.set_font('MoscowSans', '', 32)
        pdf.cell(w//2, 10, 'По будням', 0, 0, 'L')
        pdf.set_xy(x+w//2, y+rect[1]+10)
        pdf.cell(w//2, 10, 'По выходным', 0, 0, 'L')

        max_h_trips=0
        for tt_p in tt.keys():
            max_cols=len(tt.keys())
            max_h=len(tt[tt_p])
            for tt_m in tt[tt_p]:
                if max_h_trips<len(tt[tt_p][tt_m]):
                    max_h_trips=len(tt[tt_p][tt_m])
        #print(max_h_trips)
        table_box_wd=[x, y, w//2, h]
        table_box_we=[x+w//2, y, w//2, h]
        sample_row_box=[None, None, 15*(max_h_trips+1)+5, 10+5]
        #print(sample_row_box)
        cols_wd=math.floor(table_box_wd[2]/sample_row_box[2])
        rows_wd=math.ceil(max_h/cols_wd)

        cols_we=math.floor(table_box_we[2]/sample_row_box[2])
        rows_we=math.ceil(max_h/cols_we)
        pdf.set_xy(table_box_wd[0], y+rect[1]+30)
        col_widths_wd=[]
        col_widths_we=[]
        text_aligns_wd=[]
        text_aligns_we=[]
        for i in range(cols_wd):
            text_aligns_wd.append('RIGHT')
            col_widths_wd.append(15)
            text_aligns_wd.append('LEFT')
            col_widths_wd.append(5*(max_h_trips+1))
        for j in range(cols_we):
            text_aligns_we.append('RIGHT')
            col_widths_we.append(15)
            text_aligns_we.append('LEFT')
            col_widths_we.append(5*(max_h_trips+1))
        available_canvas_we=None
        available_canvas_wd=None
        back_y=y
        pdf.set_draw_color(195)
        with pdf.table(width=table_box_wd[2], col_widths=col_widths_wd, borders_layout='HORIZONTAL_LINES', line_height=17, align='L', gutter_width=0, gutter_height=0, first_row_as_headings=False, v_align='T',text_align=text_aligns_wd) as table:
            pdf.set_font('MoscowSans-Bold', 'B', 24)
            hs = list(tt['wd'].keys())
            #print(hs)
            #print(len(hs))
            for hh in range(0, len(hs), cols_wd):
                #print(hh)
                row = table.row()
                for j in range(cols_wd):
                    #print(hh+j, len(hs))
                    if hh+j!=len(hs)-1:
                        #print(j, hs[hh+j], ' '.join(tt['ed'][hs[hh+j]]))
                        pdf.set_font('MoscowSans-Bold', 'B', 36)
                        row.cell(hs[hh+j])
                        pdf.set_font('MoscowSans-Bold', 'B', 24)
                        row.cell(' '.join(tt['wd'][hs[hh+j]]))
                    else:
                        y=y+rect[1]+sample_row_box[3]*rows_wd+50
                        #y+=(5+12+sample_row_box[3])*rows
                        available_canvas_wd = (x, y, w, h-((rect[1]+sample_row_box[3])*rows_wd+50))
        y=back_y
        pdf.set_xy(table_box_we[0], y+rect[1]+30)
        with pdf.table(width=table_box_we[2], col_widths=col_widths_we, borders_layout='HORIZONTAL_LINES', line_height=17, align='L', gutter_width=0, gutter_height=0, first_row_as_headings=False, v_align='T',text_align=text_aligns_we) as table:
            pdf.set_font('MoscowSans-Bold', 'B', 24)
            hs = list(tt['we'].keys())
            #print(hs)
            #print(len(hs))
            for hh in range(0, len(hs), cols_we):
                #print(hh)
                row = table.row()
                for j in range(cols_we):
                    #print(hh+j, len(hs))
                    if hh+j<len(hs)-1:
                        #print(j, hs[hh+j], ' '.join(tt['ed'][hs[hh+j]]))
                        pdf.set_font('MoscowSans-Bold', 'B', 36)
                        row.cell(hs[hh+j])
                        pdf.set_font('MoscowSans-Bold', 'B', 24)
                        row.cell(' '.join(tt['we'][hs[hh+j]]))
                    else:
                        y=y+rect[1]+sample_row_box[3]*rows_we+50
                        #y+=(5+12+sample_row_box[3])*rows
                        available_canvas_we = (x, y, w, h-((rect[1]+sample_row_box[3])*rows_we+50))
        print(available_canvas_wd, available_canvas_we)
        return available_canvas_wd

# available_canvas: x, y, w, h
# в эту канву нужно вместить как можно большее число маршрутов
A1=A1_1.copy()
A1.update(A1_2)
print_platform(A1, 1)
print_platform(A2, 2)
print_platform(A3, 3)

        