#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 02:27:42 2018

@author: phantom
"""

import sqlite3
import csv


def csv_reader(file_obj):   #Read a csv file   
    reader = csv.reader(file_obj)
    arry_in = []
    for row in reader:
        celect_p = row[2]
        mark = 0
        for i in celect_p:
            mark += 1            
        if mark == 5:
            continue          
        arry_in.append(row[0])
    
    cursor.execute("SELECT code FROM company;") #WHERE link = 'None'
    all_company = cursor.fetchall()
    for i in range(0 , len(all_company)):
        all_company[i] = all_company[i][0]
   
    print("Обычная разность set(arry_in) - set(all_company) новое") #новое
    peresechenie=list(set(arry_in) - set(all_company))
    new_company = []
    for i in range(0, len (peresechenie)):
        if len(peresechenie[i]) == 4:
            new_company.append(peresechenie[i])
    print(len(new_company))
    for i in new_company:
        print(i)
        c_in = "insert into company (code, presence) values ('" +i+"','1');"
        cursor.execute(c_in)
    print("Обычная разность set(all_company) - set(arry_in) выбыло")
    out_company=list(set(all_company) - set(arry_in))
    print(len(out_company))
    print(out_company) # что выбыло из списка
    for i in out_company:
        print(i)
        link = "UPDATE company SET presence = '0' WHERE code = '" + str(i) +"';"
        print(link)
        cursor.execute(link)
        
    conn.commit()    

def csv_append(file_obj): 
    reader = csv.reader(file_obj)
    for row in reader:
        print(" ".join(row))
        #print(row[2])
        celect_p = row[2]
        mark = 0
        for i in celect_p:
            mark += 1            
            #print(i)
        if mark == 5:
            continue          
        print (row)
        print(row[0])
        price = row[1].replace(',', '.')
        print(row[2])
        link = "UPDATE company SET price = '"+price+ "', number_of_shares = '"+row[2]+"' WHERE code = '" + str(row[0]) +"';"
        print(link)
        cursor.execute(link)
        
    conn.commit()    
        
    '''
        insertToMysql = "insert into company (name, price,code,allname) values ('" + str(row[0])+"','"+str(row[1]).replace(",", ".")+"','"+str(row[2])+"','"+str(row[4])+"');"
        print(insertToMysql)
        cursor.execute(insertToMysql)
        conn.commit()
        '''

conn = sqlite3.connect('moex.db')
cursor = conn.cursor() # Создаем курсор
csv_path = 'C:\\Users\\Phantom\\Desktop\\price.csv'
with open(csv_path, "r") as f_obj:
    csv_reader(f_obj)

with open(csv_path, "r") as f_obj:
    csv_append(f_obj)

#results = cursor.fetchall()
#print(results)

#conn.close() # Не забываем закрыть соединение с базой данных