import logging

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


# 查询本月预购量
def get_expected_medication_this_month(conn):
    sql = " SELECT SUM(em.dose) " \
          " FROM expected_medication em " \
          " JOIN patients p " \
          " ON p.id = em.patient_id" \
          " WHERE em.type = 1 " \
          " AND p.status = 1 " \
          " AND em.deleted_at = '{}' " + \
          " AND p.deleted_at = '{}' " + \
          " AND em.expected_at BETWEEN datetime('now', 'start of day') AND datetime('now', 'start of month', '+1 month', '-1 second')"
    this_month_expected_count = 0
    try:
        cusor = conn.execute(sql.format(time_util.get_delete_time(), time_util.get_delete_time()))
        for row in cusor:
            this_month_expected_count += row[0]
    except Exception as e:
        logging.warning("get_expected_medication_this_month", e)
    return this_month_expected_count


# 查询本月已购量
def get_records_medication_this_month(conn):
    sql = " SELECT SUM(mr.dose) " \
          " FROM medication_records mr " \
          " JOIN patients p " \
          " ON p.id = mr.patient_id" \
          " WHERE mr.type = 0 " \
          " AND p.status = 1 " \
          " AND mr.deleted_at = '{}' " + \
          " AND p.deleted_at = '{}' " + \
          " AND mr.record_at BETWEEN datetime('now', 'start of month', '-1 month', '+1 second') AND datetime('now', 'start of day', '+1 day')"
    print(sql.format(time_util.get_delete_time(), time_util.get_delete_time()))
    this_month_record_count = 0
    try:
        cusor = conn.execute(sql.format(time_util.get_delete_time(), time_util.get_delete_time()))
        for row in cusor:
            this_month_record_count += row[0]
    except Exception as e:
        logging.warning("get_records_medication_this_month", e)
    return this_month_record_count


# 录入一次用药信息
def insert_mediation_records(conn, patient_id, dose, status, remark, expected_id):
    sql = "INSERT INTO mediaction_recorfs " \
          "(patient_id, dose, status, remark, expected_id) " \
          "VALUES (?, ?, ?, ?, ?)"
    try:
        conn.execute(sql, patient_id, dose, status, remark, expected_id)
    except Exception as e:
        logging.warning("insert_mediation_records", e)
        return False
    return True


# 修改一次已用药信息，或许？用于更改备注
def update_mediation_records(conn):
    pass
