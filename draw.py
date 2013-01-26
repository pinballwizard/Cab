# -*- coding: utf-8 -*-

'''
Created on 09.10.2012

@author: Karbovnichiy-VY
'''

import numpy
import os
import matplotlib.pyplot as plt
import matplotlib
import database

class Draw:
    def __init__(self, platform, outputlevel = 1, showplot = False, replot = False, save_flag = False):
        if platform == u"windows":
            matplotlib.rc('font',**{'family':'arial'})
        if platform == u"linux":
            matplotlib.rc('font',**{'family':'Cantarell'})
        matplotlib.pyplot.ticklabel_format(style='sci',scilimits=(-4,4),axis='both')
        self.showplot = showplot
        self.outputlevel = outputlevel
        self.replot = replot
        self.save_flag = save_flag
        
    def __labelchoiser(self, data, mtype):
        xdict = {u"Time" : u"Время (с)", u"Spectrogram" : u"Частота (Гц)"}
        ydict = {u"Volts" : u"Напряжение (В)", u"Amps" : u"Ток (А)"}
        if data.device == u"Oscilloscope":
            if mtype == u"Time":
                x = data.xvalue
                y = data.yvalue
            elif mtype == u"Spectrogram":
                x = data.fftxvalue
                y = data.fftyvalue
        xpiclabel = xdict[mtype]
        ypiclabel = ydict[data.units]
        return (x, y, xpiclabel, ypiclabel)
        
    def plot(self, data, conn):
        for mtype in data.type:
            path = unicode(data.path[:-4] + " " + mtype + ".png")
            if os.path.exists(path) == False or self.replot == True:
                (x, y, xpiclabel, ypiclabel) = self.__labelchoiser(data, mtype)
                end = self.__crop(y)
#                 fig = plt.figure()
                plt.plot(x[0:end], y[0:end], linewidth = .5)
                plt.xlabel(xpiclabel)
                plt.ylabel(ypiclabel)
                plt.grid(True)
                self.saveplot(path, conn)
                if self.showplot == True:
                    plt.show()
                plt.close("all")
            if self.outputlevel >= 1:
                print path
            if mtype == u"Time":
                data.picpath = path
            if mtype == u"Spectrogram":
                data.fftpicpath = path
                
    def saveplot(self, path, conn):
        if self.save_flag:
            plt.savefig(path, format = "png", dpi = 200)
#             g = plt.imread(path)
#             database.updatetable(conn, "main", "Picture", g)
        
    def __crop(self, y):
        normy = numpy.abs(y/numpy.max(y)) 
        normy = normy[::-1]
        h = 1
        for n in normy:
            if n > 0.05:
                end = len(y)-h
                break
            h += 1
        return end

if __name__ == "__main__":
    import re
    import sys
    platform = re.findall(u"linux|windows", sys.platform, flags=re.UNICODE+re.IGNORECASE)[0]
    class DataForTest:
        def __init__(self,limitvalue = 10):
            self.xvalue = range(1,limitvalue,1)
            self.yvalue = range(1,limitvalue,1)
            self.fftxvalue = range(1,limitvalue,1)
            self.fftyvalue = range(1,limitvalue,1)
            self.params = {}
            self.params['wiretype'] = u"multicord"
            self.params['wire'] = u"154.6290.600-01"
            self.params['antenna'] = u"Воздушная"
            self.params['range'] = u"Центр"
            self.params['distance'] = u"1см"
            self.params['amplitude'] = u"20кВ"
            self.params['measure'] = u"Напряжение"
            self.type = ["Time", "Spectrogram"]
            self.device = u"Oscilloscope"
            self.units = u"Volts"
            self.path = "D:\\1.csv"
    data1 = DataForTest()
    draw1 = Draw(platform = platform, showplot = True, save_flag = True, replot = True)
    conn = database.opendb()
    draw1.plot(data1, conn)