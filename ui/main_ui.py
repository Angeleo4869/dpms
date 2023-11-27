import wx

from service import dpms_service


def get_total_text_data():
    return (("剩余预购量", (1, 1)),
            ("本月已购量", (1, 2)),
            ("本月预购总量", (1, 3)))


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


    def get_expect_and_record_num_text(self, panel, totalBox):
        nums = dpms_service.get_expect_and_record_num()
        i = 0
        for num in nums:
            numText = wx.StaticText(panel)
            numText.SetLabelText(str(num))
            totalBox.Add(numText, pos=(0, i), flag=wx.ALL)
            i += 1

    def get_total_text(self, panel, totalBox):
        for text, pos in get_total_text_data():
            st = wx.StaticText(panel, label=text)
            totalBox.Add(st, pos, flag=wx.ALL)
        self.get_expect_and_record_num_text(panel, totalBox)
