# -*- coding: utf-8 -*-
'''
Created on 25.09.2012

@author: Karbovnichiy-VY
'''

'''
Переделать сортировку
Добавить сохранение в базу данных
Переделать класс данных для наследования
'''

import first
import odtwrite
import time
import database
import draw
import GUI

device = u"Oscilloscope"
outputlevel = 1
showplot = False
replot = False
plot_flag = True
report_flag = True
save_flag = True

dt = lambda x,y: " " + "in" + " " + str((y-x)/60) + " " + "min"

fileproc = first.FileSys(device,outputlevel)
filedir = GUI.dirchoise(1)
savepath = GUI.dirchoise(2)

t1 = time.clock()
data = []
for path in fileproc.filelist(filedir):
    if outputlevel >= 1:
        print path
    measurment = first.Data(fileproc.csvread(path), path)
    conn = database.opendb(savepath)
    database.inittable(conn)
    database.insert(conn, measurment)
    data.append(measurment)
    if measurment.a_flag == True and outputlevel >= 2:
        print "attenuator!!!"
t2 = time.clock()
print "taking data DONE" + dt(t1,t2)
 
if plot_flag == True:
    t1 = time.clock()
    pl = draw.Draw(outputlevel, showplot, replot, save_flag)
    for element in data:
        pl.plot(element,conn)
    t2 = time.clock()
    print "plotting DONE" + dt(t1,t2)

if report_flag == True:
    t1 = time.clock()
    odtwrite.odtwrite(data, fileproc.selfsort(data), savepath, plot_flag)
    t2 = time.clock()
    print "writing DONE" + dt(t1,t2)