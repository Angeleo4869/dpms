# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import wx
import util.db_util as db
from dao.dpms_dao import get_expected_medication_this_month, get_records_medication_this_month
from dao.patient_dao import get_patient, insert_patient
from service.dpms_service import register_a_medication, get_patient_data
from ui import main_ui
from ui import create_patients_ui
from ui.main_ui import DPMS_Main
from util import time_util


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    connect = db.get_sqlite3_connect()
    print(get_records_medication_this_month(connect))
    print(get_expected_medication_this_month(connect))
    # insert_patient(connect, "小八", "14935502580")
    # register_a_medication(7, 3, time_util.get_now_strf_time(), 1, "不错", 13)
    # connect.commit()
    # connect.close()
    # print("success connect")
    # # for row in connect.cursor().execute("SELECT * FROM patients"):
    # #     print(row[:])
    # connect.close()
    # get_patient_data(None)

    app = wx.PySimpleApp()
    frame = DPMS_Main(parent=None, id=-1)
    frame.Show()
    app.MainLoop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
