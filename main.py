# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import wx
from ui.patients_ui import PatientInfo


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = wx.App(False)
    frame = PatientInfo(None, 1)
    frame.Show()
    app.MainLoop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
