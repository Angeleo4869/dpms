import wx

from service import dpms_service
from util import time_util


def get_total_text_data():
    return (("剩余预购量", (1, 0)),
            ("+", (1, 1)),
            ("本月已购量", (1, 2)),
            ("=", (1, 3)),
            ("本月预购总量", (1, 4)),
            ("更  多", (0, 6)))


def get_patient_record_box(panel, parentBox, recordDatas, firstX):
    for record_data in recordDatas:
        record_text = wx.StaticText(panel, label=record_data.get('record_at'))
        parentBox.Add(record_text, pos=(0, firstX), span=(1, 1), flag=wx.EXPAND | wx.ALL)
        firstX += 1


def get_expected_time_to_int(expected_time):
    return time_util.get_time_diff(time_util.string_to_time(expected_time), time_util.get_now_time())


def get_expected_color(expectedData):
    if expectedData.get('status') == 1:
        return 0, 255, 0
    diff_day = get_expected_time_to_int(expectedData.get('expected_at'))
    if diff_day < 0:
        return 50, 50, 50
    return 255, diff_day * 2 + 40, diff_day * 2 + 40


def get_patient_status(status):
    if 1 == status:
        return "健康", "Green"
    if 0 == status:
        return "已去世", "Red"
    return "生病中", "Yellow"


class DPMS_Main(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Refactor Example', size=(500, 300))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")
        mainBox = wx.BoxSizer(wx.VERTICAL)
        totalDataBox = wx.GridBagSizer(2, 4)
        mainBox.Add(totalDataBox, 0, wx.CENTER, 5)
        panel.SetSizer(mainBox)
        self.get_total_text(panel, totalDataBox)

        patientsDataBox = wx.BoxSizer(wx.VERTICAL)
        self.get_patient_data_box(panel, patientsDataBox)

        mainBox.Add(patientsDataBox)

    def get_expect_and_record_num_text(self, panel, totalBox):
        nums = dpms_service.get_expect_and_record_num()
        for i, num in enumerate(nums):
            numText = wx.StaticText(panel)
            numText.SetLabelText(str(num))
            totalBox.Add(numText, pos=(0, i), flag=wx.ALL)

    def get_total_text(self, panel, totalBox):
        for text, pos in get_total_text_data():
            st = wx.StaticText(panel, label=text)
            totalBox.Add(st, pos, flag=wx.ALL)
        self.get_expect_and_record_num_text(panel, totalBox)

    def get_patient_data_box(self, panel, parentBox):
        for pat_data in dpms_service.get_patient_data(None):
            pat_gb = wx.GridBagSizer(0, 0)
            pat_status, status_colour = get_patient_status(pat_data.get('status'))
            pat_name_text = wx.StaticText(panel, label=pat_data.get('name'))
            pat_phone_text = wx.StaticText(panel, label=pat_data.get('phone'))
            pat_status_text = wx.StaticText(panel, label=pat_status)
            pat_status_text.SetBackgroundColour(status_colour)
            pat_gb.Add(pat_name_text, pos=(1, 1), span=(4, 1), border=10)
            pat_gb.Add(pat_phone_text, pos=(1, 2), span=(4, 1), border=10)
            pat_gb.Add(pat_status_text, pos=(1, 3), span=(4, 1), border=10)
            parentBox.Add(pat_gb)
            get_patient_record_box(panel, pat_gb, pat_data.get('patient_record'), 4)
            self.get_patient_expected_box(panel, pat_gb, pat_data.get('patient_expected'), 4)

    def get_patient_expected_box(self, panel, parentBox, expectedDatas, firstX):
        for expectedData in expectedDatas:
            expect_text = wx.StaticText(panel, label=expectedData.get('expected_at'))
            expect_prop_text = wx.StaticText(panel, label="购药时间")
            expect_dose = wx.StaticText(panel, label=str(expectedData.get('dose')))
            expect_text.SetBackgroundColour(get_expected_color(expectedData))
            parentBox.Add(expect_text, pos=(2, firstX), span=(1, 1), flag=wx.EXPAND | wx.ALL)
            parentBox.Add(expect_prop_text, pos=(3, firstX), span=(1, 1))
            parentBox.Add(expect_dose, pos=(1, firstX), span=(1, 1))
            firstX += 1
