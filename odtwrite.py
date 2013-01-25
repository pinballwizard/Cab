# -*- coding: utf-8 -*-
'''
Created on 22.10.2012

@author: Karbovnichiy-VY
'''


from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, H, LineBreak
from odf.draw import Frame, Image
from odf.table import Table, TableColumn, TableRow, TableCell
import numpy
import os

def odtwrite(data, dictwire, savepath, plot_flag = True):
    
    def ent(h,n):
        for k in range(0,n,1):
            lb = LineBreak()
            h.addElement(lb)
        return h
    
    def headerwire():
        h = H(outlinelevel=1, stylename=h1style)
        ent(h,13)
        h.addText(text = wire)
        ent(h,12)
        return h
    
    def ttb(style, intext):
        tc = TableCell()
        p = P(stylename = style, text = intext)
        tc.addElement(p)
        return tc
    
    def picprint(num):
        picref = textdoc.addPictureFromFile(data[num].picpath)
        fftpicref = textdoc.addPictureFromFile(data[num].fftpicpath)
        pf = Frame(width="8cm", height="6cm", x="0cm", y="0cm")
        pf2 = Frame(width="8cm", height="6cm", x="10cm", y="0cm")
        p = P(stylename=picturetext)
        pf.addElement(Image(href = picref))
        pf2.addElement(Image(href = fftpicref))
        p.addElement(pf)
        p.addElement(pf2)
        ent(p,1)
        p.addText(u"Рис." + str(picnum) + u' ' + data[num].params['measure'] + u" от времени и его амплитудно-частотная характеристика" )
        ent(p,1)
        return p
    
    def pictable(num):
        table = Table()
        table.addElement(TableColumn(numbercolumnsrepeated=2,stylename=tablestyle))
        for word in data[num].params.keys():
            if word in transword and data[num].params[word] != None:
                tr = TableRow()
                tr.addElement(ttb(tabletext, transword[word]))
                tr.addElement(ttb(tabletext, data[num].params[word]))
                table.addElement(tr)
        return table
    
    def sumtable():
        ad = {u"Напряжение" : u' (В)', u"Ток" : u' (А)', u"Мощность" : u' (Вт/c)'}
        table = Table()
        table.addElement(TableColumn(numbercolumnsrepeated = len(ampl)+1, stylename = tablestyle))
        tr = TableRow()
        tc = TableCell()
        tr.addElement(tc)
        for a in ampl:
            tr.addElement(ttb(tabletextbold, a))
        table.addElement(tr)
        for antenna in sorted(dictwire[wire].keys()):
            tr = TableRow()
            tr.addElement(ttb(tabletextbold, antenna))
            table.addElement(tr)
            for port in sorted(dictwire[wire][antenna].keys()):
                for m in [u"Напряжение", u"Ток", u"Мощность"]:
                    tr = TableRow()
                    tr.addElement(ttb(tabletextbold, m+ad[m]))
                    if port is not None:
                        tr.addElement(ttb(tabletextbold, port))
                    table.addElement(tr)
                    for rg in sorted(dictwire[wire][antenna][port].keys()):
                        for k in dictwire[wire][antenna][port][rg].keys():
                            if k != None:
                                b = sorted(dictwire[wire][antenna][port][rg].keys(), key = len)
                            else:
                                b = dictwire[wire][antenna][port][rg].keys()
                        for distance in b:
                            tr = TableRow()
                            tc = TableCell()
                            try:
                                p = P(text = distance + ', ' + rg)
                            except:
                                p = P(text = rg)
                            tc.addElement(p)
                            tr.addElement(tc)
                            for amplitude in ampl:
                                try:
                                    if m == u"Мощность":
                                        a = data[dictwire[wire][antenna][port][rg][distance][amplitude][u"Напряжение"]]
                                        amu = a.energy((0,len(a.xvalue)), bytime = True)
                                        amu = '{0:.03e}'.format(amu)
                                        wiretype = a.params['wiretype']
                                    else:
                                        a = data[dictwire[wire][antenna][port][rg][distance][amplitude][m]]
                                        amu = a.max()
                                        amu = '{0:.03f}'.format(amu)
                                        wiretype = a.params['wiretype']
                                except KeyError:
                                    amu = u'--'
                                tr.addElement(ttb(tabletext, amu))
                            table.addElement(tr)
        return [table, wiretype]

    for wire in sorted(dictwire.keys()):
        picnum = 1
        
        transword = {'wire':u'Кабель', 'antenna':u'Антенна', 'port':u'Порт', 'distance':u'Дальность', 'range':u'Расстояние'}
        ampl = [u'9кВ', u'12кВ', u'15кВ', u'18кВ', u'20кВ']
        
        textdoc = OpenDocumentText()
    
        h1style = Style(name = "Heading 1", family = "paragraph")
        h1style.addElement(TextProperties(attributes = {'fontfamily':"Times New Roman", 'fontsize':"24pt",'fontweight':"bold"}))
        h1style.addElement(ParagraphProperties(attributes = {'textalign':"center"}))
        textdoc.styles.addElement(h1style)
    
        t1style = Style(name = "Text 1", family = "paragraph")
        t1style.addElement(TextProperties(attributes = {'fontfamily':"Times New Roman", 'fontsize':"14pt"}))
        textdoc.styles.addElement(t1style)
    
        prepicturetext = Style(name = "Pre Picture Text", family = "paragraph")
        prepicturetext.addElement(TextProperties(attributes = {'fontfamily':"Times New Roman", 'fontsize':"12pt",'fontstyle':"italic"}))
        prepicturetext.addElement(ParagraphProperties(attributes = {'textalign':"right"}))
        textdoc.styles.addElement(prepicturetext)
    
        picturetext = Style(name = "Picture Text", family = "paragraph")
        picturetext.addElement(TextProperties(attributes = {'fontfamily':"Times New Roman", 'fontsize':"10pt",'fontstyle':"italic"}))
        picturetext.addElement(ParagraphProperties(attributes = {'textalign':"center"}))
        textdoc.styles.addElement(picturetext)
        
        tabletextbold = Style(name = "Table Text 2", family = "paragraph")
        tabletextbold.addElement(TextProperties(attributes = {'fontfamily':"Times New Roman", 'fontsize':"14pt", 'fontweight':"bold"}))
        tabletextbold.addElement(ParagraphProperties(numberlines = "false", linenumber = "0"))
        textdoc.styles.addElement(tabletextbold)
        
        tabletext = Style(name = "Table Text", family = "paragraph")
        tabletext.addElement(TextProperties(attributes = {'fontfamily':"Times New Roman", 'fontsize':"12pt"}))
        tabletext.addElement(ParagraphProperties(numberlines = "false", linenumber = "0"))
        textdoc.styles.addElement(tabletext)
    
        tablestyle = Style(name = "Table", family = "table-column")
        textdoc.automaticstyles.addElement(tablestyle)
        
        textdoc.text.addElement(headerwire())
        [st,wiretype] = sumtable()
        textdoc.text.addElement(st)
        p = P(stylename=picturetext)
        textdoc.text.addElement(p)
        if plot_flag == True:
#             amplitude = u'20кВ'
            for antenna in sorted(dictwire[wire].keys()):
                for port in sorted(dictwire[wire][antenna].keys()):
                    maxnum = {}
                    for rg in sorted(dictwire[wire][antenna][port].keys()):
                        for distance in sorted(dictwire[wire][antenna][port][rg].keys()):
                            num = []
                            for amplitude in sorted(dictwire[wire][antenna][port][rg][distance].keys()):
                                for units in sorted(dictwire[wire][antenna][port][rg][distance][amplitude].keys()):
                                    num.append(dictwire[wire][antenna][port][rg][distance][amplitude][units])
                                maxnum[data[num[0]].max()] = num
                    mn = maxnum[numpy.max(maxnum.keys())]
                    textdoc.text.addElement(pictable(mn[0]))
                    p = P(stylename=picturetext)
                    textdoc.text.addElement(p)
                    for num in mn:
                        textdoc.text.addElement(picprint(num))
                        picnum += 1
        sp = savepath + os.sep + wiretype
        if not os.path.exists(sp):
            os.mkdir(sp)
        textdoc.save(sp + os.sep + wire, True)
        