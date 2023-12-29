# -*- coding: utf-8 -*-

# DATA sources
DATA_SOURCE = {
    'BUSY': {
        'url': 'https://rmsp.nalog.ru/',
        'store_path': 'C:/My/DATA/RMSP',
        'store_prefix': 'busy_',
        'spr_file': './SPR/spr_b.xlsx',
        'description': 'МСП занятые',
        'cron': '0 */2 10-12 * *'
    },
    'MSP': {
        'url': 'https://www.nalog.gov.ru/opendata/7707329152-rsmp/',
        'store_path': 'C:/My/DATA/XML/CSV',
        'store_prefix': 'msp_',
        'spr_file': './SPR/regions.xlsx',
        'archive_path': 'C:/My/DATA/XML/ZIP/data*.zip',
        'archive_date_re': 'data-\d{8}',
        'archive_date_format': 'data-%d%m%Y',
        'temp_path': 'C:/My/DATA/XML/TMP',
        'description': 'МСП реестр',
        'cron': '30 */4 11-15 * *'
    }
}
