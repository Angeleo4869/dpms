import util.db_util as db_util
from dao import dpms_dao, patient_dao
from dao.dpms_dao import update_expected_with_records, insert_medication_records


def get_or_create_patient(name, phone):
    connect = db_util.get_sqlite3_connect()
    patient_id = patient_dao.get_patient_by_name_and_phone(connect, name, phone)
    if patient_id == 0 and name and phone:
        patient_dao.insert_patient(connect, name, phone)
    patients = patient_dao.get_all_filter_patients(connect, patient_id=patient_id)
    connect.close()
    return patients[0]


def get_expect_and_record_num():
    connect = db_util.get_sqlite3_connect()
    expected_num = dpms_dao.get_expected_medication_this_month(connect)
    record_num = dpms_dao.get_records_medication_this_month(connect)
    connect.close()
    return expected_num, record_num, expected_num + record_num


def register_a_medication(patient_id, dose, time, status, remark, expected_id, type):
    connect = db_util.get_sqlite3_connect()
    if insert_medication_records(connect, patient_id, dose, status, remark, expected_id, time, type) and \
            update_expected_with_records(connect, patient_id, dose, time, expected_id, time):
        connect.commit()
    connect.close()


# 主页数据看板
def get_patient_data(page):
    connect = db_util.get_sqlite3_connect()
    patients = patient_dao.get_patients_order_by_expected(connect, page=page)
    patient_add_ex_and_re(connect, patients)
    connect.close()
    return patients


def get_excel_filter_data():
    connect = db_util.get_sqlite3_connect()
    patients = patient_dao.get_all_filter_patients(connect)
    patient_add_ex_and_re(connect, patients)
    connect.close()
    return patients


def patient_add_ex_and_re(connect, patients):
    for i in range(len(patients)):
        patients[i]["patient_record"] = dpms_dao.get_patient_records(connect, patients[i].get('id'))
        patients[i]["patient_expected"] = dpms_dao.get_patient_expected(connect, patients[i].get("id"))
    return patients


def update_patient(patient_id, sex, status, hospital, department, doctor):
    connect = db_util.get_sqlite3_connect()
    patient_dao.update_patient(connect, patient_id, sex, status, hospital, department, doctor)
    patients = patient_dao.get_all_filter_patients(connect, patient_id=patient_id)
    connect.commit()
    connect.close()
    return patients[0]


def get_patient_next_last_order(patient_id):
    connect = db_util.get_sqlite3_connect()
    patients_next_order = patient_dao.get_patients_order_by_expected(connect, patient_id=patient_id)
    patient_last_order = patient_dao.get_patient_last_order(connect, patient_id=patient_id)
    connect.close()
    if not len(patients_next_order) and not len(patient_last_order):
        return None, None
    if not len(patients_next_order) and len(patient_last_order):
        return None, patient_last_order[0]
    if len(patients_next_order) and not len(patient_last_order):
        return patients_next_order[0], None
    return patients_next_order[0], patient_last_order[0]


def get_hospitals_departments_doctors():
    connect = db_util.get_sqlite3_connect()
    hospitals = dpms_dao.get_hospitals(connect)
    departments = dpms_dao.get_departments(connect)
    doctors = dpms_dao.get_doctors(connect)
    connect.close()
    return hospitals, departments, doctors


def get_hospitals():
    connect = db_util.get_sqlite3_connect()
    hospitals = dpms_dao.get_hospitals(connect)
    connect.close()
    return hospitals


def get_departments():
    connect = db_util.get_sqlite3_connect()
    departments = dpms_dao.get_departments(connect)
    connect.close()
    return departments


def get_doctors():
    connect = db_util.get_sqlite3_connect()
    doctors = dpms_dao.get_doctors(connect)
    connect.close()
    return doctors
