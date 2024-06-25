from qgis.PyQt import QtGui


def LayoutManagement(layout_name):
    project=QgsProject.instance()
    manager=project.layoutManager()
    layoutName=layout_name
    layout_list=manager.printLayouts()
    for layout in layout_list:
        if layout.name()==layoutName:
            manager.removeLayout(layout)
    layout=QgsPrintLayout(project)
    layout.setName(layoutName) 
    manager.addLayout(layout)
    return layout
def AddPage(f, layout_name, layout, pos):
    with open(f, encoding='utf-8', mode='r') as f:
        sch=f.readlines()
        sched=[]
        for l in sch:
            l=l.split('; ')
            l1=[]
            for i in l:
                i=i.replace('\n', '')
                l1.append(i)
            sched.append(l1)

    data={'stopname': sched[0][1], 'routenum': sched[1][1], 'routecolor': sched[2][1], 'route': sched[3][1], 'description': '', 'agent': sched[-3][1], 'phone1': sched[-2][1], 'phone2': sched[-1][1]}

    weekday_sched=[]
    weekend_sched=[]
    everyday_sched=[]
    sun_sched=[]
    weekday_flag=False
    weekend_flag=False
    everyday_flag=False
    sun_flag=False
    description_flag=False
    description_i=0
    for i in range(len(sched)):
        if 'weekday' in sched[i]:
            weekday_flag=True
            weekday_i=i
        elif 'sun' in sched[i]:
            sun_flag=True
            sun_i=i
        elif 'weekend' in sched[i] :
            weekend_flag=True
            weekend_i=i
        elif 'everyday' in sched[i]:
            everyday_flag=True
            everyday_i=i
        elif 'Примечание' in sched[i]:
            description_flag=True
            description_i=i
            data['description']=sched[i][1]
        elif 'Перевозчик' in sched[i]:
            agent_i=i
    if weekday_flag and weekend_flag:
        for i in range(weekday_i+1, weekend_i, 1):
            #print(sched[i], weekday_flag, f)
            weekday_sched.append([sched[i][0], sched[i][1]])
        if description_i!=0:
            for i in range(weekend_i+1, description_i, 1):
                weekend_sched.append([sched[i][0], sched[i][1]])
        else:
            for i in range(weekend_i+1, agent_i, 1):
                weekend_sched.append([sched[i][0], sched[i][1]])
    elif everyday_flag:
        if description_i!=0:
            for i in range(everyday_i+1, description_i, 1):
                everyday_sched.append([sched[i][0], sched[i][1]])
        else:
            for i in range(everyday_i+1, agent_i, 1):
                everyday_sched.append([sched[i][0], sched[i][1]])
    elif weekday_flag and sun_flag:
        for i in range(weekday_i+1, sun_i, 1):
            #print(sched[i], weekday_flag, f)
            weekday_sched.append([sched[i][0], sched[i][1]])
        if description_i!=0:
            for i in range(sun_i+1, description_i, 1):
                sun_sched.append([sched[i][0], sched[i][1]])
        else:
            for i in range(sun_i+1, agent_i, 1):
                sun_sched.append([sched[i][0], sched[i][1]])
    if weekday_flag:
        data['weekday']=weekday_sched
    if weekend_flag:
        data['weekend']=weekend_sched
    if everyday_flag:
        data['everyday']=everyday_sched
    font="RF Tone Semibold"
    routenumfont="RF Tone Semibold"
    #добавить страницу
    page = QgsLayoutItemPage(layout)
    page.setPageSize('A4', QgsLayoutItemPage.Landscape)
    layout.pageCollection().addPage(page)

    #название остановки
    label_stop = QgsLayoutItemLabel(layout)
    label_stop.setText(data['stopname'])
    label_stop.setFont(QFont(font, 50))
    label_stop.setHAlign(Qt.AlignCenter)
    label_stop.setVAlign(Qt.AlignCenter)
    label_stop.setBackgroundColor(QColor(255,213,0,255))
    label_stop.setBackgroundEnabled(True)
    label_stop.attemptMove(QgsLayoutPoint(52.5, 5, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    label_stop.attemptResize(QgsLayoutSize(239.5, 40, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(label_stop) 

    #номер маршрута
    label_routenum = QgsLayoutItemLabel(layout)
    label_routenum.setText(data['routenum'])
    label_routenum.setFontColor(QColor(255,255,255,255))
    if len(data['routenum'])>3:
        label_routenum.setFont(QFont(routenumfont, 50))
    else:
        label_routenum.setFont(QFont(routenumfont, 50))
    label_routenum.setHAlign(Qt.AlignCenter)
    label_routenum.setVAlign(Qt.AlignCenter)
    print(data['routenum'])
    if data['routecolor']=="зеленый" or data['routecolor']=='зелёный':
        label_routenum.setBackgroundColor(QColor(97,176,58,255))
    elif data['routecolor']=="фиолетовый":
        label_routenum.setBackgroundColor(QColor(137,75,150,255))
    else:
        label_routenum.setBackgroundColor(QColor(255,255,255,255))
    label_routenum.setBackgroundEnabled(True)
    label_routenum.setFrameEnabled(False)
    label_routenum.setFrameStrokeColor(QColor(191,191,191,255))
    label_routenum.setFrameStrokeWidth(QgsLayoutMeasurement(1))
    label_routenum.attemptMove(QgsLayoutPoint(10, 50, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    label_routenum.attemptResize(QgsLayoutSize(45, 25, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(label_routenum)





    if weekday_flag:
        start_pos_h=[40, 80, 12.5, 10]
        start_pos_m=[40, 90, 12.5, 45]
        label_weekday=QgsLayoutItemLabel(layout)
        label_weekday.setText("Будни")
        label_weekday.setFont(QFont(font, 20))
        label_weekday.setHAlign(Qt.AlignCenter)
        label_weekday.setVAlign(Qt.AlignTop)
        label_weekday.setItemRotation(90.0)
        label_weekday.attemptMove(QgsLayoutPoint(38, 90, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
        label_weekday.attemptResize(QgsLayoutSize(45, 35, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(label_weekday)
        for i in range(len(data['weekday'])):
            label_houritem=QgsLayoutItemLabel(layout)
            label_houritem.setText(data['weekday'][i][0])
            label_houritem.setFont(QFont(font, 22))
            label_houritem.setVAlign(Qt.AlignCenter)
            label_houritem.setHAlign(Qt.AlignCenter)
            label_houritem.attemptMove(QgsLayoutPoint(start_pos_h[0], start_pos_h[1], QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
            label_houritem.attemptResize(QgsLayoutSize(start_pos_h[2], start_pos_h[3], QgsUnitTypes.LayoutMillimeters))
            label_houritem.setFrameEnabled(True)
            label_houritem.setFrameStrokeColor(QColor(191,191,191,255))
            label_houritem.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
            layout.addLayoutItem(label_houritem)
            label_minitem=QgsLayoutItemLabel(layout)
            label_minitem.setText(data['weekday'][i][1])
            label_minitem.setFont(QFont(font, 18))
            label_minitem.setVAlign(Qt.AlignTop)
            label_minitem.setHAlign(Qt.AlignCenter)
            label_minitem.attemptMove(QgsLayoutPoint(start_pos_m[0], start_pos_m[1], QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
            label_minitem.attemptResize(QgsLayoutSize(start_pos_m[2], start_pos_m[3], QgsUnitTypes.LayoutMillimeters))
            label_minitem.setFrameEnabled(True)
            label_minitem.setFrameStrokeColor(QColor(191,191,191,255))
            label_minitem.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
            layout.addLayoutItem(label_minitem)
            start_pos_h[0]+=12.5
            start_pos_m[0]+=12.5
            end_pos=start_pos_h

    if weekend_flag or sun_flag:
        #start_pos_h=[40, 135, 12.5, 5]
        start_pos_m=[40, 135, 12.5, 45]
        label_weekend=QgsLayoutItemLabel(layout)
        if sun_flag:
            label_weekend.setText("Воскресенье")
        else:
            label_weekend.setText("Выходные")
        label_weekend.setFont(QFont(font, 20))
        label_weekend.setHAlign(Qt.AlignCenter)
        label_weekend.setVAlign(Qt.AlignTop)
        label_weekend.setItemRotation(90.0)
        label_weekend.attemptMove(QgsLayoutPoint(38, 135, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
        label_weekend.attemptResize(QgsLayoutSize(45, 35, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(label_weekend)
        for i in range(len(data['weekend'])):
            #label_houritem=QgsLayoutItemLabel(layout)
            #label_houritem.setText(data['weekend'][i][0])
            #label_houritem.setFont(QFont(font, 22))
            #label_houritem.setVAlign(Qt.AlignCenter)
            #label_houritem.setHAlign(Qt.AlignLeft)
            #label_houritem.attemptMove(QgsLayoutPoint(start_pos_h[0], start_pos_h[1], QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
            #label_houritem.attemptResize(QgsLayoutSize(start_pos_h[2], start_pos_h[3], QgsUnitTypes.LayoutMillimeters))
            #layout.addLayoutItem(label_houritem)
            label_minitem=QgsLayoutItemLabel(layout)
            label_minitem.setText(data['weekend'][i][1])
            label_minitem.setFont(QFont(font, 18))
            label_minitem.setVAlign(Qt.AlignTop)
            label_minitem.setHAlign(Qt.AlignCenter)
            label_minitem.attemptMove(QgsLayoutPoint(start_pos_m[0], start_pos_m[1], QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
            label_minitem.attemptResize(QgsLayoutSize(start_pos_m[2], start_pos_m[3], QgsUnitTypes.LayoutMillimeters))
            label_minitem.setFrameEnabled(True)
            label_minitem.setFrameStrokeColor(QColor(191,191,191,255))
            label_minitem.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
            layout.addLayoutItem(label_minitem)
            #start_pos_h[1]+=10
            start_pos_m[0]+=12.5
        
    if everyday_flag:
        start_pos_h=[40, 80, 12.5, 10]
        start_pos_m=[40, 90, 12.5, 90]
        label_everyday=QgsLayoutItemLabel(layout)
        label_everyday.setText("Ежедневно")
        label_everyday.setFont(QFont(font, 20))
        label_everyday.setHAlign(Qt.AlignCenter)
        label_everyday.setVAlign(Qt.AlignTop)
        label_everyday.setItemRotation(90.0)
        label_everyday.attemptMove(QgsLayoutPoint(38, 90, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
        label_everyday.attemptResize(QgsLayoutSize(90, 35, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(label_everyday)
        for i in range(len(data['everyday'])):
            label_houritem=QgsLayoutItemLabel(layout)
            label_houritem.setText(data['everyday'][i][0])
            label_houritem.setFont(QFont(font, 22))
            label_houritem.setVAlign(Qt.AlignCenter)
            label_houritem.setHAlign(Qt.AlignCenter)
            label_houritem.attemptMove(QgsLayoutPoint(start_pos_h[0], start_pos_h[1], QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
            label_houritem.attemptResize(QgsLayoutSize(start_pos_h[2], start_pos_h[3], QgsUnitTypes.LayoutMillimeters))
            label_houritem.setFrameEnabled(True)
            label_houritem.setFrameStrokeColor(QColor(191,191,191,255))
            label_houritem.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
            layout.addLayoutItem(label_houritem)
            label_minitem=QgsLayoutItemLabel(layout)
            label_minitem.setText(data['everyday'][i][1])
            label_minitem.setFont(QFont(font, 18))
            if 'каждые' not in data['everyday'][i][1]:
                label_minitem.setVAlign(Qt.AlignTop)
                label_minitem.setHAlign(Qt.AlignCenter)
                label_minitem.attemptMove(QgsLayoutPoint(start_pos_m[0], start_pos_m[1], QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
                label_minitem.attemptResize(QgsLayoutSize(start_pos_m[2], start_pos_m[3], QgsUnitTypes.LayoutMillimeters))
            else:
                label_minitem.setVAlign(Qt.AlignCenter)
                label_minitem.setHAlign(Qt.AlignCenter)
                label_minitem.setItemRotation(90.0)
                label_minitem.attemptMove(QgsLayoutPoint(start_pos_m[0]+12.5, start_pos_m[1], QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
                label_minitem.attemptResize(QgsLayoutSize(start_pos_m[3], start_pos_m[2], QgsUnitTypes.LayoutMillimeters))
            label_minitem.setFrameEnabled(True)
            label_minitem.setFrameStrokeColor(QColor(191,191,191,255))
            label_minitem.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
            layout.addLayoutItem(label_minitem)
            start_pos_h[0]+=12.5
            start_pos_m[0]+=12.5

    label_route = QgsLayoutItemLabel(layout)
    label_route.setText(data['route'])
    label_route.setFont(QFont(font, 30))
    label_route.setHAlign(Qt.AlignCenter)
    label_route.setVAlign(Qt.AlignCenter)
    label_route.attemptMove(QgsLayoutPoint(60, 50, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    label_route.attemptResize(QgsLayoutSize(232, 25, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(label_route)
    label_agent=QgsLayoutItemLabel(layout)
    #label_agent.setText(f"Маршрут обслуживается {data['agent']}\nТелефон диспетчерской: {data['phone1']}\nТелефон перевозчика: {data['phone2']}")
    label_agent.setText(f"Маршрут обслуживается {data['agent']}\nТелефон диспетчерской: {data['phone1']}")
    label_agent.setFont(QFont(font, 12))
    label_agent.setVAlign(Qt.AlignTop)
    label_agent.setHAlign(Qt.AlignLeft)
    label_agent.attemptMove(QgsLayoutPoint(5, 185, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    label_agent.attemptResize(QgsLayoutSize(140, 20, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(label_agent)

    label_description2=QgsLayoutItemLabel(layout)
    label_description2.setText(f"Не пришел автобус вовремя?\nСообщите об этом нам,\nотсканировав QR-код:")
    label_description2.setFont(QFont(font, 12))
    label_description2.setVAlign(Qt.AlignTop)
    label_description2.setHAlign(Qt.AlignLeft)
    label_description2.attemptMove(QgsLayoutPoint(195, 185, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    label_description2.attemptResize(QgsLayoutSize(65, 25, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(label_description2)

    qr=QgsLayoutItemPicture(layout)
    qr.setPicturePath(r"C:\Users\gamma\qr-code2.gif")
    qr.attemptMove(QgsLayoutPoint(267, 182.5, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    qr.attemptResize(QgsLayoutSize(22.5, 22.5, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(qr)
    logo_back=QgsLayoutItemLabel(layout)
    logo_back.setText(' ')
    logo_back.setFont(QFont(font, 12))
    logo_back.setBackgroundColor(QColor(255,213,0,255))
    logo_back.setBackgroundEnabled(True)
    logo_back.setVAlign(Qt.AlignTop)
    logo_back.setHAlign(Qt.AlignLeft)
    logo_back.attemptMove(QgsLayoutPoint(5, 5, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    logo_back.attemptResize(QgsLayoutSize(48.5, 40, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(logo_back)

    logo=QgsLayoutItemPicture(layout)
    logo.setPicturePath(r"C:\Users\gamma\mt.png")
    logo.attemptMove(QgsLayoutPoint(10, 10, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    logo.attemptResize(QgsLayoutSize(40, 30, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(logo)
    #d1=QgsLayoutItemPicture(layout)
    #d1.setPicturePath(r"C:\Users\gamma\MCD_D1.png")
    #d1.setBackgroundColor(QColor(255,213,0,255))
    #d1.setBackgroundEnabled(True)
    #d1.attemptMove(QgsLayoutPoint(105, 12, QgsUnitTypes.LayoutUnit.Millimeters), page=pos)
    #d1.attemptResize(QgsLayoutSize(48, 12, QgsUnitTypes.LayoutMillimeters))
    #layout.addLayoutItem(d1)
layout_name="Расписание ЧИСТОВИК 50"
layout=LayoutManagement(layout_name)
AddPage(r"C:\Users\gamma\schedules\schedule_50a.txt", layout_name, layout, 13)
#AddPage(r"C:\Users\gamma\schedules\schedule_1.txt", layout_name, layout, 0)
#AddPage(r"C:\Users\gamma\schedules\schedule_2.txt", layout_name, layout, 1)
#AddPage(r"C:\Users\gamma\schedules\schedule_5.txt", layout_name, layout, 2)
#AddPage(r"C:\Users\gamma\schedules\schedule_9.txt", layout_name, layout, 3)
#AddPage(r"C:\Users\gamma\schedules\schedule_21a_int.txt", layout_name, layout, 4)
#AddPage(r"C:\Users\gamma\schedules\schedule_21b_int.txt", layout_name, layout, 5)
#AddPage(r"C:\Users\gamma\schedules\schedule_23.txt", layout_name, layout, 6)
#AddPage(r"C:\Users\gamma\schedules\schedule_25.txt", layout_name, layout, 7)
#AddPage(r"C:\Users\gamma\schedules\schedule_36.txt", layout_name, layout, 8)
#AddPage(r"C:\Users\gamma\schedules\schedule_38.txt", layout_name, layout, 9)
#AddPage(r"C:\Users\gamma\schedules\schedule_41.txt", layout_name, layout, 10)
#AddPage(r"C:\Users\gamma\schedules\schedule_42.txt", layout_name, layout, 11)
#AddPage(r"C:\Users\gamma\schedules\schedule_48.txt", layout_name, layout, 12)
#AddPage(r"C:\Users\gamma\schedules\schedule_50.txt", layout_name, layout, 13)
#AddPage(r"C:\Users\gamma\schedules\schedule_60.txt", layout_name, layout, 14)
#AddPage(r"C:\Users\gamma\schedules\schedule_171k.txt", layout_name, layout, 15)
#AddPage(r"C:\Users\gamma\schedules\schedule_459.txt", layout_name, layout, 16)
#layout_name="Расписание 1к 4к"
#layout=LayoutManagement(layout_name)
#AddPage(r"C:\Users\gamma\schedules\schedule_1k.txt", layout_name, layout, 0)
#AddPage(r"C:\Users\gamma\schedules\schedule_4k.txt", layout_name, layout, 1)