# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cn2an
import wx
import util.db_util as db
from dao.dpms_dao import get_expected_medication_this_month, get_records_medication_this_month
from service import dpms_service
from service.dpms_service import register_a_medication, get_patient_data
from service.output_excel import OutPutExcel, get_expected_batch
from ui import main_ui
from ui import patients_ui
from ui.patients_ui import CreatePatient, PatientInfo
from ui.main_ui import DPMS_Main
from util import time_util


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # print((time_util.string_to_time('1970-01-01') - time_util.get_now_time()).days)
    # connect = db.get_sqlite3_connect()
    # print(get_records_medication_this_month(connect))
    # print(get_expected_medication_this_month(connect))
    # register_a_medication(7, 3, time_util.get_now_strf_time(), 1, "不错", 13)
    # connect.commit()
    # connect.close()
    # print("success connect")
    # # for row in connect.cursor().execute("SELECT * FROM patients"):
    # #     print(row[:])
    # connect.close()
    # get_patient_data(None)
    # print(dpms_service.get_or_create_patient('九久', '19909992000'))

    app = wx.PySimpleApp()
    frame = PatientInfo(parent=None, frame_id=-1)
    frame.Show()
    app.MainLoop()

    # OutPutExcel()
    # print(get_expected_batch(str(3)))
    # output = cn2an.an2cn("123", "low")
    # print(output)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
