# -*- coding: utf-8 -*-
import redis
import BotWoody


R_PREFIX_PRIMARY = 'Woody2:'
R_PREFIX_TASK = 'task:'
R_PREFIX_EMAIL_USERS = ':email_users'
R_PREFIX_FILES_USERS = ':files_users'
R_SET_TASKS = R_PREFIX_PRIMARY + 'tasks'


def db_task_add(name, description):
    key_name = R_PREFIX_PRIMARY + R_PREFIX_TASK + name
    res = BotWoody.r.exists(key_name)
    if res == 0:
        p = BotWoody.r.pipeline()
        p.multi()
        p.hset(name=key_name,
               mapping={'desc': description})
        p.sadd(R_SET_TASKS, name)
        res = p.execute()
    else:
        return 'Tasc exists'
    return 0 not in res


def db_task_add_user_email(task_name, user_id):
    key_name = R_PREFIX_PRIMARY + R_PREFIX_TASK + task_name + R_PREFIX_EMAIL_USERS
    res = BotWoody.r.sadd(key_name, user_id)
    return res


def db_task_del_user_email(task_name, user_id):
    key_name = R_PREFIX_PRIMARY + R_PREFIX_TASK + task_name + R_PREFIX_EMAIL_USERS
    res = BotWoody.r.srem(key_name, user_id)
    return res
