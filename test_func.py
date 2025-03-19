import pandas as pd
import BotWoody.ds_check
import DbRedis

import Scaner
from Parser.Prom import prom_last_date
from Parser.Prom import prom_data
from Parser.Budget import budget_data

import Parser.Urls as urls


def create_users():
    print(DbRedis.db_user_add(5172447001, role='admin', username='LarinMA'))
    print(DbRedis.db_user_add(1280985750, role='admin', username='MasharginGV'))
    print(DbRedis.db_user_add(1919089583, role='operator', username='KuznecovAO'))
    print(DbRedis.db_user_add(803218706, role='operator', username='KoryahovaOA'))
    print(DbRedis.db_user_add(1475591829, role='operator', username='Kulaeva E.A.'))
    print(DbRedis.db_user_add(1575674198, role='user', username='Afanasev Pavel'))


def user_email():
    DbRedis.db_user_update(5172447001, mapping={'e_mail': 'larinma@cbr.ru'})
    DbRedis.db_user_update(1919089583, mapping={'e_mail': 'kuznetsovao@cbr.ru'})
    DbRedis.db_user_update(1475591829, mapping={'e_mail': 'kulaevaea@cbr.ru'})
    DbRedis.db_user_update(1575674198, mapping={'e_mail': 'afanasevpm@cbr.ru'})


def create_tasks():
    pass
    print(DbRedis.db_task_add('BUSY', 'МСП занятые'))
    print(DbRedis.db_task_add('MSP', 'МСП реестр'))
    print(DbRedis.db_task_add('STAFF', 'МСП персонал'))
    print(DbRedis.db_task_add('DEBT_LOAN_MSP', 'МСП в т.ч. просроч.'))
    print(DbRedis.db_task_add('DEBT_LOAN_IP', 'ИП в т.ч. просроч.'))
    print(DbRedis.db_task_add('PROM', 'Произв.осн. видов продукции'))


def grant_tasks_to_user():
    # DbRedis.db_task_add_user_file('MSP', 1919089583)
    # DbRedis.db_task_add_user_file('MSP', 803218706)
    # DbRedis.db_task_add_user_file('PROM', 1475591829)
    #
    # DbRedis.db_task_add_user_msg('MSP', 1919089583)
    # DbRedis.db_task_add_user_msg('MSP', 803218706)
    # DbRedis.db_task_add_user_msg('MSP', 5172447001)

    DbRedis.db_task_add_user_msg('BUSY', 1919089583)
    DbRedis.db_task_add_user_msg('BUSY', 803218706)
    DbRedis.db_task_add_user_msg('BUSY', 5172447001)

    DbRedis.db_task_add_user_msg('DEBT_LOAN_IP', 1919089583)
    DbRedis.db_task_add_user_msg('DEBT_LOAN_IP', 803218706)
    DbRedis.db_task_add_user_msg('DEBT_LOAN_IP', 5172447001)
    DbRedis.db_task_add_user_msg('DEBT_LOAN_MSP', 1919089583)
    DbRedis.db_task_add_user_msg('DEBT_LOAN_MSP', 803218706)
    DbRedis.db_task_add_user_msg('DEBT_LOAN_MSP', 5172447001)


    DbRedis.db_task_add_user_msg('PROM', 1475591829)
    DbRedis.db_task_add_user_msg('PROM', 5172447001)

def set_emails():
    DbRedis.db_task_add_user_email(task_name='BUSY', user_id=1919089583)
    DbRedis.db_task_add_user_email(task_name='BUSY', user_id=1575674198)
    DbRedis.db_task_add_user_email(task_name='BUSY', user_id=5172447001)

    DbRedis.db_task_add_user_email(task_name='DEBT_LOAN_IP', user_id=1919089583)
    DbRedis.db_task_add_user_email(task_name='DEBT_LOAN_IP', user_id=1575674198)
    DbRedis.db_task_add_user_email(task_name='DEBT_LOAN_MSP', user_id=1919089583)
    DbRedis.db_task_add_user_email(task_name='DEBT_LOAN_MSP', user_id=1575674198)
    DbRedis.db_task_add_user_email(task_name='PROM', user_id=1475591829)
    DbRedis.db_task_add_user_email(task_name='PROM', user_id=1575674198)


if __name__ == '__main__':
    print('------------------------')
    # Scaner.check_prom()
    # a = prom_last_date('https://rosstat.gov.ru/enterprise_industrial/')
    # prom_data(a[1])
    # print(a)
    # b = urls.url_download_file(a[1], 'c:/my/DATA/PROM/TMP', verify=False)
    # print(b)
    # print(DbRedis.get_users_by_role(['admin']))
    # print(DbRedis.db_task_add_user_email(task_name='BUSY', user_id=1919089583))
    # create_tasks()
    # print(DbRedis.db_task_get_users_email(task_name='BUSY'))
    # print(DbRedis.db_task_get_emails(task_name='MSP'))
    # print(DbRedis.db_task_get_emails(task_name='BUSY'))
    # print(DbRedis.db_task_get_emails(task_name='DEBT_LOAN_MSP'))
    # print(DbRedis.db_task_get_emails(task_name='DEBT_LOAN_IP'))
    # elist = DbRedis.db_task_get_emails(task_name='BUSY')
    # BotWoody.ds_check.send_email_attach(msg_to=elist,
    #                                     msg_subj='send busy',
    #                                     attachment_file='C:/My/DATA/RMSP/busy_2023-11-01.csv',
    #                                     filename='busy_2023-11-01.csv')
    # print(DbRedis.db_task_add('PROM', 'Произв.осн. видов продукции'))
    # a = DbRedis.db_task_get_users_msg('BUSY')
    # print(a)
    # url_budget = "https://budget.gov.ru/epbs/registry/7710568760-ASFKDOHKASSAMO/data?filtermeanstypecode=1&filter_equal_asfkbudgetlevels=16&filtercode=101;103;105;106;107;108;109;111;112;113;114;115;116;117"
    # d, a = budget_data(url_budget)
    # a.to_csv('123.csv')
    # print(d)
    # create_tasks()
    # grant_tasks_to_user()
    set_emails()
    # user_email()
