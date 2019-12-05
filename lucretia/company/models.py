from django.db import models


# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=20)  # короткое имя компании
    code = models.CharField(max_length=4)  # тикер компании на бирже
    all_name = models.CharField(max_length=200)  # прочие названия компаний для поиска по новостям
    link = models.CharField(max_length=50)  # ссылка на сайт с отчетностями
    price = models.FloatField()  # цена компании
    information = models.TextField()  # информация о компании
    number_of_shares = models.IntegerField()  # кол акций
    presence = models.BooleanField()  # наличие в листинге

    def __str__(self):
        return self.name


class Balance(models.Model):  # бухгалтерский баланс
    code = models.ForeignKey(Company,
                             on_delete=models.CASCADE,
                             related_name='Balance')  # - тикер компании на бирже
    date = models.IntegerField()  # - дата ( год отчетности)
    currency = models.CharField(max_length=3)  # - валюта

    current_liabilities = models.IntegerField()  # - краткосрочне обязательства
    long_term_liabilities = models.IntegerField()  # -долгосрочные обязательства
    equity = models.IntegerField()  # - капитал

    def __str__(self):
        return self.code


class IncomeStatement(models.Model):  # - отчет о прибылях и убытках
    code = models.ForeignKey(Company,
                             on_delete=models.CASCADE,
                             related_name='IncomeStatement')  # - тикер компании на бирже
    date = models.IntegerField()  # - дата ( год отчетности)
    currency = models.CharField(max_length=3)  # - валюта

    operating_income = models.IntegerField()  # - операционные доходы
    operation_expenses = models.IntegerField()  # - операционные расходы
    net_income = models.IntegerField()  # - чистая прибыль

    def __str__(self):
        return self.code
