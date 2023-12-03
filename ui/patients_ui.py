import os

import wx
import wx.adv
from service import dpms_service, output_excel
from util import time_util


def get_sex():
    return [u'女', u'男', u'未知']


def get_status():
    return [u'已去世', u'健康', u'生病中']


def get_hospitals():
    hospital_combo = []
    for hospital in dpms_service.get_hospitals():
        hospital_combo.append(hospital.get('name'))
    return hospital_combo


def get_departments():
    department_combo = []
    for hospital in dpms_service.get_departments():
        department_combo.append(hospital.get('name'))
    return department_combo


def get_doctors():
    doctor_combo = []
    for hospital in dpms_service.get_doctors():
        doctor_combo.append(hospital.get('name'))
    return doctor_combo


class PatientInfo(wx.Frame):

    def __init__(self, parent, frame_id, patient_info=None):
        wx.Frame.__init__(self, parent, frame_id, "患者信息看板", size=(600, 500))
        self.SetIcon(wx.Icon('data/title.ico', wx.BITMAP_TYPE_ICO))
        self.panel = CreatePatient(self, wx.NewId(), patient_info)


class CreatePatient(wx.Panel):

    def __init__(self, parent, panel_id, patient_info=None):
        wx.Panel.__init__(self, parent=parent, id=panel_id)
        # 公共值
        self.patient_info = None
        self.next_expected_info = patient_info
        self.SetBackgroundColour("White")
        self.mainBox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainBox)
        # 公共组件，用于取值
        self.phone_search = wx.TextCtrl(self)
        self.name_search = wx.TextCtrl(self)
        # 基本信息
        self.sex = wx.RadioBox(self, label="性别", choices=get_sex(), majorDimension=3)
        self.status = wx.ComboBox(self, choices=get_status())
        self.hospital = wx.ComboBox(self, choices=get_hospitals())
        self.department = wx.ComboBox(self, choices=get_departments())
        self.doctor = wx.ComboBox(self, choices=get_doctors())
        self.last_time = wx.TextCtrl(self, size=(100, 30), style=wx.TE_READONLY | wx.TE_CENTER)
        self.last_dose = wx.TextCtrl(self, size=(100, 30), style=wx.TE_READONLY | wx.TE_CENTER)
        self.last_remark = wx.TextCtrl(self, size=(100, 30), style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.next_expect_time = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_CENTER)
        # 购药信息
        self.record_time = wx.adv.DatePickerCtrlGeneric(self, dt=wx.DateTime.Now(), size=(100, 30), style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.record_dose = wx.TextCtrl(self, size=(100, 30),)
        self.record_remark = wx.TextCtrl(self, size=(200, 50), style=wx.TE_MULTILINE)
        # 所有组件注册
        self.get_all_box(self, self.mainBox)

    def get_all_box(self, panel, mainBox):
        self.get_name_and_phone_add_or_search(panel, mainBox)
        self.get_patient_info(panel, mainBox)
        self.get_record_last_info(panel, mainBox)

    # 姓名电话
    def get_name_and_phone_add_or_search(self, panel, parentBox):
        searchBox = wx.BoxSizer(wx.HORIZONTAL)
        self.createTextFields(panel, searchBox)
        self.set_name_phone()
        searchBox.Add(self.buildOneButton(panel), 0, wx.ALL, 20)
        parentBox.Add(searchBox, 0, wx.LEFT | wx.HORIZONTAL, 10)

    def buildOneButton(self, panel, pos=(0, 0)):
        label, handler = self.buttonData()
        button = wx.Button(panel, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    def buttonData(self):  # 按钮栏数据
        return "查询/创建", self.OnCommit

    def createTextFields(self, panel, parentBox):
        self.createNameText(panel, parentBox, "姓名:")
        self.createPhoneText(panel, parentBox, "电话:")

    def createNameText(self, panel, parentBox, label):
        name_static = wx.StaticText(panel, label=label)
        name_static.SetBackgroundColour("White")
        parentBox.Add(name_static, 0, wx.ALL, 20)
        parentBox.Add(self.name_search, 0, wx.ALIGN_CENTER, 20)

    def createPhoneText(self, panel, parentBox, label):
        phone_static = wx.StaticText(panel, label=label)
        phone_static.SetBackgroundColour("White")
        parentBox.Add(phone_static, 0, wx.ALL, 20)
        parentBox.Add(self.phone_search, 0, wx.ALIGN_CENTER, 20)

    def set_name_phone(self):
        if self.patient_info:
            self.name_search.SetValue(self.patient_info.get('name'))
            self.phone_search.SetValue(self.patient_info.get('phone'))

    # 触发查询
    def OnCommit(self, event):
        name = self.name_search.GetValue()
        phone = self.phone_search.GetValue()
        if not name or not phone:
            return
        self.patient_info = dpms_service.get_or_create_patient(name, phone)
        self.set_patient_info()
        self.set_patient_order()

    # 基本信息看板
    def get_patient_info(self, panel, parentBox):
        patient_info_layout = wx.GridBagSizer(0, 0)
        patient_info_layout.Add(self.patientEditButton(panel), pos=(1, 6), span=(1, 2), border=5, flag=wx.ALIGN_CENTER )
        self.get_status_sex(panel, patient_info_layout, )
        self.get_hospital_department_doctor(panel, patient_info_layout)
        parentBox.Add(patient_info_layout, 1, wx.LEFT | wx.HORIZONTAL, 10)

    def patientEditButtonData(self):  # 按钮栏数据
        return "提交修改", self.OnEditPatient

    def patientEditButton(self, panel, pos=(0, 0)):
        label, handler = self.patientEditButtonData()
        button = wx.Button(panel, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    # 状态
    def get_status_sex(self, panel, parentBox):
        parent_status = wx.StaticText(panel, label='健康状态:')
        parentBox.Add(self.sex, pos=(1, 1), span=(1, 2), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(parent_status, pos=(1, 3), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.status, pos=(1, 4), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)

    # 医院
    def get_hospital_department_doctor(self, panel, parentBox):
        hospital = wx.StaticText(panel, label='医院:')
        parentBox.Add(hospital, pos=(3, 1), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.hospital, pos=(3, 2), span=(1, 1), border=5)
        department = wx.StaticText(panel, label='科室:')
        parentBox.Add(department, pos=(3, 3), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.department, pos=(3, 4), span=(1, 1), border=5)
        doctor = wx.StaticText(panel, label='医生:')
        parentBox.Add(doctor, pos=(3, 5), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.doctor, pos=(3, 6), span=(1, 1), border=5)
        if self.patient_info:
            self.hospital.SetSelection(self.patient_info.get('hospital'))
            self.department.SetSelection(self.patient_info.get('department'))
            self.doctor.SetSelection(self.patient_info.get('doctor'))

    def OnEditPatient(self, event):
        sex = self.sex.GetSelection()
        status = self.status.GetSelection()
        hospital = self.hospital.GetSelection()
        department = self.department.GetSelection()
        doctor = self.doctor.GetSelection()
        self.patient_info = dpms_service.update_patient(self.patient_info.get('id'), sex, status, hospital, department, doctor)
        self.set_patient_info()

    # 已购信息看板
    def get_record_last_info(self, panel, parentBox):
        record_last_info_layout = wx.GridBagSizer(0, 0)
        record_last_info_layout.Add(self.patientOrderButton(panel), pos=(4, 5), span=(2, 2), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        self.get_last_record(panel, record_last_info_layout)
        self.get_next_expected_record(panel, record_last_info_layout)
        record_last_info_layout.Add(self.outPutDataButton(panel), pos=(6, 5), span=(2, 2), border=5, flag=wx.ALIGN_CENTER | wx.ALL)

        parentBox.Add(record_last_info_layout, 1, wx.LEFT | wx.HORIZONTAL, 10)

    def patientOrderButtonData(self):  # 按钮栏数据
        return "登记购药", self.registerMedicine

    def patientOrderButton(self, panel, pos=(0, 0)):
        label, handler = self.patientOrderButtonData()
        button = wx.Button(panel, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    def registerMedicine(self, event):
        order_time = self.get_time(self.record_time.GetValue())
        order_dose = self.record_dose.GetValue()
        order_remark = self.record_remark.GetValue()
        patient_id = self.patient_info.get('id')
        next_expected_id = self.next_expected_info.get('next_order_id')
        next_expected_type = self.next_expected_info.get('type')
        print(patient_id, order_time, order_dose, next_expected_id, next_expected_type, order_remark)
        dpms_service.register_a_medication(patient_id, order_dose, order_time, 1, order_remark, next_expected_id, next_expected_type)
        self.set_patient_order()

    def get_last_record(self, panel, parentBox):
        last_drug_purchase_record_title = wx.StaticText(panel, label="上次购药记录")
        parentBox.Add(last_drug_purchase_record_title, pos=(1, 1), span=(1, 1), border=5)
        last_time_title = wx.StaticText(panel, label="购药时间")
        last_dose_title = wx.StaticText(panel, label="数量")
        last_remark_title = wx.StaticText(panel, label="备注")
        parentBox.Add(last_time_title, pos=(2, 1), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.last_time, pos=(2, 2), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(last_dose_title, pos=(2, 3), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.last_dose, pos=(2, 4), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(last_remark_title, pos=(2, 5), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.last_remark, pos=(2, 6), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)

    def get_next_expected_record(self, panel, parentBox):
        next_record_title = wx.StaticText(panel, label="下次购药时间")
        parentBox.Add(next_record_title, pos=(3, 1), span=(1, 1), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(self.next_expect_time, pos=(3, 2), span=(1, 2), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        next_time_title = wx.StaticText(panel, label="购药时间")
        next_dose_title = wx.StaticText(panel, label="数量")
        next_remark_title = wx.StaticText(panel, label="备注")
        parentBox.Add(next_time_title, pos=(4, 1), span=(1, 1), border=5)
        parentBox.Add(self.record_time, pos=(4, 2), span=(1, 2), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(next_dose_title, pos=(5, 1), span=(1, 1), border=5)
        parentBox.Add(self.record_dose, pos=(5, 2), span=(1, 2), border=5, flag=wx.ALIGN_CENTER | wx.ALL)
        parentBox.Add(next_remark_title, pos=(6, 1), span=(1, 1), border=5)
        parentBox.Add(self.record_remark, pos=(6, 2), span=(1, 2), border=5, flag=wx.ALIGN_CENTER | wx.ALL)

    def set_patient_info(self):
        if self.patient_info:
            self.sex.SetSelection(self.patient_info.get('sex'))
            self.status.SetSelection(self.patient_info.get('status'))

    def set_patient_order(self):
        if self.patient_info:
            patient_id = self.patient_info.get('id')
            next_expect_data, patient_last_order = dpms_service.get_patient_next_last_order(patient_id=patient_id)
            if patient_last_order:
                self.last_time.SetValue(patient_last_order.get('last_order_time'))
                self.last_dose.SetValue(str(patient_last_order.get('dose')))
                self.last_remark.SetValue(patient_last_order.get('remark'))
            if next_expect_data:
                self.next_expected_info = next_expect_data
                self.next_expect_time.SetValue(next_expect_data.get('next_order_time'))
                self.record_dose.SetValue(str(next_expect_data.get('dose')))

    def get_time(self, event):
        return time_util.wx_time_to_string(self.record_time.GetValue().FormatISOCombined())

    def outPutDataButton(self, panel, pos=(0, 0)):
        label, handler = self.outPutData()
        button = wx.Button(panel, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    def outPutData(self):  # 按钮栏数据
        return "导出数据", self.outPutExcel

    def outPutExcel(self, event):
        file_path = os.path.join("output-files", "data.xlsx")
        dlg = wx.FileDialog(self, message="选择文件",
                            defaultFile=file_path,
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = os.path.join(dlg.GetPath())
        output_excel.OutPutExcel(file_path)
