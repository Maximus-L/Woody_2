# -*- coding: utf-8 -*-

import Lib
import Scaner

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.INFO)


def check_msp():
    name = 'MSP'
    try:
        f = Lib.DLStore(name=name,
                        url=Scaner.DATA_SOURCE[name]['url'],
                        store_path=Scaner.DATA_SOURCE[name]['store_path'],
                        store_prefix=Scaner.DATA_SOURCE[name]['store_prefix'],
                        archive_path=Scaner.DATA_SOURCE[name]['archive_path'],
                        archive_date_re=Scaner.DATA_SOURCE[name]['archive_date_re'],
                        archive_date_format=Scaner.DATA_SOURCE[name]['archive_date_format'],
                        temp_path=Scaner.DATA_SOURCE[name]['temp_path'],
                        spr_file=Scaner.DATA_SOURCE[name]['spr_file']
                        )
        url_date = f.get_last_date_url()
        log.info(f'{name}: Проверка: {url_date}')
        if (f.archive_store_last_date is None or
                url_date > f.archive_store_last_date):
            fname = f.download_to_arc()
            if fname is not None:
                log.info(f'{name}: Загружен: {fname}')
                f.extract_arc(f.archive_store_last_date)
                f.download_to_csv(f.archive_store_last_date)
                log.info(f'{name}: Результаты обработки помещены в CSV')
            else:
                log.info(f'{name}: НЕ Загружен: {fname}')
        else:
            log.info(f'{name}: дата  архива актуальна')
            if (f.store_last_date is None or
                    f.archive_store_last_date > f.store_last_date):
                f.extract_arc(f.archive_store_last_date)
                f.download_to_csv(f.archive_store_last_date)
                log.info(f'{name}: Результаты обработки помещены в CSV')
            else:
                log.info(f'{name}: дата  CSV актуальна')
    except Exception as e:
        log.error(e)
