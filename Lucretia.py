#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 18:38:50 2018

@author: phantom
"""
import csv
def csv_reader(file_obj):   #Read a csv file   
    reader = csv.reader(file_obj)
    for row in reader:
        #print(" ".join(row))
        #print(row[2])
        celect_p = row[2]
        mark = 0
        for i in celect_p:
            mark += 1            
            #print(i)
        if mark == 5:
            continue          
        print (row)
        insertToMysql = "insert into company (name, price,code,allname) values ('" + str(row[0])+"','"+str(row[1]).replace(",", ".")+"','"+str(row[2])+"','"+str(row[4])+"');"
        print(insertToMysql)
        cursor.execute(insertToMysql)
        conn.commit()
             
        
def rentabel(company): #нет сортировки при отсутствии значений
    print("============ROI start============")
    cursor.execute("SELECT date FROM balance WHERE code = '" + str(company) +"';")
    balance_date = cursor.fetchall()
    cursor.execute("SELECT date FROM income_statement WHERE code = '" + str(company) +"';")
    income_statement_date = cursor.fetchall()
    date=list(set(balance_date) & set(income_statement_date))
    date = sorted(date)
    arry_rent = []
    for i in date:
        arry_tmp = []
        arry_tmp.append(i[0])
        cursor.execute("SELECT equity FROM balance WHERE code = '" + str(company) +"'AND date ='"+i[0] +"';")
        equity_date = cursor.fetchall()
        equity_date = equity_date[0][0]
        
        cursor.execute("SELECT net_income FROM income_statement WHERE code = '" + str(company) +"'AND date ='"+i[0] +"';")
        net_income = cursor.fetchall()
        net_income = net_income[0][0]
        ROE = net_income / equity_date
        ROE = float('{:.3f}'.format(ROE))
        arry_tmp.append(ROE)
        
        cursor.execute("SELECT current_liabilities FROM balance WHERE code = '" + str(company) +"'AND date ='"+i[0] +"';")
        current_liabilitie = cursor.fetchall()
        current_liabilitie = current_liabilitie[0][0]
        cursor.execute("SELECT long_term_liabilities FROM balance WHERE code = '" + str(company) +"'AND date ='"+i[0] +"';")
        long_term_liabilities = cursor.fetchall()
        long_term_liabilities = long_term_liabilities[0][0]
        
        ROA = net_income / (equity_date + current_liabilitie + long_term_liabilities)
        ROA = float('{:.3f}'.format(ROA))   
        arry_tmp.append(ROA)
        
        
        #доходы/расходы
        cursor.execute("SELECT operating_income FROM income_statement WHERE code = '" + str(company) +"'AND date ='"+i[0] +"';")
        operating_income = cursor.fetchall()
        operating_income = operating_income[0][0]
        cursor.execute("SELECT operation_expenses FROM income_statement WHERE code = '" + str(company) +"'AND date ='"+i[0] +"';")
        operation_expenses = cursor.fetchall()
        operation_expenses = operation_expenses[0][0]
        i_e = operating_income / operation_expenses
        i_e = float('{:.3f}'.format(i_e))
        arry_tmp.append(i_e)
        
        arry_rent.append(arry_tmp)
    print("date, ROE, ROA, i/e")
    for i in arry_rent:
        print(i)
    
    date
#(ROE Return On Equity) = Чистая прибыль / Собственный капитал
#ROA Return On Assets) = Чистая прибыль / Активы или (Чистая прибыль+Процентный расход) / Активы

def coefficient_prise (company):
    
    cursor.execute("SELECT price FROM company WHERE code = '" + str(company) +"';")
    price = cursor.fetchall()
    price = price[0][0]
    cursor.execute("SELECT number_of_shares FROM company WHERE code = '" + str(company) +"';")
    number_of_shares = cursor.fetchall()
    number_of_shares = number_of_shares[0][0]
    cursor.execute("SELECT date FROM balance WHERE code = '" + str(company) +"';")
    last_year = cursor.fetchall()
    if not last_year: return
    temp = 0
    for i in last_year:
        if int(i[0]) > temp: temp = int(i[0])
    last_year = str(temp)
    cursor.execute("SELECT equity FROM balance WHERE code = '" + str(company) +"'AND date ='"+last_year +"';")
    equity = cursor.fetchall()
    equity = equity[0][0]
    cursor.execute("SELECT current_liabilities FROM balance WHERE code = '" + str(company)+"'AND date ='"+last_year +"';")
    current_liabilitie = cursor.fetchall()
    current_liabilitie = current_liabilitie[0][0]
    cursor.execute("SELECT long_term_liabilities FROM balance WHERE code = '" + str(company) +"'AND date ='"+last_year+"';")
    long_term_liabilities = cursor.fetchall()
    long_term_liabilities = long_term_liabilities[0][0]
    p_b = (price * number_of_shares)/ (equity+ current_liabilitie+long_term_liabilities)
    p_b =float('{:.3f}'.format(p_b))
    print('P/B    ' + str(company)+'   '+ str(p_b))
    
    
    cursor.execute("SELECT net_income FROM income_statement WHERE code = '" + str(company) +"'AND date ='"+last_year+"';")
    net_income = cursor.fetchall()
    net_income = net_income[0][0]
    p_e = (price * number_of_shares) / net_income
    p_e  =float('{:.3f}'.format(p_e))
    print('P/E    ' + str(company)+'   '+ str(p_e))

def Show_company(company): #показать информацию о компании
    cursor.execute("SELECT * FROM company WHERE code = '" + str(company) +"';")
    print(cursor.fetchall())
    #вывод информации из таблиц
    print("вывод баланса:")
    cursor.execute("SELECT * FROM balance WHERE code = '" + str(company) +"';")
    currentBalance = cursor.fetchall()
    for i in currentBalance:
        print(i)
    print("отчет о прибылях и убытках:")
    cursor.execute("SELECT * FROM income_statement WHERE code = '" + str(company) +"';")
    currentIncome_statement = cursor.fetchall()
    for i in currentIncome_statement:
        print(i)
    rentabel(company)
        
def Company_information_update(company):
    cursor.execute("SELECT link FROM company WHERE code = '" + str(company) +"';")
    link = cursor.fetchall()    
    if link[0][0]: #если есть ссылка, то открываем
        webbrowser.open(link[0][0])
    '''
    print("обновить ссылку и инфу о компании y/n?")
    i = input()
    if i == 'y':
        print("введите ссылку на компанию")
        link = input()
        print('Инвормация о компании')
        information = input()
        link = "UPDATE company SET link = '" + link + "',information='"+information + "' WHERE code = '" + str(company) +"';"
        cursor.execute(link)
        conn.commit()
        print("____сохранено____")
    print("обновить отчетность компании y/n?")
    i = input() '''
    i = 'y'
    if i == 'y':
        print('дата начала отчетности')
        date_in = input()
        print('дата конца отчетности')
        date_last = input()
        for i in range (int(date_in), (int(date_last)+1)):
            print('год ' +str(i))
            print('введите мультипликатор')
            mult = int(input())
            print('введите валюту')
            currency = input()
            
            print('введите краткосрочне обязательства')
            current_liabilities = (float(input().replace(",", "."))) * mult
            print('введите долгосрочные обязательства')
            long_term_liabilities = (float(input().replace(",", "."))) * mult
            print('введите капитал')
            equity = (float(input().replace(",", "."))) * mult
            print('введите операционные доходы')
            operating_income = (float(input().replace(",", "."))) * mult
            print('введите операционные расходы ')
            operation_expenses = (float(input().replace(",", "."))) * mult
            print('введите чистая прибыль')
            net_income = (float(input().replace(",", "."))) * mult
            print("insert into balance (code,currency, date, current_liabilities,long_term_liabilities,equity) values ('" +str(company)+"','"+str(currency)+"','"+str(i)+"','"+str(current_liabilities)+"','"+str(long_term_liabilities)+"','"+str(equity)+"');")
            print("insert into income_statement (code,currency, date,operating_income,operation_expenses,net_income) values ('" +str(company)+"','"+str(currency)+"','"+str(i)+"','"+str(operating_income)+"','"+str(operation_expenses)+"','"+str(net_income)+"');")
            cursor.execute("insert into balance (code,currency, date, current_liabilities,long_term_liabilities,equity) values ('" +str(company)+"','"+str(currency)+"','"+str(i)+"','"+str(current_liabilities)+"','"+str(long_term_liabilities)+"','"+str(equity)+"');")
            cursor.execute("insert into income_statement (code,currency, date,operating_income,operation_expenses,net_income) values ('" +str(company)+"','"+str(currency)+"','"+str(i)+"','"+str(operating_income)+"','"+str(operation_expenses)+"','"+str(net_income)+"');")
            conn.commit()
            print("_________________________сохранено_____________________________")
    
def re_search(company):
    cursor.execute("SELECT code, name,allname FROM company;") #WHERE link = 'None'
    all_company = cursor.fetchall()
    companyNamber = 1
    for company_name in all_company:
        for i in company_name:
            match = re.search(company, i)
            if match:
                print("+++++++++++++++++++++++++")
                print('Found "{}" in "{}"'.format(company, i))
                text_pos = match.span()
                print(text_pos)
                print(i[match.start():match.end()])
                print(company_name[0])
                print('+++++++++++++++++')
                Show_company(company_name[0])
                return company_name[0]
        #print(str(companyNamber) +' компания из ' +str(len(all_company)))
        companyNamber += 1
    print('Did not find "{}"'.format(company))

import sqlite3
import webbrowser
import re 
#'C:\\my_progect\\mmvb_analysis.git\\moex.db'
link = 'moex.db'
try:
    conn = sqlite3.connect(link)
    cursor = conn.cursor()
except:
    print("ошибка подключения к базе данных")


while 1:
    print ("search поиск информации о компании")
    print ("add добавление информации о компании")
    i = input()
    if i == "search":
        print ("введите компанию")
        i1 = input()
        re_search(i1)
        #Show_company(i1)
    if i == "add":
        print ("введите компанию")
        i1 = input()
        Show_company(i1)
        Company_information_update(i1)
    if i =='e':
        break
'''

cursor.execute("SELECT code FROM company WHERE presence ='1';") #WHERE link = 'None'
all_company = cursor.fetchall()
companyNamber = 1
for companyCode in all_company:
    #print(str(companyNamber) +' компания из ' +str(len(all_company)))
    companyNamber += 1
    #Show_company(companyCode[0])
    coefficient_prise (companyCode[0])
        
'''
conn.close()


#####################################
