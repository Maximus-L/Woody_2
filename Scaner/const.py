# -*- coding: utf-8 -*-

# DATA sources
DATA_SOURCE = {
    'BUSY': {
        'url': 'https://rmsp.nalog.ru/',
        'store_path': 'C:/My/DATA/RMSP',
        'store_prefix': 'busy_',
        'spr_file': './SPR/spr_b.xlsx',
        'description': 'МСП занятые',
        'cron': '5 */2 10-13 * *'
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
        'cron': '31 */4 11-15 * *'
    },
    'DEBT_LOAN_MSP': {
        'url': 'https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_13_F_Debt_sme_subj.xlsx',
        'store_path': 'C:/My/DATA/DEBT_LOAN/MSP',
        'store_prefix': 'debt_msp_',
        'spr_file': './SPR/spr_b.xlsx',
        'archive_date_re': '\d{,2}-\d{,2}-\d{4}',
        'archive_date_format': '%d.%m.%Y',
        'description': 'Задолж.кред.МСП',
        'cron': '5 */3 18-25 * *',
        'values': [[56, 'МСП Итого '], [57, 'МСП в т.ч. просроч.']],
        'header': 1,
        'region_col': 'Unnamed: 0',
        'region_id_col': 'Unnamed: 1',
        'region_suffix': ' (по методологии)'
},
    'DEBT_LOAN_IP': {
        'url': 'https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_13_I_Debt_sme_subj.xlsx',
        'store_path': 'C:/My/DATA/DEBT_LOAN/IP',
        'store_prefix': 'debt_ip_',
        'spr_file': './SPR/spr_b.xlsx',
        'description': 'Задолж.кред.ИП',
        'cron': '10 */3 18-25 * *',
        'values': [[58, 'ИП Итого '], [59, 'ИП в т.ч. просроч.']],
        'header': 1,
        'region_col': 'Unnamed: 0',
        'region_id_col': 'Unnamed: 1',
        'region_suffix': ' (по методологии)'
    }

}
