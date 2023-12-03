import logging

import util.time_util as time_util


# 获取患者预购信息
def get_patient_expected(conn, patient_id):
    sql = "SELECT `id`, date(`expected_at`), `status`, `type`, `dose` " \
          " FROM expected_medication " \
          " WHERE deleted_at = {} " \
          " AND patient_id = ?;" \
        .format(time_util.get_sql_delete_time())
    pat_expects = []
    try:
        cusor = conn.execute(sql, (patient_id, ))
        for row in cusor:
            if row[0] is None:
                continue
            pat_exp = {
                "id": row[0],
                "expected_at": row[1],
                "status": row[2],
                "type": row[3],
                "dose": row[4],
            }
            pat_expects.append(pat_exp)
    except Exception as e:
        logging.warning("get_patient_expected", e)
    return pat_expects


# 获取患者已购信息
def get_patient_records(conn, patient_id):
    sql = "SELECT `id`, date(`record_at`), `dose`, `status`, `type`, `remark` " \
          " FROM medication_records " \
          " WHERE deleted_at = {} " \
          " AND patient_id = ?;" \
        .format(time_util.get_sql_delete_time())
    pat_records = []
    try:
        cusor = conn.execute(sql, (patient_id, ))
        for row in cusor:
            if row[0] is None:
                continue
            pat_record = {
                "id": row[0],
                "record_at": row[1],
                "dose": row[2],
                "status": row[3],
                "type": row[4],
                "remark": row[5]
            }
            pat_records.append(pat_record)
    except Exception as e:
        logging.warning("get_patient_records", e)
    return pat_records


# 查询本月剩余预购量
def get_expected_medication_this_month(conn):
    begin, end = time_util.get_sql_start_month_from_today()
    sql = " SELECT SUM(em.dose) " \
          " FROM expected_medication em " \
          " JOIN patients p " \
          " ON p.id = em.patient_id" \
          " WHERE p.deleted_at = {} " \
          " AND em.deleted_at = {} " \
          " AND em.type = 1 " \
          " AND p.status = 0 " \
          " AND em.expected_at BETWEEN {} AND {} ;" \
        .format(time_util.get_sql_delete_time(), time_util.get_sql_delete_time(), begin, end)
    this_month_expected_count = 0
    try:
        cusor = conn.execute(sql)
        for row in cusor:
            if row[0] is None:
                continue
            this_month_expected_count += row[0]
    except Exception as e:
        logging.warning("get_expected_medication_this_month", e)
    return this_month_expected_count


# 查询本月已购量
def get_records_medication_this_month(conn):
    begin, end = time_util.get_sql_start_month_from_today()
    sql = " SELECT SUM(mr.dose) " \
          " FROM medication_records mr " \
          " JOIN patients p " \
          " ON p.id = mr.patient_id" \
          " WHERE p.deleted_at = {}" \
          " AND mr.deleted_at = {} " \
          " AND mr.type = 1 " \
          " AND p.status = 1 " \
          " AND mr.record_at BETWEEN {} AND {} ;" \
        .format(time_util.get_sql_delete_time(), time_util.get_sql_delete_time(), begin, end)
    this_month_record_count = 0
    try:
        cusor = conn.execute(sql)
        for row in cusor:
            if row[0] is None:
                continue
            this_month_record_count += row[0]
    except Exception as e:
        logging.warning("get_records_medication_this_month", e)
    return this_month_record_count


# 录入一次用药信息
def insert_medication_records(conn, patient_id, dose, status, remark, expected_id, time, reType):
    sql = "INSERT INTO medication_records " \
          "(patient_id, dose, status, remark, expected_id, record_at, type) " \
          "VALUES (?, ?, ?, ?, ?, ?, ?);"
    try:
        conn.execute(sql, (str(patient_id), str(dose), str(status), remark, str(expected_id), time, str(reType)))
    except Exception as e:
        logging.warning("insert_mediation_records", e)
        return False
    return True


# 修改一次已用药信息，或许？用于更改备注
def update_mediation_records(conn):
    pass


# 计算剩余预计用药时间
def update_expected_with_records(conn, patient_id, dose, record_at, expected_id):
    date_diff_sql = ["SELECT id, expected_at, (julianday(date(expected_at)) - julianday(date('{}'))) AS diff_time".format(record_at),
                     "FROM expected_medication",
                     "WHERE deleted_at={}".format(time_util.get_sql_delete_time()),
                     "AND id=?"]

    exp_status_sql = "UPDATE expected_medication SET status=1 WHERE id = ?;"

    sql = "UPDATE expected_medication SET expected_at={}, dose=? WHERE patient_id=? AND expected_at>?;"
    try:
        cusor = conn.execute(" ".join(date_diff_sql), (expected_id, ))
        conn.execute(exp_status_sql, (expected_id, ))
        for row in cusor:
            if row[0] is None:
                continue
            conn.execute(sql.format(time_util.get_sql_diff_date("expected_at", row[2])), (str(dose), str(patient_id), record_at))
    except Exception as e:
        logging.warning("update_expected_with_records", e)
        return False
    return True


# 获取医院
def get_hospitals(conn):
    sql = "SELECT `id`, `name`, `address`, `phone` FROM hospitals;"
    hospitals = []
    try:
        cusor = conn.execute(sql)
        for row in cusor:
            if row[0] is None:
                continue
            hospital = {
                "id": row[0],
                "name": row[1],
                "address": row[2],
                "phone": row[3],
            }
            hospitals.append(hospital)
    except Exception as e:
        logging.warning("get_hospitals", e)
    return hospitals


def get_departments(conn):
    sql = "SELECT `id`, `name`, `hospital_id` FROM departments;"
    departments = []
    try:
        cusor = conn.execute(sql)
        for row in cusor:
            if row[0] is None:
                continue
            department = {
                "id": row[0],
                "name": row[1],
                "hospital_id": row[2],
            }
            departments.append(department)
    except Exception as e:
        logging.warning("get_departments", e)
    return departments


# 获取医生
def get_doctors(conn):
    sql = "SELECT `id`, `name`, `phone`, `hospital_id`, `department_id` FROM doctors;"
    doctors = []
    try:
        cusor = conn.execute(sql)
        for row in cusor:
            if row[0] is None:
                continue
            doctor = {
                "id": row[0],
                "name": row[1],
                "phone": row[2],
                "hospital_id": row[3],
                "department_id": row[4],
            }
            doctors.append(doctor)
    except Exception as e:
        logging.warning("get_hospitals", e)
    return doctors
