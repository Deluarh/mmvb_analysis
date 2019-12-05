import sqlite3

conn = sqlite3.connect('moex.db')
cursor = conn.cursor() # Создаем курсор
try:
    conn2 = sqlite3.connect('lucretia/db.sqlite3')
    cursor2 = conn2.cursor() # Создаем курсор

except:
    print("qwe")

cursor.execute("SELECT * FROM company;") #WHERE link = 'None'
all_company = cursor.fetchall()
for company in all_company:
    print(company)
    if not company[5]:
        info = ''
    else:
        info = company[5]
    c_in = "insert into company_company (name, code, all_name, link,  price,information, number_of_shares, presence) values ('"+company[0]+"','"+company[1]+"','"+company[2]+"','"+company[3]+"','"+str(company[4])+"','"+info+"','"+str(company[6])+"','"+str(company[7])+"');"
    print(c_in)
    cursor2.execute(c_in)
conn2.commit()


#CREATE TABLE "company" ( `name` `code`  `allname`  `link`  `price`  `information`  `number_of_shares`  `presence`
#CREATE TABLE "company_company" ("name" "code" "all_name" "link"  "price" "information" "number_of_shares" "presence"
#CREATE TABLE "company_company" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL, "code" varchar(4) NOT NULL, "all_name" varchar(200) NOT NULL, "link" varchar(50) NOT NULL, "price" real NOT NULL, "information" text NOT NULL, "number_of_shares" integer NOT NULL, "presence" bool NOT NULL)