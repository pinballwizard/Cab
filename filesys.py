# -*- coding: utf-8 -*-

'''
Created on 09.10.2012

@author: Karbovnichiy-VY
'''

import numpy
import os
import re
import wx
import csv

class Data:
    '''New class for data'''
    def __init__(self, inputdata, path):
        self.params = {}
        self.path = path
        self._parser()
        self._data(inputdata)
        if "Time" in self.type:
            self._sfft()
            
    def max(self):
        return numpy.max(numpy.abs(self.data[:,1]))
    
    def fftmax(self):
        return numpy.max(self.fftdata[:,1])
    
    def energy(self, (r1,r2), bytime = False):
        s = 1
        if bytime:
            s = 1/(self.data[1,0]-self.data[0,0])
        E = numpy.sum(self.data[r1:r2,1]**2)/s
        return E
  
    def _parser(self):
        dictmatch = {'wiretype' : u"Многожильные|Коаксиальные|Тонкие",
                     'wire' : u"\d+.\d+-\d+-*\d+|Образец|Абсолютный экран|№\d+ \(.*\)",
                     'port' : u"[\d,]+ -- \d+|[\d,]+ -- \Э",
                     'antenna' : u"\Воз\w+|\Инд\w+|\Ёмк\w+|\Емк\w+|\Ток\w+ \w+",
                     'distance' : u"\d+см",
                     'range' : u"\Нач\w+|\Цен\w+|\Кон\w+",
                     'amplitude' : u"\d+кВ",
                     'measure' : u'\Нап\w+|\\bТок\\b'}
        for m in dictmatch:
            try:
                self.params[m] = re.findall(dictmatch[m], self.path, flags=re.UNICODE+re.IGNORECASE)[0]
            except:
                self.params[m] = None
        
        if re.findall(u"\Аттенюатор|\Атенюатор", self.path, flags=re.UNICODE+re.IGNORECASE):
            self.a_flag = True
            if re.findall(u"\~", self.path, flags=re.UNICODE+re.IGNORECASE):
                self.a_flag = False
        else:
            self.a_flag = False
                
        if self.params['range'] == None:
            self.params['range'] = self.params['distance']
            self.params['distance'] = None
        
        measuredict = {u"Напряжение" : u"Напряжение",
                       u"напряжение" : u"Напряжение",
                       u"Ток" : u"Ток",
                       u"ток" : u"Ток",
                       None : u"Напряжение"}
        unitsdict = {u"Напряжение" : u"Volts",
                     u"Ток" : u"Amps"}
        self.params['measure'] = measuredict[self.params['measure']]
        self.units = unitsdict[self.params['measure']]
            
    def _data(self, data):
        if data[0] == "x-axis,1":
            self.device = u"Oscilloscope"
            csvsplit = u','
            DataErase = 2
#            if data[1].split(csvsplit)[1] == u'Volt':
#                self.units = u"Volts"
#            elif data[1].split(csvsplit)[1] == u'Ampere':
#                self.units = u"Amps"
            if data[1].split(csvsplit)[0] == 'second':
                self.type = ["Time"]
        for n in range(0,len(data),1):
            try:
                data[n] = data[n].split(csvsplit)
            except:
                print self.path
                data[n] = data[n].split(csvsplit)
        data[0:DataErase] = []
        data = numpy.array(data, dtype = float)
        if self.device == u"Oscilloscope":
            data[:,0] = data[:,0]-data[0,0] # убираем сдвиг по времени на Осциллографе
        if self.units == u"Amps":
            data[:,1] *= 10 # Для токового щупа TCP202
        if self.a_flag == True and self.units == u"Volts":
            data[:,1] *= 100# Для аттенюатора
        self.data = data
        self.xvalue = data[:,0]
        self.yvalue = data[:,1]
            
    def _sfft (self):
        '''return ndarray[:,2]'''
        sfft = numpy.abs(numpy.fft.fft(self.yvalue))
        x = numpy.fft.fftfreq(len(sfft),self.xvalue[1]-self.xvalue[0])[0:len(sfft)/2]
        sfft = sfft[0:len(sfft)/2]*2
        self.fftdata = numpy.column_stack([x,sfft])
        self.type.append("Spectrogram")
        self.fftxvalue = self.fftdata[:,0]
        self.fftyvalue = self.fftdata[:,1]
        
class FileSys:
    def __init__(self, device = None, outputlevel = 1):
        self.device = device
        self.outputlevel = outputlevel
    
    def csvread(self, csvpath):
        '''getting information from CSV'''
        data = []
        with open(csvpath, 'r') as datafile:
