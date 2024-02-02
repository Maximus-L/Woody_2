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


def main():
    #
    Scaner.check_msp()
    Scaner.check_busy()


if __name__ == '__main__':
    asyncio.get_event_loop().run_forever()
    # main()
