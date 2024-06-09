import math
from fpdf import FPDF

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
stop=A1
stop_id=1
stop_name='Станция МЦД Лобня'
pdf = FPDF(format=(475, 675))
pdf.add_font('MoscowSans', '', r"D:\fonts\Moscow Sans\MoscowSans-Regular.otf", uni=True)
pdf.add_font('MoscowSans-Bold', 'B', r"D:\fonts\Moscow Sans\MoscowSans-Bold.otf", uni=True)
pdf.alias_nb_pages()
pdf.add_page()
page=1
pdf.set_font('MoscowSans-Bold', 'B', 108)
#pdf.image("stop-01.png", x=10, y=10, w = 50, h = 50)
pdf.set_xy(20, 20)
pdf.cell(475-20-20, 40, stop_name, 0, 0, 'L')
# X Y W H
available_canvas=(20, 80, 435, 615)
pdf.set_xy(available_canvas[0], available_canvas[1])
for route in A1.keys():
    tt=A1[route]['timetable']
    print(route, len(tt))
    if len(tt)==1 and route=='bus_21':
        max_h_trips=0
        for tt_p in tt.keys():
            max_cols=len(tt.keys())
            max_h=len(tt[tt_p])
            
            for tt_m in tt[tt_p]:
                if max_h_trips<len(tt[tt_p][tt_m]):
                    max_h_trips=len(tt[tt_p][tt_m])
        #print(max_h_trips)
        x, y, w, h = available_canvas
        table_box=[x, y, w, h]
        sample_row_box=[None, None, 10*max_h_trips, 12]
        print(sample_row_box)
        # количество колонок
        cols=math.floor(table_box[2]/sample_row_box[2])
        rows=math.ceil(max_h/cols)
        print(cols, rows)

        #pdf.set_draw_color(255)
        #pdf.set_line_width(0)
        col_widths=[]
        for i in range(cols):
            col_widths.append(10)
            col_widths.append(5*max_h_trips)
        with pdf.table(width=w, col_widths=col_widths, line_height=12, align='L', gutter_width=5, gutter_height=5, first_row_as_headings=False, v_align='T', borders_layout='NONE') as table:
            
            pdf.set_font('MoscowSans-Bold', 'B', 24)
            hs = list(tt['ed'].keys())
            print(len(hs))
            for h in range(0, len(hs), cols):
                print(h)
                row = table.row()
                for j in range(cols):
                    if h+j!=len(hs):
                        print(j, hs[h+j], ' '.join(tt['ed'][hs[h+j]]))
                        pdf.set_font('MoscowSans-Bold', 'B', 30)
                        row.cell(hs[h+j])
                        pdf.set_font('MoscowSans-Bold', 'B', 24)
                        row.cell(' '.join(tt['ed'][hs[h+j]]))

pdf.output(f'stop_{stop_id}_mrg.pdf')