# -*- coding: utf-8 -*-

import datetime as dt

from typing import Any
import requests
import json
import pandas as pd
from pandas import DataFrame, Series

import Lib

# COLUMNS = [
#             'date', 'filedate', 'reportdate',
#             'tofkcode', 'tofkname',
#             'budgetcode', 'budgetname', 'asfkbudgetlevels',
#             'indcode', 'indname',
#             'code', 'oktmo',
#             'sumfordate'
#            ]

COLUMNS = [
            'date', 'reportdate', 'dateupdate',
            'datatype', 'tofkcode', 'tofkname',
            'budgetcode', 'budgetname', 'oktmo',
            'pb303', 'pb306', 'pb307', 'pb308', 'pb310', 'pb311',
            'code', 'budgetlevel'
          ]





def budget_data(url, spr_regions: Lib.Spr = None) -> list[DataFrame | Series | None | Any]:
    pass
    date = None
    result = pd.DataFrame(columns=COLUMNS, index=None)
    pageSize = 1000
    x = json.loads(requests.get(url + f"&pagesize={pageSize}").text)
    page_count = x['pageCount']
    print(type(page_count))
    for page in list(range(1, page_count+1)):
        x = json.loads(requests.get(url + f"&pagesize={pageSize}&pagenum={page}").text)
        print(page, page_count)
        for one_row in x['data']:
            # cur_date = one_row['date']
            cur_date = dt.datetime.strptime(one_row['date'][:10], '%Y-%m-%d').date()
            # cur_date = dt.date(cur_date.year, cur_date.month, cur_date.day)
            if date is None or date < cur_date: date = cur_date
            r = [one_row[field_name] for field_name in COLUMNS]
            result = pd.concat([result,
                                pd.DataFrame([r], columns=COLUMNS)
                                ], ignore_index=True)
    # result['date'] = result['date'].apply(lambda y: dt.datetime.strptime(str(int(y)), '%Y%m%d'))
    result['code3'] = result['code'].apply(lambda y: str(int(y))[:3] )
    # resonedate = result.where(result['date']==date).dropna()
    # resonedate = resonedate[['oktmo', 'budgetname', 'sumfordate']].groupby(['oktmo', 'budgetname']).sum()
    return list([date, result])