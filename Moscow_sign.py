from fpdf import FPDF

from feed import Feed
def HexToRGB(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

feed=Feed('k26_static')
stop=feed.DescribeForFlag(20)
stop_name=feed.StopInfo(20).stop_name.item()
print(stop)

pdf = FPDF(format='A4')
pdf.add_font('MoscowSans', '', r"D:\fonts\Moscow Sans\MoscowSans-Regular.otf", uni=True)
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('MoscowSans', '', 32)
pdf.image("stop-01.png", x=10, y=10, w = 50, h = 50)
pdf.cell(60)
pdf.multi_cell(120, 30, stop_name, 0, 'L')
pdf.set_font('MoscowSans', '', 32)
pdf.ln(h=30)
pdf.cell(190, 20, 'Маршруты', 0, 1, 'L')
pdf.ln(h=5)
for route in list(stop.keys()):
    pdf.set_font('MoscowSans', '', 32)
    pdf.set_fill_color(*HexToRGB(stop[route]['route_color']))
    pdf.set_text_color(*HexToRGB(stop[route]['route_text_color']))
    pdf.cell(30, 20, str(stop[route]['route_short_name']), 0, 0, 'C', True)
    pdf.ln(h=25)

pdf.output('Moscow_sign.pdf')