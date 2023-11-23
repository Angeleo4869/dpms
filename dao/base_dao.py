import util.time_util as time_util


class BaseDao:

    def __init__(self):
        self.updated_at = time_util.get_now_time
        self.deleted_at = time_util.get_delete_time
