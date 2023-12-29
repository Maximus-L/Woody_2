.0# -*- coding: utf-8 -*-

import Lib
import Scaner

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.INFO)


def check_busy():
    name = 'BUSY'
    try:
        f = Lib.DLStore(name=name,
                        url=Scaner.DATA_SOURCE[name]['url'],
                        store_path=Scaner.DATA_SOURCE[name]['store_path'],
                        store_prefix=Scaner.DATA_SOURCE[name]['store_prefix'],
                        spr_file=Scaner.DATA_SOURCE[name]['spr_file']
                        )
        url_date = f.get_last_date_url()
        log.info(f'{name}: Проверка: {url_date}')
        if f.store_last_date is None or url_date > f.store_last_date:
            print('Download ...')
            fname = f.download_to_csv(url_date)
            log.info(f'{name}: Загружен: {fname}')
        else:
            log.info(f'{name}: дата  CSV актуальна')
    except Exception as e:
        log.error(e)
