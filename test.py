# -*- coding: utf-8 -*-
'''
Created on 06.11.2012

@author: Karbovnichiy-VY
'''
import sqlite3
import pickle
import database
import matplotlib.pyplot as plt

conn = database.opendb()
c = conn.cursor()
c.execute('SELECT Picture FROM' + " " + "main" + " " + "WHERE id=1")
rows = c.fetchall()
# print rows
g = pickle.loads(rows[0][0])

plt.imshow(g)
plt.show()
# for row in rows :
#     print pickle.loads(row[3])
#    print [int (x) for x in row[0][1:-1].split(', ')]

#print c.fetchone()