#         datafile = open(csvpath, 'r')
            for row in datafile:
                data.append(row.strip())
            datafile.close()
        return data
    
    def csvwrite(self,csvfile,data):
        datafile = csv.writer(csvfile, delimiter = ' ', dialect = 'excel')
        for row in data:
            datafile.writerow(row)
        
    def rename(self,directory):
        a = lambda x: x[:-4].split('_')
        for root, dirs, files in os.walk(directory):
            n = 0
            renamedict = {}
            newname = [u'20кВ.csv', u'18кВ.csv', u'15кВ.csv', u'12кВ.csv', u'9кВ.csv', u'6кВ.csv', u'3кВ.csv']
            for name in files:
                if u'.csv' in name and u'кВ' not in name and u'defined' not in name:
                    nm = {5 : 3, 4 : 2, 3 : 1, 2 : 1}
                    num = int(a(name)[nm[len(a(name))]])
                    renamedict.update({num : name})
                if u'.csv' in name and u'кВ' in name:
                    newname.pop(newname.index(name))          
            for num in sorted(renamedict.keys(), reverse = True):
                if n > len(newname)-1:
                    os.rename(os.path.join(root, renamedict[num]), os.path.join(root, u'not defined ' + str(num) + u'.csv'))
                else:
                    os.rename(os.path.join(root, renamedict[num]), os.path.join(root, newname[n]))
                    if  self.outputlevel >= 1:
                        print root
                        print (renamedict[num] + "--->" + newname[n])
                n += 1
        print "rename DONE"
        
    def filelist(self,directory):
        '''Getting path of Data'''
        if self.device == u"Oscilloscope":
            self.rename(directory)
        pathlist=[]
        for root, dirs, files in os.walk(directory):
            for name in files:
                if u'.csv' in name :
                    path = unicode(os.path.join(root, name))
                    pathlist.append(path)
        return pathlist
                        
    def selfsort(self, data):
        count = 0
        dictwire = {}
        for element in data:
            wire = element.params['wire']
            antenna = element.params['antenna']
            port = element.params['port']
            distance = element.params['distance']
            amplitude = element.params['amplitude']
            measure = element.params['measure']
            rg = element.params['range']
            if wire in dictwire:
                if antenna in dictwire[wire]:
                    if port in dictwire[wire][antenna]:
                        if rg in dictwire[wire][antenna][port]:
                            if distance in dictwire[wire][antenna][port][rg]:
                                if amplitude in dictwire[wire][antenna][port][rg][distance]:
                                    dictwire[wire][antenna][port][rg][distance][amplitude][measure] = count
                                else:
                                    dictwire[wire][antenna][port][rg][distance][amplitude] = {}
                                    dictwire[wire][antenna][port][rg][distance][amplitude][measure] = count
                            else:
                                dictwire[wire][antenna][port][rg][distance] = {}
                                dictwire[wire][antenna][port][rg][distance][amplitude] = {}
                                dictwire[wire][antenna][port][rg][distance][amplitude][measure] = count
                        else:
                            dictwire[wire][antenna][port][rg] = {}
                            dictwire[wire][antenna][port][rg][distance] = {}
                            dictwire[wire][antenna][port][rg][distance][amplitude] = {}
                            dictwire[wire][antenna][port][rg][distance][amplitude][measure] = count
                    else:
                        dictwire[wire][antenna][port] = {}
                        dictwire[wire][antenna][port][rg] = {}
                        dictwire[wire][antenna][port][rg][distance] = {}
                        dictwire[wire][antenna][port][rg][distance][amplitude] = {}
                        dictwire[wire][antenna][port][rg][distance][amplitude][measure] = count
                else:
                    dictwire[wire][antenna] = {}
                    dictwire[wire][antenna][port] = {}
                    dictwire[wire][antenna][port][rg] = {}
                    dictwire[wire][antenna][port][rg][distance] = {}
                    dictwire[wire][antenna][port][rg][distance][amplitude] = {}
                    dictwire[wire][antenna][port][rg][distance][amplitude][measure] = count
            else:
                dictwire[wire]={}
                dictwire[wire][antenna] = {}
                dictwire[wire][antenna][port] = {}
                dictwire[wire][antenna][port][rg] = {}
                dictwire[wire][antenna][port][rg][distance] = {}
                dictwire[wire][antenna][port][rg][distance][amplitude] = {}
                dictwire[wire][antenna][port][rg][distance][amplitude][measure] = count
            count += 1
        return dictwire