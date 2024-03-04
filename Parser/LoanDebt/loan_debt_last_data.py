# -*- coding: utf-8 -*-

import pandas as pd

import Parser.XLS
import Scaner.const as const
import Lib.Spr


def loan_debt_last_date(url: str, name: str):
    spr: Lib.Spr = Lib.Spr(const.DATA_SOURCE[name]['spr_file'])
    result = Parser.XLS.xls_reader_date_column(
        url,
        sheet_name=const.DATA_SOURCE[name]['values'][0][1],
        val_id=const.DATA_SOURCE[name]['values'][0][0],
        header=const.DATA_SOURCE[name]['header'],
        region_name_col=const.DATA_SOURCE[name]['region_col'],
        region_id_col=const.DATA_SOURCE[name]['region_id_col'],
        region_suffix=const.DATA_SOURCE[name]['region_suffix'],
        date_re=const.DATA_SOURCE[name]['archive_date_re'],
        date_format=const.DATA_SOURCE[name]['archive_date_format'],
        spr=spr)
    return result


def loan_debt_data(url: str, name: str, only_last_date: bool = True) -> pd.DataFrame | None:
    spr: Lib.Spr = Lib.Spr(const.DATA_SOURCE[name]['spr_file'])
    result = None
    for val in const.DATA_SOURCE[name]['values']:
        res = Parser.XLS.xls_reader_date_column(
            url,
            sheet_name=val[1],
            val_id=val[0],
            header=const.DATA_SOURCE[name]['header'],
            region_name_col=const.DATA_SOURCE[name]['region_col'],
            region_id_col=const.DATA_SOURCE[name]['region_id_col'],
            region_suffix=const.DATA_SOURCE[name]['region_suffix'],
            date_re=const.DATA_SOURCE[name]['archive_date_re'],
            date_format=const.DATA_SOURCE[name]['archive_date_format'],
            spr=spr,
            return_last_date=only_last_date
        )[1]
        result = pd.concat([result, res])
    return result
