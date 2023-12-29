# -*- coding: utf-8 -*-
import datetime
import os.path

import pandas as pd

import Lib
import Parser.Busy.busy_parser
import Parser.MSP.xml2csv


def parse2csv(name,
              url=None,
              spr_regions: Lib.Spr = None,
              date: datetime.date = None,
              csv_path=None) -> pd.DataFrame() | None:
    file_name = None
    if name == 'BUSY':
        if url is not None and spr_regions is not None:
            res_df = Parser.Busy.busy_parser.busy_last_date(url, spr_regions=spr_regions)[1]
            file_name = os.path.join(csv_path, 'busy_{:%Y-%m-%d}.csv'.format(date))
            res_df.to_csv(file_name, sep=';', mode='w', index=False, header=True)

    if name == 'MSP':
        file_name = os.path.join(csv_path, 'msp_{:%Y-%m-%d}.csv'.format(date))
        Parser.MSP.parse_xml_msp_2csv(xml_dir=url,
                                      csv_file=file_name,
                                      spr_regions=spr_regions)

    return file_name
