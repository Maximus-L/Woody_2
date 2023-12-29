# -*- coding: utf-8 -*-
import os.path

import Scaner
import Lib

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/bot.log',
                                   log_level=Lib.ERROR)


def data_stores_init():
    result = []
    for data_store in Scaner.DATA_SOURCE.keys():
        store_zip_path = os.path.join(Scaner.DATA_SOURCE[data_store]['store_path'], 'zip')
        if os.path.isdir(store_zip_path):
            store_path = store_zip_path
            store_ext = 'zip'
        else:
            store_path = Scaner.DATA_SOURCE[data_store]['store_path']
            store_ext = 'csv'
        try:
            f = Lib.DLStore(name=data_store,
                            url=Scaner.DATA_SOURCE[data_store]['url'],
                            store_path=store_path,
                            store_prefix=Scaner.DATA_SOURCE[data_store]['store_prefix'],
                            store_ext=store_ext,
                            spr_file=None
                            )
            result.append(f)
        except Exception as e:
            log.error(f'Не создано хранилище {data_store}: {e}')
    return result
