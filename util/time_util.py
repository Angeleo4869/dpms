from time import strftime, localtime


def get_now_time():
    return str(strftime('%Y-%m-%d %H:%M:%S', localtime()))


# DELETED_AT
def get_delete_time():
    return '1970-01-01 00:00:00'
