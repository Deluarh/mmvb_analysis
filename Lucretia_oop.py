# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 04:40:22 2019

@author: Phantom
"""


'''
class DataBase: #херня с селектом
    def __init__(self):
        import sqlite3
        link = 'C:\\my_progect\\mmvb_analysis.git\\moex.db'
        try:
            conn = sqlite3.connect(link)
            self.cursor = conn.cursor()
        except:
            print("ошибка подключения к базе данных")

    #interface
    def select(self, what, where, wi1h):
        search = "SELECT "# + str(what) + "FROM " + str(where) + " WHERE code = '" + str(company) +"'AND date ='"+i[0] +"';")
        self.cursor.execute(search)
        '''
        


class Balance: #для внутреннего пользования Company
    def __init__(self):
        self._currentLiabilities = None
        self._longTermLiabilities = None
        self._equity = None
        
    #interface
    def getEquity(self):
        return self._equity
    def getLongTermLiabilities(self):
        return self._longTermLiabilities
    def getCurrentLiabilities(self):
        return self._currentLiabilities
    
    def setEquity(self, equity):
        try:
            self._equity = float(equity)
        except:
            print("невозможно преобразовать -" + str(equity))
    def setLongTermLiabilities(self, longTermLiabilities):
        try:
            self._longTermLiabilities = float(longTermLiabilities)
        except:
            print("невозможно преобразовать -" + str(longTermLiabilities))
    def setCurrentLiabilities(self, currentLiabilities):
        try:
            self._currentLiabilities = float(currentLiabilities)
        except:
            print("невозможно преобразовать -" + str(currentLiabilities))

class IncomeStatement: #для внутреннего пользования Company
    def __init__(self):
        self._netIncome = None
        self._operatingIncome = None
        self._operationExpenses = None
        
    #interface
    def getNetIncome(self):
        return self._netIncome
    def getOperatingIncome(self):
        return self._operatingIncome
    def getOperationExpenses(self):
        return self._operationExpenses
    
    def setNetIncome(self, netIncome):
        try:
            self._netIncome = float(netIncome)
        except:
            print("невозможно преобразовать -" + str(netIncome))
    def setOperatingIncome(self, operatingIncome):
        try:
            self._operatingIncome = float(operatingIncome)
        except:
            print("невозможно преобразовать -" + str(operatingIncome))
    def setOperationExpenses(self, operationExpenses):
        try:
            self._operationExpenses = float(operationExpenses)
        except:
            print("невозможно преобразовать -" + str(operationExpenses))



class Company: #снимок компании во времени
    def __init__(self, compName, datetmp):
        self.companyName = compName
        self.date = datetmp
        
        self.balance = Balance()
        self.incomeStatement = IncomeStatement()
        self._creationOfObjects()
        
    def _cutback(self, i): # отрезаем до 3 цифр после запятой
        return float('{:.3f}'.format( i ))
    
    def _searchInDB(self,selWhat, fromWhere):
        cursor.execute("SELECT "+ selWhat +" FROM "+ fromWhere + 
                       " WHERE code = '" + self.companyName +
                       "'AND date ='"+ self.date +"';")
        temp = cursor.fetchall()
        temp = temp[0][0]
        return temp
        
    def _creationOfObjects(self):
        equity = self._searchInDB("equity", "balance")
        long_term_liabilities = self._searchInDB("long_term_liabilities", "balance")
        current_liabilities = self._searchInDB("current_liabilities", "balance")
        
        operating_income = self._searchInDB("operating_income", "income_statement")
        operation_expenses = self._searchInDB("operation_expenses", "income_statement")
        net_income = self._searchInDB("net_income", "income_statement")
        
        self.balance.setCurrentLiabilities( current_liabilities )
        self.balance.setLongTermLiabilities( long_term_liabilities )
        self.balance.setEquity( equity )
        
        self.incomeStatement.setNetIncome( net_income )
        self.incomeStatement.setOperatingIncome( operating_income )
        self.incomeStatement.setOperationExpenses( operation_expenses )
    
    #   INTERFACE
    def returnOnEquity(self): #(ROE Return On Equity) = Чистая прибыль / Собственный капитал
        roe = (self.incomeStatement.getNetIncome() / self.balance.getEquity())
        roe = self._cutback(roe)
        return roe
    
    def returnOnAssets(self): #ROA Return On Assets) = Чистая прибыль / Активы
        roa = self.incomeStatement.getNetIncome() / (self.balance.getEquity() + 
                                                self.balance.getCurrentLiabilities() + 
                                                self.balance.getLongTermLiabilities())
        roa = self._cutback(roa)
        return roa
    
    def incomeExpenses(self):
        IncomeExpenses = self.incomeStatement.getOperatingIncome() / self.incomeStatement.getOperationExpenses()
        IncomeExpenses = self._cutback(IncomeExpenses)
        return IncomeExpenses
    
    def leverageRatio(self):
        leverageRatio = (self.balance.getCurrentLiabilities() +
                         self.balance.getLongTermLiabilities()) / self.balance.getEquity()
        leverageRatio = self._cutback(leverageRatio)
        return leverageRatio                
        
    #написать реализацию методов записи текущего состояния в бд и извлечения сз бд состояния

class CompanyInTime:
    def __init__(self, company):
        
        cursor.execute("SELECT date FROM balance WHERE code = '" + company +"';")
        balance_date = cursor.fetchall()
        cursor.execute("SELECT date FROM income_statement WHERE code = '" + company +"';")
        income_statement_date = cursor.fetchall()
        date=list(set(balance_date) & set(income_statement_date))
        date = sorted(date) 
        self.date = []
        for i in date:
            self.date.append(i[0])
            
        self.vocabularyCompany = {}
        for curDate in self.date:
            self.vocabularyCompany[str(curDate)] = Company(company, curDate)
            
    def _expectedCashFlows(self):
        expectedCashFlows = []
        print(self.date)
        for curDate in self.date:
            expectedCashFlows.append(self.vocabularyCompany[str(curDate)].incomeStatement.getNetIncome())
        '''
        if x == 'USD':
            expectedCashFlows[0] = expectedCashFlows[0] * _getCourse('USD', год)
        '''
        expectedCashFlows[0] = expectedCashFlows[0] * 60
        print(expectedCashFlows)
        for curCashF in range(0, (len(expectedCashFlows)-1)):
            print("=")
            print((expectedCashFlows[curCashF + 1] - expectedCashFlows[curCashF]) - 0)
            #y = x*k + c 
            
    #   INTERFACE     
    def discountedCashFlow(self):
        self._expectedCashFlows()
        discounted = 0
        r = 0.1 #Ставка дисконтирования = Безрисковая ставка + Премия за риск
        x = 10
        print("w")
        for i in range(1, 100):
            discounted += x / ((1 + r)**i)
            #print(x / ((1 + r)**i))
        
        return discounted
    def recordinDB(self):
        #проверка на нахождение в бд 
        return
    '''
    расчет средних показателей, прогнозы для одной компании
    как просчитать эфективность менеджмента? снижающий коээфициент
    коэффициент ожидания(среды) перерасчет при каждой интерации
    '''
    
    #класс сравнивающий отраслии весь рынок
    '''
    валюта - оценка всей экономики государства 
    оценка базовых валют 
    '''
#различные программы для расчетов и занесения в базу данных
    
###############################################################################
class Сurrency():
    pass

class USD (Сurrency):
    pass

class RUB(Сurrency):
    pass

class EUR (Сurrency):
    pass

class CNY(Сurrency):
    pass


    
    
###############################################################################
import sqlite3
link = 'moex.db'
try:
    conn = sqlite3.connect(link)
    cursor = conn.cursor()
    
    
    test = Company("ABRD", "2017")
    print(test.returnOnAssets())
    print(test.returnOnEquity())
    print(test.incomeExpenses())
    print("lev")
    print(test.leverageRatio())
    try:
        test2  = CompanyInTime("ABRD")
        print(test2.discountedCashFlow())
    except:
        print("не работает")
    
    conn.close()
except:
    print("ошибка подключения к базе данных")

