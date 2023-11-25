from dao.base_dao import BaseDao
import util.time_util as time_util


class DPMSDao(BaseDao):

    def __init__(self):
        pass

def get_patient_medication_records(conn, name, phone, page):
    sql = "SELECT * FROM patients patient JOIN medication_records mr ON patient.id = mr.patient_id"
    sql.join(" WHERE patient.deleted_at = ").join(time_util.get_delete_time())
    sql.join(" AND mr.deleted_ad = ").join(time_util.get_delete_time())
    if name:
        sql.join(" AND name = ").join(name)
    if phone:
        sql.join(" AND phone = ").join(phone)
    cusor = conn.execute(sql, ())