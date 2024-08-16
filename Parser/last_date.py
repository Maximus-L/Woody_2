# -*- coding: utf-8 -*-
import datetime as dt

import Parser.Busy
import Parser.MSP
import Parser.LoanDebt
import Parser.Prom
import Scaner.const as const

def url_data_last_date(name, url) -> dt.date | None:
    result = None
    if name == 'BUSY':
        try:
            result = Parser.Busy.busy_last_date(url)
        except Exception as e:
            result = None
        finally:
            return result
    if name == 'MSP':
        try:
            result = Parser.MSP.msp_last_date(url)
        except Exception as e:
            result = None
        finally:
            return result
    if name in ['DEBT_LOAN_MSP', 'DEBT_LOAN_IP']:
        try:
            result = Parser.LoanDebt.loan_debt_last_date(url, name)
        except Exception as e:
            result = None
        finally:
            return result

    if name == 'PROM':
        try:
            result = Parser.Prom.prom_last_date(url,
                                                fdate_re=const.DATA_SOURCE[name]['archive_date_re'],
                                                fdate_format=const.DATA_SOURCE[name]['archive_date_format'])
        except Exception as e:
            result = None
        finally:
            return result
