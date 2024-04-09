# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

# загрузка файла конфигурации
dotenv_path = './.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# DATA sources
DATA_SOURCE = {
    'BUSY': {
        'url': 'https://rmsp.nalog.ru/',
        'store_path': os.environ.get('BUSY_STORE', default='C:/My/DATA/RMSP'),
        'store_prefix': 'busy_',
        'spr_file': './SPR/spr_b.xlsx',
        'description': 'МСП занятые',
        'cron': '5 */2 10-13 * *'
    },
    'MSP': {
        'url': 'https://www.nalog.gov.ru/opendata/7707329152-rsmp/',
        'store_path': os.environ.get('MSP_STORE', default='C:/My/DATA/XML/CSV'),
        'store_prefix': 'msp_',
        'spr_file': './SPR/regions.xlsx',
        'archive_path': os.environ.get('MSP_STORE_ARC', default='C:/My/DATA/XML/ZIP/data*.zip'),
        'archive_date_re': 'data-\d{8}',
        'archive_date_format': 'data-%d%m%Y',
        'temp_path': os.environ.get('MSP_STORE_TMP', default='C:/My/DATA/XML/TMP'),
        'description': 'МСП реестр',
        'cron': '31 */4 11-15 * *'
    },
    'DEBT_LOAN_MSP': {
        'url': 'https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_13_F_Debt_sme_subj.xlsx',
        'store_path': os.environ.get('DEBT_LOAN_MSP_STORE', default='C:/My/DATA/DEBT_LOAN/MSP'),
        'store_prefix': 'debt_msp_',
        'spr_file': './SPR/spr_b.xlsx',
        'archive_date_re': '\d{,2}-\d{,2}-\d{4}',
        'archive_date_format': '%d.%m.%Y',
        'description': 'Задолж.кред.МСП',
        'cron': '8 */3 7-20 * *',
        'values': [[56, 'МСП Итого '], [58, 'МСП в т.ч. просроч.']],
        'header': 1,
        'region_col': 'Unnamed: 0',
        'region_id_col': 'Unnamed: 1',
        'region_suffix': ' (по методологии)'
},
    'DEBT_LOAN_IP': {
        'url': 'https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_13_I_Debt_sme_subj.xlsx',
        'store_path': os.environ.get('DEBT_LOAN_IP_STORE', default='C:/My/DATA/DEBT_LOAN/IP'),
        'store_prefix': 'debt_ip_',
        'spr_file': './SPR/spr_b.xlsx',
        'archive_date_re': '\d{,2}-\d{,2}-\d{4}',
        'archive_date_format': '%d.%m.%Y',
        'description': 'Задолж.кред.ИП',
        'cron': '10 */3 7-20 * *',
        'values': [[57, 'ИП итого'], [59, 'ИП в т.ч.просроч.']],
        'header': 1,
        'region_col': 'Unnamed: 0',
        'region_id_col': 'Unnamed: 1',
        'region_suffix': ' (по методологии)'
    }

}
