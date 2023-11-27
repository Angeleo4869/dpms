import util.db_util as db_util
from dao import patient_dao, dpms_dao
from dao.dpms_dao import update_expected_with_records, insert_medication_records


def get_expect_and_record_num():
    connect = db_util.get_sqlite3_connect()
    expected_num = dpms_dao.get_expected_medication_this_month(connect)
    record_num = dpms_dao.get_records_medication_this_month(connect)
    connect.close()
    return expected_num, record_num, expected_num + record_num


def register_a_medication(patient_id, dose, time, status, remark, expected_id):
    connect = db_util.get_sqlite3_connect()
    if insert_medication_records(connect, patient_id, dose, status, remark, expected_id, time, 1) and \
            update_expected_with_records(connect, patient_id, dose, time, expected_id, time):
        connect.commit()
    connect.close()
