import wx


app = wx.App()
window = wx.Frame(None, title="这里是一个 Title 不知道取什么名字好呢", size=(400, 300))
panel = wx.Panel(window)
label = wx.StaticText(panel, label="Hello World", pos=(100, 100))
window.Show(True)
app.MainLoop()
