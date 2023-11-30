from openpyxl import Workbook

from service import dpms_service


def get_sheet_titles():
    return ("编号",
            "姓名",
            "性别",
            "电话",
            "状态",
            "医院",
            "科室",
            "医生",
            "预购批次",
            "预购时间",
            "预购数量",
            "实际购买时间",
            "购买数量",
            "赠送/直购",
            "",
            "备注")


def set_sheet_title(sheet):
    for index, title in enumerate(get_sheet_titles()):
        sheet.cell(1, index+1, title)


class OutPutExcel:

    def __init__(self):
        book = Workbook()
        sheet = book.active
        set_sheet_title(sheet)
        self.set_pdms_data(sheet)
        book.save('data/test.xlsx')

    def set_pdms_data(self, sheet):
        for index, dpm in enumerate(dpms_service.get_patient_data(None)):
            # sheet.merge_cells(":")
            sheet.cell(index + 2, 1, dpm.get('id'))
            sheet.cell(index + 2, 2, dpm.get('name'))
            sheet.cell(index + 2, 4, dpm.get('sex'))
            sheet.cell(index + 2, 3, dpm.get('phone'))
            sheet.cell(index + 2, 5, dpm.get('status'))
            sheet.cell(index + 2, 6, dpm.get('hospital'))
            sheet.cell(index + 2, 7, dpm.get('department'))
            self.set_expected_data(sheet, dpm.get('patient_expected'), len(dpm.get('patient_expected'))+index+2)
            self.set_record_data(sheet, dpm.get('patient_record'), len(dpm.get('patient_expected'))+index+2)

    def set_expected_data(self, sheet, expectedDatas, patientIndex):
        for index, expect in enumerate(expectedDatas):
            sheet.cell(patientIndex + index, 9, expect.get('expected_at'))

    def set_record_data(self, sheet, recordDatas, patientIndex):
        for index, record in enumerate(recordDatas):
            sheet.cell(patientIndex + index, 11, record.get('record_at'))
