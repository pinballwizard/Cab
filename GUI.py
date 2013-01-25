# -*- coding: utf-8 -*-

'''
Created on 06.11.2012

@author: Karbovnichiy-VY
'''
import os
import wx

def dirchoise(v):
    '''Dialog windows for directory choice'''
    cwd = os.getcwd()
    dpath = {1 : u"D:\Многожильные", 2 : cwd}
    mess = {1: u"Выберите директорию для получения файлов", 2 : u"Выберите место для сохранения"}
    s = {1 : wx.DD_DIR_MUST_EXIST, 2 : wx.DD_CHANGE_DIR}
    app = wx.PySimpleApp()
    dialog = wx.DirDialog(None, message = mess[v], defaultPath = dpath[v], style = s[v])
    if dialog.ShowModal() == wx.ID_OK:
        return dialog.GetPath()
    dialog.Destroy()

class Frame(wx.Frame):
    def __init__(self, parent = None, id = -1, pos=wx.DefaultPosition, title='hello'):
#         size = wx.Size(510,450)
        wx.Frame.__init__(self, parent, id, title, pos)
        self.doLayout()
    
    def doLayout(self):
        panel = wx.Panel(self)
        voltage1 = wx.StaticText(panel, wx.NewId(), label = "Max Voltage")
        power1 = wx.StaticText(panel, wx.NewId(), label = "Power")
        powerps1 = wx.StaticText(panel, wx.NewId(), label = "Power per second")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel)
        sizer.Add(voltage1, border = 8)
        sizer.Add(power1, border = 8)
        sizer.Add(powerps1, border = 8)
        self.SetSizer(sizer)
        self.Layout()
        
        

class App(wx.App):

    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == "__main__": 
    app = App()
    app.MainLoop()