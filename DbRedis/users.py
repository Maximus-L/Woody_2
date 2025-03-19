# -*- coding: utf-8 -*-
import redis
import BotWoody

BotWoody.r = redis.Redis(host="localhost", port=6379)

R_PREFIX_PRIMARY = 'Woody2:'
R_PREFIX_USER = 'user:'

R_USERS_NAME_KEY = 'name'
R_USERS_ROLE_KEY = 'role'
R_USERS_EMAIL_KEY = 'e_mail'
R_USERS_ENABLED_KEY = 'enable'

R_SET_USERS = R_PREFIX_PRIMARY + 'users'

R_SET_TASKS = R_PREFIX_PRIMARY + 'tasks'


def db_user_add(user_id, role='guest', username='guest'):
    name = R_PREFIX_PRIMARY+R_PREFIX_USER+str(user_id)
    res = BotWoody.r.exists(name)
    if res == 0:
        p = BotWoody.r.pipeline()
        p.multi()
        p.hset(name=name,
               mapping={R_USERS_ROLE_KEY: role,
                        R_USERS_NAME_KEY: username,
                        R_USERS_EMAIL_KEY: '-',
                        R_USERS_ENABLED_KEY: 1})
        p.sadd(R_SET_USERS, user_id)
        res = p.execute()
    else:
        return 'User exists'
    return 0 not in res


def db_user_del(user_id):
    name = R_PREFIX_PRIMARY+R_PREFIX_USER+str(user_id)
    res = BotWoody.r.exists(name)
    if res > 0:
        # f = [bytes.decode(a) for a in BotWoody.r.hkeys(name)]
        # res = BotWoody.r.hdel(name, ' '.join(f))
        p = BotWoody.r.pipeline()
        p.multi()
        p.delete(name)
        p.srem(R_SET_USERS, user_id)
        res = p.execute()
    else:
        return 'NOT User'
    return 0 not in res


def db_user_update(user_id, mapping: dict = None):
    if BotWoody.r.sismember(R_SET_USERS, user_id):
        name = R_PREFIX_PRIMARY + R_PREFIX_USER + str(user_id)
        if mapping is not None:
            BotWoody.r.hdel(name, ' '.join(mapping.keys()))
            res = BotWoody.r.hset(name, mapping=mapping)
        else:
            return None
    else:
        return 'None user'
    return res


def get_users_by_role(role: list = None) -> list:
    res = []
    users = [bytes.decode(x) for x in BotWoody.r.smembers(R_SET_USERS)]
    for user in users:
        name = R_PREFIX_PRIMARY + R_PREFIX_USER + str(user)
        usr_role = BotWoody.r.hget(name, 'role')
        # print(name, usr_role)
        if role is None or bytes.decode(usr_role) in role:
            res.append(int(user))
    return res


def get_users_by_task():
    pass


def get_user_detail(user_id: str) -> dict | None:
    user_detail = BotWoody.r.hgetall(R_PREFIX_PRIMARY + R_PREFIX_USER + user_id)
    user_detail_keys = [bytes.decode(x) for x in user_detail.keys()]
    res = {}
    for key in user_detail.keys():
        res[bytes.decode(key)] = bytes.decode(user_detail[key])
    return res


