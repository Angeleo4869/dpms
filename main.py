# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import wx
import util.db_util as db
from dao.dpms_dao import get_expected_medication_this_month, get_records_medication_this_month
from ui import main
from ui import create_patients


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    connect = db.get_sqlite3_connect()
    get_records_medication_this_month(connect)
    # print("success connect")
    # # for row in connect.cursor().execute("SELECT * FROM patients"):
    # #     print(row[:])
    # connect.close()
    # app = wx.PySimpleApp()
    # frame = create_patients.CreatePatient(parent=None, id=-1)
    # frame.Show()
    # app.MainLoop()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
