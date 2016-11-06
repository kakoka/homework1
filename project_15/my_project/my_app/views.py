from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.views.generic import View
from django.contrib import messages
import xml.etree.ElementTree as ET
import requests
from datetime import datetime, date, timedelta

# Create your views here.
# функция (можно вынести в отдельный файл)
# получим урл для селекта данных на сайте ЦБ РФ

def get_currency_json_data_by_date(date):
    formatter_string = "%Y-%m-%d"
    datetime_object = datetime.strptime(date, formatter_string)
    date_object = datetime_object.date()
    start_date = date_object.strftime('%d/%m/%Y')
    end_date = date_object - timedelta(days=14)
    end_date = end_date.strftime('%d/%m/%Y')
    new_url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + end_date + \
              '&date_req2=' + start_date + '&VAL_NM_RQ=R01235'
    return new_url

# функция (можно вынести в отдельный файл)
# сегенирм правильную структуру JSON
# для fusioncharts (www.fusioncharts.com)
# кстати для джанги есть модуль, но мы идем напролом

def new_json(url):
    response = requests.get(url)
    dict_curr = []
    root = ET.fromstring(response.content)
    for Record in root.findall('Record'):
        dt = Record.get('Date')
        v = Record.find('Value').text
        dict_curr.append({'label': dt, 'value': v.replace(',', '.')})
    context = {}
    context = {'data': dict_curr}
    context.update({
        "chart": {
            "caption": "2 Weeks USD/RUR course",
            "numberPrefix": "RUR",
            "yAxisMinValue": '62',
            "yAxisMaxValue": '64',
            "placeValuesInside": "0",
            "rotateValues": "0",
            "labelDisplay": "rotate",
            "valueFontColor": "#000000",
            "decimals": "4",
            "theme": "fint"
        }
    })
    return context

# /json_data/ по нему GET выдает JSON для графика для текущей даты минус 14 дней.
# Если метод POST - получаем из datepicker дату которую мы задаем.
# Кстати, на сайте ЦБ доступны сведения начиная с 01/07/1992 года.
# Валидация данных происходит непосредственно в jquery datepicker путем задания в конфиге
# диапазона дат с 01/07/1992 по текущее число.

def json_data(request):
    if request.method == 'GET':
        context = new_json(get_currency_json_data_by_date(str(datetime.now().date())))
        return JsonResponse(context, safe=False)
    if request.method == 'POST':
        global qq # ну вот этот костыль - жесть как не хорошо!!!
        get_date_from_ajax = list(request.POST)
        qq = get_date_from_ajax[0]
        context = new_json(get_currency_json_data_by_date(get_date_from_ajax[0]))
        return JsonResponse(context, safe=False)

def json_data_no(request):
    if request.method == 'GET':
        context = new_json(get_currency_json_data_by_date(qq))
        print(context)
        return JsonResponse(context, safe=False)

def index(request):
    if request.method == 'GET':
        return render(request, 'my_app/index.html')
