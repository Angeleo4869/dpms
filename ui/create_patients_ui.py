import wx


class CreatePatient(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "患者信息录入", size=(300, 200))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")
        self.createTextFields(panel)
        self.buildOneButton(panel)

    def buildOneButton(self, parent, pos=(0, 0)):
        label, handler = self.buttonData()
        button = wx.Button(parent, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    def buttonData(self):  # 按钮栏数据
        return "提   交", self.OnCommit

    def createTextFields(self, panel):
        for eachLabel, eachPos in self.textFieldData():
            self.createCaptionedText(panel, eachLabel, eachPos, )

    def createCaptionedText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), label, pos)
        static.SetBackgroundColour("White")
        textPos = (pos[0] + 70, pos[1])
        wx.TextCtrl(panel, wx.NewId(), "", size=(100, -1), pos=textPos)

    def textFieldData(self):  # 文本数据
        return (("*姓 名：", (10, 50)),
                ("*电 话：", (10, 110)))

    def OnCommit(self, event):
        pass
