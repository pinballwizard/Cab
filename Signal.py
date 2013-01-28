'''
Created on 28.01.2013

@author: Karbovnichiy-VY
'''

import filesys
import GUI
import os

if __name__ == '__main__':
    filepath = GUI.filechoise()
    f = filesys.FileSys(device = u"Oscilloscope")
    data = filesys.Data(f.csvread(filepath), filepath)
    signal = data.data[:,:]
    savepath = GUI.dirchoise(2)
    name = u"signal.csv"
    with open(savepath + os.sep + name, 'wb') as csvfile:
        f.csvwrite(csvfile, signal)
    