# -*- coding: utf-8 -*-
'''
Created on 26.12.2012

@author: Karbovnichiy-VY
'''
import sqlite3
import pickle

def opendb(path = "D:\\"):
#     databasename = path + "structuremeta.db"
    databasename = ":memory:"
    try:
        conn = sqlite3.connect(database = databasename)
    except:
        print u"Невозможно создать/открыть базу данных"
    return conn

def inittable(conn):
    c = conn.cursor()
    tablename = "main"
    c.execute("DROP TABLE IF EXISTS"+ " " + tablename)
    c.execute("CREATE TABLE " + tablename +
              '''(Id INTEGER PRIMARY KEY,
                  Time BLOB, Value BLOB, Picture BLOB,
                  Frequency BLOB, FFT BLOB, FFTPicture BLOB,
                  Wiretype STRING, Wire STRING, Antenna STRING, Range STRING, Distance STRING,
                  Amplitude STRING, Units STRING)''')
    conn.commit()
    
def insert(conn, data):
    tablename = "main"
    c = conn.cursor()
    c.execute("INSERT INTO" + " " + tablename +
              '''(Time, Value, Frequency, FFT, Wiretype, Wire, Antenna, Range,
                  Distance, Amplitude, Units) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
              (pickle.dumps(data.xvalue), pickle.dumps(data.yvalue), pickle.dumps(data.fftxvalue),
               pickle.dumps(data.fftyvalue), data.params['wiretype'], data.params['wire'], data.params['antenna'],
               data.params['range'], data.params['distance'], data.params['amplitude'], data.params['measure']))
    conn.commit()

def updatetable(conn, tablename, upname, upvalue):
    c = conn.cursor()
    if not isinstance(upvalue,str):
        upvalue = pickle.dumps(upvalue)
    c.execute("UPDATE" + " " + tablename + " " + "SET" + " " + upname + "=?", (upvalue,))
    conn.commit()

def gettable(conn, tablename, grabname):    
    c = conn.cursor()
    c.execute("SELECT" + " " + grabname + " " + "FROM" + " " + tablename)
    
if __name__ == "__main__":
    class DataForTest:
        def __init__(self,limitvalue = 10):
            self.xvalue = range(1,limitvalue,1)
            self.yvalue = range(1,limitvalue,1)
            self.fftxvalue = range(1,limitvalue,1)
            self.fftyvalue = range(1,limitvalue,1)
            self.params = {}
            self.params['wiretype'] = u"coax"
            self.params['wire'] = u"600-01"
            self.params['antenna'] = u"Воздушная"
            self.params['range'] = u"Центр"
            self.params['distance'] = u"1см"
            self.params['amplitude'] = u"20кВ"
            self.params['measure'] = u"Напряжение"
    limitvalue = 10
    data1 = DataForTest(limitvalue)
    conn = opendb()
    inittable(conn)
    insert(conn, data1)
    conn.close()
    