# -*- coding: utf-8 -*-

import asyncio
import aiocron
import Lib
import Scaner

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.INFO)


@aiocron.crontab(Scaner.DATA_SOURCE['MSP']['cron'])
async def msp():
    await Scaner.check_msp()


@aiocron.crontab(Scaner.DATA_SOURCE['BUSY']['cron'])
async def busy():
    await Scaner.check_busy()


@aiocron.crontab(Scaner.DATA_SOURCE['DEBT_LOAN_MSP']['cron'])
async def debt_loan():
    await Scaner.check_debt_loan()

@aiocron.crontab(Scaner.DATA_SOURCE['PROM']['cron'])
async def prom():
    await Scaner.check_prom()


def main():
    pass
    # Scaner.check_msp()
    # Scaner.check_busy()
    Scaner.check_debt_loan()


if __name__ == '__main__':
    print('                                  ____')
    print(' __      __                      /_^  \\')
    print(' \\ \\ /\\ / /___  ___  __/\\__ __   ` /  /')
    print('  \\ V  V // _ \\/ _ \\/ _ `\\ V /    /  /__')
    print('   \\_/\\_/ \\___/\\___/\\_^_/ \\ /    /_____/  ')
    print('                         /_/')
    print('=======================SCANER===========================')
    print(' Сканируемые задачи:')
    for src in Scaner.DATA_SOURCE.keys():
        print(src, Scaner.DATA_SOURCE[src]['cron'])
    asyncio.get_event_loop().run_forever()
    # main()
