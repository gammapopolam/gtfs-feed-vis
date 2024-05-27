from fpdf import FPDF

from feed import Feed
def HexToRGB(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def ServiceTime(start, end):
    return f"{start.split(':')[0]}:{start.split(':')[1]}...{end.split(':')[0]}:{end.split(':')[1]}"
stop_id=18
feed=Feed('k26_static')
stop=feed.DescribeForFlag(stop_id)
stop_name=feed.StopInfo(stop_id).stop_name.item()
print(stop)

pdf = FPDF(format='A4')
pdf.add_font('MoscowSans', '', r"D:\fonts\Moscow Sans\MoscowSans-Regular.otf", uni=True)
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('MoscowSans', '', 40)
pdf.image("stop-01.png", x=10, y=10, w = 50, h = 50)
pdf.cell(60)
pdf.multi_cell(120, 30, stop_name, 0, 'L')
pdf.set_font('MoscowSans', '', 32)
pdf.ln(h=20)
pdf.cell(190, 20, 'Маршруты', 0, 1, 'L')
pdf.ln(h=5)
for route in list(stop.keys()):
    pdf.set_font('MoscowSans', '', 40)
    pdf.set_fill_color(*HexToRGB(stop[route]['route_color']))
    pdf.set_text_color(*HexToRGB(stop[route]['route_text_color']))
    pdf.cell(30, 20, str(stop[route]['route_short_name']), 0, 0, 'C', True)
    pdf.cell(5, 10, '', 0, 0, 'L', False)
    pdf.set_text_color(r=0)
    pdf.cell(160, 15, str(stop[route]['headsign']), 0, 0, 'L', False)
    pdf.ln(h=15)
    pdf.cell(35, 20, '', 0, 0, 'L', False)
    pdf.set_font('MoscowSans', '', 24)
    pdf.cell(160, 5, ServiceTime(stop[route]['start'],stop[route]['end']), 0, 0, 'L', False)
    pdf.ln(h=15)

pdf.output(f'stop_{stop_id}_msc.pdf')