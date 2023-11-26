from dao.base_dao import BaseDao


class Patient(BaseDao):

    def __init__(self, name, sex, phone, job, purchase, treatment):
        super().__init__()
        self.name = name
        self.sex = sex
        self.phone = phone
        self.job = job
        self.purchase = purchase
        self.treatment = treatment


# 创建角色
def insert_patient(conn, name, phone):
    sql = "INSERT INTO patients (name, phone) VALUES (?,?)"
    conn.execute(sql, (name, phone))
    conn.close()


# 编辑角色信息
def update_patient(conn, patient):
    sql = "UPDATE patients"
    conn.execute(sql, patient)
    conn.close()


# 获取角色
def get_patient(conn, page):
    patients = []
    sql = "SELECT * FROM patients LIMIT ?,?"
    cursor = conn.execute(sql, (page.offset, page.row_count))
    for row in cursor:
        patients.append(Patient(row[:]))
    var = conn.close
    return patients


# 获取角色
def get_patient(conn, name, phone):
    patients = []
    sql = "SELECT * FROM patients WHERE name = ? AND phone = ?"
    cursor = conn.execute(sql, (name, phone))
    for row in cursor:
        patients.append(Patient(row[:]))
    var = conn.close
    return patients