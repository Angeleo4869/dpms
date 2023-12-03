import logging

from util import time_util


def get_patient_by_name_and_phone(conn, name, phone):
    sql = "SELECT `id`FROM patients WHERE deleted_at={} AND name=? AND phone=?;".format(time_util.get_sql_delete_time())
    pat_id = 0
    try:
        cusor = conn.execute(sql, (name, str(phone)))
        for row in cusor:
            if row[0]:
                return row[0]
    except Exception as e:
        logging.warning("get_patient_by_name_and_phone", e)
        return pat_id
    return pat_id


# 创建角色
def insert_patient(conn, name, phone):
    sql = "INSERT INTO patients (`name`, `phone`) VALUES (?,?)"
    pat_id = 0
    try:
        conn.execute(sql, (name, phone))
        pat_id = get_patient_by_name_and_phone(conn, name, phone)
    except Exception as e:
        logging.warning("insert_patient", e)
    return pat_id


# 编辑角色信息
def update_patient(conn, id, sex=3, status=1, hospital=0, department=0, doctor=0):
    sql = ["UPDATE patients",
           "SET sex=?, status=?, hospital_id=?, department_id=?, doctor_id=?",
           "WHERE id=?"]
    try:
        conn.execute(sql, (str(sex), str(status), str(hospital), str(department), str(doctor), str(id)))
    except Exception as e:
        logging.warning("update_patient", e)


# 最近一次预购
def get_patients_order_by_expected(conn, patient_id=None, page=None):
    sql = ["SELECT p.id, p.name, p.sex, p.phone, p.status, MIN(em.expected_at), em.id, em.dose, em.type",
           "FROM  patients p",
           "LEFT JOIN expected_medication em", "ON em.patient_id = p.id",
           "WHERE p.deleted_at={}".format(time_util.get_sql_delete_time()),
           "AND em.deleted_at={}".format(time_util.get_sql_delete_time()),
           "AND em.status=0 "]
    if patient_id:
        sql.append("AND p.id={}".format(patient_id))
    sql.append("GROUP BY p.id")
    if page:
        sql.append("LIMIT {}, {} ".format(page.offset, page.row_count))
    patients = []
    try:
        cusor = conn.execute(" ".join(sql))
        for row in cusor:
            if row[0] is None:
                continue
            pat = {
                "id": row[0],
                "name": row[1],
                "sex": row[2],
                "phone": row[3],
                "status": row[4],
                "next_order_time": row[5],
                "next_order_id": row[6],
                "dose": row[7],
                "type": row[8]
            }
            if not pat['sex']:
                pat['sex'] = 2
            patients.append(pat)
    except Exception as e:
        logging.warning("get_patients_order_by_expected", e)
    return patients


# 上一次购药信息
def get_patient_last_order(conn, patient_id):
    sql = ["SELECT mr.id, mr.patient_id, MAX(mr.record_at), mr.dose, mr.remark",
           "FROM medication_records mr",
           "WHERE mr.deleted_at={}".format(time_util.get_sql_delete_time()),
           "AND mr.status=1",
           "AND mr.patient_id=?"]
    patients = []
    try:
        cusor = conn.execute(" ".join(sql), (patient_id, ))
        for row in cusor:
            if row[0] is None:
                continue
            pat = {
                "id": row[0],
                "patient_id": row[1],
                "last_order_time": row[2],
                "dose": row[3],
                "remark": row[4]
            }
            patients.append(pat)
    except Exception as e:
        logging.warning("get_patients_order_by_expected", e)
    return patients


# 根据筛选条件获取患者信息
def get_all_filter_patients(conn, patient_id=None, name=None, phone=None, status=None, hospital=None, department=None, doctor=None):
    sql = ["SELECT p.id, p.name, p.sex, p.phone, p.status, h.name, dp.name, d.name",
           "FROM patients p",
           "LEFT JOIN hospitals h ON h.id=p.hospital_id",
           "AND h.deleted_at={}".format(time_util.get_sql_delete_time()),
           "LEFT JOIN departments dp ON dp.id = p.department_id",
           "AND dp.deleted_at={}".format(time_util.get_sql_delete_time()),
           "LEFT JOIN doctors d ON d.id=p.doctor_id",
           "AND d.deleted_at={}".format(time_util.get_sql_delete_time()),
           "WHERE p.deleted_at={}".format(time_util.get_sql_delete_time())]
    if patient_id:
        sql.append("AND p.id={}".format(patient_id))
    if hospital:
        sql.append("AND h.id={}".format(hospital))
    if department:
        sql.append("AND dp.id={}".format(department))
    if doctor:
        sql.append("AND d.id={}".format(doctor))
    if name:
        sql.append("AND p.name='{}'".format(name))
    if phone:
        sql.append("AND p.phone='{}'".format(phone))
    if status:
        sql.append("AND p.status='{}'".format(status))

    patients = []
    try:
        cusor = conn.execute(" ".join(sql))
        for row in cusor:
            if row[0] is None:
                continue
            pat = {
                "id": row[0],
                "name": row[1],
                "sex": row[2],
                "phone": row[3],
                "status": row[4],
                "hospital": row[5],
                "departments": row[6],
                "doctors": row[7],
            }
            if not pat['sex']:
                pat['sex'] = 2
            patients.append(pat)
    except Exception as e:
        logging.warning("get_all_filter_patients", e)
    return patients