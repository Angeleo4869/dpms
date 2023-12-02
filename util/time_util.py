from datetime import datetime
from time import strftime, localtime


def get_sql_diff_date(dateTime, diff):
    if 0 <= diff:
        return "datetime('{}', '+{} day')".format(dateTime, diff)
    return "datetime({}', '{} day')".format(dateTime, diff)


# NOW
def get_sql_now_time():
    return "datetime('now')"


# DELETED_AT
def get_sql_delete_time():
    return "datetime('1970-01-01 00:00:00')"


# 获取剩余一个月
def get_sql_today_form_month_end():
    return "datetime('now', 'start of day')", " datetime('now', 'start of month', '+1 month', '-1 second')"


# 获取前一个月
def get_sql_start_month_from_today():
    return "datetime('now', 'start of month', '-1 month', '+1 second')", "datetime('now', 'start of day', '+1 day')"


# 获取一年内
def get_one_year():
    pass


def get_now_strf_time():
    return str(strftime('%Y-%m-%d %H:%M:%S', localtime()))


def get_now_time():
    return datetime.now()


def string_to_time(strTime):
    return datetime.strptime(strTime, "%Y-%m-%d")


def time_to_string(time):
    print(time)
    return datetime.strftime(time, "%Y-%m-%d %H:%M:%S")


def get_time_diff(time1, time2):
    return (time1 - time2).days
