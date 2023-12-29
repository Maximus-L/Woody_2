# -*- coding: utf-8 -*-
import datetime as dt

import Parser.Busy
import Parser.MSP


def url_data_last_date(name, url) -> dt.date:
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
