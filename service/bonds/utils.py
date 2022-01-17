from decimal import *
import datetime
import requests
import os


def currency_exchange(fecha=None):
    getcontext().prec = 4
    token = os.environ.get('API_TOKEN')
    serie = 'SF43718'
    if fecha is None:
        fecha = datetime.date.today()
    headers = {
        'Bmx-Token': token,
        'token': token
    }
    # the API does'nt return the exchange rate on weekends
    days = datetime.timedelta(3)
    fecha_inicial = fecha - days
    url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie}/datos/{fecha_inicial.isoformat()}/{fecha.isoformat()}'     
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        json_response = r.json()
        ce = json_response['bmx']['series'][0]['datos']
        # getting the last recorded
        value = json_response['bmx']['series'][0]['datos'][-1]['dato']
        return Decimal(value)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


if __name__ == '__main__':
    pass