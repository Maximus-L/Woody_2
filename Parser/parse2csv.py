# -*- coding: utf-8 -*-
import datetime
import os.path

import pandas as pd

import Lib
import Parser.Busy.busy_parser
import Parser.MSP.xml2csv
import Scaner.const as const
import Parser.LoanDebt
import Parser.Prom

def parse2csv(name,
              url=None,
              spr_regions: Lib.Spr = None,
              date: datetime.date = None,
              csv_path=None,
              last_url=None) -> pd.DataFrame() | None:
    file_name = None
    if name == 'BUSY':
        if url is not None and spr_regions is not None:
            res_df = Parser.Busy.busy_last_date(url, spr_regions=spr_regions)[1]
            file_name = os.path.join(csv_path, 'busy_{:%Y-%m-%d}.csv'.format(date))
            res_df.to_csv(file_name, sep=';', mode='w', index=False, header=True)

    if name == 'MSP':
        file_name = os.path.join(csv_path, 'msp_{:%Y-%m-%d}.csv'.format(date))
        Parser.MSP.parse_xml_msp_2csv(xml_dir=url,
                                      csv_file=file_name,
                                      spr_regions=spr_regions)
        # name = 'STAFF'
        # file_name = os.path.join(const.DATA_SOURCE[name]['store_path'],
        #                          const.DATA_SOURCE[name]['store_prefix']+'{:%Y-%m-%d}.csv'.format(date))
        # Parser.MSP.parse_xml_staff_2csv(xml_dir=url,
        #                                 csv_file=file_name)

    if name in ['DEBT_LOAN_MSP', 'DEBT_LOAN_IP']:
        file_name = os.path.join(csv_path, const.DATA_SOURCE[name]['store_prefix']+'{:%Y-%m-%d}.csv'.format(date))
        only_last_date = True
        res_df = Parser.LoanDebt.loan_debt_data(url, name, only_last_date=only_last_date)
        if res_df is not None:
            res_df.to_csv(file_name, sep=';', mode='w', index=False, header=True)
        else:
            file_name = None

    if name == 'PROM':
        file_name = os.path.join(csv_path, 'prom_{:%Y-%m-%d}.csv'.format(date))
        if last_url is not None:
            res_df = Parser.Prom.prom_data(last_url)
        if res_df is not None:
            res_df.to_csv(file_name, sep=';', mode='w', index=False, header=True)
        else:
            file_name = None

    return file_name
