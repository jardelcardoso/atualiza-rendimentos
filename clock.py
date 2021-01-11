
from apscheduler.schedulers.blocking import BlockingScheduler

import buscaRendimento 

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10)
def scheduled_job():
    print('This job is run every weekday at 10 am. =================')
    buscaRendimento.exec_busca()

sched.start()